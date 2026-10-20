package render

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"iter"
	"net/http"
	"strings"
	"time"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	sandboxes "github.com/render-oss/sdk/go/pkg/render/internal/client/sandboxes"
)

// Errors returned by SandboxClient and SnapshotClient. Match them with errors.Is.
var (
	// ErrSandboxNotFound means the sandbox does not exist or has been terminated.
	ErrSandboxNotFound = errors.New("sandbox not found")
	// ErrSandboxFileNotFound means the sandbox is alive but has no such path.
	ErrSandboxFileNotFound = errors.New("sandbox file not found")
	// ErrSnapshotNotFound means the snapshot does not exist, was deleted, has
	// expired, or belongs to another sandbox group.
	ErrSnapshotNotFound = errors.New("snapshot not found")
	// ErrSnapshotNotReady means the snapshot is still creating (on delete) or
	// is not available to start a sandbox from (on create).
	ErrSnapshotNotReady = errors.New("snapshot not ready")
	// ErrSnapshotPlanMismatch means a sandbox create named a runtime snapshot
	// captured on a different plan.
	ErrSnapshotPlanMismatch = errors.New("snapshot plan mismatch")
	// ErrSandboxDownload means a download could not be written to disk safely:
	// a truncated archive, an entry that escapes the destination, or a
	// response encoding the SDK cannot decode.
	ErrSandboxDownload = errors.New("sandbox download failed")
	// ErrSandboxExec means an exec stream ended abnormally: no terminal event,
	// an unknown event type, or unparseable event data.
	ErrSandboxExec = errors.New("sandbox exec failed")
	// ErrSandboxIdleTimeout means an exec or file transfer stream received no
	// bytes for 45 seconds. It also matches context.DeadlineExceeded.
	ErrSandboxIdleTimeout = fmt.Errorf("sandbox stream idle timeout: %w", context.DeadlineExceeded)
)

// SandboxExecStreamError is a terminal error event delivered by an exec stream.
type SandboxExecStreamError struct {
	Status  int
	Message string
}

func (e *SandboxExecStreamError) Error() string { return e.Message }

// Codes the API and sandbox agent send in error bodies.
const (
	fileNotFoundCode         = "file_not_found"
	snapshotNotFoundCode     = "snapshot_not_found"
	snapshotPlanMismatchCode = "snapshot_plan_mismatch"
	snapshotCreatingCode     = "snapshot_creating"
	snapshotNotAvailableCode = "snapshot_not_available"
)

// Read timeout at 3x the server's 15s SSE keep-alive interval, so a dead
// connection is detected without cutting off a live but idle stream.
const sandboxIdleTimeout = 45 * time.Second

// EgressRule is a destination admitted by an allow-list network policy.
// Domain matching is exact; a wildcard is only allowed as the leftmost label.
type EgressRule struct {
	Domain string
	// Protocol defaults to https.
	Protocol string
}

// NetworkPolicy controls outbound sandbox traffic. Type is allow-all, deny-all,
// or allow-list. Rules are accepted only for allow-list.
type NetworkPolicy struct {
	Type  string
	Rules []EgressRule
}

// Sandbox is a sandbox as returned by Create, FromID, and List.
type Sandbox struct {
	ID             string
	Status         string
	Plan           string
	NetworkPolicy  NetworkPolicy
	Region         string
	TimeoutSeconds int
	CreatedAt      time.Time
	TerminatedAt   *time.Time
}

// SandboxList is a page of sandboxes. NextCursor is nil when the page is empty.
type SandboxList struct {
	Sandboxes  []Sandbox
	NextCursor *string
}

// SandboxGroup is a sandbox group as returned by ListGroups.
type SandboxGroup struct {
	ID               string
	OwnerID          string
	Name             string
	Region           string
	IsDefault        bool
	ConcurrencyLimit int
	CreatedAt        time.Time
	UpdatedAt        time.Time
	EnvironmentID    *string
}

// SandboxGroupList is a page of sandbox groups.
type SandboxGroupList struct {
	Groups     []SandboxGroup
	NextCursor *string
}

// Snapshot is a snapshot of a sandbox.
type Snapshot struct {
	ID              string
	SandboxGroupID  string
	SourceSandboxID string
	Kind            string
	Status          string
	Plan            string
	RequestedAt     time.Time
	ExpiresAt       time.Time
	Name            *string
	CapturedAt      *time.Time
	SizeBytes       *int64
	Error           *string
}

