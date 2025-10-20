package main

import (
	"log"

	"github.com/render-oss/sdk/go/pkg/tasks"
)

func square(ctx tasks.TaskContext, a int) int {
	return a * a
}

func addSquares(ctx tasks.TaskContext, a int, b int) int {
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
	tasks.MustRegister(square)
	tasks.MustRegister(addSquares)

	err := tasks.Start()
	if err != nil {
		panic(err)
	}
}
