#!/usr/bin/env python3
"""Create conservative .min.html delivery copies of HTML prototypes."""

from __future__ import annotations

import argparse
import base64
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


RASTER_DATA_URI_PATTERN = re.compile(
    r"data:image/(?P<format>png|jpe?g);base64,(?P<payload>[A-Za-z0-9+/=]+)",
    re.IGNORECASE,
)


def data_uri_bytes(content: str) -> int:
    return sum(len(match.group(0).encode("utf-8")) for match in re.finditer(r"data:[^\"'\s>]+", content))


def encode_webp(image: bytes, image_format: str, quality: int, converter: str) -> bytes | None:
    source_path: Path | None = None
    output_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix=f".{image_format}", delete=False) as source_file:
            source_file.write(image)
            source_path = Path(source_file.name)
        output_path = source_path.with_suffix(".webp")
        result = subprocess.run(
            [converter, "-quiet", "-mt", "-m", "6", "-q", str(quality), "-alpha_q", str(quality), "-o", str(output_path), str(source_path)],
            capture_output=True,
            timeout=60,
            check=False,
        )
        if result.returncode != 0 or not output_path.is_file():
            return None
        encoded = output_path.read_bytes()
        return encoded if encoded.startswith(b"RIFF") and encoded[8:12] == b"WEBP" else None
    finally:
        if source_path and source_path.exists():
            source_path.unlink()
        if output_path and output_path.exists():
            output_path.unlink()


def convert_raster_data_uris(content: str, quality: int) -> tuple[str, dict[str, int]]:
    converter = shutil.which("cwebp")
    if not converter:
        raise RuntimeError("cwebp is required to convert embedded PNG/JPEG images to WebP")

    cache: dict[str, str] = {}
    stats = {"seen": 0, "converted": 0, "source_bytes": 0, "webp_bytes": 0}

    def replace(match: re.Match[str]) -> str:
        source_uri = match.group(0)
        stats["seen"] += 1
        if source_uri in cache:
            replacement = cache[source_uri]
            if replacement != source_uri:
                stats["converted"] += 1
                stats["source_bytes"] += len(source_uri.encode("utf-8"))
                stats["webp_bytes"] += len(replacement.encode("utf-8"))
            return replacement

        payload = match.group("payload")
        image = base64.b64decode(payload + "=" * (-len(payload) % 4))
        webp = encode_webp(image, match.group("format").lower(), quality, converter)
        replacement = source_uri
        if webp and len(webp) < len(image):
            replacement = f"data:image/webp;base64,{base64.b64encode(webp).decode('ascii')}"
        cache[source_uri] = replacement
        if replacement != source_uri:
            stats["converted"] += 1
            stats["source_bytes"] += len(source_uri.encode("utf-8"))
            stats["webp_bytes"] += len(replacement.encode("utf-8"))
        return replacement

    return RASTER_DATA_URI_PATTERN.sub(replace, content), stats


def output_path(source: Path) -> Path:
    return source.with_name(f"{source.stem}.min{source.suffix}")


def compress(source: Path, webp_quality: int | None, overwrite: bool = False) -> None:
    if source.suffix.lower() != ".html":
        raise ValueError("only .html prototype files are supported")
    if ".min" in source.stem:
        raise ValueError("refusing to recompress an existing .min.html delivery file")

    original = source.read_bytes().decode("utf-8")
    compressed = original
    image_stats = None
    if webp_quality is not None:
        compressed, image_stats = convert_raster_data_uris(compressed, webp_quality)
    destination = source if overwrite else output_path(source)
    destination.write_bytes(compressed.encode("utf-8"))

    before = len(original.encode("utf-8"))
    after = len(compressed.encode("utf-8"))
    reduction = 0 if before == 0 else (before - after) / before * 100
    data_bytes = data_uri_bytes(original)
    print(f"source: {source}")
    print(f"output: {destination}")
    print(f"overwrite source: {overwrite}")
    print(f"size: {before} B -> {after} B ({reduction:.1f}% smaller)")
    if image_stats:
        print(
            "webp: "
            f"{image_stats['converted']}/{image_stats['seen']} raster data URIs converted "
            f"at quality {webp_quality}"
        )
        if image_stats["converted"]:
            image_reduction = 1 - image_stats["webp_bytes"] / image_stats["source_bytes"]
            print(f"converted image data: {image_reduction * 100:.1f}% smaller")
    if data_bytes:
        print(f"inline data URIs: {data_bytes} B ({data_bytes / before * 100:.1f}% of source)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path, help="prototype .html files to compress")
    parser.add_argument(
        "--webp-quality",
        type=int,
        default=78,
        help="WebP quality for embedded PNG/JPEG images (0-100; default: 78)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite the source HTML instead of writing a sibling .min.html (default: false)",
    )
    parser.add_argument(
        "--no-webp",
        action="store_true",
        help="copy the original without image conversion for comparison",
    )
    args = parser.parse_args()
    if not 0 <= args.webp_quality <= 100:
        parser.error("--webp-quality must be between 0 and 100")

    for source in args.sources:
        if not source.is_file():
            parser.error(f"source file does not exist: {source}")
        try:
            compress(
                source,
                None if args.no_webp else args.webp_quality,
                args.overwrite,
            )
        except (RuntimeError, ValueError) as error:
            parser.error(f"{source}: {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
