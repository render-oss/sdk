package executor_test

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/executor"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
	"github.com/stretchr/testify/require"
)

func testTask(_ task.TaskContext) (interface{}, error) {
	return "test", nil
}

func failingTask(_ task.TaskContext) (string, error) {
	return "partial result", errors.New("task failed")
}

// parentTask is defined up here so we can get a real name for the task
// anonymous functions don't have a clear name
type parentTask struct {
	t *testing.T
}

func (p *parentTask) ParentTask(ctx task.TaskContext) (interface{}, error) {
	result := ctx.ExecuteTask(testTask)
	require.NoError(p.t, result.Error)
	return "parent-" + result.Result[0].(string), nil
}

func TestExecuteTask(t *testing.T) {
	t.Run("simple task", func(t *testing.T) {
		tasks := task.NewTasks()
		err := tasks.RegisterTask(testTask)
		require.NoError(t, err)

		completeTaskCalled := false
		completeTask := func(ctx context.Context, taskName string, result []interface{}, err error) error {
			completeTaskCalled = true
			require.Equal(t, taskName, "testTask")
			require.NoError(t, err)
			resultValue := result[0].(string)
			require.Equal(t, resultValue, "test")
			return nil
		}
		executeTask := func(taskName string, input ...interface{}) ([]interface{}, error) {
			require.Fail(t, "should not be called")
			return []interface{}{"test"}, nil
		}

		executor := executor.NewExecutor(tasks)
		err = executor.Execute(context.Background(), completeTask, executeTask, "testTask")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return completeTaskCalled
		}, time.Second*1, time.Millisecond*100)
	})

	t.Run("subtask", func(t *testing.T) {
		tasks := task.NewTasks()
		err := tasks.RegisterTask(testTask)
		require.NoError(t, err)

		executor := executor.NewExecutor(tasks)

		completeTaskCalled := false
		completeTask := func(ctx context.Context, taskName string, result []interface{}, err error) error {
			completeTaskCalled = true
			require.NoError(t, err)
			resultValue := result[0].(string)
			require.Equal(t, "parent-subtask", resultValue)
			return nil
		}
		executeTask := func(taskName string, input ...interface{}) ([]interface{}, error) {
			require.Equal(t, taskName, "testTask")
			require.Len(t, input, 0)
			return []interface{}{"subtask"}, nil
		}

		p := parentTask{t: t}
		err = tasks.RegisterTask(p.ParentTask)
		require.NoError(t, err)

		err = executor.Execute(context.Background(), completeTask, executeTask, "ParentTask")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return completeTaskCalled
		}, time.Second*1, time.Millisecond*100)
	})

	t.Run("task with error", func(t *testing.T) {
		// Test that errors from tasks are properly passed through
		tasks := task.NewTasks()
		err := tasks.RegisterTask(failingTask)
		require.NoError(t, err)

		completeTaskCalled := false
		var receivedError error
		var receivedResult []interface{}

		completeTask := func(ctx context.Context, taskName string, result []interface{}, err error) error {
			completeTaskCalled = true
			receivedError = err
			receivedResult = result
			require.Equal(t, "failingTask", taskName)
			return nil
		}

		executeTask := func(taskName string, input ...interface{}) ([]interface{}, error) {
			require.Fail(t, "should not be called")
			return nil, nil
		}

		executor := executor.NewExecutor(tasks)
		err = executor.Execute(context.Background(), completeTask, executeTask, "failingTask")
		require.NoError(t, err)

		require.Eventually(t, func() bool {
			return completeTaskCalled
		}, time.Second*1, time.Millisecond*100)

		// Verify the error was passed through
		require.Error(t, receivedError)
		require.Equal(t, "task failed", receivedError.Error())

		// Verify the result was passed through (without the error)
		require.NotNil(t, receivedResult)
		resultSlice := receivedResult[0].(string)
		require.Equal(t, "partial result", resultSlice)
	})
}
