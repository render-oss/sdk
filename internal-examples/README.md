# Internal Examples

These are example tasks intended for internal testing use cases. These should not be published externally.

## Using these examples

1. Create a new workflow in the dashboard.
1. For `Source Code`, select the `renderinc/sdk` repository.
1. For `Language`, select `Python`
1. For `Branch`, select `main` unless you are testing a specific branch
1. For `Auto-Deploy`, select `Off` if you don't need this workflow to update automatically
1. For `Region`, select the region you want to run the workflow in.
    - If you want to run the workflow in a specific cluster, use the workspace email override: https://slab.render.com/posts/how-to-test-in-a-specific-cluster-9cjlhb7p#h82dc-using-workspace-email-override
1. For `Root Directory`, enter `internal-examples`.
1. For `Build Command`, enter `pip install -r requirements.txt` (which should be the default).
1. For `Start Command`, enter `python main.py` (which should be the default).
