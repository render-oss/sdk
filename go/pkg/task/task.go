package task

import (
	"fmt"
	"reflect"
	"runtime"
	"strings"
)

type Tasks struct {
	Tasks map[string]Task
}

type Task interface{}

// GetFunctionName returns the short name of the given Task (function).
func GetFunctionName(t Task) (string, error) {
	v := reflect.ValueOf(t)
	if v.Kind() != reflect.Func {
		return "", fmt.Errorf("input is not a function")
	}

	// Get the function pointer
	fn := runtime.FuncForPC(v.Pointer())
	if fn == nil {
		return "", fmt.Errorf("unable to get function information")
	}

	// Get the full name and extract the short name
	fullName := fn.Name() // e.g., "github.com/foo/bar.MyFunction"
	parts := strings.Split(fullName, ".")
	shortName := parts[len(parts)-1] // e.g., "MyFunction"

	// Remove any closure suffix if present, like "-fm" or ".func1"
	shortName = strings.SplitN(shortName, "-", 2)[0]
	shortName = strings.SplitN(shortName, ".", 2)[0]

	return shortName, nil
}

func NewTasks() *Tasks {
	return &Tasks{
		Tasks: make(map[string]Task),
	}
}

func (t *Tasks) RegisterTask(task Task) error {
	name, err := GetFunctionName(task)
	if err != nil {
		return err
	}
	t.Tasks[name] = task
	return nil
}

func (t *Tasks) GetTaskByName(name string) (Task, error) {
	task, ok := t.Tasks[name]
	if !ok {
		return nil, fmt.Errorf("task %s not found", name)
	}
	return task, nil
}

func (t *Tasks) GetTaskNames() []string {
	names := make([]string, 0, len(t.Tasks))
	for name := range t.Tasks {
		names = append(names, name)
	}
	return names
}
