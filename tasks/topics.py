from core.api_stats import measure_api_stats

@measure_api_stats
def add_topic_to_repos(client, topic, repos):
    """
    Add topic to each repo in dict if missing.
    repos: dict {repo_full_name: {"object": repo_obj, ...}}
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        topics = repo.get_topics()
        if topic not in topics:
            topics.append(topic)
            repo.replace_topics(topics)
            print(f"[+] {repo.full_name}: topic '{topic}' added")


@measure_api_stats
def remove_topic_from_repos(client, topic, repos):
    """
    Remove topic from each repo if exists.
    repos: dict {repo_full_name: {"object": repo_obj, ...}}
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        topics = repo.get_topics()
        if topic in topics:
            topics.remove(topic)
            repo.replace_topics(topics)
            print(f"[-] {repo.full_name}: topic '{topic}' removed")


@measure_api_stats
def rename_topic_in_repos(client, old_topic, new_topic, repos):
    """
    Rename topic: replace old with new across repos.
    repos: dict {repo_full_name: {"object": repo_obj, ...}}
    """
    for repo_name, data in repos.items():
        repo = data["object"]
        topics = repo.get_topics()
        if old_topic in topics:
            topics.remove(old_topic)
            if new_topic not in topics:
                topics.append(new_topic)
            repo.replace_topics(topics)
            print(f"[~] {repo.full_name}: topic '{old_topic}' renamed to '{new_topic}'")
