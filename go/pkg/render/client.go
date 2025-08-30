package render

import (
	"context"
	"fmt"
	"net/http"
	"strings"

	"github.com/renderinc/workflow-sdk/go/pkg/render/internal/client"
)

// Client represents the Render API client
type Client struct {
	internal *client.ClientWithResponses
	token    string

	// Service clients
	Workflows *WorkflowsService
}

// NewClient creates a new Render API client
func NewClient(hostURL, token string) (*Client, error) {
	if !strings.HasPrefix(hostURL, "http://") && !strings.HasPrefix(hostURL, "https://") {
		hostURL = "https://" + hostURL
	}

	// Create the internal generated client with auth
	internalClient, err := client.NewClientWithResponses(
		strings.TrimSuffix(hostURL, "/"),
		client.WithRequestEditorFn(func(ctx context.Context, req *http.Request) error {
			req.Header.Set("Authorization", "Bearer "+token)
			return nil
		}),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create internal client: %w", err)
	}

	renderClient := &Client{
		internal: internalClient,
		token:    token,
	}

	renderClient.Workflows = &WorkflowsService{client: renderClient}

	return renderClient, nil
}
