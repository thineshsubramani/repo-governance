from core.api_stats import measure_api_stats
import requests
import os

@measure_api_stats
def discover_repositories(client):
    """
    Discover all repos owned by user.
    Return dict: repo_full_name -> {
        'meta': lightweight metadata for filtering
    }
    """
    user = client.get_user()
    # Don't convert to list, iterate directly
    repo_info = {}
    for repo in user.get_repos():  # generator, fetches page by page
        repo_info[repo.full_name] = {
            "meta": {
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "fork": repo.fork,
                "private": repo.private,
                "default_branch": repo.default_branch,
                "pushed_at": repo.pushed_at,
                "open_issues_count": repo.open_issues_count,
                # Optionally fetch topics here if needed:
                # "topics": repo.get_topics(),
            }
        }
    return repo_info

def discover_repositories_graphql(client, token, owner=None):
    """
    Discover all repos for the authenticated user (or a specific owner/org) using GraphQL.
    Returns: dict of {repo_full_name: {"meta": ...}}
    """
    headers = {"Authorization": f"Bearer {token}"}
    api_url = "https://api.github.com/graphql"

    # If owner is None, use authenticated user login
    if owner is None:
        owner = client.get_user().login

    query = """
    query($owner: String!, $cursor: String) {
      repositoryOwner(login: $owner) {
        repositories(first: 100, after: $cursor, ownerAffiliations: OWNER) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            name
            nameWithOwner
            owner { login }
            isFork
            isPrivate
            defaultBranchRef { name }
            pushedAt
            openIssues: issues(states: OPEN) { totalCount }
            topics: repositoryTopics(first: 20) {
              nodes { topic { name } }
            }
          }
        }
      }
    }
    """

    repo_info = {}
    cursor = None
    while True:
        variables = {"owner": owner, "cursor": cursor}
        resp = requests.post(api_url, json={"query": query, "variables": variables}, headers=headers)
        data = resp.json()
        repos = data["data"]["repositoryOwner"]["repositories"]["nodes"]
        for repo in repos:
            topics = [t["topic"]["name"] for t in repo["topics"]["nodes"]]
            repo_info[repo["nameWithOwner"]] = {
                "meta": {
                    "name": repo["name"],
                    "full_name": repo["nameWithOwner"],
                    "owner": repo["owner"]["login"],
                    "fork": repo["isFork"],
                    "private": repo["isPrivate"],
                    "default_branch": repo["defaultBranchRef"]["name"] if repo["defaultBranchRef"] else None,
                    "pushed_at": repo["pushedAt"],
                    "open_issues_count": repo["openIssues"]["totalCount"],
                    "topics": topics,
                }
            }
        page_info = data["data"]["repositoryOwner"]["repositories"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]
    return repo_info