// SnapshotList is a page of snapshots.
type SnapshotList struct {
	Snapshots  []Snapshot
	NextCursor *string
}

// SandboxExecEvent is a SandboxExecOutput or a SandboxExecExit.
type SandboxExecEvent interface{ isSandboxExecEvent() }

// SandboxExecOutput is a chunk of stdout or stderr from an exec stream.
type SandboxExecOutput struct {
	Stream string
	Data   string
}

// SandboxExecExit is the terminal exit event of an exec stream.
type SandboxExecExit struct {
	ExitCode int
}

func (SandboxExecOutput) isSandboxExecEvent() {}
func (SandboxExecExit) isSandboxExecEvent()   {}

// CreateSandboxParams configures a new sandbox. Zero fields fall back to the
// workspace defaults enforced by the API (plan starter, 7200s timeout,
// workspace default region and network policy).
type CreateSandboxParams struct {
	Plan           string
	TimeoutSeconds int
	// NetworkPolicy nil uses the API default.
	NetworkPolicy *NetworkPolicy
	// Region defaults to the client's region.
	Region string
	Env    map[string]string
	// SnapshotID starts the sandbox from that snapshot. SnapshotName starts it
	// from the available snapshot that name currently resolves to in the
	// sandbox group. They are mutually exclusive.
	SnapshotID   string
	SnapshotName string
}

// ListSandboxesOptions filters and pages ListSandboxes.
type ListSandboxesOptions struct {
	// Status filters by sandbox status (creating, running, suspended,
	// resuming, errored, terminated).
	Status []string
	Cursor string
	// Limit is capped at 100 by the API.
	Limit int
}

// CreateSnapshotParams configures a new snapshot.
type CreateSnapshotParams struct {
	// Kind is filesystem or runtime (the default; also memory and CPU state).
	Kind string
	// Name is case sensitive and can be reused within a sandbox group.
	Name string
	// ExpiresAt must be in the future. Nil means Render's default lifetime.
	ExpiresAt *time.Time
}

// ListSnapshotsOptions filters and pages ListSnapshots.
type ListSnapshotsOptions struct {
	// Status filters by snapshot status (creating, available, failed).
	Status []string
	Cursor string
	// Limit is capped at 100 by the API.
	Limit int
}

// SandboxClient creates and operates Render sandboxes.
//
// Calls are scoped to the client's owner ID (WithOwnerID, or the
// RENDER_WORKSPACE_ID environment variable).
type SandboxClient struct {
	client    *Client
	Snapshots *SnapshotClient
}

// SnapshotClient manages sandbox snapshots, via SandboxClient.Snapshots.
type SnapshotClient struct {
	sandboxes *SandboxClient
}

func (s *SandboxClient) ownerID() (string, error) {
	if id := s.optionalOwnerID(); id != nil {
		return *id, nil
	}
	return "", fmt.Errorf("owner ID is required: use WithOwnerID or set the RENDER_WORKSPACE_ID environment variable")
}

func (s *SandboxClient) optionalOwnerID() *string {
	id := s.client.defaultOwnerID()
	if id == "" {
		return nil
	}
	return &id
}

