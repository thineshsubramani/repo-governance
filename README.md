# repo-governor

**Governance-as-Code toolkit** to discover, validate, and enforce tags, workflows, README standards, and policies across all your GitHub repos.
Built for real engineering teams to standardize and secure hundreds of repos : fast, automated, and declarative.

---

## Why I built this

I wanted every repo to stay consistent, secure, and production-ready — without manual fixes.
When `config.yaml` or standard workflows change, updates roll out automatically across all repos.
End result: no drift, no outdated workflows, built-in security scanning everywhere.

---

## Key design goals

**Declarative YAML config** : describe your governance once, apply to many repos
**CI/CD agnostic** : works with GitHub Actions, GitLab CI, Jenkins, or even cron
**Security & compliance first** : keep branch rules, CODEOWNERS, and workflows aligned
**No vendor lock-in** : Python + REST, works anywhere your repos live

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




