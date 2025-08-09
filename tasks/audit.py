from github import GithubException
from datetime import datetime

AUDIT_FILE = "README.md"
HEADER = "# 🛡️ GitHub Audit Report\n\n_Last updated: {}_\n\n"
TABLE_HEADER = "| Repository | Last Updated | Workflow Present | Topics | Branch |\n|------------|---------------|------------------|------|--------|\n"

def get_repo_data(repo, workflow_name):
    # Check workflow presence
    try:
        repo.get_contents(f".github/workflows/{workflow_name}")
        has_wf = "✅"
    except GithubException as e:
        if e.status == 404:
            has_wf = "❌"
        else:
            has_wf = "⚠️"

    return {
        "name": repo.name,
        "full_name": repo.full_name,
        "url": repo.html_url,
        "updated": repo.pushed_at.strftime("%Y-%m-%d %H:%M UTC") if repo.pushed_at else "N/A",
        "has_workflow": has_wf,
        "topics": ", ".join(repo.get_topics()) or "-",
        "branch": repo.default_branch,
    }

def update_audit_readme(client, audit_repo_name, workflow_name, repos):
    """
    Update the audit report README with workflow status for each repo.
    repos: dict of {repo_full_name: {meta, ...}}
    """
    audit_repo = client.get_repo(audit_repo_name)

    repo_data = []
    for repo_full_name, data in repos.items():
        repo = client.get_repo(repo_full_name)  # ← FIXED: fetch repo object here
        info = get_repo_data(repo, workflow_name)
        repo_data.append(info)

    # Sort by most recently pushed
    repo_data.sort(key=lambda r: r["updated"], reverse=True)

    table_rows = ""
    for r in repo_data:
        table_rows += f"| [{r['full_name']}]({r['url']}) | {r['updated']} | {r['has_workflow']} | {r['topics']} | {r['branch']} |\n"

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
                message="Create audit report",
                content=readme_content,
                branch=audit_repo.default_branch
            )
            print(f"[+] README.md created in {audit_repo.full_name}")
        else:
            raise
