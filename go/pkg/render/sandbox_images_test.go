package render

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

// imageID is an image ID in the API's format. CreateSandboxParams.Image sends
// only this format as an ID; anything else, including a shorter sbb- value, is
// a name.
const imageID = "sbb-cph1rs3idesc73a2b2mg"

const (
	runningImageJSON   = `{"id":"sbb-1","sandboxGroupId":"sbg-1","name":"python","source":{"repository":"docker.io/library","image":"python","reference":"3.13"},"sourceDigest":"sha256:c19d4a1","status":"running","createdAt":"2026-10-01T00:00:00Z"}`
	succeededImageJSON = `{"id":"sbb-1","sandboxGroupId":"sbg-1","name":"python","source":{"repository":"docker.io/library","image":"python","reference":"3.13"},"sourceDigest":"sha256:c19d4a1","status":"succeeded","createdAt":"2026-10-01T00:00:00Z","finishedAt":"2026-10-01T00:00:10Z"}`
	failedImageJSON    = `{"id":"sbb-1","sandboxGroupId":"sbg-1","name":"python","source":{"repository":"docker.io/library","image":"python","reference":"3.13"},"sourceDigest":"sha256:c19d4a1","status":"failed","failureReason":"image is not linux/amd64","createdAt":"2026-10-01T00:00:00Z","finishedAt":"2026-10-01T00:00:10Z"}`
)

// newImageTestClient serves handler as the whole API.
func newImageTestClient(t *testing.T, handler http.HandlerFunc) *SandboxClient {
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")
	srv := httptest.NewServer(handler)
	t.Cleanup(srv.Close)
	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"), WithOwnerID("tea-1"))
	require.NoError(t, err)
	return c.Experimental.Sandboxes
}

func writeJSON(w http.ResponseWriter, status int, body string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write([]byte(body))
}

func TestImageImport(t *testing.T) {
	tests := []struct {
		name   string
		params ImportImageParams
		wire   string
	}{
		{
			"without credentials",
			ImportImageParams{Name: "python", Source: "python:3.13"},
			`{"name":"python","sourceImage":"python:3.13"}`,
		},
		{
			"with credentials",
			ImportImageParams{Name: "internal", Source: "ghcr.io/acme/internal:1.0",
				RegistryCredentials: &RegistryCredentials{Username: "bot", Password: "s3cret"}},
			`{"name":"internal","sourceImage":"ghcr.io/acme/internal:1.0","registryCredential":{"username":"bot","password":"s3cret"}}`,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
				require.Equal(t, http.MethodPost, r.Method)
				require.Equal(t, "/v1/sandbox-groups/sbg-1/builds", r.URL.Path)
				require.Empty(t, r.URL.RawQuery)
				body, _ := io.ReadAll(r.Body)
				require.JSONEq(t, tt.wire, string(body))
				writeJSON(w, http.StatusCreated, runningImageJSON)
			})

			image, err := sandboxes.Images.Import(context.Background(), "sbg-1", tt.params)
			require.NoError(t, err)
			require.Equal(t, &Image{
				ID:             "sbb-1",
				SandboxGroupID: "sbg-1",
				Name:           "python",
				Source:         ImageSource{Repository: "docker.io/library", Image: "python", Reference: "3.13"},
				SourceDigest:   "sha256:c19d4a1",
				Status:         "running",
				CreatedAt:      time.Date(2026, 10, 1, 0, 0, 0, 0, time.UTC),
			}, image)
		})
	}
}

