# repo-governance

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

- The toolkit creates a single authenticated GitHub client (`Github(token)`), which manages a persistent HTTP session for all API calls.
- Repository metadata (such as full name, owner, etc.) is stored in lightweight data structures.
- When an operation is needed (e.g., get topics, update workflows), the repo object is fetched on demand using `client.get_repo(full_name)`.
- All API calls use the same session and TCP connection, which is efficient and conserves rate limits.

*Result:*
- Faster (no handshake / TLS per call)
- Scales (single session O(1))
- Saves rate limit

---

## Comments
