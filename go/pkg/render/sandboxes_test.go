package render

import (
	"archive/tar"
	"bytes"
	"compress/gzip"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"testing/iotest"
	"time"

	"github.com/stretchr/testify/require"
)

const sandboxJSON = `{"id":"sbx-1","status":"running","plan":"starter","networkPolicy":{"type":"allow-all","default":"allow-all"},"region":"oregon","timeoutSeconds":60,"createdAt":"2026-01-01T00:00:00Z"}`

// newSandboxTestClient serves the API under /v1 and the sandbox proxy under
// /proxy. Every token mint points at /proxy/<operation>.
func newSandboxTestClient(t *testing.T, proxy http.HandlerFunc) *SandboxClient {
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")
	mux := http.NewServeMux()
	var srv *httptest.Server
	mint := func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "tea-1", r.URL.Query().Get("ownerId"))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		method := map[string]string{"stream": "POST", "upload": "PUT", "download": "GET"}[r.PathValue("op")]
		_, _ = fmt.Fprintf(w, `{"executionId":"e","expiresAt":"2026-01-01T00:00:00Z","method":%q,"token":"tok","uri":"%s/proxy/%s"}`,
			method, srv.URL, r.PathValue("op"))
	}
	mux.HandleFunc("POST /v1/sandboxes/sbx-1/runs/{op}/token", mint)
	mux.HandleFunc("POST /v1/sandboxes/sbx-1/files/{op}/token", mint)
	mux.HandleFunc("POST /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"ownerId":"tea-1","plan":"pro"}`, string(body))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(sandboxJSON))
	})
	mux.HandleFunc("GET /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "running", r.URL.Query().Get("status"))
		w.Header().Set("Content-Type", "application/json")
		_, _ = fmt.Fprintf(w, `[{"cursor":"c1","sandbox":%s}]`, sandboxJSON)
	})
	mux.HandleFunc("GET /v1/sandboxes/missing", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusNotFound)
		_, _ = w.Write([]byte(`{"message":"not found"}`))
	})
	mux.HandleFunc("DELETE /v1/sandbox-groups/grp-1/snapshots/snap-1", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusConflict)
		_, _ = w.Write([]byte(`{"code":"snapshot_creating","message":"still creating"}`))
	})
	mux.HandleFunc("/proxy/", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "Bearer tok", r.Header.Get("Authorization"))
		proxy(w, r)
	})
	srv = httptest.NewServer(mux)
	t.Cleanup(srv.Close)

	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"), WithOwnerID("tea-1"), WithRegion("ohio"))
	require.NoError(t, err)
	return c.Experimental.Sandboxes
}

func TestSandboxAPI(t *testing.T) {
	sandboxes := newSandboxTestClient(t, nil)
	ctx := context.Background()

	sbx, err := sandboxes.Create(ctx, CreateSandboxParams{Plan: "pro"})
	require.NoError(t, err)
	require.Equal(t, &Sandbox{ID: "sbx-1", Status: "running", Plan: "starter", NetworkPolicy: NetworkPolicy{Type: "allow-all"},
		Region: "oregon", TimeoutSeconds: 60, CreatedAt: sbx.CreatedAt}, sbx)

	list, err := sandboxes.List(ctx, &ListSandboxesOptions{Status: []string{"running"}})
	require.NoError(t, err)
	require.Len(t, list.Sandboxes, 1)
	require.Equal(t, "c1", *list.NextCursor)

	_, err = sandboxes.FromID(ctx, "missing")
	require.ErrorIs(t, err, ErrSandboxNotFound)

	err = sandboxes.Snapshots.Delete(ctx, "grp-1", "snap-1")
	require.ErrorIs(t, err, ErrSnapshotNotReady)
	require.ErrorContains(t, err, "still creating")

	_, err = sandboxes.Create(ctx, CreateSandboxParams{SnapshotID: "a", SnapshotName: "b"})
	require.ErrorContains(t, err, "mutually exclusive")
}

