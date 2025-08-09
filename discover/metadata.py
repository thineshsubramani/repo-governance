from core.api_stats import measure_api_stats
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

@measure_api_stats
def enrich_and_filter_repos_by_date(client, repo_info, filter_by, start_date, sort_by, descending):
    """
    Enrich repos with commit date and filter/sort.
    repo_info: dict of {repo_full_name: {"meta": ...}}
    """
    def enrich_repo(repo_full_name, data):
        repo = client.get_repo(repo_full_name)
        created_date = repo.created_at
        default_branch = repo.default_branch
        last_commit_date = None
        try:
            commits = repo.get_commits(sha=default_branch)
            last_commit_date = commits[0].commit.author.date
        except Exception as e:
            print(f"[-] Couldn’t get last commit for {repo.full_name}: {e}")
        return repo_full_name, {
            **data,
            "created_date": created_date,
            "last_commit_date": last_commit_date
        }

    enriched = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(enrich_repo, repo_full_name, data)
            for repo_full_name, data in repo_info.items()
        ]
        for future in as_completed(futures):
            repo_full_name, enriched_data = future.result()
            enriched[repo_full_name] = enriched_data

    # Filter by date range
    if filter_by in ("created", "last_commit") and (start_date):
        key = f"{filter_by}_date"
        filtered = {}
        for name, item in enriched.items():
            dt = item.get(key)
            if dt:
                if dt < start_date:
                    continue
                filtered[name] = item
        enriched = filtered

    # Sort
    if sort_by in ("created", "last_commit"):
        key = f"{sort_by}_date"
        enriched = dict(
            sorted(enriched.items(), 
                   key=lambda x: x[1].get(key) or datetime.min, 
                   reverse=descending)
        )

    return enriched
