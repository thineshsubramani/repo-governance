import datetime
from assets.workflow_content import get_workflow_content
from core.auth import github_client
from core.parser import load_yaml_config
from filter.filter import filter_repos
from discover.repos import discover_repositories
from discover.metadata import enrich_and_filter_repos_by_date
from tasks.workflows import ensure_workflow_in_repos
from tasks.audit import update_audit_readme  # ← Make sure this is placed correctly

def main():
    client = github_client()

    print("\n== Loading config ==")
    config = load_yaml_config("config.yaml")

    print("\n== Discovering all repositories ==")
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

    # Apply the workflow if not present
    # workflow_content = get_workflow_content()
    # ensure_workflow_in_repos(client, "hardening.yml", workflow_content, enriched)

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
