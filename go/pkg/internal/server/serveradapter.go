package server

import (
	"context"
	"fmt"
	"log"
	"strings"
	"sync"

	"render.com/pkg/internal/client"
	"render.com/pkg/internal/executor"
)

type exec interface {
	Execute(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error
}

type ServerAdapter struct {
	responseURL string
	taskID      string
	ch          chan SubtaskResultWithResponseURL
	executor    exec

	mu sync.Mutex
}

func NewServerAdapter(executor exec) *ServerAdapter {
	return &ServerAdapter{
		ch:       make(chan SubtaskResultWithResponseURL, 1),
		executor: executor,
	}
}

func (s *ServerAdapter) setTaskState(responseURL string, taskID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.taskID != "" {
		return fmt.Errorf("task already started")
	}

	s.responseURL = responseURL
	s.taskID = taskID
	return nil
}

func (s *ServerAdapter) clearTaskState() {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.responseURL = ""
	s.taskID = ""
}

func (s *ServerAdapter) StartTask(responseURL string, taskName string, taskID string, input ...interface{}) error {
	err := s.setTaskState(responseURL, taskID)
	if err != nil {
		return err
	}

	return s.executor.Execute(context.Background(), s.completeTask, s.executeTask, taskName, input...)
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

func (s *ServerAdapter) completeTask(ctx context.Context, taskName string, result interface{}) error {
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
	if err != nil {
		return err
	}

	s.clearTaskState()
	return nil
}

func (s *ServerAdapter) executeTask(taskName string, input ...interface{}) ([]interface{}, error) {
	c, err := client.NewClientWithResponses(s.responseURL)
	if err != nil {
		return nil, err
	}
	_, err = c.PostCallbackWithResponse(context.Background(), &client.PostCallbackParams{
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
	result := s.WaitForTaskResult()
	s.responseURL = result.ResponseURL

	return result.Result, nil
}

func (s *ServerAdapter) WaitForTaskResult() SubtaskResultWithResponseURL {
	log.Printf("Waiting for task result")
	return <-s.ch
}

func (s *ServerAdapter) SubtaskComplete(result []interface{}, responseURL string) {
	s.ch <- SubtaskResultWithResponseURL{
		SubtaskResult: SubtaskResult{
			Result: result,
		},
		ResponseURL: responseURL,
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
