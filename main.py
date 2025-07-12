import datetime
from core.auth import github_client
from core.parser import load_yaml_config
from filter.filter import filter_repos
from discover.repos import discover_repositories
from discover.metadata import enrich_and_filter_repos_by_date
from tasks.topics import add_topic_to_repos, remove_topic_from_repos

def main():
    client = github_client()

    print("\n== Loading config ==")
    config = load_yaml_config("config.yaml")

    print("\n== Discovering all repositories ==")
    repo_info = discover_repositories(client)
    print(f"Total repos: {len(repo_info)}")

    print("\n== Filtering repos based on ownership only ==")

    my_owners = config.get('ownership', []) if config else []
    print(my_owners)
    filtered_repo_info = filter_repos(
        repo_info,
        my_owners=my_owners,
        keep_fields=['object', 'meta']
    )
    # print(filtered_repo_info)
    # get_repo_dates = get_repo(client, filtered_repo_info)
    # print(get_repo_dates)


    start = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)


    enriched = enrich_and_filter_repos_by_date(
        client,
        filtered_repo_info,
        filter_by="last_commit", 
        start_date=start,
        sort_by="last_commit",
        descending=True
    )
    print(enriched)

    # print("\n== Adding topic to filtered repos ==")
    # add_topic_to_repos(
    #     client,
    #     topic="certified",
    #     repos=filtered_repo_info
    # )

    # remove_topic_from_repos(
    #     client,
    #     topic="certified",
    #     repos=filtered_repo_info
    # )

if __name__ == "__main__":
    main()
