def filter_repos(repo_info, my_owners=None, keep_fields=None):
    """
    Filter repos by owner and return a dict of {repo_full_name: {meta, ...}}
    """
    if not my_owners:
        return repo_info  # No filtering needed
    my_owners = set(my_owners)
    # Use dictionary comprehension for speed
    return {
        repo_full_name: {k: v for k, v in data.items() if not keep_fields or k in keep_fields}
        for repo_full_name, data in repo_info.items()
        if data["meta"]["owner"] in my_owners
    }
