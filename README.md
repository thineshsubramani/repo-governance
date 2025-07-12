# repo-governor

**Governance-as-Code toolkit** to discover, validate, and enforce tags, workflows, README standards, and policies across all your GitHub repos. Built to govern and standardize multiple repositories with a policy-as-code approach.

---

## Why it exists

* GitHub CLI (`gh`) gives low-level commands, but no orchestration or policy layer
* Need a **declarative**, YAML-driven tool to scale governance across 10, 50, or 100+ repos
* Designed to plug directly into any CI/CD: GitHub Actions, GitLab CI, Jenkins, or cron

---

## What it does (planned)

* Discover repos by name regex, tags, branch, existing workflows
* Add / rename / remove tags in batch
* Add / update / remove standard workflows (like SAST, lint, compliance)
* Validate and enforce README standards (headers, sections)
* Dry-run and diff before apply
* Modular task system: add branch protection, CODEOWNERS enforcement, etc.

---

## Tech stack

* Python core (PyGithub, YAML, regex) for fast dev and flexibility
* Docker for consistent builds across CI/CD
* Composite GitHub Action for native use in GitHub workflows
