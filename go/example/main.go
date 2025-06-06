package main

import (
	"log"
	"os"
	"strconv"

	"render.com/pkg/executor"
	"render.com/pkg/server"
	"render.com/pkg/task"
)

func square(ctx task.TaskContext, a int) int {
	return a * a
}

func addSquares(ctx task.TaskContext, a int, b int) int {
	log.Printf("addSquares: %d, %d", a, b)
	var result1 int
	var result2 int

	log.Printf("Executing square: %d", a)
	err := ctx.ExecuteTask(square, a).Get(&result1)
	if err != nil {
		log.Printf("Error executing square: %d", a)
		panic(err)
	}
	log.Printf("Executing square: %d", b)
	err = ctx.ExecuteTask(square, b).Get(&result2)
	if err != nil {
		log.Printf("Error executing square: %d", b)
		panic(err)
	}
	return result1 + result2
}

func main() {
	tasks := task.NewTasks()
	err := tasks.RegisterTask(square)
	if err != nil {
		panic(err)
	}

	err = tasks.RegisterTask(addSquares)
	if err != nil {
		panic(err)
	}

	executor := executor.NewExecutor(tasks)
	serverAdapter := server.NewServerAdapter(executor)
	handler := server.NewServerHandler(tasks, serverAdapter)

	port := os.Getenv("SIDECAR_PORT")
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
