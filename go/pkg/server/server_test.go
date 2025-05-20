package server_test

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/stretchr/testify/require"
	"render.com/pkg/client"
	"render.com/pkg/executor"
	"render.com/pkg/executor/orchestratoradapter"
	"render.com/pkg/server"
	sdkserver2 "render.com/pkg/server"
	"render.com/pkg/task"
)

func addSquares(ctx task.TaskContext, a int, b int) int {
	var result1 int
	var result2 int

	_ = ctx.ExecuteTask(square, a).Get(&result1)
	_ = ctx.ExecuteTask(square, b).Get(&result2)
	return result1 + result2
}

func square(ctx task.TaskContext, a int) int {
	return a * a
}

func TestServer(t *testing.T) {
	t.Run("integration test", func(t *testing.T) {
		var finalResult int

		tasks := task.NewTasks()
		err := tasks.RegisterTask(addSquares)
		require.NoError(t, err)
		err = tasks.RegisterTask(square)
		require.NoError(t, err)

		serverOrchestrator := orchestratoradapter.NewServerAdapterFactory()
		executors := executor.NewExecutors(tasks, 3)
		handler := server.NewServerHandler(executors, serverOrchestrator)

		port := 8083
		go func() {
			srv, err := handler.Start(port)
			require.NoError(t, err)
			defer srv.Close()
		}()

		serverURL := fmt.Sprintf("http://localhost:%d", port)

		var testServerURL string

		squareATaskID := uuid.New().String()
		squareBTaskID := uuid.New().String()
		addSquaresTaskID := uuid.New().String()

		nextToken := uuid.New().String()

		remoteServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")

			if r.Method == "POST" && strings.HasPrefix(r.URL.Path, "/callback") {
				token := r.URL.Query().Get("token")
				require.Equal(t, nextToken, token)

				nextToken = uuid.New().String()

				var body client.CallbackRequest
				err := json.NewDecoder(r.Body).Decode(&body)
				require.NoError(t, err)

				if body.Status == client.CallbackRequestStatusSubtask {
					require.Equal(t, "square", body.Subtask.Name)
					var taskID string
					if body.Subtask.Input.([]interface{})[0].(float64) == 2 {
						taskID = squareATaskID
					} else if body.Subtask.Input.([]interface{})[0].(float64) == 3 {
						taskID = squareBTaskID
					} else {
						require.Fail(t, "invalid input")
					}

					response := client.CallbackResponse{
						TaskId: &taskID,
					}

					require.NoError(t, json.NewEncoder(w).Encode(response))

					request := sdkserver2.StartRequest{
						Name:        "square",
						TaskId:      taskID,
						Input:       body.Subtask.Input,
						ResponseUrl: testServerURL + fmt.Sprintf("/callback?token=%s", nextToken),
					}
					startBytes, err := json.Marshal(request)
					require.NoError(t, err)

					_, err = http.DefaultClient.Post(serverURL+"/start", "application/json", bytes.NewBuffer(startBytes))
					require.NoError(t, err)
				} else if body.Status == client.CallbackRequestStatusComplete {
					if body.Name == "addSquares" {
						require.Equal(t, client.CallbackRequestStatusComplete, body.Status)
						finalResult = int(body.Complete.Result.([]interface{})[0].(float64))

						response := client.CallbackResponse{
							TaskId: &body.TaskId,
						}
						require.NoError(t, json.NewEncoder(w).Encode(response))
					}
					if body.Name == "square" {
						response := client.CallbackResponse{}
						require.NoError(t, json.NewEncoder(w).Encode(response))

						request := sdkserver2.ContinueRequest{
							Name:        "square",
							TaskId:      body.TaskId,
							Input:       body.Complete.Result,
							ResponseUrl: testServerURL + fmt.Sprintf("/callback?token=%s", nextToken),
						}
						continueBytes, err := json.Marshal(request)
						require.NoError(t, err)
						_, err = http.DefaultClient.Post(serverURL+"/continue", "application/json", bytes.NewBuffer(continueBytes))
						require.NoError(t, err)
					}
				}

			}
		}))
		defer remoteServer.Close()

		testServerURL = remoteServer.URL

		request := sdkserver2.StartRequest{
			Name:        "addSquares",
			TaskId:      addSquaresTaskID,
			Input:       []interface{}{2, 3},
			ResponseUrl: testServerURL + fmt.Sprintf("/callback?token=%s", nextToken),
		}
		startBytes, err := json.Marshal(request)
		require.NoError(t, err)

		_, err = http.DefaultClient.Post(
			serverURL+"/start",
			"application/json",
			bytes.NewBuffer(startBytes),
		)
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			fmt.Println("finalResult", finalResult)
			return finalResult == 13
		}, time.Second*1, time.Millisecond*100)
	})
}
