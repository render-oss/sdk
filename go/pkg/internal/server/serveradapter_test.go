package server_test

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"

	"github.com/stretchr/testify/require"
	"render.com/pkg/internal/client"
	"render.com/pkg/internal/executor"
	"render.com/pkg/internal/server"
)

type testExecutor struct {
	execute func(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error
}

func (e *testExecutor) Execute(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error {
	return e.execute(ctx, completeTask, executeTask, taskName, input...)
}

func TestNewServerAdapter(t *testing.T) {
	t.Run("can execute task", func(t *testing.T) {
		executor := &testExecutor{
			execute: func(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error {
				result, err := executeTask("test", 1)
				require.NoError(t, err)
				require.Equal(t, []interface{}{"test result"}, result)

				result, err = executeTask("test", 2)
				require.NoError(t, err)
				require.Equal(t, []interface{}{"test result 2"}, result)

				require.NoError(t, completeTask(ctx, taskName, "test result 3"))
				return nil
			},
		}

		orchestrator := server.NewServerAdapter(executor)

		waitGroup := sync.WaitGroup{}
		waitGroup.Add(1)

		var url string
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")

			token := r.URL.Query().Get("token")
			if r.Method == "POST" && token == "first" {
				var body client.CallbackRequest
				err := json.NewDecoder(r.Body).Decode(&body)
				require.NoError(t, err)
				require.Equal(t, "test", body.Name)
				require.Equal(t, "taskID", body.TaskId)
				require.Equal(t, client.CallbackRequestStatusSubtask, body.Status)
				require.Equal(t, "test", body.Subtask.Name)
				require.Equal(t, 1, int(body.Subtask.Input.([]interface{})[0].(float64)))

				taskID := "subtaskID"

				orchestrator.SubtaskComplete([]interface{}{"test result"}, url+"?token=second")

				response := &client.CallbackResponse{
					TaskId: &taskID,
				}
				require.NoError(t, json.NewEncoder(w).Encode(response))
			} else if r.Method == "POST" && token == "second" {
				var body client.CallbackRequest
				err := json.NewDecoder(r.Body).Decode(&body)
				require.NoError(t, err)
				require.Equal(t, "test", body.Name)
				require.Equal(t, "taskID", body.TaskId)
				require.Equal(t, client.CallbackRequestStatusSubtask, body.Status)
				require.Equal(t, "test", body.Subtask.Name)
				require.Equal(t, 2, int(body.Subtask.Input.([]interface{})[0].(float64)))

				taskID := "subtaskID2"

				orchestrator.SubtaskComplete([]interface{}{"test result 2"}, url+"?token=third")

				response := &client.CallbackResponse{
					TaskId: &taskID,
				}
				require.NoError(t, json.NewEncoder(w).Encode(response))
			} else if r.Method == "POST" && token == "third" {
				var body client.CallbackRequest
				err := json.NewDecoder(r.Body).Decode(&body)
				require.NoError(t, err)
				require.Equal(t, "test", body.Name)
				require.Equal(t, "taskID", body.TaskId)
				require.Equal(t, client.CallbackRequestStatusComplete, body.Status)
				require.Equal(t, "test result 3", body.Complete.Result)

				taskID := body.TaskId

				// Wait for the task to be completed
				waitGroup.Done()

				response := &client.CallbackResponse{
					TaskId: &taskID,
				}
				require.NoError(t, json.NewEncoder(w).Encode(response))
			} else {
				require.Fail(t, "unexpected request")
			}
			w.WriteHeader(http.StatusOK)
		}))
		defer server.Close()

		url = server.URL
		err := orchestrator.StartTask(url+"?token=first", "test", "taskID")
		require.NoError(t, err)

		waitGroup.Wait()
	})

	t.Run("can complete task", func(t *testing.T) {
		waitGroup := sync.WaitGroup{}
		waitGroup.Add(1)

		executor := &testExecutor{
			execute: func(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error {
				require.NoError(t, completeTask(ctx, taskName, "test result"))
				return nil
			},
		}
		orchestrator := server.NewServerAdapter(executor)

		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")

			if r.Method == "POST" && r.URL.Path == "/callback" {
				waitGroup.Done()
				var body client.CallbackRequest
				err := json.NewDecoder(r.Body).Decode(&body)
				require.NoError(t, err)
				require.Equal(t, "test", body.Name)
				require.Equal(t, "taskID", body.TaskId)
				require.Equal(t, client.CallbackRequestStatusComplete, body.Status)
				require.Equal(t, "test result", body.Complete.Result)

				taskID := body.TaskId

				response := &client.CallbackResponse{
					TaskId: &taskID,
				}
				require.NoError(t, json.NewEncoder(w).Encode(response))
			}
		}))
		defer server.Close()

		err := orchestrator.StartTask(server.URL, "test", "taskID")
		require.NoError(t, err)

		waitGroup.Wait()
	})
}
