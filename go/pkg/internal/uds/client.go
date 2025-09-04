package uds

import (
	"context"
	"fmt"
	"net"
	"net/http"

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

	callbackClient, err := callbackapi.NewClientWithResponses(
		"http://unix",
		callbackapi.WithHTTPClient(httpClient),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create UDS callback API client: %w", err)
	}

	return callbackClient, nil
}
