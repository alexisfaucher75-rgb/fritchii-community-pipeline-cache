# Fritchii Community Pipeline Library

This public repository is the data-library scaffold for Fritchii. Emulator source and builds belong
in a separate repository.

## Current status

This repository currently contains documentation and the Fritchii manifest schema only. **It does
not yet contain a usable shader/pipeline pack, accept uploads, or provide a production download
endpoint.** The Ocarina of Time records from Lichii Shader Sync were inspected but are not included:
the upstream repository has no declared license, and its manifest does not identify the game update
needed to establish compatibility.

Do not configure this repository as Fritchii's community source yet. The shipped client expects a
version-3 Fritchii snapshot manifest at a specific endpoint layout; publishing the files here does
not by itself make that endpoint available or compatible.

## Format and scope

The library is intended to distribute portable emulator pipeline records, never GPU-specific
`VkPipeline` objects or Vulkan driver-cache blobs. Each user's computer validates the records and
rebuilds pipelines with its own GPU and driver.

The current Fritchii runtime uses a manually configured version-3 snapshot library. The schema is
in `schema/manifest-v3.schema.json`. Unknown schemas, game identities, record formats, and
translator ABIs must be rejected or migrated explicitly.

## Repository contents

## Contents

- `schema/manifest-v3.schema.json`: the proposed snapshot manifest schema.
- `POLICY.md`: draft contribution, provenance, and privacy requirements.
- `RELEASE-POLICY.md`: draft release, integrity, signatures, and rollback plan.
- `UPSTREAM-COMPATIBILITY.md`: observed upstream format and unresolved import gates.
- `fixtures/README.md`: synthetic-only fixture policy.

## Contributions and licensing

Uploads and contributions are not enabled. Do not submit game images, saves, keys, profiles, logs,
GPU driver caches, or other user data. The repository does not yet grant a license for pipeline
records; no third-party records may be redistributed until their rights and provenance are
documented. The contribution and release policies are drafts, not an operational service.

The project needs an explicit data license, compatibility attestation, signed release process,
moderation/removal rules, and automated validation before accepting or distributing real records.

