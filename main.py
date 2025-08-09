import datetime
from assets.workflow_content import get_workflow_content
from core.auth import github_client, get_github_token  # Add get_github_token
from core.parser import load_yaml_config
from filter.filter import filter_repos
from discover.repos import discover_repositories, discover_repositories_graphql
from discover.metadata import enrich_and_filter_repos_by_date
from tasks.workflows import ensure_workflow_in_repos
from tasks.audit import update_audit_readme  # ← Make sure this is placed correctly

def main():
    client = github_client()
    token = get_github_token()  # Implement this to read from env/config
    use_graphql = True  # set this to False to use REST

    print("\n== Loading config ==")
    config = load_yaml_config("config.yaml")

    print("\n== Discovering all repositories ==")
    if use_graphql:
        repo_info = discover_repositories_graphql(client, token)
    else:
        repo_info = discover_repositories(client)
    print(f"Total repos: {len(repo_info)}")

    print("\n== Filtering repos based on ownership only ==")
    my_owners = config.get('ownership', []) if config else []
    filtered_repo_info = filter_repos(
        repo_info,
        my_owners=my_owners,
        keep_fields=['object', 'meta']
    )

    # Filter repos by commit date (last 3 days) and sort
    start = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=120)
    enriched = enrich_and_filter_repos_by_date(
        client,
        filtered_repo_info,
        filter_by="last_commit",
        start_date=start,
        sort_by="last_commit",
        descending=True
    )

    # When passing to tasks, pass only the list of repo full names or meta dicts
    repo_full_names = list(enriched.keys())

    # Example: in ensure_workflow_in_repos, fetch repo object inside the function
    # ensure_workflow_in_repos(client, "hardening.yml", workflow_content, repo_full_names)

    # Similarly for audit, topics, etc.

    # Update audit report
    print("\n== Updating audit report README ==")
    update_audit_readme(
        client=client,
        audit_repo_name="thineshsubramani/audit-reports",  
        workflow_name="hardening.yml",
        repos=enriched
    )

if __name__ == "__main__":
    main()
