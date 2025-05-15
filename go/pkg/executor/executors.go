package executor

import (
	"errors"

	"render.com/pkg/task"
)

type Executors struct {
	tasks         *task.Tasks
	executors     map[string]*Executor
	maxConcurrent int
}

func NewExecutors(tasks *task.Tasks, maxConcurrent int) *Executors {
	executors := make(map[string]*Executor)

	return &Executors{
		tasks:         tasks,
		executors:     executors,
		maxConcurrent: maxConcurrent,
	}
}

func (e *Executors) NewExecutor(taskID string, orchestratorAdapter OrchestratorAdapter) (*Executor, error) {
	if _, ok := e.executors[taskID]; ok {
		return nil, errors.New("executor already exists")
	}

	if len(e.executors) >= e.maxConcurrent {
		return nil, errors.New("max concurrent executors reached")
	}

	executor := NewExecutor(e.tasks, orchestratorAdapter, e.ExecutorDone)
	e.executors[taskID] = executor
	return executor, nil
}

func (e *Executors) ExecutorDone(taskID string) {
	delete(e.executors, taskID)
}