// Create creates a sandbox and returns its initial state.
//
// For a runtime snapshot, Plan must match the snapshot's plan. Returns
// ErrSnapshotNotFound if the snapshot does not resolve, ErrSnapshotNotReady if
// it is not available, and ErrSnapshotPlanMismatch on a runtime plan mismatch.
func (s *SandboxClient) Create(ctx context.Context, params CreateSandboxParams) (*Sandbox, error) {
	if params.SnapshotID != "" && params.SnapshotName != "" {
		return nil, fmt.Errorf("SnapshotID and SnapshotName are mutually exclusive")
	}
	ownerID, err := s.ownerID()
	if err != nil {
		return nil, err
	}

	body := sandboxes.SandboxPOST{OwnerId: ownerID}
	if params.Plan != "" {
		plan := sandboxes.SandboxPlan(params.Plan)
		body.Plan = &plan
	}
	if params.TimeoutSeconds != 0 {
		body.TimeoutSeconds = &params.TimeoutSeconds
	}
	if params.NetworkPolicy != nil {
		body.NetworkPolicy, err = toNetworkPolicyPost(*params.NetworkPolicy)
		if err != nil {
			return nil, err
		}
	}
	region := params.Region
	if region == "" {
		region = s.client.defaultRegion()
	}
	if region != "" {
		body.Region = &region
	}
	if params.Env != nil {
		body.Env = &params.Env
	}
	if params.SnapshotID != "" {
		body.SnapshotId = &params.SnapshotID
	}
	if params.SnapshotName != "" {
		body.SnapshotName = &params.SnapshotName
	}

	resp, err := s.client.internal.CreateSandboxWithResponse(ctx, body)
	if err != nil {
		return nil, fmt.Errorf("failed to make create sandbox request: %w", err)
	}
	if resp.StatusCode() != 201 {
		snapshotRef := params.SnapshotID
		if snapshotRef == "" {
			snapshotRef = params.SnapshotName
		}
		if snapshotRef == "" {
			return nil, apiError("create sandbox", resp.StatusCode(), resp.Body)
		}
		return nil, snapshotError("create sandbox", snapshotRef, resp.StatusCode(), resp.Body, false)
	}
	if resp.JSON201 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toSandbox(*resp.JSON201), nil
}

