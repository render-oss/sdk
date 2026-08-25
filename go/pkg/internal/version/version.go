package version

import (
	"fmt"
	"runtime"
	"runtime/debug"
	"strings"
	"sync"
)

// Version returns the current version of the Render Go SDK.
// It reads the version from Go module info when used as a dependency.
var Version = sync.OnceValue(func() string {
	if info, ok := debug.ReadBuildInfo(); ok {
		for _, dep := range info.Deps {
			if dep.Path == "github.com/render-oss/sdk/go" {
				return dep.Version
			}
		}
	}
	return "unknown"
})

// UserAgent returns the User-Agent string for the SDK.
//
// Returns a string like:
//
//	render-sdk-go/0.1.3 (go/1.21.4; darwin/arm64)
var UserAgent = sync.OnceValue(func() string {
	goVersion := strings.TrimPrefix(runtime.Version(), "go")
	return fmt.Sprintf("render-sdk-go/%s (go/%s; %s/%s)", Version(), goVersion, runtime.GOOS, runtime.GOARCH)
})
