"""Validate independently importable public Sente packs (GPL-3.0-only)."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ("spending_groups", "categories", "merchants", "merchant_rules", "rules")
PRIVATE_FIELDS = {"exported_at", "account_name", "merchant_account_name", "logo_data"}


def read_json(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def identity(collection, item):
    if collection == "categories":
        return (item["name"].strip().casefold(), item["kind"])
    if collection in ("merchants", "spending_groups"):
        return item["name"].strip().casefold()
    return (item["pattern"].strip().casefold(), item.get("direction", "any"))


def check_pack(data, schema):
    errors = [f"schema {'.'.join(map(str, e.path))}: {e.message}"
              for e in Draft202012Validator(schema).iter_errors(data)]
    if errors:
        return errors
    if "exported_at" in data:
        errors.append("public packs must omit exported_at")
    if sum(len(data.get(key) or []) for key in COLLECTIONS) > 10000:
        errors.append("more than 10,000 combined entries")
    for collection in COLLECTIONS:
        seen = set()
        for item in data.get(collection) or []:
            key = identity(collection, item)
            if key in seen:
                errors.append(f"duplicate {collection} identity: {key}")
            seen.add(key)
            for field in PRIVATE_FIELDS & item.keys():
                errors.append(f"{collection}: public packs must omit {field}")
            for field in ("group_name", "category_group_name"):
                if item.get(field):
                    errors.append(f"{collection}: {field} must be empty")
            if collection == "categories" and item.get("spending_group"):
                errors.append("categories must not imply a spending group")
            if "name" in item and item["name"] != item["name"].strip():
                errors.append(f"{collection}: trim names")
            if collection in ("rules", "merchant_rules"):
                if item.get("direction") not in ("debit", "credit"):
                    errors.append(f"{collection}: explicit debit/credit direction required")
                expected = -1000 if collection == "rules" else 100
                if item.get("priority") != expected:
                    errors.append(f"{collection}: expected priority {expected}")
                if collection == "rules" and item.get("builtin") is not True:
                    errors.append("category rules must be global built-in fallbacks")
    categories = {x["name"] for x in data.get("categories") or []}
    groups = {x["name"] for x in data.get("spending_groups") or []}
    merchants = {x["name"] for x in data.get("merchants") or []}
    for collection in COLLECTIONS:
        for item in data.get(collection) or []:
            for field, names in (("category", categories), ("spending_group", groups),
                                 ("merchant", merchants)):
                if item.get(field) and item[field] not in names:
                    errors.append(f"{collection}: unresolved {field}: {item[field]}")
    return errors


def validate(root=ROOT):
    schema = read_json(root / "schema.json")
    Draft202012Validator.check_schema(schema)
    paths = [root / "sente.json", *sorted((root / "packs").glob("*.json"))]
    shared = {}
    errors = []
    for path in paths:
        label = str(path.relative_to(root))
        if path.stat().st_size > 32 * 1024 * 1024:
            errors.append(f"{label}: exceeds 32 MiB")
            continue
        try:
            data = read_json(path)
            problems = check_pack(data, schema)
            errors.extend(f"{label}: {problem}" for problem in problems)
            if problems:
                continue
            for collection in COLLECTIONS:
                for item in data.get(collection) or []:
                    key = (collection, identity(collection, item))
                    if key in shared and shared[key] != item:
                        errors.append(f"{label}: conflicting shared definition {key}")
                    shared[key] = item
        except (ValueError, OSError) as error:
            errors.append(f"{label}: {error}")
    return paths, errors


if __name__ == "__main__":
    paths, errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"Validated {len(paths)} independent public packs.")
