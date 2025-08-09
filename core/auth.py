from github import Github
import os

def github_client(token: str = None):
    """
    Return authenticated Github client.
    
    Priority:
    1. Use token passed as argument
    2. Fallback to GITHUB_TOKEN from environment
    
    Raises:
        ValueError if token is missing.
    """
    if not token:
        token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise ValueError("GitHub token is missing. Provide as argument or set GITHUB_TOKEN env var.")
    
    # TODO: add logging if needed
    return Github(token)

def get_github_token():
    """
    Return GitHub token from environment variable GITHUB_TOKEN.
    """
    import os
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")
    return token
