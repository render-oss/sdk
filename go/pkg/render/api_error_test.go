package render

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"
)

func conflictRenderClient(t *testing.T, code string) *Client {
	t.Helper()
	return statusRenderClient(t, http.StatusConflict, code, "conflict")
}

func statusRenderClient(t *testing.T, status int, code, message string) *Client {
	t.Helper()
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(status)
		_, _ = fmt.Fprintf(w, "{\"code\":%q,\"message\":%q}\n", code, message)
	}))
	t.Cleanup(server.Close)
	c, err := NewClient(WithBaseURL(server.URL), WithToken("t"), WithOwnerID("tea-1"))
	require.NoError(t, err)
	return c
}

const unmappedConflictBody = `{"code":"something_else","message":"conflict"}`

type apiErrorOutcome struct {
	StatusCode      int
	Code            string
	Message         string
	MatchesSentinel bool
	Error           string
}

func outcomeOf(t *testing.T, err, sentinel error) apiErrorOutcome {
	t.Helper()
	var apiErr *APIError
	require.ErrorAs(t, err, &apiErr)
	return apiErrorOutcome{
		StatusCode:      apiErr.StatusCode,
		Code:            apiErr.Code,
		Message:         apiErr.Message,
		MatchesSentinel: errors.Is(err, sentinel),
		Error:           err.Error(),
	}
}

func TestAPIErrorCarriesStatusAndCode(t *testing.T) {
	ctx := context.Background()
	tests := []struct {
		name     string
		code     string
		sentinel error
		call     func(c *Client) error
		want     apiErrorOutcome
	}{
		{
			name:     "sandbox call with a mapped code",
			code:     "sandbox_group_suspended",
			sentinel: ErrSandboxGroupSuspended,
			call: func(c *Client) error {
				_, err := c.Experimental.Sandboxes.Create(ctx, CreateSandboxParams{})
				return err
			},
			want: apiErrorOutcome{
				StatusCode:      409,
				Code:            "sandbox_group_suspended",
				Message:         "conflict",
				MatchesSentinel: true,
				Error:           "sandbox group suspended: create sandbox failed: conflict",
			},
		},
		{
			name: "sandbox call with an unmapped code",
			code: "something_else",
			call: func(c *Client) error {
				return c.Experimental.Sandboxes.DeleteGroup(ctx, "sbg-1")
			},
			want: apiErrorOutcome{
				StatusCode: 409,
				Code:       "something_else",
				Message:    "conflict",
				Error:      "delete sandbox group failed with status 409: " + unmappedConflictBody,
			},
		},
		{
			name: "object storage call",
			code: "something_else",
			call: func(c *Client) error {
				return c.Experimental.Objects.Delete(ctx, "tea-1", Region("oregon"), "key")
			},
			want: apiErrorOutcome{
				StatusCode: 409,
				Code:       "something_else",
				Message:    "conflict",
				Error:      "delete object failed with status 409: " + unmappedConflictBody,
			},
		},
		{
			name: "workflows call",
			code: "something_else",
			call: func(c *Client) error {
				return c.Workflows.CancelTaskRun(ctx, "trn-1")
			},
			want: apiErrorOutcome{
				StatusCode: 409,
				Code:       "something_else",
				Message:    "conflict",
				Error:      "cancel task run failed with status 409: " + unmappedConflictBody,
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.call(conflictRenderClient(t, tt.code))

			require.Equal(t, tt.want, outcomeOf(t, err, tt.sentinel))
		})
	}
}

const fileNotFoundBody = `{"code":"file_not_found","message":"not found"}`

var sandboxNotFound = apiErrorOutcome{
	StatusCode:      404,
	Message:         "not found",
	MatchesSentinel: true,
	Error:           "sandbox not found: sbx-1",
}

func TestNotFoundErrorsAreAPIErrors(t *testing.T) {
	ctx := context.Background()
	tests := []struct {
		name     string
		code     string
		sentinel error
		call     func(s *SandboxClient) error
		want     apiErrorOutcome
	}{
		{
			name:     "sandbox FromID",
			sentinel: ErrSandboxNotFound,
			call: func(s *SandboxClient) error {
				_, err := s.FromID(ctx, "sbx-1")
				return err
			},
			want: sandboxNotFound,
		},
		{
			name:     "Terminate",
			sentinel: ErrSandboxNotFound,
			call:     func(s *SandboxClient) error { return s.Terminate(ctx, "sbx-1") },
			want:     sandboxNotFound,
		},
		{
			name:     "Snapshots.Create",
			sentinel: ErrSandboxNotFound,
			call: func(s *SandboxClient) error {
				_, err := s.Snapshots.Create(ctx, "sbx-1", CreateSnapshotParams{})
				return err
			},
			want: sandboxNotFound,
		},
		{
			name:     "Snapshots.FromID",
			code:     "snapshot_not_found",
			sentinel: ErrSnapshotNotFound,
			call: func(s *SandboxClient) error {
				_, err := s.Snapshots.FromID(ctx, "sbg-1", "snap-1")
				return err
			},
			want: apiErrorOutcome{
				StatusCode:      404,
				Code:            "snapshot_not_found",
				Message:         "not found",
				MatchesSentinel: true,
				Error:           "snapshot not found: snap-1",
			},
		},
		{
			name:     "Images.FromID",
			code:     "build_not_found",
			sentinel: ErrImageNotFound,
			call: func(s *SandboxClient) error {
				_, err := s.Images.FromID(ctx, "sbg-1", "sbb-1")
				return err
			},
			want: apiErrorOutcome{
				StatusCode:      404,
				Code:            "build_not_found",
				Message:         "not found",
				MatchesSentinel: true,
				Error:           "image not found: sbb-1",
			},
		},
		{
			name:     "CopyFrom a missing path",
			code:     "file_not_found",
			sentinel: ErrSandboxFileNotFound,
			call: func(s *SandboxClient) error {
				_, err := s.CopyFrom(ctx, "sbx-1", "/missing", t.TempDir()+"/out")
				return err
			},
			want: apiErrorOutcome{
				StatusCode:      404,
				Code:            "file_not_found",
				Message:         "not found",
				MatchesSentinel: true,
				Error:           "sandbox file not found: " + fileNotFoundBody,
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			c := statusRenderClient(t, http.StatusNotFound, tt.code, "not found")
			err := tt.call(c.Experimental.Sandboxes)

			require.Equal(t, tt.want, outcomeOf(t, err, tt.sentinel))
		})
	}
}
