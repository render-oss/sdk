package render

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"
)

const (
	taskRunJSON        = `{"id":"trn-1","taskId":"tsk-1","status":"pending","attempts":[],"retries":0,"parentTaskRunId":"","rootTaskRunId":"trn-1"}`
	taskRunDetailsJSON = `{"id":"trn-1","taskId":"tsk-1","status":"completed","attempts":[],"retries":0,"parentTaskRunId":"","rootTaskRunId":"trn-1","input":[1],"results":[2],"completedAt":"2026-01-01T00:00:00Z"}`
	flowRunJSON        = `{"id":"frn-1","flowId":"flw-1","status":"pending"}`
	flowRunDetailsJSON = `{"id":"frn-1","flowId":"flw-1","status":"succeeded","attempts":[],"input":[1],"results":[2],"completedAt":"2026-01-01T00:00:00Z"}`
)

type workflowsTestServer struct {
	handlers map[string]http.HandlerFunc
}

type workflowsTestOption func(*workflowsTestServer)

// withWorkflowsHandler replaces the handler for a "METHOD /path" pattern.
func withWorkflowsHandler(pattern string, h http.HandlerFunc) workflowsTestOption {
	return func(s *workflowsTestServer) {
		s.handlers[pattern] = h
	}
}

func respondJSON(status int, body string) http.HandlerFunc {
	return func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(status)
		_, _ = io.WriteString(w, body)
	}
}

func noContent(w http.ResponseWriter, _ *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

// newWorkflowsTestClient serves the task-run and flow-run endpoints under /v1
// with handlers that succeed by default. Options replace individual handlers.
func newWorkflowsTestClient(t *testing.T, opts ...workflowsTestOption) *WorkflowsService {
	t.Helper()
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")

	s := &workflowsTestServer{handlers: map[string]http.HandlerFunc{
		"POST /v1/task-runs":         respondJSON(http.StatusAccepted, taskRunJSON),
		"GET /v1/task-runs":          respondJSON(http.StatusOK, `[{"cursor":"c1","taskRun":`+taskRunJSON+`}]`),
		"GET /v1/task-runs/trn-1":    respondJSON(http.StatusOK, taskRunDetailsJSON),
		"DELETE /v1/task-runs/trn-1": noContent,
		"POST /v1/flow-runs":         respondJSON(http.StatusAccepted, flowRunJSON),
		"GET /v1/flow-runs":          respondJSON(http.StatusOK, `[{"cursor":"c1","flowRun":`+flowRunJSON+`}]`),
		"GET /v1/flow-runs/frn-1":    respondJSON(http.StatusOK, flowRunDetailsJSON),
		"DELETE /v1/flow-runs/frn-1": noContent,
	}}
	for _, opt := range opts {
		opt(s)
	}

	mux := http.NewServeMux()
	for pattern, h := range s.handlers {
		mux.HandleFunc(pattern, h)
	}
	srv := httptest.NewServer(mux)
	t.Cleanup(srv.Close)

	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"))
	require.NoError(t, err)
	return c.Workflows
}

// recordBody captures the request body and then responds with next.
func recordBody(got *string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		b, _ := io.ReadAll(r.Body)
		*got = string(b)
		next(w, r)
	}
}

// recordQuery captures the raw query string and then responds with next.
func recordQuery(got *string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		*got = r.URL.RawQuery
		next(w, r)
	}
}

func TestRunTask(t *testing.T) {
	tests := []struct {
		name     string
		opts     []RunTaskOption
		wantBody string
	}{
		{
			name:     "without idempotency key",
			wantBody: `{"task":"wf/my-task","input":[1,"a"]}`,
		},
		{
			name:     "with idempotency key",
			opts:     []RunTaskOption{WithIdempotencyKey("key-1")},
			wantBody: `{"task":"wf/my-task","input":[1,"a"],"idempotencyKey":"key-1"}`,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var gotBody string
			w := newWorkflowsTestClient(t, withWorkflowsHandler("POST /v1/task-runs",
				recordBody(&gotBody, respondJSON(http.StatusAccepted, taskRunJSON))))

			var input TaskData
			require.NoError(t, input.FromTaskData0([]interface{}{1, "a"}))

			run, err := w.RunTask(context.Background(), "wf/my-task", input, tt.opts...)
			require.NoError(t, err)
			require.JSONEq(t, tt.wantBody, gotBody)
			require.Equal(t, "trn-1", run.Id)
			require.Equal(t, TaskRunStatusPending, run.Status)
		})
	}
}

