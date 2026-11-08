# Legacy Lichii Shader Sync compatibility

Source supplied for evaluation: <https://github.com/oceanpacificpeace/lichii-shader-sync>.
The source repository describes the tool as unofficial. GitHub has no repository license metadata,
and no license file was found. No upstream code or data is copied into this prototype.

Observed OoT manifest format 1 identifies title `0400486024DEC000`, name
`The Legend of Zelda: Ocarina of Time`, `source_version: 54`, 90,740 total entries, and 64 chunks.
Chunks carry `tag`, `file`, compressed `size`, SHA-256, `entries`, and ordered 32-hex-character
IDs. The gzip payloads are raw serialized emulator records, without a header.

Compatibility gaps:

- No separate edition is stated. Fritchii currently uses the title ID as edition ID. Import requires
  an explicit compatibility attestation selecting that convention; it does not establish a region.
- No game update version or content fingerprint is stated. `source_version` is a cache record
  layout and release dates are pack publication dates. Neither may be used as the game update.
- No source record-format version, producer emulator version, or translator ABI is stated. The
  importer validates actual bytes, requires an attested target translator ABI, labels the source
  producer/ABI as unknown, and records the converter version separately.
- GitHub release downloads redirect to an asset CDN; the current Fritchii client intentionally
  refuses redirects. The legacy asset paths also differ from the Fritchii v3 manifest path.
- Redistribution rights are unconfirmed. The repository has no declared license. Do not publish
  converted data until permission is documented.

The conversion utility accepts staged local files only and requires an attestation bound to the
exact manifest SHA-256, explicit game identity/update evidence, and redistribution evidence. This is
a human review gate and is not a digital signature. See the code-repo
`tools/community_pipeline/UPSTREAM_IMPORT_AUDIT.md` for exact release asset paths and tested hashes.

The source asset root for read-only retrieval is
`https://github.com/oceanpacificpeace/lichii-shader-sync/releases/download`. It is not a Fritchii
app base URL and is not configured in this prototype.
