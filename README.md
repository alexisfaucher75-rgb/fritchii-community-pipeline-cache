# Fritchii Community Pipeline Library

This public repository is the data-library scaffold for Fritchii. Emulator source and builds belong
in a separate repository.

## Current status

This repository contains documentation, the Fritchii manifest schema, and a tiny synthetic fixture
for exercising the client's import path. **It does not contain an OoT pack, accept uploads, or
provide a production download endpoint.** The Ocarina of Time records from Lichii Shader Sync were
inspected but are not included: the upstream repository has no declared license, and its manifest
does not identify the game update needed to establish compatibility.

Do not configure this repository as Fritchii's community source for a game. The checked-in fixture
uses the deliberately fake title `FFFFFFFFFFFFCACE`, contains one synthetic compute record, and is
only for the developer import probe. It does not establish OoT compatibility or test Vulkan pipeline
creation. Production packs need reviewed game edition/update metadata, record provenance, rights,
publisher authentication, moderation, and a release process.

## Format and scope

The library is intended to distribute portable emulator pipeline records, never GPU-specific
`VkPipeline` objects or Vulkan driver-cache blobs. Each user's computer validates the records and
rebuilds pipelines with its own GPU and driver.

The current Fritchii runtime uses a manually configured version-3 snapshot library. The schema is
in `schema/manifest-v3.schema.json`. Unknown schemas, game identities, record formats, and
translator ABIs must be rejected or migrated explicitly.

## Repository contents

- `schema/manifest-v3.schema.json`: the proposed snapshot manifest schema.
- `POLICY.md`: draft contribution, provenance, and privacy requirements.
- `RELEASE-POLICY.md`: draft release, integrity, signatures, and rollback plan.
- `UPSTREAM-COMPATIBILITY.md`: observed upstream format and unresolved import gates.
- `fixtures/client-import/`: synthetic snapshot exposed at the direct raw-content route expected by
  the client.
- `fixtures/client-import-negative-hash/`: the same synthetic content with an intentionally wrong
  declared SHA-256, for testing rejection and preservation of an existing cache.
- `tools/`: deterministic fixture generation and validation; these scripts are GPL-3.0-or-later as
  marked in their file headers. This does not license any pipeline records.
- `.github/workflows/validate.yml`: CI validation of the schema identity, fixture fields, sizes,
  hashes, gzip stream, deterministic generation, and record structure.

## Contributions and licensing

Uploads and contributions are not enabled. Do not submit game images, saves, keys, profiles, logs,
GPU driver caches, or other user data. The repository does not yet grant a license for pipeline
records; no third-party records may be redistributed until their rights and provenance are
documented. The contribution and release policies are drafts, not an operational service.

The project needs an explicit data license, compatibility attestation, signed release process,
moderation/removal rules, and automated validation before accepting or distributing real records.
The synthetic fixture's versioned raw-content base URL is documented in `fixtures/README.md`; it is
for tests only and is not an approved source for game data.

## Reproduce the synthetic checks

From a clean checkout, run:

```sh
python tools/validate_library.py --root .
python -m unittest discover -s tests -v
python tools/generate_synthetic_fixture.py --check-against fixtures
```

These checks validate the checked-in fixture and its direct endpoint layout. The separate Fritchii
source-tree probe exercises the C++ downloader against the pinned valid and negative-hash URLs in
`fixtures/README.md`; it is an opt-in developer test and does not require a game or Vulkan device.

