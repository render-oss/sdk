package tasks

import (
	"os"
	"strconv"

	"render.com/pkg/internal/executor"
	"render.com/pkg/internal/server"
	"render.com/pkg/internal/task"
)

var taskSingleton = task.NewTasks()

func RegisterTask(task task.Task) error {
	return taskSingleton.RegisterTask(task)
}

func Start() {
	executor := executor.NewExecutor(taskSingleton)
	serverAdapter := server.NewServerAdapter(executor)
	handler := server.NewServerHandler(taskSingleton, serverAdapter)

	port, ok := os.LookupEnv("SIDECAR_PORT")
	if !ok {
		panic("SIDECAR_PORT must be set")
	}
	intPort, err := strconv.Atoi(port)
	if err != nil {
		panic(err)
	}

	srv, err := handler.Start(intPort)
	if err != nil {
		panic(err)
	}
	defer func() {
		_ = srv.Close()
	}()
}

type TaskContext = task.TaskContext
