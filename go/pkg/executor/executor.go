package executor

import (
	"context"
	"log"
	"runtime/debug"

	"render.com/pkg/task"
)

type Executor struct {
	tasks        *task.Tasks
	orchestrator OrchestratorAdapter
	executorDone func(taskID string)
}

type OrchestratorAdapter interface {
	CompleteTask(ctx context.Context, taskName string, result interface{}) error
	ExecuteTask(taskName string, input ...interface{}) ([]interface{}, error)
}

func NewExecutor(tasks *task.Tasks, orchestrator OrchestratorAdapter, executorDone func(taskID string)) *Executor {
	return &Executor{
		tasks:        tasks,
		orchestrator: orchestrator,
		executorDone: executorDone,
	}
}

func (e *Executor) Execute(ctx context.Context, taskName string, taskID string, input ...interface{}) error {
	// Ensure the task is registered
	_, err := e.tasks.GetTaskByName(taskName)
	if err != nil {
		return err
	}

	go func() {
		defer func() {
			if r := recover(); r != nil {
				log.Printf("Recovered from panic: %v", r)
				log.Printf("Stack trace: %s", string(debug.Stack()))
			}
		}()

		log.Printf("Executing task: %s, input: %v", taskName, input)

		result, err := e.tasks.ExecuteTaskByName(taskName, e, input...)
		if err == nil {
			log.Printf("Task completed: %s", taskName)
			e.orchestrator.CompleteTask(context.Background(), taskName, result)
			e.executorDone(taskID)
		}
	}()

	return nil
}

func (e *Executor) ExecuteTask(t task.Task, input ...interface{}) *task.TaskResult {
	taskName, err := task.GetFunctionName(t)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	log.Printf("Calling task: %s", taskName)

	result, err := e.orchestrator.ExecuteTask(taskName, input...)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	log.Printf("Task completed: %s", taskName)

	return &task.TaskResult{Result: result}
}
