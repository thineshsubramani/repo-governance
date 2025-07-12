from core.auth import github_client

def list_repositories(token: str = None):
    """
    List all repositories accessible by the token.
    """
    g = github_client(token)
    user = g.get_user()
    repos = user.get_repos()
    repo_names = [repo.full_name for repo in repos]
    return repo_names
