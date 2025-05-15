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

func VerifySignature(t Task) error {
	// Step 1: Check that t is a function
	tType := reflect.TypeOf(t)
	if tType.Kind() != reflect.Func {
		return fmt.Errorf("task must be a function")
	}

	// Step 2: Check the function has at least one input
	if tType.NumIn() == 0 {
		return fmt.Errorf("task function must have at least one input parameter")
	}

	// Step 3: Check that the first argument implements TaskContext
	firstParam := tType.In(0)
	taskCtxType := reflect.TypeOf((*TaskContext)(nil)).Elem()

	if !firstParam.Implements(taskCtxType) {
		return fmt.Errorf("first argument must implement TaskContext interface")
	}

	return nil
}

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

// CallTask invokes the given Task (a function) with the provided arguments.
func CallTask(t Task, args ...interface{}) ([]interface{}, error) {
	v := reflect.ValueOf(t)
	if v.Kind() != reflect.Func {
		return nil, fmt.Errorf("task is not a function")
	}

	tType := v.Type()

	// We receive arguments in the form of []interface{}, but we want to pass
	// each argument as a separate argument to the function.
	if len(args) > 0 {
		if slice, ok := args[0].([]interface{}); ok && (1+len(slice) == tType.NumIn()) {
			args = append([]interface{}{args[0]}, slice...)
		}
	}

	if len(args) != tType.NumIn() {
		return nil, fmt.Errorf("expected %d arguments, got %d", tType.NumIn(), len(args))
	}

	// Prepare arguments for reflection
	in := make([]reflect.Value, len(args))
	for i, arg := range args {
		expectedType := tType.In(i)

		if arg == nil {
			// Accept nil only for interface or pointer types
			if expectedType.Kind() != reflect.Interface && expectedType.Kind() != reflect.Ptr {
				return nil, fmt.Errorf("argument %d is nil, but expected non-nil type %s", i, expectedType)
			}
			in[i] = reflect.Zero(expectedType)
			continue
		}

		argValue := reflect.ValueOf(arg)

		// Auto-cast float64 to int if the target type is int and float is an integer
		// JSON unmarshals all numbers as float64, so we need to check for this
		if expectedType.Kind() == reflect.Int && argValue.Kind() == reflect.Float64 {
			floatVal := argValue.Float()
			if floatVal == float64(int(floatVal)) {
				argValue = reflect.ValueOf(int(floatVal))
			}
		}

		if !argValue.Type().AssignableTo(expectedType) {
			return nil, fmt.Errorf("argument %d has type %s, expected %s", i, argValue.Type(), expectedType)
		}

		in[i] = argValue
	}

	// Call the function
	out := v.Call(in)

	// Convert results to []interface{}
	results := make([]interface{}, len(out))
	for i, val := range out {
		results[i] = val.Interface()
	}

	return results, nil
}

type TaskContext interface {
	ExecuteTask(task Task, input ...interface{}) *TaskResult
}

func NewTasks() *Tasks {
	return &Tasks{
		Tasks: make(map[string]Task),
	}
}

func (t *Tasks) RegisterTask(task Task) error {
	err := VerifySignature(task)
	if err != nil {
		return err
	}
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

func (t *Tasks) ExecuteTaskByName(name string, tctx TaskContext, input ...interface{}) (interface{}, error) {
	task, err := t.GetTaskByName(name)
	if err != nil {
		return nil, err
	}

	input = append([]interface{}{tctx}, input...)

	return CallTask(task, input...)
}
