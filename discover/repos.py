from core.api_stats import measure_api_stats

@measure_api_stats
def discover_repositories(client):
    """
    Discover all repos owned by user.
    Return dict: repo_full_name -> {
        'object': repo_object,
        'meta': lightweight metadata for filtering
    }
    """
    user = client.get_user()
    repos = list(user.get_repos())

    repo_info = {}
    for repo in repos:
        repo_info[repo.full_name] = {
            "object": repo,  # keep the PyGithub Repository object
            "meta": {
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "fork": repo.fork,
                "private": repo.private,
                "default_branch": repo.default_branch,            }
        }

    return repo_info
