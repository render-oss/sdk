package server

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"render.com/pkg/internal/task"
)

type ServerHandler struct {
	tasks              *task.Tasks
	serverOrchestrator *ServerAdapter
}

func NewServerHandler(tasks *task.Tasks, serverOrchestrator *ServerAdapter) *ServerHandler {
	return &ServerHandler{
		tasks:              tasks,
		serverOrchestrator: serverOrchestrator,
	}
}

func (h *ServerHandler) PostContinue(ctx context.Context, request PostContinueRequestObject) (PostContinueResponseObject, error) {
	log.Printf("Subtask complete: %s, input: %v", request.Body.TaskId, request.Body.Input)
	h.serverOrchestrator.SubtaskComplete(request.Body.Input.([]interface{}), request.Body.ResponseUrl)

	return PostContinue200Response{}, nil
}

func (h *ServerHandler) PostStart(ctx context.Context, request PostStartRequestObject) (PostStartResponseObject, error) {
	var input []interface{}
	if i, ok := request.Body.Input.([]interface{}); ok {
		input = i
	} else {
		input = []interface{}{request.Body.Input}
	}

	err := h.serverOrchestrator.StartTask(request.Body.ResponseUrl, request.Body.Name, request.Body.TaskId, input...)
	if err != nil {
		return PostStart400Response{}, err
	}

	return PostStart202Response{}, nil
}

func (h *ServerHandler) GetTasks(ctx context.Context, request GetTasksRequestObject) (GetTasksResponseObject, error) {
	taskSlice := make([]Task, 0, len(h.tasks.Tasks))
	for name := range h.tasks.Tasks {
		taskSlice = append(taskSlice, Task{Name: name})
	}

	return GetTasks200JSONResponse{
		Tasks: taskSlice,
	}, nil
}

func recoverMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if r := recover(); r != nil {
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				log.Printf("Recovered from panic: %v", r)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func logMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Request: %s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func (h *ServerHandler) Start(port int) (*http.Server, error) {
	handler := NewStrictHandler(h, nil)
	mux := chi.NewRouter()
	mux.Use(recoverMiddleware)
	mux.Use(logMiddleware)
	HandlerFromMux(handler, mux)
	server := &http.Server{
		Addr:    fmt.Sprintf(":%d", port),
		Handler: mux,
	}
	return server, server.ListenAndServe()
}