func TestImageImportAcceptsANameWithTheIDPrefix(t *testing.T) {
	sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"name":"sbb-runtime","sourceImage":"python:3.13"}`, string(body))
		writeJSON(w, http.StatusCreated, runningImageJSON)
	})

	_, err := sandboxes.Images.Import(context.Background(), "sbg-1", ImportImageParams{Name: "sbb-runtime", Source: "python:3.13"})
	require.NoError(t, err)
}

func TestImageImportReportsAPIErrors(t *testing.T) {
	sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusTooManyRequests, `{"message":"sandbox group has too many builds in progress (limit 5)"}`)
	})

	_, err := sandboxes.Images.Import(context.Background(), "sbg-1", ImportImageParams{Name: "python", Source: "python:3.13"})
	require.ErrorContains(t, err, "import image failed with status 429")
	require.ErrorContains(t, err, "limit 5")
}

func TestImageFromID(t *testing.T) {
	t.Run("returns the image", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			require.Equal(t, http.MethodGet, r.Method)
			require.Equal(t, "/v1/sandbox-groups/sbg-1/builds/sbb-1", r.URL.Path)
			writeJSON(w, http.StatusOK, failedImageJSON)
		})

		image, err := sandboxes.Images.FromID(context.Background(), "sbg-1", "sbb-1")
		require.NoError(t, err)
		require.Equal(t, "failed", image.Status)
		require.Equal(t, "image is not linux/amd64", *image.FailureReason)
		require.Equal(t, 10, image.FinishedAt.Second())
	})

	t.Run("maps build_not_found", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			writeJSON(w, http.StatusNotFound, `{"code":"build_not_found","message":"not found: build"}`)
		})

		_, err := sandboxes.Images.FromID(context.Background(), "sbg-1", "sbb-missing")
		require.ErrorIs(t, err, ErrImageNotFound)
		require.ErrorContains(t, err, "sbb-missing")
	})

	t.Run("keeps a 404 without the code generic", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			writeJSON(w, http.StatusNotFound, `{"message":"not found: sandbox group"}`)
		})

		_, err := sandboxes.Images.FromID(context.Background(), "sbg-missing", "sbb-1")
		require.Error(t, err)
		require.NotErrorIs(t, err, ErrImageNotFound)
	})
}

// imageStatusServer serves image status checks from a queue; the last one repeats.
func imageStatusServer(t *testing.T, bodies ...string) (*SandboxClient, *int) {
	calls := 0
	sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "/v1/sandbox-groups/sbg-1/builds/sbb-1", r.URL.Path)
		body := bodies[min(calls, len(bodies)-1)]
		calls++
		writeJSON(w, http.StatusOK, body)
	})
	return sandboxes, &calls
}

func TestImageWaitUntilReady(t *testing.T) {
	t.Run("polls until the image succeeds", func(t *testing.T) {
		sandboxes, calls := imageStatusServer(t, runningImageJSON, runningImageJSON, succeededImageJSON)

		image, err := sandboxes.Images.WaitUntilReady(context.Background(), "sbg-1", "sbb-1")
		require.NoError(t, err)
		require.Equal(t, "succeeded", image.Status)
		require.Equal(t, 3, *calls)
	})

	t.Run("returns at once when already succeeded", func(t *testing.T) {
		sandboxes, calls := imageStatusServer(t, succeededImageJSON)

		_, err := sandboxes.Images.WaitUntilReady(context.Background(), "sbg-1", "sbb-1")
		require.NoError(t, err)
		require.Equal(t, 1, *calls)
	})

	t.Run("fails with the reason when the import fails", func(t *testing.T) {
		sandboxes, _ := imageStatusServer(t, runningImageJSON, failedImageJSON)

		_, err := sandboxes.Images.WaitUntilReady(context.Background(), "sbg-1", "sbb-1")
		require.ErrorIs(t, err, ErrImageFailed)
		require.ErrorContains(t, err, "image sbb-1: image is not linux/amd64")
	})

	t.Run("stops when the context ends", func(t *testing.T) {
		sandboxes, _ := imageStatusServer(t, runningImageJSON)
		ctx, cancel := context.WithTimeout(context.Background(), 600*time.Millisecond)
		defer cancel()

		_, err := sandboxes.Images.WaitUntilReady(ctx, "sbg-1", "sbb-1")
		require.ErrorIs(t, err, context.DeadlineExceeded)
		require.ErrorContains(t, err, "last status running")
	})

	t.Run("returns status check errors unchanged", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			writeJSON(w, http.StatusNotFound, `{"code":"build_not_found","message":"not found: build"}`)
		})

		_, err := sandboxes.Images.WaitUntilReady(context.Background(), "sbg-1", "sbb-1")
		require.ErrorIs(t, err, ErrImageNotFound)
	})
}

func TestSandboxCreateWithImage(t *testing.T) {
	tests := []struct {
		name, image, field, other string
	}{
		{"id", imageID, "buildId", "buildName"},
		{"name", "agent-runtime", "buildName", "buildId"},
		{"name with the id prefix", "sbb-runtime", "buildName", "buildId"},
		{"short id-like name", "sbb-1", "buildName", "buildId"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
				var body map[string]json.RawMessage
				require.NoError(t, json.NewDecoder(r.Body).Decode(&body))
				require.JSONEq(t, `"`+tt.image+`"`, string(body[tt.field]))
				require.NotContains(t, body, tt.other)
				writeJSON(w, http.StatusCreated, sandboxJSON)
			})

			sbx, err := sandboxes.Create(context.Background(), CreateSandboxParams{Image: tt.image})
			require.NoError(t, err)
			require.Equal(t, "sbx-1", sbx.ID)
		})
	}

	t.Run("omits image fields by default", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			var body map[string]json.RawMessage
			require.NoError(t, json.NewDecoder(r.Body).Decode(&body))
			require.NotContains(t, body, "buildId")
			require.NotContains(t, body, "buildName")
			writeJSON(w, http.StatusCreated, sandboxJSON)
		})

		_, err := sandboxes.Create(context.Background(), CreateSandboxParams{})
		require.NoError(t, err)
	})

	t.Run("rejects an image with a snapshot", func(t *testing.T) {
		sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
			t.Fatal("no request expected")
		})

		for _, params := range []CreateSandboxParams{
			{Image: "python", SnapshotID: "snp-1"},
			{Image: "python", SnapshotName: "gold"},
		} {
			_, err := sandboxes.Create(context.Background(), params)
			require.ErrorContains(t, err, "mutually exclusive")
		}
	})
}

func TestSandboxCreateMapsImageErrors(t *testing.T) {
	tests := []struct {
		name   string
		image  string
		status int
		body   string
		want   error
	}{
		{"id not found", imageID, 404, `{"code":"build_not_found","message":"not found: build"}`, ErrImageNotFound},
		{"name not found", "missing", 404, `{"code":"build_not_found","message":"not found: build"}`, ErrImageNotFound},
		{"id not succeeded", imageID, 409, `{"code":"build_not_succeeded","message":"build has not succeeded"}`, ErrImageNotReady},
		{"name not succeeded", "python", 409, `{"code":"build_not_succeeded","message":"build has not succeeded"}`, ErrImageNotReady},
		{"other conflict", "python", 409, `{"code":"sandbox_group_suspended","message":"suspended"}`, nil},
		{"404 without code", imageID, 404, `{"message":"not found: sandbox group"}`, nil},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			sandboxes := newImageTestClient(t, func(w http.ResponseWriter, r *http.Request) {
				writeJSON(w, tt.status, tt.body)
			})

			_, err := sandboxes.Create(context.Background(), CreateSandboxParams{Image: tt.image})
			require.Error(t, err)
			if tt.want != nil {
				require.ErrorIs(t, err, tt.want)
				return
			}
			require.False(t, errors.Is(err, ErrImageNotFound) || errors.Is(err, ErrImageNotReady))
		})
	}
}
