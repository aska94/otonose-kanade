# Source metadata

This directory stores provenance for locally downloaded source files without storing the source files themselves.

Metadata should include:

- source URL
- retrieval timestamp
- local filename
- SHA-256 checksum
- parser version
- imported broadcast and performance counts
- rawFileUploaded set to false

## Daily web extraction

The daily ChatGPT check may update this metadata using structured observations from the public Setlist Index page. It must record extraction mode and comparison summary. It must not upload the original source HTML.
