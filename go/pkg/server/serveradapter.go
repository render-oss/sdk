package server

import (
	"context"
	"log"
	"strings"
	"sync"

	"render.com/pkg/client"
)

type ServerAdapter struct {
	responseURL   string
	taskID        string
	waitForResult waitForResult
}

func NewServerAdapter(responseURL string, taskID string, waitForResult waitForResult) *ServerAdapter {
	return &ServerAdapter{
		responseURL:   responseURL,
		taskID:        taskID,
		waitForResult: waitForResult,
	}
}

func (s *ServerAdapter) tokenFromURL(url string) string {
	parts := strings.Split(url, "?")
	if len(parts) != 2 {
		return ""
	}
	token := parts[1]
	parts = strings.Split(token, "=")
	if len(parts) != 2 {
		return ""
	}
	return parts[1]
}

func (s *ServerAdapter) CompleteTask(ctx context.Context, taskName string, result interface{}) error {
	c, err := client.NewClientWithResponses(s.responseURL)
	if err != nil {
		return err
	}
	_, err = c.PostCallback(ctx, &client.PostCallbackParams{
		Token: s.tokenFromURL(s.responseURL),
	}, client.PostCallbackJSONRequestBody{
		Name:   taskName,
		Status: client.CallbackRequestStatusComplete,
		TaskId: s.taskID,
		Complete: &client.TaskComplete{
			Result: result,
		},
	})
	return err
}

func (s *ServerAdapter) ExecuteTask(taskName string, input ...interface{}) ([]interface{}, error) {
	c, err := client.NewClientWithResponses(s.responseURL)
	if err != nil {
		return nil, err
	}
	rsp, err := c.PostCallbackWithResponse(context.Background(), &client.PostCallbackParams{
		Token: s.tokenFromURL(s.responseURL),
	}, client.PostCallbackJSONRequestBody{
		Name:   taskName,
		TaskId: s.taskID,
		Status: client.CallbackRequestStatusSubtask,
		Subtask: &client.Subtask{
			Name:  taskName,
			Input: input,
		},
	})
	if err != nil {
		return nil, err
	}
	subTaskID := *rsp.JSON200.TaskId
	result := s.waitForResult(subTaskID)
	s.responseURL = result.ResponseURL

	return result.Result, nil
}

type ServerAdapterFactory struct {
	mu            sync.Mutex
	waitForResult map[string]chan SubtaskResultWithResponseURL
}

func NewServerAdapterFactory() *ServerAdapterFactory {
	return &ServerAdapterFactory{
		waitForResult: make(map[string]chan SubtaskResultWithResponseURL),
	}
}

type SubtaskResultWithResponseURL struct {
	SubtaskResult
	ResponseURL string
}

type SubtaskResult struct {
	Name   string
	Result []interface{}
	TaskID string
}

type waitForResult func(taskID string) SubtaskResultWithResponseURL

func (f *ServerAdapterFactory) NewOrchestratorAdapter(responseURL string, taskID string) *ServerAdapter {
	return NewServerAdapter(responseURL, taskID, f.WaitForTaskResult)
}

func (f *ServerAdapterFactory) GetChannel(taskID string) chan SubtaskResultWithResponseURL {
	f.mu.Lock()
	defer f.mu.Unlock()
	channel, ok := f.waitForResult[taskID]
	if !ok {
		channel = make(chan SubtaskResultWithResponseURL, 1)
		f.waitForResult[taskID] = channel
	}
	return channel
}

func (f *ServerAdapterFactory) WaitForTaskResult(taskID string) SubtaskResultWithResponseURL {
	log.Printf("Waiting for task result: %s", taskID)
	return <-f.GetChannel(taskID)
}

func (f *ServerAdapterFactory) SubtaskComplete(taskID string, result []interface{}, responseURL string) {
	f.GetChannel(taskID) <- SubtaskResultWithResponseURL{
		SubtaskResult: SubtaskResult{
			Result: result,
		},
		ResponseURL: responseURL,
	}
}
