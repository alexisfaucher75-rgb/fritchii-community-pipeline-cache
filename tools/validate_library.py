# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate this repository's versioned schema and synthetic client-import fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zlib
from pathlib import Path

from generate_synthetic_fixture import synthetic_compute_record

TITLE_ID = "FFFFFFFFFFFFCACE"
UPDATE_VERSION = 0
MAX_COMPRESSED = 64 * 1024 * 1024
MAX_EXPANDED = 256 * 1024 * 1024
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(ValueError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValidationError(reason)


def _safe_relative(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and not value.startswith("/") and
            "\\" not in value and all(part not in {"", ".", ".."} and
                                         re.fullmatch(r"[A-Za-z0-9._-]+", part)
                                         for part in value.split("/")))


def _read_gzip(path: Path, expected_size: int) -> bytes:
    compressed = path.read_bytes()
    require(0 < len(compressed) <= MAX_COMPRESSED, "compressed fixture size is out of bounds")
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = inflater.decompress(compressed, MAX_EXPANDED + 1)
    require(len(expanded) <= MAX_EXPANDED and not inflater.unconsumed_tail,
            "fixture expansion exceeds its bound")
    require(inflater.eof and not inflater.unused_data,
            "fixture gzip stream is truncated or contains trailing data")
    expanded += inflater.flush(MAX_EXPANDED + 1 - len(expanded))
    require(len(expanded) == expected_size <= MAX_EXPANDED,
            "expanded fixture size does not match the manifest")
    return expanded


def _validate_record_stream(data: bytes) -> None:
    # The published fixture is intentionally one small compute record, not a real game's cache.
    require(data == synthetic_compute_record(),
            "record differs from the deterministic synthetic compute fixture")


def validate_package(package: Path, *, expected_hash: bool) -> dict:
    manifest_path = package / "manifests" / TITLE_ID / f"update-{UPDATE_VERSION}.json"
    require(manifest_path.is_file() and not manifest_path.is_symlink(),
            f"missing safe manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid manifest JSON: {error}") from error
    require(isinstance(manifest, dict), "manifest must be a JSON object")
    require(manifest_path.resolve(strict=True).is_relative_to(package.resolve(strict=True)),
            "manifest path escapes the fixture package")
    require(set(manifest) == {"manifest_format", "record_format", "compression", "kind",
                              "game", "producer", "source_cache_version", "total_entries",
                              "chunks"}, "manifest has missing or unknown fields")
    require(type(manifest["manifest_format"]) is int and manifest["manifest_format"] == 3,
            "unsupported manifest format")
    require(type(manifest["record_format"]) is int and manifest["record_format"] == 1,
            "unsupported portable record format")
    require(manifest["compression"] == "gzip" and manifest["kind"] == "snapshot",
            "unsupported compression or package kind")
    game = manifest["game"]
    require(isinstance(game, dict) and set(game) == {"title_id", "edition_id", "update_version"},
            "invalid game identity fields")
    require(game["title_id"] == TITLE_ID and game["edition_id"] == TITLE_ID and
            type(game["update_version"]) is int and game["update_version"] == UPDATE_VERSION,
            "fixture identity does not match the synthetic title/update")
    producer = manifest["producer"]
    require(isinstance(producer, dict) and
            set(producer) == {"emulator_version", "translator_abi"} and
            producer["emulator_version"] == "synthetic-fixture-0.2.0" and
            type(producer["translator_abi"]) is int and producer["translator_abi"] == 1,
            "invalid synthetic producer or translator ABI")
    require(type(manifest["source_cache_version"]) is int and
            manifest["source_cache_version"] in {52, 53, 54},
            "unsupported source cache record layout")
    require(type(manifest["total_entries"]) is int and manifest["total_entries"] == 1,
            "synthetic fixture must contain one record")
    chunks = manifest["chunks"]
    require(isinstance(chunks, list) and len(chunks) == 1,
            "synthetic fixture must contain exactly one chunk")
    chunk = chunks[0]
    require(isinstance(chunk, dict) and set(chunk) == {
        "tag", "file", "compressed_size", "expanded_size", "sha256", "entries"},
        "invalid chunk fields")
    require(_safe_relative(chunk["tag"]) and chunk["tag"].startswith("chunks/" + TITLE_ID + "/"),
            "unsafe or mismatched chunk path")
    require(isinstance(chunk["file"], str) and
            re.fullmatch(r"[A-Za-z0-9._-]+", chunk["file"]) is not None and
            chunk["file"] not in {".", ".."},
            "unsafe chunk file name")
    require(type(chunk["compressed_size"]) is int and
            0 < chunk["compressed_size"] <= MAX_COMPRESSED and
            type(chunk["expanded_size"]) is int and
            0 < chunk["expanded_size"] <= MAX_EXPANDED and
            type(chunk["entries"]) is int and chunk["entries"] == 1,
            "invalid chunk sizes or record count")
    require(isinstance(chunk["sha256"], str) and SHA256.fullmatch(chunk["sha256"]) is not None,
            "invalid chunk SHA-256")
    chunk_path = package.joinpath(*chunk["tag"].split("/"), chunk["file"])
    package_root = package.resolve(strict=True)
    chunk_real = chunk_path.resolve(strict=True)
    require(not chunk_path.is_symlink() and chunk_real.is_relative_to(package_root),
            "chunk path escapes the fixture package")
    compressed = chunk_path.read_bytes()
    require(len(compressed) == chunk["compressed_size"],
            "compressed fixture size does not match the manifest")
    actual_hash = hashlib.sha256(compressed).hexdigest()
    if expected_hash:
        require(actual_hash == chunk["sha256"], "compressed fixture SHA-256 mismatch")
    else:
        require(chunk["sha256"] == "0" * 64 and actual_hash != chunk["sha256"],
                "negative fixture must contain an intentionally incorrect SHA-256")
    expanded = _read_gzip(chunk_path, chunk["expanded_size"])
    _validate_record_stream(expanded)
    return manifest


def validate_repository(root: Path) -> None:
    root = root.resolve(strict=True)
    schema_path = root / "schema" / "manifest-v3.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid versioned schema JSON: {error}") from error
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema" and
            schema.get("title") == "Fritchii community pipeline manifest v3",
            "unexpected manifest schema identity")
    require(schema.get("properties", {}).get("manifest_format", {}).get("const") == 3 and
            schema.get("properties", {}).get("record_format", {}).get("const") == 1,
            "manifest schema constants are out of sync with the fixture")
    require(not (root / "manifests").exists() and not (root / "chunks").exists(),
            "production data is not enabled in this synthetic-only prototype")
    validate_package(root / "fixtures" / "client-import", expected_hash=True)
    validate_package(root / "fixtures" / "client-import-negative-hash", expected_hash=False)
    forbidden = {".nsp", ".nso", ".nca", ".ncz", ".xci", ".tik", ".keys", ".sav",
                 ".save", ".dmp", ".rdc"}
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        require(path.suffix.lower() not in forbidden,
                f"forbidden user/game data file present: {path.relative_to(root)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="library repository root")
    args = parser.parse_args()
    try:
        validate_repository(args.root)
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    print("Library schema and synthetic client-import fixtures are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
