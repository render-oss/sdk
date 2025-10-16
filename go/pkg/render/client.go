package render

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
)

const (
	LocalDevURL = "RENDER_LOCAL_DEV_URL"
	UseLocalDev = "RENDER_USE_LOCAL_DEV"
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

func WithToken(token string) ClientOption {
	return func(c *Client) error {
		c.token = token
		return nil
	}
}

// NewClient creates a new Render API client
func NewClient(options ...ClientOption) (*Client, error) {
	// Create a temporary client to apply options
	tempClient := &Client{}

	// Apply all options to determine configuration
	for _, option := range options {
		if err := option(tempClient); err != nil {
			return nil, fmt.Errorf("failed to apply option: %w", err)
		}
	}

	if tempClient.token == "" {
		tempClient.token = os.Getenv("RENDER_API_KEY")
		if tempClient.token == "" {
			return nil, fmt.Errorf("RENDER_API_KEY environment variable is not set and no token was provided")
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

	useLocalDev := os.Getenv(UseLocalDev)
	if value, _ := strconv.ParseBool(useLocalDev); value {
		baseURL = "http://localhost:8120"
	}

	localDevURL := os.Getenv(LocalDevURL)
	if localDevURL != "" {
		baseURL = localDevURL
	}

	// Create the internal generated client with auth
	internalClient, err := client.NewClientWithResponses(
		fmt.Sprintf("%s/v1", strings.TrimSuffix(baseURL, "/")),
		client.WithRequestEditorFn(func(ctx context.Context, req *http.Request) error {
			req.Header.Set("Authorization", "Bearer "+tempClient.token)
			return nil
		}),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create internal client: %w", err)
	}

	// Create the final client with all configuration
	renderClient := &Client{
		internal: internalClient,
		token:    tempClient.token,
		baseURL:  baseURL,
	}

	renderClient.Workflows = &WorkflowsService{client: renderClient}

	return renderClient, nil
}

func NewSocketClient(unixSocketPath string) (*Client, error) {
	// Create HTTP client with Unix domain socket transport
	httpClient := &http.Client{
		Transport: &http.Transport{
			DialContext: func(_ context.Context, _, _ string) (net.Conn, error) {
				return net.Dial("unix", unixSocketPath)
			},
		},
	}

	c, err := client.NewClientWithResponses(
		"http://unix",
		client.WithHTTPClient(httpClient),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create client: %w", err)
	}

	// Create the final client with all configuration
	renderClient := &Client{
		internal: c,
	}

	renderClient.Workflows = &WorkflowsService{client: renderClient}
	return renderClient, nil
}
