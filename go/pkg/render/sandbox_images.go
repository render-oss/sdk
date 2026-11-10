package render

import (
	"context"
	"errors"
	"fmt"
	"regexp"
	"time"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	sandboxes "github.com/render-oss/sdk/go/pkg/render/internal/client/sandboxes"
)

// Errors returned by ImageClient and by SandboxClient.Create with an Image.
// Match them with errors.Is.
var (
	// ErrImageNotFound means the sandbox group has no image with the ID or name.
	ErrImageNotFound = errors.New("image not found")
	// ErrImageNotReady means a sandbox create named an image that has not
	// succeeded, whether still importing or failed.
	ErrImageNotReady = errors.New("image not ready")
	// ErrImageFailed means the import of an image failed while
	// WaitUntilReady waited for it.
	ErrImageFailed = errors.New("image import failed")
)

// The API still calls images builds, in its paths and error codes.
const (
	imageNotFoundCode     = "build_not_found"
	imageNotSucceededCode = "build_not_succeeded"
)

// imageIDPattern is the format of an image ID. CreateSandboxParams.Image
// treats any other value as a name.
var imageIDPattern = regexp.MustCompile(`^sbb-[0-9a-v]{20}$`)

// The first delay between WaitUntilReady checks, and the longest one once the
// backoff has grown.
const (
	imageWaitInterval    = 250 * time.Millisecond
	imageWaitMaxInterval = 2 * time.Second
)

// ImageSource is the OCI image an import converts, as the registry resolved it.
type ImageSource struct {
	// Repository is the registry host and namespace, like docker.io/library.
	Repository string
	// Image is the name within the repository, like python.
	Image string
	// Reference is the tag or digest the image was imported at, like 3.13.
	Reference string
}

// Image is an image that sandboxes can start from. Status is pending,
// running, succeeded, or failed.
type Image struct {
	ID             string
	SandboxGroupID string
	Name           string
	Source         ImageSource
	SourceDigest   string
	Status         string
	CreatedAt      time.Time
	FailureReason  *string
	FinishedAt     *time.Time
}

// RegistryCredentials pull an image from a private registry. The API uses them
// for that import only and does not store them.
type RegistryCredentials struct {
	Username string
	Password string
}

// ImportImageParams configures an image import.
type ImportImageParams struct {
	// Name identifies the image and is shared by all its versions, so a
	// sandbox created with Image set to the name starts from the newest one
	// that succeeded.
	Name string
	// Source is the image to import by tag or digest, like
	// ghcr.io/acme/agent-runtime:v1. It must be linux/amd64.
	Source string
	// RegistryCredentials nil pulls Source without credentials.
	RegistryCredentials *RegistryCredentials
}

// ListImagesOptions filters and pages ImageClient.List.
type ListImagesOptions struct {
	// Name returns only versions of the image with this name.
	Name string
	// Status filters by import status (pending, running, succeeded, failed).
	Status []string
	Cursor string
	// Limit is capped at 100 by the API.
	Limit int
}

// ImageList is one page of images. Pass NextCursor as
// ListImagesOptions.Cursor to fetch the next page; it is nil on an empty page.
type ImageList struct {
	Images     []Image
	NextCursor *string
}

// ImageClient manages the images sandboxes start from, via SandboxClient.Images.
type ImageClient struct {
	sandboxes *SandboxClient
}

// Import starts importing an OCI image so sandboxes can start from it. The
// image comes back before the import finishes; call WaitUntilReady to wait
// for it. Importing a name and digest the group already has, or is
// importing, returns that image instead of starting another.
func (s *ImageClient) Import(ctx context.Context, sandboxGroupID string, params ImportImageParams) (*Image, error) {
	body := sandboxes.SandboxBuildPOST{Name: params.Name, SourceImage: params.Source}
	if params.RegistryCredentials != nil {
		body.RegistryCredential = &struct {
			Password string `json:"password"`
			Username string `json:"username"`
		}{Password: params.RegistryCredentials.Password, Username: params.RegistryCredentials.Username}
	}
	resp, err := s.sandboxes.client.internal.CreateSandboxBuildWithResponse(ctx, sandboxGroupID, body)
	if err != nil {
		return nil, fmt.Errorf("failed to make import image request: %w", err)
	}
	if resp.StatusCode() != 201 {
		return nil, sandboxAPIError("import image", resp.StatusCode(), resp.Body)
	}
	if resp.JSON201 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toImage(*resp.JSON201), nil
}

