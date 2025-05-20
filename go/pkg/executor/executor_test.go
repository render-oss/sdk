package executor_test

import (
	"context"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	"render.com/pkg/executor"
	"render.com/pkg/task"
)

func testTask(_ task.TaskContext) (interface{}, error) {
	return "test", nil
}

// parentTask is defined up here so we can get a real name for the task
// anonymous functions don't have a clear name
type parentTask struct {
	t        *testing.T
	executor *executor.Executor
}

func (p *parentTask) ParentTask(_ task.TaskContext) (interface{}, error) {
	result := p.executor.ExecuteTask(testTask)
	require.NoError(p.t, result.Error)
	return "parent-" + result.Result[0].(string), nil
}

type fakeOrchestrator struct {
	completeTask func(ctx context.Context, taskName string, result interface{}) error
	executeTask  func(taskName string, input ...interface{}) ([]interface{}, error)
}

func (f *fakeOrchestrator) CompleteTask(ctx context.Context, taskName string, result interface{}) error {
	return f.completeTask(ctx, taskName, result)
}

func (f *fakeOrchestrator) ExecuteTask(taskName string, input ...interface{}) ([]interface{}, error) {
	return f.executeTask(taskName, input...)
}

func TestExecuteTask(t *testing.T) {
	t.Run("simple task", func(t *testing.T) {

		tasks := task.NewTasks()
		err := tasks.RegisterTask(testTask)
		require.NoError(t, err)

		orchestrator := &fakeOrchestrator{}
		completeTaskCalled := false
		orchestrator.completeTask = func(ctx context.Context, taskName string, result interface{}) error {
			completeTaskCalled = true
			require.Equal(t, taskName, "testTask")
			resultValue := result.([]interface{})[0].(string)
			require.Equal(t, resultValue, "test")
			return nil
		}
		orchestrator.executeTask = func(taskName string, input ...interface{}) ([]interface{}, error) {
			require.Fail(t, "should not be called")
			return []interface{}{"test"}, nil
		}

		executors := executor.NewExecutors(tasks, 1)

		executor, err := executors.NewExecutor("taskID", orchestrator)
		require.NoError(t, err)
		err = executor.Execute(context.Background(), "testTask", "taskID")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return completeTaskCalled
		}, time.Second*1, time.Millisecond*100)
	})

	t.Run("subtask", func(t *testing.T) {
		taskID := "taskID"

		orchestrator := &fakeOrchestrator{}
		tasks := task.NewTasks()
		err := tasks.RegisterTask(testTask)
		require.NoError(t, err)
		executors := executor.NewExecutors(tasks, 2)

		executor, err := executors.NewExecutor(taskID, orchestrator)
		require.NoError(t, err)

		completeTaskCalled := false
		orchestrator.completeTask = func(ctx context.Context, taskName string, result interface{}) error {
			completeTaskCalled = true
			resultValue := result.([]interface{})[0].(string)
			require.Equal(t, "parent-subtask", resultValue)
			return nil
		}
		orchestrator.executeTask = func(taskName string, input ...interface{}) ([]interface{}, error) {
			require.Equal(t, taskName, "testTask")
			require.Len(t, input, 0)
			return []interface{}{"subtask"}, nil
		}

		p := parentTask{t: t, executor: executor}
		err = tasks.RegisterTask(p.ParentTask)
		require.NoError(t, err)

		err = executor.Execute(context.Background(), "ParentTask", "taskID")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return completeTaskCalled
		}, time.Second*20, time.Millisecond*100)
	})

	t.Run("too many executors", func(t *testing.T) {
		orchestrator := &fakeOrchestrator{}
		tasks := task.NewTasks()
		executors := executor.NewExecutors(tasks, 1)

		_, err := executors.NewExecutor("task", orchestrator)
		require.NoError(t, err)

		_, err = executors.NewExecutor("other task", orchestrator)
		require.Error(t, err)
	})

	t.Run("cannot get executor for the same task", func(t *testing.T) {
		orchestrator := &fakeOrchestrator{}
		tasks := task.NewTasks()
		executors := executor.NewExecutors(tasks, 1)

		_, err := executors.NewExecutor("task", orchestrator)
		require.NoError(t, err)

		_, err = executors.NewExecutor("task", orchestrator)
		require.Error(t, err)
	})
}
