package render

import (
	"bytes"
	"encoding/json"
	"fmt"
)

// APIError is a failed API response. Match it with errors.As to read the
// HTTP status and the error code the API sent, if any. An APIError for a code
// the SDK knows also matches that code's sentinel error with errors.Is, like
// ErrSandboxGroupSuspended.
type APIError struct {
	StatusCode int
	Code       string
	Message    string

	sentinel error
	text     string
}

func (e *APIError) Error() string { return e.text }

func (e *APIError) Unwrap() error { return e.sentinel }

// withSentinel makes e match sentinel with errors.Is and leads its message with it.
func (e *APIError) withSentinel(sentinel error, subject string) *APIError {
	e.sentinel = sentinel
	e.text = fmt.Sprintf("%v: %s", sentinel, subject)
	return e
}

// errorBody pulls code and message out of an API error body, if it has them.
func errorBody(body []byte) (code, message string) {
	var e struct{ Code, Message string }
	_ = json.Unmarshal(body, &e)
	return e.Code, e.Message
}

func apiError(op string, status int, body []byte) *APIError {
	code, message := errorBody(body)
	text := fmt.Sprintf("%s failed with status %d", op, status)
	if trimmed := bytes.TrimSpace(body); len(trimmed) > 0 {
		text += ": " + string(trimmed)
	}
	return &APIError{StatusCode: status, Code: code, Message: message, text: text}
}

// notFoundError is an APIError for a 404 whose message names what is missing.
func notFoundError(sentinel error, subject string, status int, body []byte) *APIError {
	return apiError("", status, body).withSentinel(sentinel, subject)
}
