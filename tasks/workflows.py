from core.api_stats import measure_api_stats
from github import GithubException

def has_workflow(repo, filename):
    try:
        repo.get_contents(f".github/workflows/{filename}")
        return True
    except GithubException as e:
        if e.status == 404:
            return False
        raise

@measure_api_stats
def ensure_workflow_in_repos(client, workflow_name, workflow_content, repos):
    """
    Add workflow to repos if missing (disabled by default).
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        if not has_workflow(repo, workflow_name):
            repo.create_file(
                path=f".github/workflows/{workflow_name}",
                message=f"Add {workflow_name} workflow (disabled by default)",
                content=workflow_content,
                branch=repo.default_branch
            )
            print(f"[+] {repo.full_name}: workflow '{workflow_name}' added")
        else:
            print(f"[=] {repo.full_name}: workflow '{workflow_name}' already exists")

@measure_api_stats
def remove_workflow_from_repos(client, workflow_name, repos):
    """
    Remove workflow file if exists.
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        path = f".github/workflows/{workflow_name}"
        try:
            file = repo.get_contents(path)
            repo.delete_file(
                path=path,
                message=f"Remove workflow {workflow_name}",
                sha=file.sha,
                branch=repo.default_branch
            )
            print(f"[-] {repo.full_name}: workflow '{workflow_name}' removed")
        except GithubException as e:
            if e.status == 404:
                print(f"[=] {repo.full_name}: workflow '{workflow_name}' does not exist")
            else:
                raise

@measure_api_stats
def rename_workflow_in_repos(client, old_name, new_name, repos):
    """
    Rename workflow file across repos: copy then delete old.
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        old_path = f".github/workflows/{old_name}"
        new_path = f".github/workflows/{new_name}"
        try:
            file = repo.get_contents(old_path)
            # create new file with same content
            repo.create_file(
                path=new_path,
                message=f"Rename workflow {old_name} to {new_name}",
                content=file.decoded_content.decode(),
                branch=repo.default_branch
            )
            # delete old file
            repo.delete_file(
                path=old_path,
                message=f"Remove old workflow {old_name} after renaming",
                sha=file.sha,
                branch=repo.default_branch
            )
            print(f"[~] {repo.full_name}: workflow '{old_name}' renamed to '{new_name}'")
        except GithubException as e:
            if e.status == 404:
                print(f"[=] {repo.full_name}: workflow '{old_name}' does not exist")
            else:
                raise
