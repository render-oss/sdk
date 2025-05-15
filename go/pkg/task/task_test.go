package task_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"
	"render.com/pkg/task"
)

func add(_ task.TaskContext, a int, b int) int {
	return a + b
}

type fakeTaskContext struct {
}

func (f *fakeTaskContext) ExecuteTask(ctx context.Context, taskName string, input interface{}) (interface{}, error) {
	return nil, nil
}

func TestTaskGetTaskNames(t *testing.T) {
	tasks := task.NewTasks()
	err := tasks.RegisterTask(add)
	require.NoError(t, err)

	names := tasks.GetTaskNames()
	require.Len(t, names, 1)
	require.Equal(t, names[0], "add")
}

func TestTaskExecuteTask(t *testing.T) {
	t.Run("should execute task", func(t *testing.T) {
		tasks := task.NewTasks()
		err := tasks.RegisterTask(add)
		require.NoError(t, err)

		result, err := tasks.ExecuteTaskByName("add", &fakeTaskContext{}, 1, 2)
		require.NoError(t, err)

		resultInt := result.([]interface{})[0].(int)

		require.Equal(t, resultInt, 3)
	})

	t.Run("should return error if task not found", func(t *testing.T) {
		tasks := task.NewTasks()
		_, err := tasks.ExecuteTaskByName("testTask", nil)
		require.Error(t, err)
	})
}
