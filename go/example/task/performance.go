package main

import (
	"context"
	"os"
	"os/exec"
	"sync"
	"time"

	"github.com/render-oss/sdk/go/pkg/tasks"
)

func runCommand(ctx context.Context, cmdStr string, args ...string) {
	cmd := exec.CommandContext(ctx, cmdStr, args...) // #nosec G204
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	_ = cmd.Run()
}

func init() {
	tasks.MustRegister(burn_cpu_1m)
	tasks.MustRegister(sleep)
	tasks.MustRegister(measure_latency)
	tasks.MustRegister(testCancellationWithSubtasks)
}

func burn_cpu_1m(_ tasks.TaskContext) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()
	runCommand(ctx, "/app/timers/cpu_burner")
}

func sleep(_ tasks.TaskContext) {
	time.Sleep(time.Hour)
}

func measure_latency(_ tasks.TaskContext, startAt int) int {
	now := time.Now().UnixMilli()
	asInt := int64(startAt)
	out := now - asInt

	return int(out)
}

func testCancellationWithSubtasks(ctx tasks.TaskContext, num int) {
	var wg sync.WaitGroup
	for i := 0; i < num; i++ {
		wg.Add(1)

		go func(i, num int) {
			defer wg.Done()
			_ = ctx.ExecuteTask(sleep)
		}(i, num)
	}
	wg.Wait()
}
