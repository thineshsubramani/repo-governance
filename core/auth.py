from github import Github

def github_client(token: str = None):
    """
    Return authenticated GitHub client.
    """
    if not token:
        # fallback to env var
        import os
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GitHub token not provided")
    return Github(token)
