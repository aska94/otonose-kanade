# Karaoke scripts

Planned scripts:

- import Setlist Index snapshots
- normalize and deduplicate records
- calculate yearly and frequency statistics
- build the dashboard
- generate playlist manifests
- validate source and normalized data

Scripts should be deterministic and report unresolved records instead of silently dropping them.

## Local pipeline

From the repository root:

    python scripts/karaoke/import_setlist_index.py
    python scripts/karaoke/normalize_setlist_index.py
    python scripts/karaoke/build_stats.py
    python scripts/validate_karaoke.py

The importer writes raw snapshots and candidate records. Normalization preserves source labels and does not invent artists or original-song mappings.
