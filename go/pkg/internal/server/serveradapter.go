package server

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"log/slog"
	"os"
	"sync"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/callbackapi"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/executor"
)

type exec interface {
	Execute(ctx context.Context, completeTask executor.CompleteTask, executeTask executor.ExecuteTask, taskName string, input ...interface{}) error
}

type ServerAdapter struct {
	responseURL  string
	taskID       string
	ch           chan SubtaskResultWithResponseURL
	executor     exec
	taskComplete chan struct{}

	callbacker *callbackapi.ClientWithResponses
	mu         sync.Mutex
}

func NewServerAdapter(executor exec, callbacker *callbackapi.ClientWithResponses) *ServerAdapter {
	return &ServerAdapter{
		ch:           make(chan SubtaskResultWithResponseURL, 1),
		executor:     executor,
		taskComplete: make(chan struct{}),
		callbacker:   callbacker,
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

func (s *ServerAdapter) CancelTask(taskID string) error {
	os.Exit(0)
	return nil
}

func (s *ServerAdapter) completeTask(ctx context.Context, taskName string, result []interface{}, taskErr error) error {
	defer close(s.taskComplete)
	output, err := json.Marshal(result)
	if err != nil {
		return fmt.Errorf("failed to marshal output: %w", err)
	}

	resp, err := s.callbacker.PostCallbackWithResponse(ctx, callbackapi.CallbackRequest{
		Complete: &callbackapi.TaskComplete{
			Output: output,
		},
		Metadata: &callbackapi.TaskMetadata{
			TaskName: taskName,
		},
		Status: callbackapi.Complete,
	})
	if err != nil {
		return err
	}

	if resp.StatusCode() != 200 {
		return fmt.Errorf("callback failed with status code %d", resp.StatusCode())
	}

	s.clearTaskState()
	return nil
}

func (s *ServerAdapter) WaitForTaskComplete() {
	slog.Info("waiting for task complete")
	<-s.taskComplete
	slog.Info("finished waiting for task complete")
}

func (s *ServerAdapter) executeTask(taskName string, input ...interface{}) ([]interface{}, error) {
	return nil, errors.New("not implemented")
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
