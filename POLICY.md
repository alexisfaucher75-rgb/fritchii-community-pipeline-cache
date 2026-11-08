# Record contribution and privacy policy draft

This draft is not an operational upload workflow. The app currently has no contribution feature,
and no record is sent anywhere.

Before any future submission, the user must explicitly choose **Participate in the community
effort**, see the exact eligible record count and metadata, and confirm each submission action.
Consent must be revocable, and declining or withdrawing must not affect local cache use.

Eligible content may include only validated portable emulator records: serialized shader
environments and pipeline keys. Never collect or transmit game images (NUP/ROM), save data, title
keys, console keys, user profiles, filesystem paths, logs containing private data, Vulkan driver
cache blobs, or `VkPipeline` objects.

Every proposed record needs source build, game title/edition/update, record-format/translator ABI,
provenance, duplicate screening, privacy review, and rights review. Submissions need automated
parsing and size limits, malware/content review for attached files, human moderation, a removal
process, and an abuse-report channel. This prototype does not implement these services.
