def filter_repos(repo_info, my_owners, config=None, keep_fields=None):
    """
    Filter repos: keep only repos owned by config.ownership and not forked.
    keep_fields: list of fields to keep, e.g. ['object', 'meta']
    """
    filtered = {}

    for repo_full_name, data in repo_info.items():
        meta = data.get('meta', {})
        owner = meta.get('owner')
        is_fork = meta.get('fork', False)

        if owner in my_owners and not is_fork:
            # keep only needed fields
            if keep_fields:
                filtered_data = {k: v for k, v in data.items() if k in keep_fields}
            else:
                filtered_data = data
            filtered[repo_full_name] = filtered_data

    return filtered
