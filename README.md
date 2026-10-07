# Sente configuration

Optional starter categories, spending groups and rules for [Sente](https://github.com/DouwJacobs/sente). No personal EFT patterns, account names, financial transactions or credentials belong in this repository.

## Use it

In Sente, open **Settings → Configuration → Pull starter and preview**, inspect the changes, then import. Updates are manual. Sente records the applied commit; it does not stay connected or sync automatically.

For an additional source, use:

- Repository: `https://github.com/DouwJacobs/sente-config.git`
- File: `sente.json`
- Branch/tag/commit: leave blank for the default branch, or pin a known-compatible tag or commit.

You can combine this pack with your own public repositories and JSON files. Private repository users can upload the file instead. Export your own configuration from Sente, edit it, and keep personal patterns in a private file or repository.

## Format

`sente.json` uses portable format **version 2**. `schema.json` helps author files; Sente also validates references, duplicates, permissions and dependencies. Maximum: 32 MiB and 10,000 combined entries. Unknown fields and unsupported versions reject. Do not insert `$schema` in the configuration itself.

Collections: `spending_groups`, `categories`, `merchants`, `merchant_rules`, and `rules`. Missing collections are empty. Categories are flat expense/income labels; spending groups are independent. Categories may retain a historical `group_name` identity key when exported. Merchant records can have category/group defaults and optional local logos.

Rules specify description `pattern`, `category`, `direction` (`any`, `debit`, `credit`), `priority` and `enabled`. `builtin: true` makes a global fallback rule; otherwise specify an existing `account_name` with editor access. Account rules take precedence over fallback rules. Merchant naming rules specify `merchant` and may use a global or explicit account scope.

Imports merge in the order you explicitly apply them. Identical entries are reused. Duplicate identities within a file reject. Different values for an existing identity appear as replacements and require confirmation, including replacements of local edits. Omitted entries remain; a repository update never silently deletes local configuration. Existing transactions are not rewritten.

See [Sente's full configuration guide](https://github.com/DouwJacobs/sente/blob/main/docs/RULESETS.md) for reference and account mapping. The application guide will be available on main after the portable configuration change is merged.

## Releases

Portable schema versions are independent of application releases. Keep format version 2 until the application supports a deliberate schema upgrade. Tag compatible pack releases and pin tags/commits where reproducibility matters. Update the application's bundled offline snapshot explicitly when shipping a release.
