package server_test

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/client"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/executor"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/server"
	"github.com/stretchr/testify/require"
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

				require.NoError(t, completeTask(ctx, taskName, []interface{}{"test result 3"}, nil))
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
				require.Equal(t, 1, int(body.Subtask.Input[0].(float64)))

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
				require.Equal(t, 2, int(body.Subtask.Input[0].(float64)))

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
				require.Equal(t, []interface{}{"test result 3"}, body.Complete.Result)
				require.Nil(t, body.Complete.Error)

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
				require.NoError(t, completeTask(ctx, taskName, []interface{}{"test result"}, nil))
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
				require.Equal(t, []interface{}{"test result"}, body.Complete.Result)
				require.Nil(t, body.Complete.Error)

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

	t.Run("can complete task with error", func(t *testing.T) {
		waitGroup := sync.WaitGroup{}
		waitGroup.Add(1)

		taskError := errors.New("task execution failed")
		executor := &testExecutor{
			execute: func(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error {
				require.NoError(t, completeTask(ctx, taskName, []interface{}{"partial result"}, taskError))
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
				require.Equal(t, []interface{}{"partial result"}, body.Complete.Result)
				require.NotNil(t, body.Complete.Error)
				require.Equal(t, "task execution failed", (*body.Complete.Error).(string))

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
