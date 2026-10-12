package render

import (
	"context"
	"fmt"
	"time"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
)

// ObjectAPI wraps the object storage REST API. It exposes the presigned URL
// flow directly: get a URL from Render, then upload to or download from it.
type ObjectAPI struct {
	client *Client
}

// UploadResponse holds a presigned upload URL.
type UploadResponse struct {
	URL          string
	ExpiresAt    time.Time
	MaxSizeBytes int64
}

// DownloadResponse holds a presigned download URL.
type DownloadResponse struct {
	URL       string
	ExpiresAt time.Time
}

// ObjectMetadata describes a stored object.
type ObjectMetadata struct {
	Key          string
	Size         int64
	LastModified time.Time
}

// ListObjectsResponse is one page of objects.
type ListObjectsResponse struct {
	Objects []ObjectMetadata
	HasNext bool
	// NextCursor is nil when there are no more results.
	NextCursor *string
}

// GetUploadURL gets a presigned URL for uploading an object.
// PUT /objects/{ownerId}/{region}/{key}
func (o *ObjectAPI) GetUploadURL(ctx context.Context, ownerID string, region Region, key string, sizeBytes int64) (*UploadResponse, error) {
	resp, err := o.client.internal.PutObjectWithResponse(ctx, ownerID, region, key, client.PutObjectJSONRequestBody{SizeBytes: sizeBytes})
	if err != nil {
		return nil, fmt.Errorf("failed to make get upload URL request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("get upload URL", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return &UploadResponse{
		URL:          resp.JSON200.Url,
		ExpiresAt:    resp.JSON200.ExpiresAt,
		MaxSizeBytes: resp.JSON200.MaxSizeBytes,
	}, nil
}

// GetDownloadURL gets a presigned URL for downloading an object.
// GET /objects/{ownerId}/{region}/{key}
func (o *ObjectAPI) GetDownloadURL(ctx context.Context, ownerID string, region Region, key string) (*DownloadResponse, error) {
	resp, err := o.client.internal.GetObjectWithResponse(ctx, ownerID, region, key)
	if err != nil {
		return nil, fmt.Errorf("failed to make get download URL request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("get download URL", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return &DownloadResponse{
		URL:       resp.JSON200.Url,
		ExpiresAt: resp.JSON200.ExpiresAt,
	}, nil
}

// Delete deletes an object.
// DELETE /objects/{ownerId}/{region}/{key}
func (o *ObjectAPI) Delete(ctx context.Context, ownerID string, region Region, key string) error {
	resp, err := o.client.internal.DeleteObjectWithResponse(ctx, ownerID, region, key)
	if err != nil {
		return fmt.Errorf("failed to make delete object request: %w", err)
	}

	if resp.StatusCode() != 204 {
		return apiError("delete object", resp.StatusCode(), resp.Body)
	}

	return nil
}

// ListObjects lists objects in storage. Pass params.Cursor from a previous
// response's NextCursor to get the next page.
// GET /objects/{ownerId}/{region}
func (o *ObjectAPI) ListObjects(ctx context.Context, ownerID string, region Region, params *ListObjectsParams) (*ListObjectsResponse, error) {
	resp, err := o.client.internal.ListObjectsWithResponse(ctx, ownerID, region, params)
	if err != nil {
		return nil, fmt.Errorf("failed to make list objects request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("list objects", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	objects := make([]ObjectMetadata, len(resp.JSON200.Items))
	for i, item := range resp.JSON200.Items {
		objects[i] = ObjectMetadata{
			Key:          item.Object.Key,
			Size:         item.Object.SizeBytes,
			LastModified: item.Object.LastModified,
		}
	}

	return &ListObjectsResponse{
		Objects:    objects,
		HasNext:    resp.JSON200.HasNext,
		NextCursor: resp.JSON200.NextCursor,
	}, nil
}
