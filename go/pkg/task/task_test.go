package task_test

import (
	"testing"

	"github.com/stretchr/testify/require"
	"render.com/pkg/task"
)

func add(_ task.TaskContext, a int, b int) int {
	return a + b
}

func TestTaskGetTaskNames(t *testing.T) {
	tasks := task.NewTasks()
	err := tasks.RegisterTask(add)
	require.NoError(t, err)

	names := tasks.GetTaskNames()
	require.Len(t, names, 1)
	require.Equal(t, names[0], "add")
}