// FromID fetches an image. Returns ErrImageNotFound if it does not exist or
// belongs to another sandbox group.
func (s *ImageClient) FromID(ctx context.Context, sandboxGroupID, imageID string) (*Image, error) {
	resp, err := s.sandboxes.client.internal.RetrieveSandboxBuildWithResponse(ctx, sandboxGroupID, imageID)
	if err != nil {
		return nil, fmt.Errorf("failed to make retrieve image request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, imageError("retrieve image", imageID, resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toImage(*resp.JSON200), nil
}

// List lists the images of one sandbox group, newest first. Each version of a
// name is its own image. opts may be nil.
func (s *ImageClient) List(ctx context.Context, sandboxGroupID string, opts *ListImagesOptions) (*ImageList, error) {
	params := &client.ListSandboxBuildsParams{}
	if opts != nil {
		params.Cursor, params.Limit = page(opts.Cursor, opts.Limit)
		if opts.Name != "" {
			params.Name = &opts.Name
		}
		if len(opts.Status) > 0 {
			statuses := make([]sandboxes.SandboxBuildStatus, len(opts.Status))
			for i, status := range opts.Status {
				statuses[i] = sandboxes.SandboxBuildStatus(status)
			}
			params.Status = &statuses
		}
	}

	resp, err := s.sandboxes.client.internal.ListSandboxBuildsWithResponse(ctx, sandboxGroupID, params)
	if err != nil {
		return nil, fmt.Errorf("failed to make list images request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, sandboxAPIError("list images", resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &ImageList{Images: make([]Image, len(items))}
	for i, item := range items {
		list.Images[i] = *toImage(item.Build)
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}

// WaitUntilReady polls the image until it has succeeded, so sandboxes can
// start from it, and returns it. The first check runs at once; the delay
// between checks starts at 250ms and doubles up to 2s.
//
// ctx bounds the wait: pass one with a deadline. When ctx ends, the error
// wraps ctx.Err() and names the last status seen. Returns an error wrapping
// ErrImageFailed, with the API's reason, as soon as the import fails. Errors
// from a status check, such as ErrImageNotFound, are returned unchanged.
func (s *ImageClient) WaitUntilReady(ctx context.Context, sandboxGroupID, imageID string) (*Image, error) {
	interval := imageWaitInterval
	lastStatus := "unknown"
	for {
		image, err := s.FromID(ctx, sandboxGroupID, imageID)
		if err != nil {
			if ctx.Err() != nil {
				return nil, fmt.Errorf("wait for image %s (last status %s): %w", imageID, lastStatus, ctx.Err())
			}
			return nil, err
		}
		switch image.Status {
		case "succeeded":
			return image, nil
		case "failed":
			reason := ""
			if image.FailureReason != nil {
				reason = ": " + *image.FailureReason
			}
			return nil, fmt.Errorf("%w: image %s%s", ErrImageFailed, imageID, reason)
		}
		lastStatus = image.Status

		timer := time.NewTimer(interval)
		select {
		case <-ctx.Done():
			timer.Stop()
			return nil, fmt.Errorf("wait for image %s (last status %s): %w", imageID, lastStatus, ctx.Err())
		case <-timer.C:
		}
		interval = min(interval*2, imageWaitMaxInterval)
	}
}

func toImage(m sandboxes.SandboxBuild) *Image {
	return &Image{
		ID:             m.Id,
		SandboxGroupID: m.SandboxGroupId,
		Name:           m.Name,
		Source: ImageSource{
			Repository: m.Source.Repository,
			Image:      m.Source.Image,
			Reference:  m.Source.Reference,
		},
		SourceDigest:  m.SourceDigest,
		Status:        string(m.Status),
		CreatedAt:     m.CreatedAt,
		FailureReason: m.FailureReason,
		FinishedAt:    m.FinishedAt,
	}
}

// imageError maps image failures to sentinel errors. Only a build_not_found
// code makes a 404 the image's, since the path also names the sandbox group.
func imageError(op, imageRef string, status int, body []byte) error {
	code, _ := errorBody(body)
	if status == 404 && code == imageNotFoundCode {
		return notFoundError(ErrImageNotFound, imageRef, status, body)
	}
	return sandboxAPIError(op, status, body)
}
