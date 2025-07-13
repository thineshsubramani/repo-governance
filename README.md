# repo-governor

**Governance-as-Code toolkit** to discover, validate, and enforce tags, workflows, README standards, and policies across all your GitHub repos.
Built for real engineering teams to standardize and secure hundreds of repos : fast, automated, and declarative.

---

## Why I built this

I wanted every repo to stay consistent, secure, and production-ready, without manual fixes.
When `config.yaml` or standard workflows change, updates roll out automatically across all repos.
End result: no drift, no outdated workflows, built-in security scanning everywhere.

---

## Key design goals

- **Declarative YAML config** : describe your governance once, apply to many repos
- **CI/CD agnostic** : works with GitHub Actions, GitLab CI, Jenkins, or even cron
- **Security & compliance first** : keep branch rules, CODEOWNERS, and workflows aligned
- **No vendor lock-in** : Python + REST, works anywhere your repos live

---

## What it does (planned)

* Discover repos by name regex, tags, branches, or existing workflows
* Add / rename / remove tags in bulk
* Add / update / remove standard workflows (SAST, lint, compliance, etc.)
* Validate README standards (required headers, sections, badges)
* Dry-run and diff before applying changes
* Modular tasks: branch protection, CODEOWNERS enforcement, and more

---

## Tech stack

* Python (PyGithub, YAML, regex) : quick to extend, hack, or integrate
* Docker : for consistent builds across CI/CD (coming soon)
* Composite GitHub Action : native drop-in for GitHub workflows (planned)

---

## Architecture

```
+-----------------------------+
| 1️⃣ Init GitHub Client      |
| github = Github(token)      |
| -------------------------  |
| Holds:                     |
| - HTTPS session            |
| - TCP socket (keep-alive)  |
+-------------+---------------+
              |
              v
+--------------------------------------------------+
| 2️⃣ Discover repos                               |
| repos = github.get_repo("org/repo1")             |
| ------------------------------------------------ |
| repos dict built like:                           |
| {                                                |
|   "org/repo1": {                                 |
|      "object": repo_obj1                         |
|   }                                              |
| }                                                |
+-------------+------------------------------------+
              |
              v
+--------------------------------------------------+
| 3️⃣ Inside repo_obj1:                            |
| PyGithub structure:                              |
| ------------------------------------------------ |
| repo_obj1.client   ---> points to same Github()  |
| repo_obj1.url      ---> repo REST URL            |
| repo_obj1._request ---> uses github._Github__requester |
|                                                      |
| So every call like:                                   |
|   repo_obj1.get_topics()                              |
|   repo_obj1.get_tags()                                |
|   repo_obj1.edit()                                    |
| all go back through the SAME client + TCP conn        |
+--------------------------------------------------+
```

* Github() creates a single requests.Session → holds TCP socket open

* repo_obj doesn’t duplicate connection; it keeps a pointer back to that session

* When you call .get_topics(), it builds REST URL & uses the same authenticated HTTP session → no new handshake

* Result:

    - Faster (no handshake / TLS per call)

    - Scales (single session O(1))

    - Saves rate limit

---
## Comments
I attached the repo object in the dict so I can reuse the same connection for filtering and future tasks.
Basically, I get all repo objects once (using a single API call) and store them in memory.
Then, when I need to get topics, tags, or update workflows, I call methods on those existing objects, this keeps using the same authenticated HTTP session + TCP socket, so it avoids opening new connections.
This helps reduce extra API calls and latency.
Still figuring out better ways to optimize and keep it fast, but right now this design already avoids a lot of repeated connects and keeps everything in-memory for batch processing.
