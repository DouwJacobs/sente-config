"""Synthetic checks for contribution validation boundaries."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.schema = validator.read_json(ROOT / "schema.json")
        self.pack = {"version": 2, "merchants": [{"name": "Example Store"}],
                     "merchant_rules": [{"merchant": "Example Store",
                         "pattern": "Example Store", "direction": "debit",
                         "priority": 100, "enabled": True}]}

    def test_valid_independent_pack(self):
        self.assertEqual(validator.check_pack(self.pack, self.schema), [])

    def test_reject_private_fields_even_if_portable_schema_allows_them(self):
        for field in ("account_name", "logo_data"):
            with self.subTest(field=field):
                pack = copy.deepcopy(self.pack)
                pack["merchants"][0][field] = "private"
                self.assertTrue(validator.check_pack(pack, self.schema))

    def test_missing_reference(self):
        self.pack["merchant_rules"][0]["merchant"] = "Missing"
        self.assertTrue(validator.check_pack(self.pack, self.schema))

    def test_duplicate_identity(self):
        self.pack["merchants"].append({"name": "example store"})
        self.assertTrue(validator.check_pack(self.pack, self.schema))

    def test_unknown_financial_data(self):
        self.pack["transactions"] = [{"amount": 100}]
        self.assertTrue(validator.check_pack(self.pack, self.schema))

    def test_direction_required(self):
        self.pack["merchant_rules"][0]["direction"] = "any"
        self.assertTrue(validator.check_pack(self.pack, self.schema))

    def test_duplicate_json_keys(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pack.json"
            path.write_text('{"version":2,"version":1}')
            with self.assertRaises(ValueError):
                validator.read_json(path)

    def test_conflicting_shared_definitions(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packs").mkdir()
            (root / "schema.json").write_text((ROOT / "schema.json").read_text())
            (root / "sente.json").write_text(json.dumps(self.pack))
            changed = copy.deepcopy(self.pack)
            changed["merchants"][0]["category"] = "Groceries"
            changed["categories"] = [{"name": "Groceries", "kind": "expense"}]
            (root / "packs/other.json").write_text(json.dumps(changed))
            self.assertTrue(validator.validate(root)[1])
