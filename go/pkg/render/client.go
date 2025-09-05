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
	baseURL  string

	// Service clients
	Workflows *WorkflowsService
}

type ClientOption func(*Client) error

func WithBaseURL(baseURL string) ClientOption {
	return func(c *Client) error {
		c.baseURL = baseURL
		return nil
	}
}

// NewClient creates a new Render API client
func NewClient(token string, options ...ClientOption) (*Client, error) {
	// Create a temporary client to apply options
	tempClient := &Client{}

	// Apply all options to determine configuration
	for _, option := range options {
		if err := option(tempClient); err != nil {
			return nil, fmt.Errorf("failed to apply option: %w", err)
		}
	}

	// Determine base URL (use option value or default)
	baseURL := tempClient.baseURL
	if baseURL == "" {
		baseURL = "https://api.render.com"
	}

	// Ensure base URL has protocol
	if !strings.HasPrefix(baseURL, "http://") && !strings.HasPrefix(baseURL, "https://") {
		baseURL = "https://" + baseURL
	}

	// Create the internal generated client with auth
	internalClient, err := client.NewClientWithResponses(
		fmt.Sprintf("%s/v1", strings.TrimSuffix(baseURL, "/")),
		client.WithRequestEditorFn(func(ctx context.Context, req *http.Request) error {
			req.Header.Set("Authorization", "Bearer "+token)
			return nil
		}),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create internal client: %w", err)
	}

	// Create the final client with all configuration
	renderClient := &Client{
		internal: internalClient,
		token:    token,
		baseURL:  baseURL,
	}

	renderClient.Workflows = &WorkflowsService{client: renderClient}

	return renderClient, nil
}
