# Synthetic matching fixtures

`matching.json` refers to actual pack patterns by file, collection and pattern, plus the intended merchant/category target. Every published pattern must have at least one positive and one negative synthetic description. Use near misses and competing processors/products, not real statement rows. The schema validator requires explicit debit/credit directions.

The Go matcher is a snapshot of Sente commit `f651682074486a4a030472e89f7783a8251ee6cc`, `internal/classification/patterns.go`, plus `Normalize` from `rules.go`, copied without changing matching semantics. It preserves Go regexp behavior, case/whitespace normalization and the literal-contains fallback. This is a matching regression check, not an import/apply test. Refresh deliberately when upstream semantics change.

## Initial community setup verification (8 October 2026)

The three retained packs passed schema/public-field/reference/consistency validation, eight synthetic validator tests, and matching checks for all 43 published patterns. An isolated Go test overlay against the Sente workspace also passed actual preview/apply checks for each independent pack, combined imports, repeat-import idempotency and preservation of mixed-merchant defaults. No application source, MCP tools, permissions, live financial records or database migrations were changed. The ongoing repository CI covers structural validation and matching; importer verification remains a separate Sente integration check.
