---
name: prototype-compressor
description: Compress generated single-file HTML prototypes into sibling .min.html delivery files while preserving the original for later AI revisions. Use after generating or updating PROTO HTML files, before sharing or uploading them for preview.
---

# Prototype Compressor

Create a smaller, directly previewable HTML file without changing the source prototype.

## Use this skill when

- A generated HTML prototype needs a smaller file for sharing or upload.
- A prototype has been updated and its delivery copy needs regeneration.

Do not use it to create an archive, split resources, or replace the original prototype. The skill keeps the prototype as a single offline-previewable HTML file.

## Workflow

1. Identify explicit prototype source files. Accept PC and H5 files, but never use an existing `*.min.html` file as input.
2. Run the bundled script with the source paths:

   ```bash
   python3 scripts/compress_prototype.py /absolute/path/to/PROTO-xxx.html
   ```

   Resolve `scripts/compress_prototype.py` relative to this SKILL.md, or run from the skill directory with an absolute input path. Requires Python 3.10+ and `cwebp` on PATH. No Node.js or npm dependencies are needed.

   It writes a sibling file named `PROTO-xxx.min.html`. Re-running refreshes that delivery copy and never changes the source file.
3. By default, the script converts embedded PNG/JPEG data URIs to WebP at quality 80, but only substitutes a WebP image when it is smaller. SVG data URIs remain unchanged. Use `--webp-quality 90` when visual fidelity takes priority, or `--no-webp` for an unchanged comparison copy.
4. Report each source/output path, byte counts, reduction percentage, and converted-image count.
5. For a newly generated or materially changed prototype, open the `.min.html` in a browser or perform an equivalent focused preview check before treating it as share-ready.

## Compression boundary

- Preserve HTML/CSS/JavaScript text, comments and whitespace. Only embedded raster image data URIs are replaced; no text minification is performed.
- It converts only embedded PNG/JPEG data URIs. This is lossy at the selected WebP quality; source images and SVG data URIs remain unchanged in the original prototype.
- It intentionally does not minify JavaScript, resize images, or change external resources.

## Outputs

For every `PROTO-xxx.html` input:

```text
PROTO-xxx.html       # source for future AI changes
PROTO-xxx.min.html   # smaller delivery and preview file
```

When a directory contains both files, upload workflows should select the `.min.html` delivery file deliberately; do not assume a broad `*.html` scan will distinguish them.
