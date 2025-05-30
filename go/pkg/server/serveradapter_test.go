package server_test

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"

	"github.com/stretchr/testify/require"
	"render.com/pkg/client"
	"render.com/pkg/executor/orchestratoradapter"
)

func TestNewServerAdapter(t *testing.T) {
	t.Run("can execute task", func(t *testing.T) {
		channel := make(chan orchestratoradapter.SubtaskResultWithResponseURL, 1)

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

				channel <- orchestratoradapter.SubtaskResultWithResponseURL{
					ResponseURL: url + "?token=second",
					SubtaskResult: orchestratoradapter.SubtaskResult{
						Name:   "test",
						Result: []interface{}{"test result"},
						TaskID: taskID,
					},
				}

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

				channel <- orchestratoradapter.SubtaskResultWithResponseURL{
					ResponseURL: url,
					SubtaskResult: orchestratoradapter.SubtaskResult{
						Name:   "test",
						Result: []interface{}{"test result 2"},
						TaskID: taskID,
					},
				}

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

		waitFunc := func(taskID string) orchestratoradapter.SubtaskResultWithResponseURL {
			return <-channel
		}

		orchestrator := orchestratoradapter.NewServerAdapter(url+"?token=first", "taskID", waitFunc)

		result, err := orchestrator.ExecuteTask("test", 1)
		require.NoError(t, err)
		require.Equal(t, []interface{}{"test result"}, result)

		result, err = orchestrator.ExecuteTask("test", 2)
		require.NoError(t, err)
		require.Equal(t, []interface{}{"test result 2"}, result)
	})

	t.Run("can complete task", func(t *testing.T) {
		waitGroup := sync.WaitGroup{}
		waitGroup.Add(1)

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

		orchestrator := orchestratoradapter.NewServerAdapter(server.URL, "taskID", nil)

		err := orchestrator.CompleteTask(context.Background(), "test", "test result")
		require.NoError(t, err)

		waitGroup.Wait()
	})
}
