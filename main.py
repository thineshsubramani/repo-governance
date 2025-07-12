from discover.repos import list_repositories

def main():
    repos = list_repositories()
    print("Discovered repositories:")
    for r in repos:
        print(f"- {r}")

if __name__ == "__main__":
    main()
