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

The upstream OoT chunks used for read-only compatibility checks are kept outside this repository.
No game image, save, key, profile, real cache record, `VkPipeline`, or Vulkan driver-cache blob is
included.

