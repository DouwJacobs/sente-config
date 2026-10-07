# Sente configuration

Optional starter categories, spending groups, merchants and rules for [Sente](https://github.com/DouwJacobs/sente). Personal transfers, recipient patterns, account names, financial transactions, credentials and personal logos stay in private files or repositories.

## Choose your packs

| File | Contents |
| --- | --- |
| [sente.json](sente.json) | General starter: 26 categories, seven spending groups, eight merchants, eight naming rules and nine global category fallbacks. |
| [packs/south-africa.json](packs/south-africa.json) | Optional South African merchants and FNB statement rules: 22 merchants, 21 naming rules and five category fallbacks. Includes its eight referenced categories and four spending groups. |
| [packs/detailed-categories.json](packs/detailed-categories.json) | Ten extra categories and four alternative spending groups, without automatic classification. |

Each file imports independently. Combine only the packs you want; shared categories/groups are reused. The starter adds Coffee, Cleaning, Security, Home Loan and Reimbursements to the original categories, and Invest-save-repay and Exceptions to the groups. Gifts received is deliberately omitted from every pack.

The detailed pack offers Birthdays, Building, Garden, Bank notices, Once-off expenses, Online shopping, Tithe & giving, Cash, Savings and Retirement. Communications, Debt, Utilities and Insurance are optional spending groups. Categories are labels: this pack does not automatically treat withdrawals, savings transfers, retirement contributions or repayments as expenses. Classify the actual transaction and use Sente's explicit transfer handling where appropriate.

## Use it

In Sente, open **Settings → Configuration → Pull starter and preview**, inspect the changes, then import. Updates are manual. Sente records the applied commit; it does not stay connected or sync automatically.

For an additional source, use:

- Repository: `https://github.com/DouwJacobs/sente-config.git`
- File: one of the paths in the table above.
- Branch/tag/commit: leave blank for the default branch, or pin a known-compatible tag or commit.

Each optional file is a separate source, even though all files are in this repository. Alternatively, download a JSON file and upload it in Sente. Private repository users can upload their own file. Export your configuration from Sente, edit it, and keep personal patterns private.

## Classification choices

Merchant recognition and categorization are separate. Woolworths, Takealot, Clicks, Engen, Momentum, Amazon, Hertz and other mixed-purpose merchants have no category default. Food-specific Woolworths and Pick n Pay descriptions can receive Groceries from the South African pack. Explicit ChatGPT subscription and SpotifyZA descriptions receive Subscriptions; other OpenAI/Amazon products are not classified as subscriptions.

Restaurant, coffee, pet-shop, parking, ISP and specific insurance descriptions have selected defaults. They are fallbacks, not a substitute for reviewing ambiguous transactions. Local merchant packs and neighbourhood aliases are excluded for location privacy.

The FNB pack includes explicit fee descriptions and directed interest rebates. EFT *charges* are bank fees; personal EFT recipients are excluded. Broad `INTEREST`, `SAVINGS`, `SCHD TRF`, `BYC DEBIT`, generic bank-notice words and account-specific project patterns are deliberately excluded.

No logos are distributed. Merchants and rules have global scope, without account names or identifiers.

## Format

All files use portable format **version 2**. [schema.json](schema.json) helps author files; Sente also validates references, duplicates, permissions and dependencies. Maximum: 32 MiB and 10,000 combined entries. Unknown fields and unsupported versions reject. Do not insert `$schema` in configuration files.

Collections: `spending_groups`, `categories`, `merchants`, `merchant_rules`, and `rules`. Categories are flat expense/income labels; spending groups are independent. The historical `group_name` key is empty here.

Rules specify description `pattern`, `category`, `direction`, `priority` and `enabled`. `builtin: true` makes a global fallback rule. These packs use category priority -1000 and merchant naming priority 100; explicit account category rules take precedence. Regex patterns are parenthesized to preserve alternation in Sente's matcher, and literal asterisks are escaped.

Imports merge in the order you explicitly apply them. Identical entries are reused. Different values for an existing identity appear as replacements and require confirmation, including replacements of local edits. Merchant definitions without defaults clear existing defaults if you confirm their replacement. Omitted entries remain; pulling a pack does not delete an existing Gifts received category or any personal rule. Existing transactions are not rewritten.

See [Sente's full configuration guide](https://github.com/DouwJacobs/sente/blob/main/docs/RULESETS.md) for reference and account mapping. The application guide becomes available on main after the portable configuration change is merged.

## Validation and releases

The packs were checked through Sente's actual preview/apply importer against isolated synthetic databases, both individually and together. Repeat imports produced no configuration changes. Focused matching checks cover subscription literals, Checkers aliases, local payment descriptions and the distinction between EFT charges and personal transfers.

Schema versions are independent of application releases. Tag compatible pack releases and pin tags/commits where reproducibility matters. The existing `v1.0.0` tag retains its original smaller starter; use main for these expanded packs. The application's bundled offline snapshot is refreshed separately when shipping an application release.
