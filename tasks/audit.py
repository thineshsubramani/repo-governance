from github import GithubException
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

AUDIT_FILE = "README.md"
HEADER = "# 🛡️ GitHub Audit Report\n\n_Last updated: {}_\n\n"
TABLE_HEADER = (
    "| Name | Open Issues | Last Updated | Updated By | Workflow Present | Topics | Branch |\n"
    "|------|-------------|--------------|------------|------------------|--------|--------|\n"
)

def get_repo_data(repo, workflow_name, fetch_topics=True):
    # Check workflow presence (1 API call)
    try:
        repo.get_contents(f".github/workflows/{workflow_name}")
        has_wf = "✅"
    except GithubException as e:
        if e.status == 404:
            has_wf = "❌"
        else:
            has_wf = "⚠️"

    # Use pushed_at instead of get_commits (no extra call)
    last_updated = repo.pushed_at.strftime("%Y-%m-%d %H:%M UTC") if repo.pushed_at else "N/A"
    last_author = "N/A"  # Can't get author without extra call

    # Only fetch topics if needed
    topics = ", ".join(repo.get_topics()) if fetch_topics else "-"

    return {
        "name": repo.name,
        "open_issues": repo.open_issues_count,
        "updated": last_updated,
        "updated_by": last_author,
        "has_workflow": has_wf,
        "topics": topics,
        "branch": repo.default_branch,
    }

def get_repo_data_cached(meta, workflow_present, fetch_topics=True):
    return {
        "name": meta["name"],
        "open_issues": meta["open_issues_count"],
        "updated": meta["pushed_at"].strftime("%Y-%m-%d %H:%M UTC") if meta["pushed_at"] else "N/A",
        "updated_by": "N/A",
        "has_workflow": workflow_present,
        "topics": ", ".join(meta.get("topics", [])) if fetch_topics else "-",
        "branch": meta["default_branch"],
    }

def update_audit_readme(client, audit_repo_name, workflow_name, repos):
    """
    Update the audit report README with workflow status for each repo.
    repos: dict of {repo_full_name: {meta, ...}}
    """
    audit_repo = client.get_repo(audit_repo_name)

    def fetch_info(repo_full_name):
        repo = client.get_repo(repo_full_name)
        return get_repo_data(repo, workflow_name)

    # Use ThreadPoolExecutor to parallelize API calls
    repo_data = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_repo = {executor.submit(fetch_info, repo_full_name): repo_full_name for repo_full_name in repos}
        for future in as_completed(future_to_repo):
            try:
                info = future.result()
                repo_data.append(info)
            except Exception as e:
                print(f"[-] Error processing {future_to_repo[future]}: {e}")

    # Sort by most recently pushed
    repo_data.sort(key=lambda r: r["updated"], reverse=True)

    table_rows = ""
    for r in repo_data:
        table_rows += (
            f"| {r['name']} "
            f"| {r['open_issues']} "
            f"| {r['updated']} "
            f"| {r['updated_by']} "
            f"| {r['has_workflow']} "
            f"| {r['topics']} "
            f"| {r['branch']} |\n"
        )

    readme_content = HEADER.format(datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")) + TABLE_HEADER + table_rows

    try:
        existing_file = audit_repo.get_contents(AUDIT_FILE)
        audit_repo.update_file(
            path=AUDIT_FILE,
            message="Update audit report",
            content=readme_content,
            sha=existing_file.sha,
            branch=audit_repo.default_branch
        )
        print(f"[+] README.md updated in {audit_repo.full_name}")
    except GithubException as e:
        if e.status == 404:
            audit_repo.create_file(
                path=AUDIT_FILE,
                content=readme_content,
                message="Create audit report",
                branch=audit_repo.default_branch
            )
            print(f"[+] README.md created in {audit_repo.full_name}")
        else:
            print(f"[-] Error updating README.md in {audit_repo.full_name}: {e}")
