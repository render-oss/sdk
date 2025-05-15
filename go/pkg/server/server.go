package server

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"render.com/pkg/executor"
	"render.com/pkg/executor/orchestratoradapter"
)

type ServerHandler struct {
	executors          *executor.Executors
	serverOrchestrator *orchestratoradapter.ServerAdapterFactory
}

func NewServerHandler(executors *executor.Executors, serverOrchestrator *orchestratoradapter.ServerAdapterFactory) *ServerHandler {
	return &ServerHandler{
		executors:          executors,
		serverOrchestrator: serverOrchestrator,
	}
}

func (h *ServerHandler) PostContinue(ctx context.Context, request PostContinueRequestObject) (PostContinueResponseObject, error) {
	log.Printf("Subtask complete: %s, input: %v", request.Body.TaskId, request.Body.Input)
	h.serverOrchestrator.SubtaskComplete(request.Body.TaskId, request.Body.Input.([]interface{}), request.Body.ResponseUrl)

	return PostContinue200Response{}, nil
}

func (h *ServerHandler) PostStart(ctx context.Context, request PostStartRequestObject) (PostStartResponseObject, error) {
	orchestratorAdapter := h.serverOrchestrator.NewOrchestratorAdapter(request.Body.ResponseUrl, request.Body.TaskId)
	executor, err := h.executors.NewExecutor(request.Body.TaskId, orchestratorAdapter)
	if err != nil {
		return PostStart400Response{}, err
	}

	err = executor.Execute(ctx, request.Body.Name, request.Body.TaskId, request.Body.Input)
	if err != nil {
		return PostStart400Response{}, err
	}

	return PostStart202Response{}, nil
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
