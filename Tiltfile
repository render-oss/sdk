# Allow only development Kubernetes contexts
GCP_DEV_CLUSTER_PREFIX = "gke_render-devs"
AWS_DEV_CLUSTER_PATTERN = "aws-{cluster name}-dev-{user name}"

def is_aws_dev_context():
    # Example: aws-us-west-2-1-dev-username
    context = k8s_context()
    parts = context.split("-")
    return len(parts) == 7 and parts[0] == "aws" and parts[5] == "dev"

def ensure_aws_dev_context(resource = "this resource"):
    context = k8s_context()
    if not is_aws_dev_context():
        fail("can only run '{}' in an AWS clusters (current context {} does not match {})".format(resource, context, AWS_DEV_CLUSTER_PATTERN))

def is_gcp_dev_context():
    # Example: aws-us-west-2-1-dev-username
    context = k8s_context()
    return context.startswith(GCP_DEV_CLUSTER_PREFIX)

def ensure_gcp_dev_context(resource = "this resource"):
    context = k8s_context()
    if not is_gcp_dev_context():
        fail("can only run '{}' in a GCP clusters (current context {} does not match {})".format(resource, context, GCP_DEV_CLUSTER_PREFIX))



def ensure_dev_context():
    """
    Raise an exception if the context is not a dev GCP or AWS cluster
    """
    context = k8s_context()
    if is_gcp_dev_context():
        print("allowing Kubernetes context {} that starts with {}".format(context, GCP_DEV_CLUSTER_PREFIX))
        allow_k8s_contexts(context)
    elif is_aws_dev_context():
        print("allowing Kubernetes context {} that matches pattern {}".format(context, AWS_DEV_CLUSTER_PATTERN))
        allow_k8s_contexts(context)
    else:
        fail("\n\nNot allowing Kubernetes context {} as it does not match any allowed patterns.\nTry running `tilt up --context <your-dev-cluster>` to avoid targeting production clusters".format(context))

# Running this top level because of the side effects that it will
# have. We need to allow the k8s context or else we won't be able to
# run `local` functions
ensure_dev_context()

# Build the Go example binary Docker image
docker_build(
    'gcr.io/render-devs/workflow-sdk-dev',
    './go',
    dockerfile='./go/Dockerfile'
)

# Load the static YAML resources
k8s_yaml('resources.yaml')

# Configure the daemonset resource - Tilt will automatically substitute the go-example image
k8s_resource('wfv-d262g3atu6bs73fvh44g')
