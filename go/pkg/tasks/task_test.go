package tasks

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/render-oss/sdk/go/pkg/internal/callbackapi"
)

func readMetadata(ctx TaskContext) []TaskRunMetadata {
	metadata := ctx.Metadata()
	return []TaskRunMetadata{metadata, ctx.Metadata()}
}

func mutateReturnedMetadata(ctx TaskContext) TaskRunMetadata {
	returned := ctx.Metadata()
	returned.TaskRunID = "modified"
	return ctx.Metadata()
}

func TestExecuteTaskRunMetadata(t *testing.T) {
	require.NoError(t, RegisterTask(readMetadata))
	for _, test := range []struct {
		name string
		ids  map[string]string
		want TaskRunMetadata
	}{
		{"older server", nil, TaskRunMetadata{}},
		{"empty root ID on root", map[string]string{"task_run_id": "trn-root", "root_task_run_id": ""}, TaskRunMetadata{TaskRunID: "trn-root"}},
		{"empty root ID on child", map[string]string{"task_run_id": "trn-child", "root_task_run_id": "", "parent_task_run_id": "trn-parent"}, TaskRunMetadata{TaskRunID: "trn-child", ParentTaskRunID: "trn-parent"}},
		{"root", map[string]string{"task_run_id": "trn-root", "root_task_run_id": "trn-root"}, TaskRunMetadata{TaskRunID: "trn-root", RootTaskRunID: "trn-root"}},
		{"child", map[string]string{"task_run_id": "trn-child", "root_task_run_id": "trn-root", "parent_task_run_id": "trn-parent"}, TaskRunMetadata{TaskRunID: "trn-child", RootTaskRunID: "trn-root", ParentTaskRunID: "trn-parent"}},
	} {
		t.Run(test.name, func(t *testing.T) {
			inputRequests := 0
			var result callbackapi.CallbackRequest
			srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				switch r.URL.Path {
				case "/input":
					inputRequests++
					payload := map[string]string{"task_name": "readMetadata", "input": "W10="}
					for key, value := range test.ids {
						payload[key] = value
					}
					w.Header().Set("Content-Type", "application/json")
					require.NoError(t, json.NewEncoder(w).Encode(payload))
				case "/callback":
					require.NoError(t, json.NewDecoder(r.Body).Decode(&result))
				default:
					t.Errorf("unexpected request: %s", r.URL.Path)
					w.WriteHeader(http.StatusNotFound)
				}
			}))
			t.Cleanup(srv.Close)
			client, err := callbackapi.NewClientWithResponses(srv.URL)
			require.NoError(t, err)
			require.NoError(t, executeTask(context.Background(), client))
			require.Equal(t, 1, inputRequests)
			require.Nil(t, result.Error)
			require.NotNil(t, result.Complete)
			var output [][]TaskRunMetadata
			require.NoError(t, json.Unmarshal(result.Complete.Output, &output))
			require.Equal(t, [][]TaskRunMetadata{{test.want, test.want}}, output)
		})
	}
}

func TestTaskContextMetadataReturnsCopy(t *testing.T) {
	metadata := TaskRunMetadata{
		TaskRunID:       "trn-child",
		RootTaskRunID:   "trn-root",
		ParentTaskRunID: "trn-parent",
	}
	require.NoError(t, RegisterTask(mutateReturnedMetadata))

	var result callbackapi.CallbackRequest
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/input":
			w.Header().Set("Content-Type", "application/json")
			require.NoError(t, json.NewEncoder(w).Encode(map[string]string{
				"task_name":          "mutateReturnedMetadata",
				"input":              "W10=",
				"task_run_id":        metadata.TaskRunID,
				"root_task_run_id":   metadata.RootTaskRunID,
				"parent_task_run_id": metadata.ParentTaskRunID,
			}))
		case "/callback":
			require.NoError(t, json.NewDecoder(r.Body).Decode(&result))
		}
	}))
	t.Cleanup(srv.Close)
	client, err := callbackapi.NewClientWithResponses(srv.URL)
	require.NoError(t, err)
	require.NoError(t, executeTask(context.Background(), client))

	var output []TaskRunMetadata
	require.NoError(t, json.Unmarshal(result.Complete.Output, &output))
	require.Equal(t, []TaskRunMetadata{metadata}, output)
}
