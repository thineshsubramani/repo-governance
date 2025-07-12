from core.api_stats import measure_api_stats

@measure_api_stats
def discover_repo_topics(client, owner_prefix="thineshsubramani/"):
    """
    Discover topics of all repos matching owner_prefix.
    Returns: {repo_full_name: [topics]}
    """
    user = client.get_user()
    repos = list(user.get_repos())

    topic_info = {}
    for repo in repos:
        if repo.full_name.startswith(owner_prefix):
            topics = repo.get_topics()
            topic_info[repo.full_name] = topics
    return topic_info


@measure_api_stats
def discover_topics_for_repos(client, repos):
    """
    Discover topics ONLY for provided list of repo full names.
    Returns: {repo_full_name: [topics]}
    """
    topic_info = {}
    for full_name in repos:
        repo = client.get_repo(full_name)
        topics = repo.get_topics()
        topic_info[full_name] = topics
    return topic_info
