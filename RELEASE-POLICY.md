# Community library release policy draft

This is a design target, not an implemented updater or publisher.

## Separate identities

- Emulator release: fork version, platform, build hash, and signed release metadata.
- Game records: exact title ID, edition ID, and installed update version.
- Community format: manifest schema, portable record format, producer provenance, and translator
  ABI. Unknown versions are migrated explicitly or rejected.
- Local Vulkan cache: GPU, driver, device features, and rebuilt local pipelines. No driver cache
  bytes or Vulkan handles are released.

## Immutable content and reversible activation

Chunks should be immutable and named by a cryptographic digest. A signed manifest identifies the
game/update and format, lists chunk hashes, compressed/expanded sizes and entry counts, and points
to either a full snapshot or a delta whose base digest is explicit. Upload chunks first; validate
the complete candidate snapshot; sign the manifest and monotonic release metadata; publish the
manifest pointer last. Consumers verify signature, trust-key status, hash, size, schema, identity,
and rollback policy, stage locally, then atomically switch the active snapshot while retaining the
previous one for rollback.

Use an offline root key with documented rotation/revocation and a pinned trust policy in signed
application releases. TLS and SHA-256 alone do not authenticate a publisher. Emulator self-update
must use its own signed release channel and reversible installation transaction; it is separate
from game updates and community record versions.

## Governance before publishing

Choose an owner and license; publish provenance and compatibility evidence; define moderation,
privacy, retention, deletion, and incident response; add CI that rejects malformed and oversized
records; and review all changes before signing. Never accept an arbitrary user upload directly into
the active library. The future upload path requires explicit per-user consent and the exclusions in
`POLICY.md`.
