# Synthetic fixtures only

The checked-in prototype contains no pipeline records. Converter and packer tests create tiny
synthetic records in temporary directories and remove them at the end of each test. The upstream
OoT chunks used for read-only compatibility checks are kept outside this prototype and are not
included in any archive.

