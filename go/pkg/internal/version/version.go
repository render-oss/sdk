package version

import (
	"fmt"
	"runtime"
	"runtime/debug"
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
var UserAgent = sync.OnceValue(func() string {
	return fmt.Sprintf("render-sdk-go/%s (%s; %s/%s)", Version(), runtime.Version(), runtime.GOOS, runtime.GOARCH)
})
