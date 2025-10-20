package executor_test

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/require"

	"github.com/render-oss/sdk/go/pkg/internal/callbackapi"
	"github.com/render-oss/sdk/go/pkg/internal/executor"
	"github.com/render-oss/sdk/go/pkg/internal/task"
)

func testTask(_ task.TaskContext) (interface{}, error) {
	return "test", nil
}

func failingTask(_ task.TaskContext) (string, error) {
	return "partial result", errors.New("task failed")
}

func TestExecuteTask(t *testing.T) {
	t.Run("simple task", func(t *testing.T) {
		tasks := task.NewTasks()
		err := tasks.RegisterTask(testTask)
		require.NoError(t, err)

		callbackCalled := false

		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			require.Equal(t, r.URL.Path, "/callback")
			body, err := io.ReadAll(r.Body)
			require.NoError(t, err)

			var callbackRequest callbackapi.CallbackRequest
			err = json.Unmarshal(body, &callbackRequest)
			require.NoError(t, err)

			require.Equal(t, callbackRequest.Complete.Output, []byte("[\"test\"]"))
			callbackCalled = true
			w.WriteHeader(200)
		}))

		callbackerClient, err := callbackapi.NewClientWithResponses(srv.URL)
		require.NoError(t, err)

		executor := executor.NewExecutor(tasks, callbackerClient)
		err = executor.Execute(context.Background(), "testTask")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return callbackCalled
		}, time.Second*1, time.Millisecond*100)
	})

	t.Run("task with error", func(t *testing.T) {
		tasks := task.NewTasks()
		err := tasks.RegisterTask(failingTask)
		require.NoError(t, err)

		callbackCalled := false

		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			require.Equal(t, r.URL.Path, "/callback")
			body, err := io.ReadAll(r.Body)
			require.NoError(t, err)

			var callbackRequest callbackapi.CallbackRequest
			err = json.Unmarshal(body, &callbackRequest)
			require.NoError(t, err)

			require.Equal(t, callbackRequest.Error.Details, "task failed")
			callbackCalled = true
			w.WriteHeader(200)
		}))

		callbackerClient, err := callbackapi.NewClientWithResponses(srv.URL)
		require.NoError(t, err)

		executor := executor.NewExecutor(tasks, callbackerClient)
		err = executor.Execute(context.Background(), "failingTask")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return callbackCalled
		}, time.Second*1, time.Millisecond*100)
	})
}
