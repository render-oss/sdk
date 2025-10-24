package render

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
)

// SSEEvent represents a Server-Sent Event
type SSEEvent struct {
	ID    string `json:"id,omitempty"`
	Event string `json:"event,omitempty"`
	Data  string `json:"data,omitempty"`
	Retry string `json:"retry,omitempty"`
}

// streamTaskRunEvents connects to the SSE endpoint and streams events for specific task run IDs
func (c *Client) streamTaskRunEvents(ctx context.Context, taskRunIDs []string) (<-chan TaskRunDetails, <-chan error) {
	eventsChan := make(chan TaskRunDetails, 10)
	errorsChan := make(chan error, 1)

	go func() {
		defer close(eventsChan)
		defer close(errorsChan)

		// Create a new context with cancellation
		ctx, cancel := context.WithCancel(ctx)
		defer cancel()

		resp, err := c.internal.StreamTaskRunsEvents(ctx, &client.StreamTaskRunsEventsParams{
			TaskRunIds: taskRunIDs,
		})
		if err != nil {
			errorsChan <- fmt.Errorf("failed to stream task run events: %w", err)
			return
		}

		if resp.StatusCode != 200 {
			errorsChan <- fmt.Errorf("stream task run events failed with status %d: %s", resp.StatusCode, resp.Status)
			return
		}

		// Read the SSE stream
		scanner := bufio.NewScanner(resp.Body)
		var event SSEEvent

		// Close the response body when the context is done
		go func() {
			<-ctx.Done()
			_ = resp.Body.Close()
		}()

		for scanner.Scan() {
			line := scanner.Text()

			// Handle context cancellation
			select {
			case <-ctx.Done():
				return
			default:
			}

			// Parse SSE line
			if line == "" {
				// Empty line indicates end of event, process it
				if event.Data != "" {
					taskEvent, err := parseTaskRunDetails(event)
					if err != nil {
						errorsChan <- fmt.Errorf("failed to parse task run event: %w", err)
						return
					}
					if taskEvent != nil {
						eventsChan <- *taskEvent
					}
				}
				event = SSEEvent{} // Reset for next event
				continue
			}

			// Parse SSE fields
			if strings.HasPrefix(line, "id:") {
				event.ID = strings.TrimSpace(line[3:])
			} else if strings.HasPrefix(line, "event:") {
				event.Event = strings.TrimSpace(line[6:])
			} else if strings.HasPrefix(line, "data:") {
				event.Data = strings.TrimSpace(line[5:])
			} else if strings.HasPrefix(line, "retry:") {
				event.Retry = strings.TrimSpace(line[6:])
			}
		}

		if err := scanner.Err(); err != nil {
			errorsChan <- fmt.Errorf("error reading SSE stream: %w", err)
		}
	}()

	return eventsChan, errorsChan
}

// parseTaskRunEvent converts an SSE event to a TaskRunEvent
func parseTaskRunDetails(event SSEEvent) (*TaskRunDetails, error) {
	// Only process task-related events
	if !strings.HasPrefix(event.Event, "task.") {
		return nil, nil
	}

	var details TaskRunDetails
	if err := json.Unmarshal([]byte(event.Data), &details); err != nil {
		return nil, fmt.Errorf("failed to unmarshal task run event: %w", err)
	}

	return &details, nil
}
