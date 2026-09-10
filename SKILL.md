---
name: prototype-compressor
description: Compress embedded PNG/JPEG images in single-file HTML prototypes. Defaults to WebP quality 78 and a sibling .min.html file; supports explicit source overwrite.
---

# Prototype Compressor

Create a smaller, directly previewable HTML file. Preserve the source by default.

## Use this skill when

- A generated HTML prototype needs a smaller file for sharing or upload.
- A prototype has been updated and its delivery copy needs regeneration.

Do not create an archive or split resources. The skill keeps the prototype as a single offline-previewable HTML file.

## Workflow

1. Identify explicit prototype source files. Accept PC and H5 files, but never use an existing `*.min.html` file as input.
2. Run the bundled script with the source paths:

   ```bash
   python3 scripts/compress_prototype.py /absolute/path/to/PROTO-xxx.html
   ```

   Resolve `scripts/compress_prototype.py` relative to this SKILL.md, or run from the skill directory with an absolute input path. Requires Python 3.10+ and `cwebp` on PATH. No Node.js or npm dependencies are needed.

   By default it writes a sibling file named `PROTO-xxx.min.html`. Re-running refreshes that copy, preserving the source. When the user or the project's integration explicitly requests overwrite, add `--overwrite`: the source HTML becomes the compressed result and no sibling file is created. This mode does not preserve the original image bytes or create a backup.
3. By default, the script converts embedded PNG/JPEG data URIs to WebP at quality 78, but only substitutes a WebP image when it is smaller. SVG data URIs remain unchanged. Use `--webp-quality 90` when visual fidelity takes priority, or `--no-webp` for an unchanged comparison copy.
4. Report each source/output path, byte counts, reduction percentage, and converted-image count.
5. For a newly generated or materially changed prototype, open the reported output file in a browser or perform an equivalent focused preview check before treating it as share-ready.

## Compression boundary

- Preserve HTML/CSS/JavaScript text, comments and whitespace. Only embedded raster image data URIs are replaced; no text minification is performed.
- It converts only embedded PNG/JPEG data URIs. This is lossy at the selected WebP quality; original image bytes remain available only when the source is preserved. SVG data URIs are unchanged.
- It intentionally does not minify JavaScript, resize images, or change external resources.

## Outputs

Default output for every `PROTO-xxx.html` input:

```text
PROTO-xxx.html       # source for future AI changes
PROTO-xxx.min.html   # smaller delivery and preview file
```

When a directory contains both files, upload workflows should select the `.min.html` delivery file deliberately; do not assume a broad `*.html` scan will distinguish them.

With `--overwrite`, the output is `PROTO-xxx.html` itself. Existing sibling copies are not refreshed or deleted in this mode.
