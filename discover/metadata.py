from core.api_stats import measure_api_stats
from datetime import datetime

@measure_api_stats
def enrich_and_filter_repos_by_date(client, repos, 
                                    filter_by=None, # "created" or "last_commit"
                                    start_date=None, end_date=None, # datetime
                                    sort_by=None, # "created" or "last_commit"
                                    descending=True):
    """
    Enrich repos with created & last_commit date.
    Then:
      - Filter: keep only repos within date range (by filter_by)
      - Sort: by created_date or last_commit_date
    """
    enriched = {}

    for repo_name, data in repos.items():
        repo = data["object"]
        created_date = repo.created_at
        default_branch = repo.default_branch
        last_commit_date = None

        try:
            commits = repo.get_commits(sha=default_branch)
            last_commit_date = commits[0].commit.author.date
        except Exception as e:
            print(f"[-] Couldn’t get last commit for {repo.full_name}: {e}")

        enriched[repo_name] = {
            **data,
            "created_date": created_date,
            "last_commit_date": last_commit_date
        }

    # Filter by date range
    if filter_by in ("created", "last_commit") and (start_date or end_date):
        key = f"{filter_by}_date"
        filtered = {}
        for name, item in enriched.items():
            dt = item.get(key)
            if dt:
                if start_date and dt < start_date:
                    continue
                if end_date and dt > end_date:
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
