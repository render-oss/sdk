package render

import (
	"context"
	"fmt"
	"time"

	workflows "github.com/render-oss/sdk/go/pkg/render/internal/client/workflows"
)

const (
	fallbackPollInterval = 5 * time.Second
)

// TaskRunWithGet extends the base TaskRun with get functionality
type TaskRunWithGet struct {
	*TaskRun
	client  *WorkflowsService
	details *TaskRunDetails
}

// Get blocks until the task run completes or the context is cancelled
func (tr *TaskRunWithGet) Get(ctx context.Context) (*TaskRunDetails, error) {
	// Create a new context with cancellation
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// If already completed, return immediately
	if tr.isTerminalStatus() {
		return tr.client.GetTaskRun(tr.Id)
	}

	// Get the client from the workflows service
	client := tr.client.client

	// Start SSE stream for this task run
	eventsChan, errorsChan := client.streamTaskRunEvents(ctx, []string{tr.Id})

	// Also set up a fallback polling mechanism in case SSE fails
	pollTicker := time.NewTicker(fallbackPollInterval)
	defer pollTicker.Stop()

	for {
		select {
		case <-ctx.Done():
			return nil, ctx.Err()

		case err := <-errorsChan:
			if err != nil {
				// SSE failed, fall back to polling
				fmt.Printf("SSE connection failed, falling back to polling: %v\n", err)
			}

		case event := <-eventsChan:
			// Process SSE event
			if event.Id == tr.Id {
				tr.details = &event
				return tr.details, nil
			}

		case <-pollTicker.C:
			// Fallback poll for updates
			details, err := tr.client.GetTaskRun(tr.Id)
			if err != nil {
				return nil, fmt.Errorf("failed to get task run status: %w", err)
			}

			// Update our status
			tr.Status = details.Status
			if details.CompletedAt != nil {
				tr.CompletedAt = details.CompletedAt
			}

			// Check if we're done
			if tr.isTerminalStatus() {
				return details, nil
			}
		}
	}
}

// isTerminalStatus returns true if the status indicates the task is finished
func (tr *TaskRunWithGet) isTerminalStatus() bool {
	return tr.Status == workflows.Completed || tr.Status == workflows.Failed
}
