# Maintaining the community repository

The owner and code owner is @DouwJacobs. Public contributors use forks, issues and pull requests. Being a contributor does not grant write access. Grant collaborator access only after explicit owner approval; review collaborators periodically.

## Main branch controls

The `Main integrity` ruleset targets `refs/heads/main` with no bypass actors: pull requests are required, `Validate configuration` from GitHub Actions must pass against the current base, merge history must be linear, and force pushes and deletion are blocked.

The separate `Community review` ruleset requires one approval, code-owner review, dismissal of stale approvals, approval of the last push and resolved review conversations. Repository administrators have a **pull-request-only** bypass for this review ruleset so a sole owner can merge their own change. That exception does not bypass the independent integrity ruleset or permit direct pushes. Use it only for owner-authored changes or a documented exceptional review decision.

`.github/CODEOWNERS` covers every file, including itself and workflows. Never weaken controls as part of an ordinary merchant contribution. Required checks are bound to GitHub Actions (integration ID 15368) to avoid accepting a status posted by another app. These settings live in GitHub, not in a file; changes to this document do not change them. Inspect Settings -> Rules -> Rulesets to verify enforcement.

## CI and merge procedure

Actions defaults are read-only, Actions cannot approve pull requests, and every external fork contributor requires approval before workflows run. Validation uses the `pull_request` event, GitHub-hosted runners, no secrets, SHA-pinned actions and checkout without persistent credentials. Inspect changes to workflows and validation code before approving a fork run. Never introduce `pull_request_target` to execute contributor code.

Before merging, inspect public-data hygiene, merchant ambiguity, examples, independent pack references and default replacements. Require green validation and review the diff even for an owner-authored PR. Squash merging and automatic source-branch deletion are enabled. Publishing compatible tags and updating Sente's bundled offline snapshot remain separate release actions.

Refresh the matcher snapshot and synthetic importer checks when Sente changes its matching/import behavior. Review dependency updates rather than treating them as merchant changes. GPL-3.0-only applies to the repository; retain license and source notices when redistributing it.
