package uds

import (
	"context"
	"fmt"
	"net"
	"net/http"

	"github.com/hashicorp/go-retryablehttp"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/callbackapi"
)

func NewCallbackClient() (*callbackapi.ClientWithResponses, error) {
	// Create HTTP client with Unix domain socket transport
	httpClient := &http.Client{
		Transport: &http.Transport{
			DialContext: func(_ context.Context, _, _ string) (net.Conn, error) {
				return net.Dial("unix", "/render/render.sock")
			},
		},
	}

	retryingHTTPClient := retryablehttp.NewClient()
	retryingHTTPClient.HTTPClient = httpClient
	retryingHTTPClient.RetryMax = 10

	callbackClient, err := callbackapi.NewClientWithResponses(
		"http://unix",
		callbackapi.WithHTTPClient(retryingHTTPClient.StandardClient()),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create UDS callback API client: %w", err)
	}

	return callbackClient, nil
}
