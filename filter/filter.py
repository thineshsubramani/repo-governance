def filter_repos(repo_info, my_owners=None, config=None, keep_fields=None):
    """
    Filter repos: keep only repos owned by me (my_owners) and not forked.
    keep_fields: list of fields to keep, e.g. ['object', 'meta']
    """
    filtered = {}

    for repo_full_name, data in repo_info.items():
        meta = data.get('meta', {})
        owner = meta.get('owner')
        is_fork = meta.get('fork', False)

        # logic: keep if owner in my_owners and not forked
        if my_owners and owner in my_owners and not is_fork:
            # keep only specified fields if any
            if keep_fields:
                filtered_data = {k: v for k, v in data.items() if k in keep_fields}
            else:
                filtered_data = data
            filtered[repo_full_name] = filtered_data

    return filtered
