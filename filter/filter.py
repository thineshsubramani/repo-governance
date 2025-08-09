def filter_repos(repo_info, my_owners=None, keep_fields=None):
    """
    Filter repos by owner and return a dict of {repo_full_name: {meta, ...}}
    """
    filtered = {}
    for repo_full_name, data in repo_info.items():
        owner = data["meta"]["owner"]
        if my_owners is None or owner in my_owners:
            filtered[repo_full_name] = {k: v for k, v in data.items() if not keep_fields or k in keep_fields}
    return filtered
