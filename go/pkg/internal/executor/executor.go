package executor

import (
	"context"
	"log"
	"runtime/debug"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
)

type Executor struct {
	tasks *task.Tasks
}

type CompleteTask func(ctx context.Context, taskName string, result interface{}) error
type ExecuteTask func(taskName string, input ...interface{}) ([]interface{}, error)

func NewExecutor(tasks *task.Tasks) *Executor {
	return &Executor{
		tasks: tasks,
	}
}

func (e *Executor) Execute(ctx context.Context, completeTask CompleteTask, executeTask ExecuteTask, taskName string, input ...interface{}) error {
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

		result, err := e.tasks.ExecuteTaskByName(taskName, newExecutorContext(executeTask), input...)
		if err == nil {
			log.Printf("Task completed: %s", taskName)
			taskErr := completeTask(context.Background(), taskName, result)
			if taskErr != nil {
				log.Printf("Error completing task: %s", taskErr)
			}
		}
	}()

	return nil
}

type executorContext struct {
	executeTask ExecuteTask
}

func newExecutorContext(executeTask ExecuteTask) *executorContext {
	return &executorContext{
		executeTask: executeTask,
	}
}

func (e *executorContext) ExecuteTask(t task.Task, input ...interface{}) *task.TaskResult {
	taskName, err := task.GetFunctionName(t)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	log.Printf("Calling task: %s", taskName)

	result, err := e.executeTask(taskName, input...)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	log.Printf("Task completed: %s", taskName)

	return &task.TaskResult{Result: result}
}
