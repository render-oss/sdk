package render

import (
	"github.com/render-oss/sdk/go/pkg/internal/version"
)

// Version returns the current version of the Render Go SDK.
// It attempts to read the version from Go module info, falling back to a hardcoded version.
func Version() string {
	return version.Version()
}

// UserAgent returns the User-Agent string for the SDK.
func UserAgent() string {
	return version.UserAgent()
}
