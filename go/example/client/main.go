package main

import (
	"context"
	"fmt"
	"log"

	"github.com/render-oss/sdk/go/pkg/render"
)

func main() {
	// Example usage of the render client
	client, err := render.NewClient()
	if err != nil {
		log.Fatalf("Failed to create render client: %v", err)
	}

	// Example: Run a task
	taskIdentifier := render.TaskIdentifier("my-workflow-slug/square")
	var input render.TaskData
	_ = input.FromTaskData0([]interface{}{4})

	taskRun, err := client.Workflows.RunTask(taskIdentifier, input)
	if err != nil {
		log.Fatalf("Failed to run task: %v", err)
	}

	fmt.Printf("Task run created with ID: %s, Status: %s\n", taskRun.Id, taskRun.Status)

	result, err := taskRun.Get(context.Background())
	if err != nil {
		log.Fatalf("Failed to get task run details: %v", err)
	}

	fmt.Printf("Task run details: ID=%s, Status=%s, Results=%v\n",
		result.Id, result.Status, result.Results)
	// Example: Get task run details
	details, err := client.Workflows.GetTaskRun(taskRun.Id)
	if err != nil {
		log.Fatalf("Failed to get task run details: %v", err)
	}

	fmt.Printf("Task run details: ID=%s, Status=%s, Results=%v\n",
		details.Id, details.Status, details.Results)

	// Example: List task runs
	params := &render.ListTaskRunsParams{
		Limit: func() *int { i := 10; return &i }(),
	}

	taskRuns, err := client.Workflows.ListTaskRuns(params)
	if err != nil {
		log.Fatalf("Failed to list task runs: %v", err)
	}

	fmt.Printf("Found %d task runs\n", len(taskRuns))
}
