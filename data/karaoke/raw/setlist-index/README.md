# Local-only Setlist Index snapshots

The original Setlist Index HTML is downloaded and processed locally. It is intentionally not uploaded to GitHub.

Local workflow:

1. Download the page to a local path such as data/karaoke/raw/setlist-index/latest.html.
2. Run the importer with that local file.
3. Upload only generated candidate or normalized JSON plus source metadata.
4. Keep the local HTML ignored by Git.

The importer records the source URL, retrieval time, local filename, SHA-256, parser version, and record counts in data/karaoke/source-metadata/setlist-index.json.
