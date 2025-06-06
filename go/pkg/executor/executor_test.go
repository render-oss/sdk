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
		completeTask := func(ctx context.Context, taskName string, result interface{}) error {
			completeTaskCalled = true
			require.Equal(t, taskName, "testTask")
			resultValue := result.([]interface{})[0].(string)
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
		completeTask := func(ctx context.Context, taskName string, result interface{}) error {
			completeTaskCalled = true
			resultValue := result.([]interface{})[0].(string)
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
}
