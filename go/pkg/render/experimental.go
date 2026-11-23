package render

// ExperimentalService exposes experimental Render SDK features.
//
// Features in this namespace may change or be removed without a migration plan.
type ExperimentalService struct {
	Objects *ObjectAPI
}

func newExperimentalService(c *Client) *ExperimentalService {
	return &ExperimentalService{Objects: &ObjectAPI{client: c}}
}
