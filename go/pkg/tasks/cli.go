package tasks

import (
	"context"
	"fmt"

	"github.com/kelseyhightower/envconfig"
)

type Config struct {
	Mode       string `split_words:"true" required:"true"`
	SocketPath string `split_words:"true" required:"true"`
}

func Start() {
	if err := StartE(); err != nil {
		panic(err)
	}
}

func StartE() error {
	ctx := context.Background()

	var cfg Config
	envconfig.MustProcess("RENDER_SDK", &cfg)

	switch cfg.Mode {
	case "run":
		return Run(ctx, cfg.SocketPath)
	case "register":
		return Register(ctx, cfg.SocketPath)
	default:
		return fmt.Errorf("unrecognized RENDER_SDK_MODE %q", cfg.Mode)
	}
}
