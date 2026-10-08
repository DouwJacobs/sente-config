# Contributing to Sente Config

Help people recognize merchants and classify transactions with optional, reusable packs. You can suggest a merchant or category in an issue, or fork this repository and open a pull request. No repository write access is needed. The maintainer is @DouwJacobs.

## Prepare a contribution

1. Search `sente.json` and `packs/*.json` for an existing name or alias. Extend an existing entry instead of adding another spelling of the same merchant.
2. Choose the smallest relevant pack: the starter for broad use, `south-africa.json` for South African merchants and FNB descriptions, or `detailed-categories.json` for optional labels. Propose new regional packs in an issue first.
3. Include all categories, groups and merchants referenced by your pack so it imports independently. Repeated definitions across packs must agree exactly.
4. Add synthetic positive and negative examples in `tests/matching.json` for every naming/category pattern you add or change. Never copy an unredacted transaction or statement into a test, issue, commit or pull request.
5. Run the checks below, update README pack counts/behavior, and open a focused pull request describing the public business, country, aliases, and classification reasoning. Explain any replacement of existing defaults.

## Public data only

Publish recognizable business names and reusable merchant tokens. Remove customer IDs, account names/numbers, policy numbers, invoice references, addresses identifying a customer, balances, dates and amounts from statement examples. Never include real statements, transactions, private people/recipients, credentials, exported timestamps, account-specific scope or logos. If a business cannot be distinguished from a private recipient, leave it out until public evidence resolves the ambiguity.

Public business names can still reveal a contributor's location or habits. Do not share neighborhood associations, nearby contractors or other location-sensitive merchants from a private catalogue without explicit contributor consent. Respect exclusions even when a business is publicly listed.

Use a public business website as evidence where available. A neutral business name can be included without a rule; do not guess a bank descriptor. Payment processors such as Yoco and PayFast identify many businesses: match a specific business token, never the processor alone.

## Merchant recognition and defaults

Naming rules identify a business; category rules classify spending. Keep them separate. Use the recognized public trading name and global scope (omit `account_name` and `merchant_account_name`). Omit `logo_data`.

Mixed retailers, banks, insurers with multiple products, investment providers and other ambiguous merchants should have no category or spending-group default. A person's past classification does not establish a community default. Prefer narrowly identified products, such as a subscription descriptor, when adding category fallbacks. Credits and refunds may differ from purchases: use explicit `debit` or `credit`, not `any`, for new rules.

## Pattern format

Sente uses case-insensitive matching, normalizes whitespace, and supports Go regular expressions plus literal contains/alias matching. Regexes containing alternation must be wrapped in parentheses (or anchored) so Sente does not interpret the branches as literal aliases. Escape literal asterisks: `(PAYFAST\*Example Store)`. Use word boundaries where they reduce false positives. Avoid lookarounds and backreferences, which Go's regexp engine does not support.

A recognition-only pack entry looks like this (JSON escapes each backslash):

```json
{
  "version": 2,
  "merchants": [{"name": "Example Store"}],
  "merchant_rules": [{
    "merchant": "Example Store",
    "pattern": "(\\bEXAMPLE STORE\\b)",
    "direction": "debit",
    "priority": 100,
    "enabled": true
  }]
}
```

Add a fixture identifying that exact file/pattern/target in `tests/matching.json`, such as positive `PURCH EXAMPLE STORE` and negative `PURCH EXAMPLE STORES`.

Use naming priority `100`. Use global category fallback priority `-1000` with `builtin: true`. Explain exceptions before changing precedence. Enabled patterns must not be empty, generic bank words, personal transfer recipients, or processor-only matches. Include at least one positive and one near-miss negative synthetic description for every pattern; test literal symbols, truncations or aliases you claim to recognize.

## Categories and spending groups

Categories are flat labels with `kind: expense` or `income`; `group_name` and `category_group_name` stay empty. Reuse a category before proposing one. New categories should be broadly understandable, distinct from existing labels, and described in the pull request. Spending groups are independent labels with one of the schema's supported colors; they are not category parents.

Cash withdrawals, savings moves, retirement contributions and repayments are not automatically expenses. Use Sente's explicit transfer handling when applicable. Do not add automatic classification merely because the optional pack offers those labels. Preserve the existing deliberate exclusion of Gifts received unless maintainers explicitly reconsider it.

## Local validation

Use Python 3.11+ and Go 1.23+:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
GOTOOLCHAIN=local go test ./...
```

The validator checks the JSON schema, public-only fields, duplicate identities, references, pack independence, shared-definition consistency and entry limits. Go checks use a documented copy of Sente's matcher and synthetic examples. These checks cannot prove privacy, ownership of names, semantic classification correctness or full importer compatibility: maintainers still review those.

For importer changes or complicated replacements, verify preview/apply and repeat-import behavior in Sente with an isolated synthetic database before merging. No changes here should require access to a contributor's real financial database.

## Review and licensing

Community contributions need a maintainer review, resolved conversations and passing validation before merging. Do not request write access just to contribute. See [MAINTAINING.md](MAINTAINING.md) for repository controls. By contributing, you agree to license your contribution under GPL-3.0-only and confirm that you have the right to submit it. Existing upstream notices must be preserved.

Be respectful, discuss the rule rather than the person, and help newcomers improve their examples. Report accidental sensitive-data disclosure through the private route in [SECURITY.md](SECURITY.md).
