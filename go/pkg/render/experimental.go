package render

// ExperimentalService exposes experimental Render SDK features.
//
// Features in this namespace may change or be removed without a migration plan.
type ExperimentalService struct {
	Objects   *ObjectAPI
	Sandboxes *SandboxClient
}

func newExperimentalService(c *Client) *ExperimentalService {
	sandboxes := &SandboxClient{client: c}
	sandboxes.Snapshots = &SnapshotClient{sandboxes: sandboxes}
	sandboxes.Images = &ImageClient{sandboxes: sandboxes}
	return &ExperimentalService{Objects: &ObjectAPI{client: c}, Sandboxes: sandboxes}
}
