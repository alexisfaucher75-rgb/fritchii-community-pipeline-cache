# SPDX-License-Identifier: GPL-3.0-or-later

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import validate_library


ROOT = Path(__file__).resolve().parents[1]


class SyntheticLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "fixtures", self.root / "fixtures")

    def tearDown(self):
        self.temporary.cleanup()

    def _package(self, name="client-import"):
        return self.root / "fixtures" / name

    def _manifest_path(self, name="client-import"):
        return self._package(name) / "manifests" / validate_library.TITLE_ID / "update-0.json"

    def test_valid_and_negative_hash_fixtures_are_distinguished(self):
        validate_library.validate_package(self._package(), expected_hash=True)
        validate_library.validate_package(
            self._package("client-import-negative-hash"), expected_hash=False)
        with self.assertRaisesRegex(validate_library.ValidationError, "SHA-256 mismatch"):
            validate_library.validate_package(
                self._package("client-import-negative-hash"), expected_hash=True)

    def test_unknown_schema_and_identity_are_rejected(self):
        path = self._manifest_path()
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["manifest_format"] = 99
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(validate_library.ValidationError, "unsupported manifest"):
            validate_library.validate_package(self._package(), expected_hash=True)

        manifest["manifest_format"] = 3
        manifest["game"]["update_version"] = 7
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(validate_library.ValidationError, "synthetic title/update"):
            validate_library.validate_package(self._package(), expected_hash=True)

    def test_unsafe_paths_and_wrong_sizes_are_rejected(self):
        path = self._manifest_path()
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["chunks"][0]["tag"] = "chunks/../outside"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(validate_library.ValidationError, "unsafe or mismatched"):
            validate_library.validate_package(self._package(), expected_hash=True)

        manifest["chunks"][0]["tag"] = f"chunks/{validate_library.TITLE_ID}/update-0"
        manifest["chunks"][0]["compressed_size"] += 1
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(validate_library.ValidationError, "compressed fixture size"):
            validate_library.validate_package(self._package(), expected_hash=True)


if __name__ == "__main__":
    unittest.main()
