package task_test

import (
	"errors"
	"testing"
	"time"

	"github.com/render-oss/sdk/go/pkg/internal/task"
	"github.com/stretchr/testify/require"
)

func add(_ task.TaskContext, a int, b int) int {
	return a + b
}

func addWithError(_ task.TaskContext, a int, b int) (int, error) {
	if a < 0 || b < 0 {
		return 0, errors.New("negative numbers not allowed")
	}
	return a + b, nil
}

func taskWithOnlyError(_ task.TaskContext, shouldFail bool) error {
	if shouldFail {
		return errors.New("task failed")
	}
	return nil
}

type fakeTaskContext struct {
}

func (f *fakeTaskContext) ExecuteTask(t task.Task, input ...interface{}) *task.TaskResult {
	return &task.TaskResult{
		Result: []interface{}{1},
	}
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

		resultInt := result[0].(int)

		require.Equal(t, resultInt, 3)
	})

	t.Run("should return error if task not found", func(t *testing.T) {
		tasks := task.NewTasks()
		_, err := tasks.ExecuteTaskByName("testTask", nil)
		require.Error(t, err)
	})
}

func TestRegisterTaskWithOptions(t *testing.T) {
	tasks := task.NewTasks()

	options := &task.Options{
		Retry: &task.Retry{
			MaxRetries:   3,
			WaitDuration: time.Second,
			Factor:       2.0,
		},
	}

	err := tasks.RegisterTaskWithOptions(add, options)
	require.NoError(t, err)

	// Verify task is registered
	names := tasks.GetTaskNames()
	require.Len(t, names, 1)
	require.Equal(t, names[0], "add")

	// Verify options are stored
	taskInfo, err := tasks.GetTaskInfoByName("add")
	require.NoError(t, err)
	require.NotNil(t, taskInfo.Options)
	require.NotNil(t, taskInfo.Options.Retry)
	require.Equal(t, 3, taskInfo.Options.Retry.MaxRetries)
	require.Equal(t, time.Second, taskInfo.Options.Retry.WaitDuration)
	require.Equal(t, float32(2.0), taskInfo.Options.Retry.Factor)
}

func TestRegisterTaskWithNilOptions(t *testing.T) {
	tasks := task.NewTasks()

	err := tasks.RegisterTaskWithOptions(add, nil)
	require.NoError(t, err)

	// Verify options are nil
	taskInfo, err := tasks.GetTaskInfoByName("add")
	require.NoError(t, err)
	require.Nil(t, taskInfo.Options)
}

func TestCallTaskWithError(t *testing.T) {
	t.Run("should return error when task function returns error", func(t *testing.T) {
		result, err := task.CallTask(addWithError, &fakeTaskContext{}, -1, 5)
		require.Error(t, err)
		require.Equal(t, "negative numbers not allowed", err.Error())
		require.Len(t, result, 1)
		require.Equal(t, 0, result[0])
	})

	t.Run("should return results without error when task succeeds", func(t *testing.T) {
		result, err := task.CallTask(addWithError, &fakeTaskContext{}, 3, 5)
		require.NoError(t, err)
		require.Len(t, result, 1)
		require.Equal(t, 8, result[0])
	})

	t.Run("should handle task that only returns error", func(t *testing.T) {
		result, err := task.CallTask(taskWithOnlyError, &fakeTaskContext{}, true)
		require.Error(t, err)
		require.Equal(t, "task failed", err.Error())
		require.Len(t, result, 0)
	})

	t.Run("should handle task that returns nil error", func(t *testing.T) {
		result, err := task.CallTask(taskWithOnlyError, &fakeTaskContext{}, false)
		require.NoError(t, err)
		require.Len(t, result, 0)
	})

	t.Run("should handle task without error return", func(t *testing.T) {
		result, err := task.CallTask(add, &fakeTaskContext{}, 3, 5)
		require.NoError(t, err)
		require.Len(t, result, 1)
		require.Equal(t, 8, result[0])
	})
}
