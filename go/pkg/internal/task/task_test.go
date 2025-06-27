package task_test

import (
	"testing"
	"time"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
	"github.com/stretchr/testify/require"
)

func add(_ task.TaskContext, a int, b int) int {
	return a + b
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

		resultInt := result.([]interface{})[0].(int)

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
			Jitter:       0.5,
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
	require.Equal(t, float32(0.5), taskInfo.Options.Retry.Jitter)
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