func TestRunFlow(t *testing.T) {
	tests := []struct {
		name     string
		opts     []RunFlowOption
		wantBody string
	}{
		{
			name:     "without idempotency key",
			wantBody: `{"flow":"wf/my-flow","input":[1,"a"]}`,
		},
		{
			name:     "with idempotency key",
			opts:     []RunFlowOption{WithFlowRunIdempotencyKey("key-1")},
			wantBody: `{"flow":"wf/my-flow","input":[1,"a"],"idempotencyKey":"key-1"}`,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var gotBody string
			w := newWorkflowsTestClient(t, withWorkflowsHandler("POST /v1/flow-runs",
				recordBody(&gotBody, respondJSON(http.StatusAccepted, flowRunJSON))))

			var input FlowInput
			require.NoError(t, input.FromFlowInput0([]interface{}{1, "a"}))

			run, err := w.RunFlow(context.Background(), "wf/my-flow", input, tt.opts...)
			require.NoError(t, err)
			require.JSONEq(t, tt.wantBody, gotBody)
			require.Equal(t, "frn-1", run.Id)
			require.Equal(t, FlowRunStatusPending, run.Status)
		})
	}
}

// workflowsCalls exercises every WorkflowsService endpoint method, keyed by the
// route it hits.
var workflowsCalls = []struct {
	name    string
	pattern string
	call    func(context.Context, *WorkflowsService) error
}{
	{
		name:    "run task",
		pattern: "POST /v1/task-runs",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.RunTask(ctx, "wf/my-task", TaskData{})
			return err
		},
	},
	{
		name:    "get task run",
		pattern: "GET /v1/task-runs/trn-1",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.GetTaskRun(ctx, "trn-1")
			return err
		},
	},
	{
		name:    "cancel task run",
		pattern: "DELETE /v1/task-runs/trn-1",
		call: func(ctx context.Context, w *WorkflowsService) error {
			return w.CancelTaskRun(ctx, "trn-1")
		},
	},
	{
		name:    "list task runs",
		pattern: "GET /v1/task-runs",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.ListTaskRuns(ctx, &ListTaskRunsParams{})
			return err
		},
	},
	{
		name:    "run flow",
		pattern: "POST /v1/flow-runs",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.RunFlow(ctx, "wf/my-flow", FlowInput{})
			return err
		},
	},
	{
		name:    "get flow run",
		pattern: "GET /v1/flow-runs/frn-1",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.GetFlowRun(ctx, "frn-1")
			return err
		},
	},
	{
		name:    "cancel flow run",
		pattern: "DELETE /v1/flow-runs/frn-1",
		call: func(ctx context.Context, w *WorkflowsService) error {
			return w.CancelFlowRun(ctx, "frn-1")
		},
	},
	{
		name:    "list flow runs",
		pattern: "GET /v1/flow-runs",
		call: func(ctx context.Context, w *WorkflowsService) error {
			_, err := w.ListFlowRuns(ctx, &ListFlowRunsParams{})
			return err
		},
	},
}

func TestWorkflowsErrorStatus(t *testing.T) {
	failing := respondJSON(http.StatusInternalServerError, `{"message":"boom"}`)
	for _, tt := range workflowsCalls {
		t.Run(tt.name, func(t *testing.T) {
			w := newWorkflowsTestClient(t, withWorkflowsHandler(tt.pattern, failing))
			require.ErrorContains(t, tt.call(context.Background(), w), tt.name+" failed with status 500")
		})
	}
}

func TestWorkflowsContextCanceled(t *testing.T) {
	for _, tt := range workflowsCalls {
		t.Run(tt.name, func(t *testing.T) {
			called := false
			w := newWorkflowsTestClient(t, withWorkflowsHandler(tt.pattern, func(http.ResponseWriter, *http.Request) {
				called = true
			}))

			ctx, cancel := context.WithCancel(context.Background())
			cancel()

			require.ErrorIs(t, tt.call(ctx, w), context.Canceled)
			require.False(t, called)
		})
	}
}

