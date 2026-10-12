package render

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestObjectAPI(t *testing.T) {
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		switch r.Method + " " + r.URL.RequestURI() {
		case "PUT /v1/objects/tea-1/oregon/a.txt":
			body, _ := io.ReadAll(r.Body)
			require.JSONEq(t, `{"sizeBytes":5}`, string(body))
			_, _ = w.Write([]byte(`{"url":"https://up","expiresAt":"2026-01-01T00:00:00Z","maxSizeBytes":5}`))
		case "GET /v1/objects/tea-1/oregon/a.txt":
			_, _ = w.Write([]byte(`{"url":"https://down","expiresAt":"2026-01-01T00:00:00Z"}`))
		case "DELETE /v1/objects/tea-1/oregon/a.txt":
			w.WriteHeader(http.StatusNoContent)
		case "GET /v1/objects/tea-1/oregon?cursor=c0&limit=1":
			_, _ = w.Write([]byte(`{"hasNext":true,"nextCursor":"c1","items":[{"cursor":"c1","object":{"key":"a.txt","sizeBytes":5,"lastModified":"2026-01-01T00:00:00Z"}}]}`))
		default:
			w.WriteHeader(http.StatusNotFound)
			_, _ = w.Write([]byte(`{"message":"not found"}`))
		}
	}))
	defer srv.Close()

	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"))
	require.NoError(t, err)
	objects := c.Experimental.Objects
	ctx := context.Background()

	up, err := objects.GetUploadURL(ctx, "tea-1", RegionOregon, "a.txt", 5)
	require.NoError(t, err)
	require.Equal(t, "https://up", up.URL)
	require.EqualValues(t, 5, up.MaxSizeBytes)

	down, err := objects.GetDownloadURL(ctx, "tea-1", RegionOregon, "a.txt")
	require.NoError(t, err)
	require.Equal(t, "https://down", down.URL)

	require.NoError(t, objects.Delete(ctx, "tea-1", RegionOregon, "a.txt"))

	cursor, limit := "c0", 1
	list, err := objects.ListObjects(ctx, "tea-1", RegionOregon, &ListObjectsParams{Cursor: &cursor, Limit: &limit})
	require.NoError(t, err)
	require.True(t, list.HasNext)
	require.Equal(t, "c1", *list.NextCursor)
	require.Equal(t, []ObjectMetadata{{Key: "a.txt", Size: 5, LastModified: list.Objects[0].LastModified}}, list.Objects)

	_, err = objects.GetDownloadURL(ctx, "tea-1", RegionOregon, "missing.txt")
	require.ErrorContains(t, err, "status 404")
}
