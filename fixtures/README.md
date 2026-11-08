# Synthetic client-import fixtures only

The fixtures use the deliberately fake title and edition `FFFFFFFFFFFFCACE`, update `0`, a
synthetic producer identifier, translator ABI `1`, and source cache-record version `52`. The valid
fixture has one deterministic, structurally valid synthetic compute record. It is meant only for
testing the Fritchii downloader's manifest/chunk validation and transactional cache write; it is not
an OoT pack, does not prove game compatibility, and is not expected to produce a usable Vulkan
pipeline on a real GPU.

For the source-controlled C++ import probe, use these direct raw-content bases:

```text
https://raw.githubusercontent.com/alexisfaucher75-rgb/fritchii-community-pipeline-cache/main/fixtures/client-import
https://raw.githubusercontent.com/alexisfaucher75-rgb/fritchii-community-pipeline-cache/main/fixtures/client-import-negative-hash
```

The first serves the valid fixture. The second serves the same tiny chunk with a deliberately
incorrect manifest SHA-256. The probe must accept the first, reject the second, and confirm the
already-installed synthetic cache file is unchanged. These are test routes, not a production
library source. The app has no default URL and no test route is configured in either build.

The valid manifest declares one entry, one 52-byte compressed chunk, and 120 expanded bytes. Its
chunk SHA-256 is
`deb2583fe8d13ede4456577734c1e4dad2e7aadc800bbe22490ff15a84013888`. The negative manifest keeps
the same bytes and counts but declares 64 zeroes as its digest.

From the repository root, reproduce the library checks with:

```sh
python tools/validate_library.py --root .
python -m unittest discover -s tests -v
python tools/generate_synthetic_fixture.py --check-against fixtures
```

The C++ probe accepts the two fixture bases followed by a new or empty temporary shader directory:

```text
community_pipeline_cache_import_probe <valid-base-url> <negative-hash-base-url> <empty-shader-directory>
```

Its CMake option and full build invocation are documented in the Fritchii source tree at
`tools/community_pipeline/README.md`.

The upstream OoT chunks used for read-only compatibility checks are kept outside this repository.
No game image, save, key, profile, real cache record, `VkPipeline`, or Vulkan driver-cache blob is
included.

