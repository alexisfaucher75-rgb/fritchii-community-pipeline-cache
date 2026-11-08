# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate deterministic, test-only Fritchii client-import fixtures."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tempfile
from pathlib import Path

TITLE_ID = "FFFFFFFFFFFFCACE"  # Synthetic ID. This is not an OoT title or edition.
UPDATE_VERSION = 0
SOURCE_CACHE_VERSION = 52
RECORD_FORMAT = 1
TRANSLATOR_ABI = 1
EMULATOR_VERSION = "synthetic-fixture-0.2.0"


def synthetic_compute_record() -> bytes:
    environment = bytearray(0x4C + 16)
    environment[0x48:0x4C] = (5).to_bytes(4, "little")
    key = bytes((index * 17 + 3) & 0xFF for index in range(24))
    return (1).to_bytes(4, "little") + environment + key


def deterministic_gzip(data: bytes) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(fileobj=output, mode="wb", compresslevel=9, mtime=0) as stream:
        stream.write(data)
    return output.getvalue()


def write_package(root: Path, *, negative_hash: bool) -> None:
    record = synthetic_compute_record()
    compressed = deterministic_gzip(record)
    digest = hashlib.sha256(compressed).hexdigest()
    tag = f"chunks/{TITLE_ID}/update-{UPDATE_VERSION}"
    filename = f"chunk-00000-{digest[:16]}.bin.gz"
    manifest = {
        "manifest_format": 3,
        "record_format": RECORD_FORMAT,
        "compression": "gzip",
        "kind": "snapshot",
        "game": {
            "title_id": TITLE_ID,
            "edition_id": TITLE_ID,
            "update_version": UPDATE_VERSION,
        },
        "producer": {
            "emulator_version": EMULATOR_VERSION,
            "translator_abi": TRANSLATOR_ABI,
        },
        "source_cache_version": SOURCE_CACHE_VERSION,
        "total_entries": 1,
        "chunks": [
            {
                "tag": tag,
                "file": filename,
                "compressed_size": len(compressed),
                "expanded_size": len(record),
                "sha256": "0" * 64 if negative_hash else digest,
                "entries": 1,
            }
        ],
    }
    manifest_path = root / "manifests" / TITLE_ID / f"update-{UPDATE_VERSION}.json"
    chunk_path = root.joinpath(*tag.split("/"), filename)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    chunk_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8", newline="\n")
    chunk_path.write_bytes(compressed)


def file_map(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file() and path.name != "README.md"}


def generate(output: Path) -> None:
    output = output.resolve()
    package_names = ("client-import", "client-import-negative-hash")
    if any((output / name).exists() for name in package_names):
        raise FileExistsError(f"a synthetic fixture package already exists under: {output}")
    output.mkdir(parents=True, exist_ok=True)
    write_package(output / "client-import", negative_hash=False)
    write_package(output / "client-import-negative-hash", negative_hash=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="new directory for the two generated fixtures; it must be empty")
    parser.add_argument("--check-against", type=Path,
                        help="compare deterministic output with this checked-in fixtures directory")
    args = parser.parse_args()
    if (args.output is None) == (args.check_against is None):
        parser.error("choose exactly one of --output or --check-against")
    if args.output is not None:
        generate(args.output)
        print(f"Generated synthetic fixtures under {args.output}")
        return 0

    with tempfile.TemporaryDirectory(prefix="fritchii-fixtures-") as temporary:
        generated = Path(temporary) / "fixtures"
        generate(generated)
        expected = file_map(generated)
        checked_in = file_map(args.check_against)
        if expected != checked_in:
            missing = sorted(set(expected) - set(checked_in))
            unexpected = sorted(set(checked_in) - set(expected))
            changed = sorted(path for path in set(expected) & set(checked_in)
                             if expected[path] != checked_in[path])
            details = []
            if missing:
                details.append(f"missing: {missing}")
            if unexpected:
                details.append(f"unexpected: {unexpected}")
            if changed:
                details.append(f"changed: {changed}")
            raise SystemExit("synthetic fixtures are not reproducible (" + "; ".join(details) + ")")
    print("Checked-in synthetic fixtures match deterministic output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
