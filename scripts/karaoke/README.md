# Karaoke scripts

The local pipeline downloads Setlist Index outside GitHub Actions, processes the local HTML, and uploads generated data only.

From the repository root:

    python scripts/karaoke/import_setlist_index.py --input data/karaoke/raw/setlist-index/latest.html
    python scripts/karaoke/normalize_setlist_index.py
    python scripts/karaoke/build_stats.py
    python scripts/validate_karaoke.py

The importer writes candidate JSON and source metadata. The original HTML remains local and is ignored by Git. GitHub Actions validates committed JSON and rebuilds statistics and playlist manifests.
