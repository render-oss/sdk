package task

import (
	"fmt"
	"reflect"
	"runtime"
	"strings"
	"time"
)

// Retry contains retry configuration for a task
type Retry struct {
	MaxRetries   int           `json:"max_retries"`
	WaitDuration time.Duration `json:"wait_duration"`
	Factor       float32       `json:"factor"`
}

// Options contains configuration options for a task
type Options struct {
	Retry *Retry `json:"retry,omitempty"`
}

// TaskInfo contains a task function and its options
type TaskInfo struct {
	Task    Task     `json:"-"`
	Options *Options `json:"options,omitempty"`
}

type Tasks struct {
	Tasks map[string]*TaskInfo
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
	numExpectedArgs := tType.NumIn()
	numArgs := len(args)

	if numArgs != numExpectedArgs {
		return nil, fmt.Errorf("task %s expected %d argument(s), got %d",
			// First argument is always TaskContext, so we subtract 1
			// to get the count of user-defined args.
			tType.Name(), numExpectedArgs-1, numArgs-1)
	}

	// We receive arguments in the form of []interface{}, but we want to pass
	// each argument as a separate argument to the function.
	if numArgs > 0 {
		if slice, ok := args[0].([]interface{}); ok && (1+len(slice) == tType.NumIn()) {
			args = append([]interface{}{args[0]}, slice...)
		}
	}

	// Prepare arguments for reflection
	in := make([]reflect.Value, numArgs)
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

	// Check if the last return value is an error type
	if len(out) > 0 {
		lastValue := out[len(out)-1]
		if lastValue.Type().Implements(reflect.TypeOf((*error)(nil)).Elem()) {
			// The last return value implements the error interface
			if !lastValue.IsNil() {
				// Return the error and the results (excluding the error)
				errorResults := results[:len(results)-1]
				return errorResults, lastValue.Interface().(error)
			}
			// Error is nil, so exclude it from results
			results = results[:len(results)-1]
		}
	}

	return results, nil
}

type TaskResult struct {
	Result []interface{}
	Error  error
}

func isIntKind(kind reflect.Kind) bool {
	return kind == reflect.Int || kind == reflect.Int8 || kind == reflect.Int16 ||
		kind == reflect.Int32 || kind == reflect.Int64
}

func (t *TaskResult) Get(output ...interface{}) error {
	if t.Error != nil {
		return t.Error
	}

	if output == nil {
		return fmt.Errorf("output cannot be nil")
	}

	if len(output) != len(t.Result) {
		return fmt.Errorf("expected %d output arguments, got %d", len(t.Result), len(output))
	}

	for i, arg := range output {
		if arg == nil {
			return fmt.Errorf("output argument %d is nil", i)
		}

		argVal := reflect.ValueOf(arg)
		if argVal.Kind() != reflect.Ptr || argVal.IsNil() {
			return fmt.Errorf("output argument %d must be a non-nil pointer", i)
		}

		targetElem := argVal.Elem()
		expectedType := targetElem.Type()
		resultVal := reflect.ValueOf(t.Result[i])

		// Handle float64 -> int coercion
		if resultVal.Kind() == reflect.Float64 && isIntKind(expectedType.Kind()) {
			floatVal := resultVal.Float()
			if floatVal == float64(int64(floatVal)) {
				intVal := reflect.ValueOf(int64(floatVal)).Convert(expectedType)
				targetElem.Set(intVal)
				continue
			}
			return fmt.Errorf("cannot assign non-integer float %v to int type %s at index %d", floatVal, expectedType, i)
		}

		if !resultVal.Type().AssignableTo(expectedType) {
			return fmt.Errorf("result value at index %d has type %s, expected %s", i, resultVal.Type(), expectedType)
		}

		targetElem.Set(resultVal)
	}

	return nil
}

type TaskContext interface {
	ExecuteTask(task Task, input ...interface{}) *TaskResult
}

func NewTasks() *Tasks {
	return &Tasks{
		Tasks: make(map[string]*TaskInfo),
	}
}

func (t *Tasks) RegisterTask(task Task) error {
	return t.RegisterTaskWithOptions(task, nil)
}

func (t *Tasks) RegisterTaskWithOptions(task Task, options *Options) error {
	err := VerifySignature(task)
	if err != nil {
		return err
	}
	name, err := GetFunctionName(task)
	if err != nil {
		return err
	}
	t.Tasks[name] = &TaskInfo{
		Task:    task,
		Options: options,
	}
	return nil
}

func (t *Tasks) GetTaskByName(name string) (Task, error) {
	taskInfo, ok := t.Tasks[name]
	if !ok {
		return nil, fmt.Errorf("task %s not found", name)
	}
	return taskInfo.Task, nil
}

func (t *Tasks) GetTaskInfoByName(name string) (*TaskInfo, error) {
	taskInfo, ok := t.Tasks[name]
	if !ok {
		return nil, fmt.Errorf("task %s not found", name)
	}
	return taskInfo, nil
}

func (t *Tasks) GetTaskNames() []string {
	names := make([]string, 0, len(t.Tasks))
	for name := range t.Tasks {
		names = append(names, name)
	}
	return names
}

func (t *Tasks) ExecuteTaskByName(name string, tctx TaskContext, input ...interface{}) ([]interface{}, error) {
	task, err := t.GetTaskByName(name)
	if err != nil {
		return nil, err
	}

	input = append([]interface{}{tctx}, input...)

	return CallTask(task, input...)
}