func TestSandboxExec(t *testing.T) {
	stream := ": keep-alive\n\n" +
		"event: output\ndata: {\"stream\":\"stdout\",\ndata: \"data\":\"hi\\n\"}\n\n" +
		"event: exit\ndata: {\"exit_code\":3}\n\n"
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"command":"echo hi"}`, string(body))
		if r.URL.Path == "/proxy/stream" {
			_, _ = w.Write([]byte(stream))
		}
	})

	var events []SandboxExecEvent
	for event, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		require.NoError(t, err)
		events = append(events, event)
	}
	require.Equal(t, []SandboxExecEvent{SandboxExecOutput{Stream: "stdout", Data: "hi\n"}, SandboxExecExit{ExitCode: 3}}, events)

	stream = "event: error\ndata: {\"status\":500,\"message\":\"boom\"}\n\n"
	var streamErr *SandboxExecStreamError
	for _, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		require.ErrorAs(t, err, &streamErr)
	}
	require.Equal(t, &SandboxExecStreamError{Status: 500, Message: "boom"}, streamErr)

	stream = "event: output\ndata: {\"stream\":\"stdout\",\"data\":\"x\"}\n\n"
	var last error
	for _, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		last = err
	}
	require.ErrorIs(t, last, ErrSandboxExec)

	// An exit event cut off before its terminating blank line is not an exit.
	stream = "event: exit\ndata: {\"exit_code\":0}\n"
	events = nil
	for event, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		events = append(events, event)
		last = err
	}
	require.Equal(t, []SandboxExecEvent{nil}, events)
	require.ErrorContains(t, last, "without an exit event")
}

func TestSSEEventsReadError(t *testing.T) {
	reset := errors.New("connection reset")
	var readErr error
	var names []string
	for name := range sseEvents(io.MultiReader(strings.NewReader("event: output\ndata: {\"str"), iotest.ErrReader(reset)), &readErr) {
		names = append(names, name)
	}
	require.Empty(t, names, "half-received event yielded")
	require.ErrorIs(t, readErr, reset)
}

// cancelMidBody serves a partial body of the given type, then cancels the
// client's context and holds the connection open. The pause lets the client
// get past Do and block reading the body, so the cancel lands mid-body.
func cancelMidBody(contentType, body string, cancel context.CancelFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		_, _ = io.Copy(io.Discard, r.Body)
		w.Header().Set("Content-Type", contentType)
		_, _ = w.Write([]byte(body))
		w.(http.Flusher).Flush()
		time.Sleep(100 * time.Millisecond)
		cancel()
		<-r.Context().Done()
	}
}

func TestSandboxStreamsReportCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	sandboxes := newSandboxTestClient(t, cancelMidBody("text/event-stream", "event: output\ndata: {\"str", cancel))
	var last error
	for _, err := range sandboxes.Exec(ctx, "sbx-1", "echo hi") {
		last = err
	}
	require.ErrorIs(t, last, context.Canceled)
	require.NotErrorIs(t, last, ErrSandboxExec)

	ctx, cancel = context.WithCancel(context.Background())
	sandboxes = newSandboxTestClient(t, cancelMidBody(contentTypeTar, strings.Repeat("x", 100), cancel))
	_, err := sandboxes.CopyFrom(ctx, "sbx-1", "/tmp/dir", t.TempDir())
	require.ErrorIs(t, err, context.Canceled)
	require.NotErrorIs(t, err, ErrSandboxDownload)

	require.ErrorIs(t, ErrSandboxIdleTimeout, context.DeadlineExceeded)
}

// TestSandboxCopyRoundTrip uploads a directory and downloads the same archive
// back, so it covers both writeTarGzip and extractTar.
func TestSandboxCopyRoundTrip(t *testing.T) {
	var archive []byte
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "PUT":
			require.Equal(t, contentTypeTar, r.Header.Get("Content-Type"))
			require.Equal(t, "gzip", r.Header.Get("Content-Encoding"))
			gz, err := gzip.NewReader(r.Body)
			require.NoError(t, err)
			archive, err = io.ReadAll(gz)
			require.NoError(t, err)
			w.WriteHeader(http.StatusNoContent)
		case "GET":
			w.Header().Set("Content-Type", contentTypeTar)
			_, _ = w.Write(archive)
		}
	})
	ctx := context.Background()

	src := t.TempDir()
	require.NoError(t, os.MkdirAll(filepath.Join(src, "sub"), 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(src, "sub", "a.txt"), []byte("hello"), 0o644))
	require.NoError(t, os.Symlink("sub/a.txt", filepath.Join(src, "link")))
	require.NoError(t, sandboxes.CopyTo(ctx, "sbx-1", src, "dir/"))

	dest := filepath.Join(t.TempDir(), "out")
	written, err := sandboxes.CopyFrom(ctx, "sbx-1", "dir", dest)
	require.NoError(t, err)
	require.Equal(t, dest, written)
	data, err := os.ReadFile(filepath.Join(dest, "link"))
	require.NoError(t, err)
	require.Equal(t, "hello", string(data))
}

func TestSandboxCopyFromFile(t *testing.T) {
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Disposition", `attachment; filename="../../evil.txt"`)
		_, _ = w.Write([]byte("data"))
	})
	dir := t.TempDir()
	written, err := sandboxes.CopyFrom(context.Background(), "sbx-1", "/tmp/x.txt", dir)
	require.NoError(t, err)
	require.Equal(t, filepath.Join(dir, "evil.txt"), written)
	entries, err := os.ReadDir(dir)
	require.NoError(t, err)
	require.Len(t, entries, 1, "temp file left behind")
}

func TestExtractTarRefusesUnsafeArchives(t *testing.T) {
	build := func(complete bool, headers ...*tar.Header) io.Reader {
		var buf bytes.Buffer
		tw := tar.NewWriter(&buf)
		for _, h := range headers {
			require.NoError(t, tw.WriteHeader(h))
			_, _ = tw.Write(make([]byte, h.Size))
		}
		if complete {
			require.NoError(t, tw.Close())
		} else {
			require.NoError(t, tw.Flush())
		}
		return terminatedReader(&buf)
	}
	file := func(name string) *tar.Header {
		return &tar.Header{Name: name, Typeflag: tar.TypeReg, Mode: 0o644, Size: 1}
	}

	for name, archive := range map[string]io.Reader{
		"dot-dot":      build(true, file("../evil")),
		"absolute":     build(true, file("/etc/evil")),
		"through link": build(true, &tar.Header{Name: "l", Typeflag: tar.TypeSymlink, Linkname: "/tmp"}, file("l/evil")),
		"truncated":    build(false, file("a")),
		"hardlink out": build(true, &tar.Header{Name: "h", Typeflag: tar.TypeLink, Linkname: "../x"}),
		"replaces dir": build(true, &tar.Header{Name: "d/", Typeflag: tar.TypeDir, Mode: 0o755}, &tar.Header{Name: "d", Typeflag: tar.TypeSymlink, Linkname: "x"}),
	} {
		t.Run(name, func(t *testing.T) {
			require.Error(t, extractTar(t.TempDir(), archive))
		})
	}
	require.NoError(t, extractTar(t.TempDir(), build(true, file("ok"))))
}

func TestSandboxNetworkPolicyCreate(t *testing.T) {
	tests := []struct {
		name   string
		policy *NetworkPolicy
		wire   string
		want   NetworkPolicy
	}{
		{"nil uses default", nil, "", NetworkPolicy{Type: "allow-all"}},
		{"allow all", &NetworkPolicy{Type: "allow-all"}, `{"type":"allow-all"}`, NetworkPolicy{Type: "allow-all"}},
		{"deny all", &NetworkPolicy{Type: "deny-all"}, `{"type":"deny-all"}`, NetworkPolicy{Type: "deny-all"}},
		{"allow list", &NetworkPolicy{Type: "allow-list", Rules: []EgressRule{{Domain: "pypi.org"}, {Domain: "*.github.com", Protocol: "https"}}}, `{"type":"allow-list","rules":[{"domain":"pypi.org","protocol":"https"},{"domain":"*.github.com","protocol":"https"}]}`, NetworkPolicy{Type: "allow-list", Rules: []EgressRule{{Domain: "pypi.org", Protocol: "https"}, {Domain: "*.github.com", Protocol: "https"}}}},
		{"empty allow list reaches API validation", &NetworkPolicy{Type: "allow-list"}, `{"type":"allow-list","rules":[]}`, NetworkPolicy{}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Setenv(UseLocalDev, "")
			t.Setenv(LocalDevURL, "")
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				require.Equal(t, "/v1/sandboxes", r.URL.Path)
				require.Equal(t, http.MethodPost, r.Method)
				var body map[string]json.RawMessage
				require.NoError(t, json.NewDecoder(r.Body).Decode(&body))
				if tt.wire == "" {
					require.NotContains(t, body, "networkPolicy")
				} else {
					require.JSONEq(t, tt.wire, string(body["networkPolicy"]))
				}
				w.Header().Set("Content-Type", "application/json")
				if tt.policy != nil && tt.policy.Type == "allow-list" && len(tt.policy.Rules) == 0 {
					w.WriteHeader(http.StatusBadRequest)
					_, _ = w.Write([]byte(`{"message":"networkPolicy.rules must list at least one rule"}`))
					return
				}
				policy := tt.wire
				if policy == "" {
					policy = `{"type":"allow-all"}`
				}
				w.WriteHeader(http.StatusCreated)
				_, _ = w.Write([]byte(strings.Replace(sandboxJSON, `{"type":"allow-all","default":"allow-all"}`, policy, 1)))
			}))
			defer server.Close()
			client, err := NewClient(WithToken("test"), WithBaseURL(server.URL), WithOwnerID("tea-1"))
			require.NoError(t, err)
			sandbox, err := client.Experimental.Sandboxes.Create(context.Background(), CreateSandboxParams{NetworkPolicy: tt.policy})
			if tt.policy != nil && tt.policy.Type == "allow-list" && len(tt.policy.Rules) == 0 {
				require.ErrorContains(t, err, "networkPolicy.rules must list at least one rule")
				return
			}
			require.NoError(t, err)
			require.Equal(t, tt.want, sandbox.NetworkPolicy)
		})
	}
}

func TestSnapshotCreateKind(t *testing.T) {
	tests := []struct {
		name string
		kind string
		wire string
	}{
		{"empty omits kind", "", ""},
		{"filesystem", "filesystem", `"filesystem"`},
		{"runtime", "runtime", `"runtime"`},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Setenv(UseLocalDev, "")
			t.Setenv(LocalDevURL, "")
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				require.Equal(t, "/v1/sandboxes/sbx-1/snapshots", r.URL.Path)
				require.Equal(t, http.MethodPost, r.Method)
				var body map[string]json.RawMessage
				require.NoError(t, json.NewDecoder(r.Body).Decode(&body))
				if tt.wire == "" {
					require.NotContains(t, body, "kind")
				} else {
					require.JSONEq(t, tt.wire, string(body["kind"]))
				}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusAccepted)
				_, _ = w.Write([]byte(`{"id":"snp-1","sandboxGroupId":"sbg-1","sourceSandboxId":"sbx-1","kind":"runtime","status":"creating","plan":"starter","requestedAt":"2026-01-01T00:00:00Z","expiresAt":"2026-01-08T00:00:00Z"}`))
			}))
			defer server.Close()
			client, err := NewClient(WithToken("test"), WithBaseURL(server.URL), WithOwnerID("tea-1"))
			require.NoError(t, err)
			snapshot, err := client.Experimental.Sandboxes.Snapshots.Create(context.Background(), "sbx-1", CreateSnapshotParams{Kind: tt.kind})
			require.NoError(t, err)
			require.Equal(t, "snp-1", snapshot.ID)
		})
	}
}

func TestSandboxRejectsInvalidNetworkPolicy(t *testing.T) {
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		t.Error("invalid policy reached the API")
	}))
	defer server.Close()
	client, err := NewClient(WithToken("test"), WithBaseURL(server.URL), WithOwnerID("tea-1"))
	require.NoError(t, err)
	for _, policy := range []NetworkPolicy{
		{Type: "allow-all", Rules: []EgressRule{{Domain: "pypi.org"}}},
		{Type: "deny-all", Rules: []EgressRule{{Domain: "pypi.org"}}},
		{Type: "allow-list", Rules: []EgressRule{{Domain: "pypi.org", Protocol: "http"}}},
		{Type: "unknown"}, {},
	} {
		_, err := client.Experimental.Sandboxes.Create(context.Background(), CreateSandboxParams{NetworkPolicy: &policy})
		require.Error(t, err)
	}
}

func TestSandboxNetworkPolicyRead(t *testing.T) {
	// Responses may contain historical protocols or omit the default protocol.
	model, err := json.Marshal(map[string]any{
		"id": "sbx-1", "status": "running", "plan": "starter", "region": "oregon",
		"timeoutSeconds": 60, "createdAt": "2026-01-01T00:00:00Z",
		"networkPolicy": map[string]any{"type": "allow-list", "rules": []map[string]string{
			{"domain": "example.com"}, {"domain": "legacy.example.com", "protocol": "http"},
		}},
	})
	require.NoError(t, err)
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.URL.Path == "/v1/sandboxes" {
			_, _ = fmt.Fprintf(w, `[{"cursor":"c1","sandbox":%s}]`, model)
		} else {
			_, _ = w.Write(model)
		}
	}))
	defer server.Close()
	client, err := NewClient(WithToken("test"), WithBaseURL(server.URL), WithOwnerID("tea-1"))
	require.NoError(t, err)
	want := NetworkPolicy{Type: "allow-list", Rules: []EgressRule{
		{Domain: "example.com", Protocol: "https"}, {Domain: "legacy.example.com", Protocol: "http"},
	}}
	sandbox, err := client.Experimental.Sandboxes.FromID(context.Background(), "sbx-1")
	require.NoError(t, err)
	require.Equal(t, want, sandbox.NetworkPolicy)
	page, err := client.Experimental.Sandboxes.List(context.Background(), nil)
	require.NoError(t, err)
	require.Len(t, page.Sandboxes, 1)
	require.Equal(t, want, page.Sandboxes[0].NetworkPolicy)
}

func TestSandboxGroupSelectionAndManagement(t *testing.T) {
	groupJSON := `{"id":"sbg-1","ownerId":"tea-1","name":"agents","region":"oregon","isDefault":false,"concurrencyLimit":10,"createdAt":"2026-01-01T00:00:00Z","updatedAt":"2026-01-01T00:00:00Z"}`
	mux := http.NewServeMux()
	mux.HandleFunc("POST /v1/sandbox-groups", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"ownerId":"tea-1","name":"agents"}`, string(body))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(groupJSON))
	})
	mux.HandleFunc("GET /v1/sandbox-groups/sbg-1", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(groupJSON))
	})
	mux.HandleFunc("PATCH /v1/sandbox-groups/sbg-1", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"concurrencyLimit":200}`, string(body))
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(groupJSON))
	})
	mux.HandleFunc("GET /v1/sandbox-groups", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "g1", r.URL.Query().Get("cursor"))
		require.Equal(t, "2", r.URL.Query().Get("limit"))
		w.Header().Set("Content-Type", "application/json")
		_, _ = fmt.Fprintf(w, `[{"sandboxGroup":%s,"cursor":"g2"}]`, groupJSON)
	})
	mux.HandleFunc("POST /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"ownerId":"tea-1","sandboxGroupId":"sbg-1"}`, string(body))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(strings.Replace(sandboxJSON, `"id":`, `"sandboxGroupId":"sbg-1","id":`, 1)))
	})
	mux.HandleFunc("GET /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "sbg-1", r.URL.Query().Get("sandboxGroupId"))
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`[]`))
	})
	srv := httptest.NewServer(mux)
	defer srv.Close()
	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"), WithOwnerID("tea-1"))
	require.NoError(t, err)
	s := c.Experimental.Sandboxes
	ctx := context.Background()
	g, err := s.CreateGroup(ctx, CreateSandboxGroupParams{Name: "agents"})
	require.NoError(t, err)
	require.Equal(t, "sbg-1", g.ID)
	_, err = s.GetGroup(ctx, g.ID)
	require.NoError(t, err)
	g, err = s.UpdateGroup(ctx, g.ID, 200)
	require.NoError(t, err)
	require.Equal(t, 10, g.ConcurrencyLimit)
	page, err := s.ListGroupsPage(ctx, &ListSandboxGroupsOptions{Cursor: "g1", Limit: 2})
	require.NoError(t, err)
	require.Equal(t, "g2", *page.NextCursor)
	sb, err := s.Create(ctx, CreateSandboxParams{SandboxGroupID: g.ID})
	require.NoError(t, err)
	require.Equal(t, g.ID, sb.SandboxGroupID)
	_, err = s.List(ctx, &ListSandboxesOptions{SandboxGroupID: g.ID})
	require.NoError(t, err)
}
