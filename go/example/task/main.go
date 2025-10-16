package main

import (
	"log"
	"sync"

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

func testCancellationWithSubtasks(ctx tasks.TaskContext, num int) {
	var wg sync.WaitGroup
	for i := 0; i < num; i++ {
		wg.Add(1)

		go func(i, num int) {
			defer wg.Done()
			_ = ctx.ExecuteTask(sleep)
		}(i, num)
	}
	wg.Wait()
}

func main() {
	err := tasks.RegisterTask(square)
	if err != nil {
		panic(err)
	}
	err = tasks.RegisterTask(addSquares)
	if err != nil {
		panic(err)
	}

	tasks.MustRegister(burn_cpu_1m)
	tasks.MustRegister(sleep)
	tasks.MustRegister(measure_latency)
	tasks.MustRegister(testCancellationWithSubtasks)

	err = tasks.Start()
	if err != nil {
		panic(err)
	}
}