func TestGetTaskRun(t *testing.T) {
	w := newWorkflowsTestClient(t)

	details, err := w.GetTaskRun(context.Background(), "trn-1")
	require.NoError(t, err)
	require.Equal(t, "trn-1", details.Id)
	require.Equal(t, TaskRunStatusCompleted, details.Status)
	require.Equal(t, []interface{}{float64(2)}, details.Results)
}

func TestGetFlowRun(t *testing.T) {
	w := newWorkflowsTestClient(t)

	details, err := w.GetFlowRun(context.Background(), "frn-1")
	require.NoError(t, err)
	require.Equal(t, "frn-1", details.Id)
	require.Equal(t, FlowRunStatusSucceeded, details.Status)
	require.Equal(t, []interface{}{float64(2)}, details.Results)
}

func TestCancelRuns(t *testing.T) {
	w := newWorkflowsTestClient(t)

	require.NoError(t, w.CancelTaskRun(context.Background(), "trn-1"))
	require.NoError(t, w.CancelFlowRun(context.Background(), "frn-1"))
}

func TestListTaskRuns(t *testing.T) {
	limit := 2
	lastCursor := "c2"
	cursor := "c0"
	tests := []struct {
		name           string
		params         *ListTaskRunsParams
		response       string
		wantQuery      string
		wantIDs        []string
		wantNextCursor *string
	}{
		{
			name:      "empty page has no next cursor",
			params:    &ListTaskRunsParams{},
			response:  `[]`,
			wantIDs:   []string{},
			wantQuery: "",
		},
		{
			name:     "next cursor is the last item's cursor",
			params:   &ListTaskRunsParams{Limit: &limit, Cursor: &cursor},
			response: `[{"cursor":"c1","taskRun":` + taskRunJSON + `},{"cursor":"c2","taskRun":` + taskRunJSON + `}]`,
			// Query parameters are sorted by name.
			wantQuery:      "cursor=c0&limit=2",
			wantIDs:        []string{"trn-1", "trn-1"},
			wantNextCursor: &lastCursor,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var gotQuery string
			w := newWorkflowsTestClient(t, withWorkflowsHandler("GET /v1/task-runs",
				recordQuery(&gotQuery, respondJSON(http.StatusOK, tt.response))))

			list, err := w.ListTaskRuns(context.Background(), tt.params)
			require.NoError(t, err)
			require.Equal(t, tt.wantQuery, gotQuery)
			ids := make([]string, len(list.TaskRuns))
			for i, run := range list.TaskRuns {
				ids[i] = run.Id
			}
			require.Equal(t, tt.wantIDs, ids)
			require.Equal(t, tt.wantNextCursor, list.NextCursor)
		})
	}
}

func TestListFlowRuns(t *testing.T) {
	cursor := "c0"
	lastCursor := "c2"
	status := []FlowRunStatus{FlowRunStatusRunning}
	tests := []struct {
		name           string
		params         *ListFlowRunsParams
		response       string
		wantQuery      string
		wantIDs        []string
		wantNextCursor *string
	}{
		{
			name:      "empty page has no next cursor",
			params:    &ListFlowRunsParams{},
			response:  `[]`,
			wantIDs:   []string{},
			wantQuery: "",
		},
		{
			name:           "next cursor is the last item's cursor",
			params:         &ListFlowRunsParams{Cursor: &cursor, Status: &status},
			response:       `[{"cursor":"c1","flowRun":` + flowRunJSON + `},{"cursor":"c2","flowRun":` + flowRunJSON + `}]`,
			wantQuery:      "cursor=c0&status=running",
			wantIDs:        []string{"frn-1", "frn-1"},
			wantNextCursor: &lastCursor,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var gotQuery string
			w := newWorkflowsTestClient(t, withWorkflowsHandler("GET /v1/flow-runs",
				recordQuery(&gotQuery, respondJSON(http.StatusOK, tt.response))))

			list, err := w.ListFlowRuns(context.Background(), tt.params)
			require.NoError(t, err)
			require.Equal(t, tt.wantQuery, gotQuery)
			ids := make([]string, len(list.FlowRuns))
			for i, run := range list.FlowRuns {
				ids[i] = run.Id
			}
			require.Equal(t, tt.wantIDs, ids)
			require.Equal(t, tt.wantNextCursor, list.NextCursor)
		})
	}
}