// FromID reconnects to an existing sandbox. Returns ErrSandboxNotFound if the
// sandbox does not exist or has been terminated.
func (s *SandboxClient) FromID(ctx context.Context, sandboxID string) (*Sandbox, error) {
	ownerID, err := s.ownerID()
	if err != nil {
		return nil, err
	}
	resp, err := s.client.internal.RetrieveSandboxWithResponse(ctx, sandboxID, &client.RetrieveSandboxParams{OwnerId: &ownerID})
	if err != nil {
		return nil, fmt.Errorf("failed to make retrieve sandbox request: %w", err)
	}
	if resp.StatusCode() == 404 {
		return nil, fmt.Errorf("%w: %s", ErrSandboxNotFound, sandboxID)
	}
	if resp.StatusCode() != 200 {
		return nil, apiError("retrieve sandbox", resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toSandbox(*resp.JSON200), nil
}

// List lists sandboxes for the workspace. opts may be nil.
func (s *SandboxClient) List(ctx context.Context, opts *ListSandboxesOptions) (*SandboxList, error) {
	ownerID, err := s.ownerID()
	if err != nil {
		return nil, err
	}
	params := &client.ListSandboxesParams{OwnerId: ownerID}
	if opts != nil {
		params.Cursor, params.Limit = page(opts.Cursor, opts.Limit)
		if len(opts.Status) > 0 {
			statuses := make([]sandboxes.SandboxStatus, len(opts.Status))
			for i, status := range opts.Status {
				statuses[i] = sandboxes.SandboxStatus(status)
			}
			params.Status = &statuses
		}
	}

	resp, err := s.client.internal.ListSandboxesWithResponse(ctx, params)
	if err != nil {
		return nil, fmt.Errorf("failed to make list sandboxes request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, apiError("list sandboxes", resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &SandboxList{Sandboxes: make([]Sandbox, len(items))}
	for i, item := range items {
		list.Sandboxes[i] = *toSandbox(item.Sandbox)
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}

// ListGroups lists the sandbox groups the workspace owns. Alpha guarantees at
// most one group per workspace, so the page holds zero or one group.
func (s *SandboxClient) ListGroups(ctx context.Context) (*SandboxGroupList, error) {
	ownerID, err := s.ownerID()
	if err != nil {
		return nil, err
	}
	resp, err := s.client.internal.ListSandboxGroupsWithResponse(ctx, &client.ListSandboxGroupsParams{OwnerId: ownerID})
	if err != nil {
		return nil, fmt.Errorf("failed to make list sandbox groups request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, apiError("list sandbox groups", resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &SandboxGroupList{Groups: make([]SandboxGroup, len(items))}
	for i, item := range items {
		g := item.SandboxGroup
		list.Groups[i] = SandboxGroup{
			ID:               g.Id,
			OwnerID:          g.OwnerId,
			Name:             g.Name,
			Region:           g.Region,
			IsDefault:        g.IsDefault,
			ConcurrencyLimit: g.ConcurrencyLimit,
			CreatedAt:        g.CreatedAt,
			UpdatedAt:        g.UpdatedAt,
			EnvironmentID:    g.EnvironmentId,
		}
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}

// Terminate terminates a sandbox. Terminating an already-terminated sandbox
// succeeds; a sandbox ID that was never valid returns ErrSandboxNotFound.
func (s *SandboxClient) Terminate(ctx context.Context, sandboxID string) error {
	ownerID, err := s.ownerID()
	if err != nil {
		return err
	}
	resp, err := s.client.internal.TerminateSandboxWithResponse(ctx, sandboxID, &client.TerminateSandboxParams{OwnerId: &ownerID})
	if err != nil {
		return fmt.Errorf("failed to make terminate sandbox request: %w", err)
	}
	if resp.StatusCode() == 404 {
		return fmt.Errorf("%w: %s", ErrSandboxNotFound, sandboxID)
	}
	if resp.StatusCode() >= 300 {
		return apiError("terminate sandbox", resp.StatusCode(), resp.Body)
	}
	return nil
}

// Exec runs command with bash -c in the sandbox and streams its output: zero
// or more SandboxExecOutput events, then one SandboxExecExit. A non-zero exit
// code arrives as a SandboxExecExit, not an error. A terminal error reported
// by the sandbox arrives as a *SandboxExecStreamError. Breaking out of the
// loop early closes the stream.
func (s *SandboxClient) Exec(ctx context.Context, sandboxID, command string) iter.Seq2[SandboxExecEvent, error] {
	return func(yield func(SandboxExecEvent, error) bool) {
		if err := s.exec(ctx, sandboxID, command, yield); err != nil {
			yield(nil, err)
		}
	}
}

func (s *SandboxClient) exec(ctx context.Context, sandboxID, command string, yield func(SandboxExecEvent, error) bool) error {
	ownerID, err := s.ownerID()
	if err != nil {
		return err
	}
	// The command rides along on the mint so the API keeps a sanitized copy
	// for the audit trail.
	mint, err := s.client.internal.ConnectSandboxRunWithResponse(ctx, sandboxID, "stream",
		&client.ConnectSandboxRunParams{OwnerId: &ownerID}, client.ConnectSandboxRunJSONRequestBody{Command: &command})
	if err != nil {
		return fmt.Errorf("failed to connect sandbox run: %w", err)
	}
	if mint.StatusCode() >= 400 {
		return sandboxHTTPError(sandboxID, mint.StatusCode(), mint.Body, "exec")
	}
	if mint.JSON201 == nil {
		return fmt.Errorf("unexpected response format")
	}

	payload, err := json.Marshal(map[string]string{"command": command})
	if err != nil {
		return err
	}
	ctx, idle := withIdleTimeout(ctx)
	defer idle.stop()
	req, err := http.NewRequestWithContext(ctx, mint.JSON201.Method, mint.JSON201.Uri, bytes.NewReader(payload))
	if err != nil {
		return err
	}
	req.Header.Set("Authorization", "Bearer "+mint.JSON201.Token)
	req.Header.Set("Accept", "text/event-stream")
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return idleError(ctx, fmt.Errorf("failed to exec in sandbox: %w", err))
	}
	defer func() { _ = resp.Body.Close() }()
	if resp.StatusCode >= 400 {
		body, _ := io.ReadAll(resp.Body)
		return sandboxHTTPError(sandboxID, resp.StatusCode, body, "exec")
	}

	var readErr error
	for name, data := range sseEvents(idle.reader(resp.Body), &readErr) {
		switch name {
		case "output":
			var event struct{ Stream, Data string }
			if err := json.Unmarshal([]byte(data), &event); err != nil {
				return fmt.Errorf("%w: failed to parse event data: %s", ErrSandboxExec, data)
			}
			if !yield(SandboxExecOutput{Stream: event.Stream, Data: event.Data}, nil) {
				return nil
			}
		case "exit":
			var event struct {
				ExitCode int `json:"exit_code"`
			}
			if err := json.Unmarshal([]byte(data), &event); err != nil {
				return fmt.Errorf("%w: failed to parse event data: %s", ErrSandboxExec, data)
			}
			yield(SandboxExecExit{ExitCode: event.ExitCode}, nil)
			return nil
		case "error":
			var event SandboxExecStreamError
			if err := json.Unmarshal([]byte(data), &event); err != nil {
				return fmt.Errorf("%w: failed to parse event data: %s", ErrSandboxExec, data)
			}
			return &event
		default:
			return fmt.Errorf("%w: unknown event %q", ErrSandboxExec, name)
		}
	}
	if err := ctx.Err(); err != nil {
		return idleError(ctx, err)
	}
	if readErr != nil {
		return fmt.Errorf("%w: failed to read stream: %w", ErrSandboxExec, readErr)
	}
	return fmt.Errorf("%w: stream ended without an exit event", ErrSandboxExec)
}

// sseEvents yields (event name, data) pairs from a server-sent event stream.
// The stream ending, cleanly or not, ends the sequence and discards any event
// not yet terminated by a blank line, as the SSE spec requires. A read error
// other than io.EOF is stored in *errp.
func sseEvents(r io.Reader, errp *error) iter.Seq2[string, string] {
	return func(yield func(string, string) bool) {
		// A Reader rather than a Scanner: an output chunk can exceed the
		// Scanner's line limit.
		br := bufio.NewReader(r)
		var name string
		var data []string
		for {
			line, err := br.ReadString('\n')
			if err != nil {
				if err != io.EOF {
					*errp = err
				}
				return
			}
			line = strings.TrimRight(line, "\r\n")
			switch {
			case line == "":
				if name != "" || data != nil {
					if !yield(name, strings.Join(data, "\n")) {
						return
					}
					name, data = "", nil
				}
			case strings.HasPrefix(line, ":"):
			case strings.HasPrefix(line, "event:"):
				name = strings.TrimSpace(line[len("event:"):])
			case strings.HasPrefix(line, "data:"):
				data = append(data, strings.TrimPrefix(line[len("data:"):], " "))
			}
		}
	}
}

// Create captures a snapshot of a running sandbox. The snapshot comes back
// with status creating; poll FromID until it is available or failed.
func (s *SnapshotClient) Create(ctx context.Context, sandboxID string, params CreateSnapshotParams) (*Snapshot, error) {
	body := sandboxes.SandboxSnapshotPOST{ExpiresAt: params.ExpiresAt}
	if params.Kind != "" {
		kind := sandboxes.SandboxSnapshotKind(params.Kind)
		body.Kind = &kind
	}
	if params.Name != "" {
		body.Name = &params.Name
	}
	resp, err := s.sandboxes.client.internal.CreateSandboxSnapshotWithResponse(ctx, sandboxID,
		&client.CreateSandboxSnapshotParams{OwnerId: s.sandboxes.optionalOwnerID()}, body)
	if err != nil {
		return nil, fmt.Errorf("failed to make create snapshot request: %w", err)
	}
	if resp.StatusCode() == 404 {
		return nil, fmt.Errorf("%w: %s", ErrSandboxNotFound, sandboxID)
	}
	if resp.StatusCode() != 202 {
		return nil, apiError("create snapshot", resp.StatusCode(), resp.Body)
	}
	if resp.JSON202 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toSnapshot(*resp.JSON202), nil
}

// FromID fetches a snapshot. Returns ErrSnapshotNotFound if it does not exist,
// was deleted, has expired, or belongs to another sandbox group.
func (s *SnapshotClient) FromID(ctx context.Context, sandboxGroupID, snapshotID string) (*Snapshot, error) {
	resp, err := s.sandboxes.client.internal.RetrieveSandboxSnapshotWithResponse(ctx, sandboxGroupID, snapshotID,
		&client.RetrieveSandboxSnapshotParams{OwnerId: s.sandboxes.optionalOwnerID()})
	if err != nil {
		return nil, fmt.Errorf("failed to make retrieve snapshot request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, snapshotError("retrieve snapshot", snapshotID, resp.StatusCode(), resp.Body, true)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return toSnapshot(*resp.JSON200), nil
}

// List lists snapshots of one sandbox group, newest first. Deleted and expired
// snapshots are omitted. opts may be nil.
func (s *SnapshotClient) List(ctx context.Context, sandboxGroupID string, opts *ListSnapshotsOptions) (*SnapshotList, error) {
	ownerID, err := s.sandboxes.ownerID()
	if err != nil {
		return nil, err
	}
	params := &client.ListSandboxSnapshotsParams{OwnerId: ownerID}
	if opts != nil {
		params.Cursor, params.Limit = page(opts.Cursor, opts.Limit)
		if len(opts.Status) > 0 {
			statuses := make([]sandboxes.SandboxSnapshotStatus, len(opts.Status))
			for i, status := range opts.Status {
				statuses[i] = sandboxes.SandboxSnapshotStatus(status)
			}
			params.Status = &statuses
		}
	}

	resp, err := s.sandboxes.client.internal.ListSandboxSnapshotsWithResponse(ctx, sandboxGroupID, params)
	if err != nil {
		return nil, fmt.Errorf("failed to make list snapshots request: %w", err)
	}
	if resp.StatusCode() != 200 {
		return nil, apiError("list snapshots", resp.StatusCode(), resp.Body)
	}
	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &SnapshotList{Snapshots: make([]Snapshot, len(items))}
	for i, item := range items {
		list.Snapshots[i] = *toSnapshot(item.Snapshot)
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}

// Delete deletes a snapshot. Deleting an already-deleted or expired snapshot
// succeeds. Returns ErrSnapshotNotFound if it never existed and
// ErrSnapshotNotReady if it is still creating.
func (s *SnapshotClient) Delete(ctx context.Context, sandboxGroupID, snapshotID string) error {
	resp, err := s.sandboxes.client.internal.DeleteSandboxSnapshotWithResponse(ctx, sandboxGroupID, snapshotID,
		&client.DeleteSandboxSnapshotParams{OwnerId: s.sandboxes.optionalOwnerID()})
	if err != nil {
		return fmt.Errorf("failed to make delete snapshot request: %w", err)
	}
	if resp.StatusCode() >= 300 {
		return snapshotError("delete snapshot", snapshotID, resp.StatusCode(), resp.Body, true)
	}
	return nil
}

func toNetworkPolicyPost(policy NetworkPolicy) (*sandboxes.SandboxNetworkPolicyPOST, error) {
	policyType := sandboxes.SandboxNetworkPolicyType(policy.Type)
	if !policyType.Valid() {
		return nil, fmt.Errorf("invalid network policy type %q", policy.Type)
	}
	body := &sandboxes.SandboxNetworkPolicyPOST{Type: &policyType}
	if policy.Type == "allow-list" {
		rules := make([]sandboxes.SandboxEgressRule, 0, len(policy.Rules))
		for _, rule := range policy.Rules {
			protocol := sandboxes.SandboxEgressRuleProtocol(rule.Protocol)
			if protocol == "" {
				protocol = sandboxes.Https
			}
			if !protocol.Valid() {
				return nil, fmt.Errorf("invalid egress rule protocol %q", rule.Protocol)
			}
			rules = append(rules, sandboxes.SandboxEgressRule{Domain: rule.Domain, Protocol: &protocol})
		}
		body.Rules = &rules
	} else if len(policy.Rules) > 0 {
		return nil, fmt.Errorf("rules are only allowed for an allow-list network policy")
	}
	return body, nil
}

func toNetworkPolicy(model sandboxes.SandboxNetworkPolicy) NetworkPolicy {
	policy := NetworkPolicy{Type: string(model.Type)}
	if model.Rules != nil {
		policy.Rules = make([]EgressRule, 0, len(*model.Rules))
		for _, rule := range *model.Rules {
			protocol := "https"
			if rule.Protocol != nil {
				protocol = string(*rule.Protocol)
			}
			policy.Rules = append(policy.Rules, EgressRule{Domain: rule.Domain, Protocol: protocol})
		}
	}
	return policy
}

func toSandbox(m sandboxes.Sandbox) *Sandbox {
	return &Sandbox{
		ID:             m.Id,
		Status:         string(m.Status),
		Plan:           string(m.Plan),
		NetworkPolicy:  toNetworkPolicy(m.NetworkPolicy),
		Region:         m.Region,
		TimeoutSeconds: m.TimeoutSeconds,
		CreatedAt:      m.CreatedAt,
		TerminatedAt:   m.TerminatedAt,
	}
}

func toSnapshot(m sandboxes.SandboxSnapshot) *Snapshot {
	return &Snapshot{
		ID:              m.Id,
		SandboxGroupID:  m.SandboxGroupId,
		SourceSandboxID: m.SourceSandboxId,
		Kind:            string(m.Kind),
		Status:          string(m.Status),
		Plan:            string(m.Plan),
		RequestedAt:     m.RequestedAt,
		ExpiresAt:       m.ExpiresAt,
		Name:            m.Name,
		CapturedAt:      m.CapturedAt,
		SizeBytes:       m.SizeBytes,
		Error:           m.Error,
	}
}

func page(cursor string, limit int) (*client.CursorParam, *client.LimitParam) {
	var c *client.CursorParam
	var l *client.LimitParam
	if cursor != "" {
		c = &cursor
	}
	if limit != 0 {
		l = &limit
	}
	return c, l
}

// errorBody pulls code and message out of an API error body, if it has them.
func errorBody(body []byte) (code, message string) {
	var e struct{ Code, Message string }
	_ = json.Unmarshal(body, &e)
	return e.Code, e.Message
}

func apiError(op string, status int, body []byte) error {
	if len(body) == 0 {
		return fmt.Errorf("%s failed with status %d", op, status)
	}
	return fmt.Errorf("%s failed with status %d: %s", op, status, body)
}

// snapshotError maps snapshot failures to sentinel errors. pathNamesSnapshot
// says whether the request path names the snapshot, in which case any 404 is
// the snapshot's; otherwise only a snapshot_not_found code is.
func snapshotError(op, snapshotRef string, status int, body []byte, pathNamesSnapshot bool) error {
	code, message := errorBody(body)
	detail := op + " failed"
	if message != "" {
		detail += ": " + message
	}
	switch {
	case status == 404 && (pathNamesSnapshot || code == snapshotNotFoundCode):
		return fmt.Errorf("%w: %s", ErrSnapshotNotFound, snapshotRef)
	case status == 409 && (code == snapshotCreatingCode || code == snapshotNotAvailableCode):
		return fmt.Errorf("%w: %s", ErrSnapshotNotReady, detail)
	case status == 409 && code == snapshotPlanMismatchCode:
		return fmt.Errorf("%w: %s", ErrSnapshotPlanMismatch, detail)
	}
	return apiError(op, status, body)
}

// sandboxHTTPError maps a failed call to the sandbox (or its token mint).
func sandboxHTTPError(sandboxID string, status int, body []byte, action string) error {
	if status == 404 {
		// The agent 404s a missing remote path with this code, and the sandbox
		// is alive when it does. Any other 404 is the sandbox itself being gone.
		if code, _ := errorBody(body); code == fileNotFoundCode {
			return fmt.Errorf("%w: %s", ErrSandboxFileNotFound, body)
		}
		return fmt.Errorf("%w: %s", ErrSandboxNotFound, sandboxID)
	}
	return apiError(action, status, body)
}

// idleTimeout cancels its context when no bytes arrive for sandboxIdleTimeout.
// It bounds the wait for the next chunk, not the whole transfer, so a long
// transfer still has as long as it needs while a dead one fails.
type idleTimeout struct {
	timer  *time.Timer
	cancel context.CancelCauseFunc
}

func withIdleTimeout(ctx context.Context) (context.Context, *idleTimeout) {
	ctx, cancel := context.WithCancelCause(ctx)
	timer := time.AfterFunc(sandboxIdleTimeout, func() { cancel(ErrSandboxIdleTimeout) })
	return ctx, &idleTimeout{timer: timer, cancel: cancel}
}

func (t *idleTimeout) stop() {
	t.timer.Stop()
	t.cancel(nil)
}

// reader resets the timer on every read from r.
func (t *idleTimeout) reader(r io.Reader) io.Reader {
	return readerFunc(func(p []byte) (int, error) {
		n, err := r.Read(p)
		t.timer.Reset(sandboxIdleTimeout)
		return n, err
	})
}

type readerFunc func([]byte) (int, error)

func (f readerFunc) Read(p []byte) (int, error) { return f(p) }

// idleError reports an idle timeout instead of the bare cancellation it caused.
func idleError(ctx context.Context, err error) error {
	if errors.Is(context.Cause(ctx), ErrSandboxIdleTimeout) {
		return ErrSandboxIdleTimeout
	}
	return err
}
