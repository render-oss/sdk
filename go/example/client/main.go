package main

import (
	"fmt"
	"log"

	"github.com/renderinc/workflow-sdk/go/pkg/render"
)

func main() {
	// Example usage of the render client
	client, err := render.NewClient("https://api.render.com", "your-api-token")
	if err != nil {
		log.Fatalf("Failed to create render client: %v", err)
	}

	// Example: Run a task
	taskIdentifier := render.TaskIdentifier("my-workflow/my-task")
	input := render.TaskData{"input1", "input2", 123}

	taskRun, err := client.Workflows.RunTask(taskIdentifier, input)
	if err != nil {
		log.Fatalf("Failed to run task: %v", err)
	}

	fmt.Printf("Task run created with ID: %s, Status: %s\n", taskRun.Id, taskRun.Status)

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
