#!/usr/bin/env python3
"""Build the Free Sitter Info Pack: HTML/CSS sheets in, unbranded PDFs out.

Run:  python3 build.py            (rebuilds printables/)
      python3 build.py --out DIR  (builds into a custom directory, e.g. for tests)
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEETS = ROOT / "sheets"

DOCS = [
    {
        "name": "babysitter-packet.pdf",
        "sources": ("intro-babysitting.html", "babysitter.html"),
        "pages": 2,
    },
    {
        "name": "pet-sitter-packet.pdf",
        "sources": ("intro-pet-sitter.html", "pet-sitter.html"),
        "pages": 2,
    },
    {
        "name": "house-sitter-packet.pdf",
        "sources": ("intro-house-sitter.html", "house-sitter.html"),
        "pages": 2,
    },
    {
        "name": "treat-fairness-card.pdf",
        "sources": ("treat-fairness-card.html",),
        "pages": 1,
    },
    {
        "name": "thank-you-certificate.pdf",
        "sources": ("thank-you-certificate.html",),
        "pages": 1,
    },
]


def render_part(source: str) -> "object":
    from weasyprint import HTML

    document = HTML(filename=str(SHEETS / source), base_url=str(SHEETS)).render()
    return document


def build_pdf(name: str, sources: tuple[str, ...], page_count: int, dest_dir: Path) -> Path:
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    for source in sources:
        buffer = io.BytesIO()
        document = render_part(source)
        document.write_pdf(buffer)
        buffer.seek(0)
        part = PdfReader(buffer)
        for page in part.pages:
            writer.add_page(page)

    actual = len(writer.pages)
    if actual != page_count:
        raise RuntimeError(
            f"{name}: expected {page_count} page(s), built {actual}. "
            "Content probably overflowed — trim the sheet or fix the CSS."
        )

    writer.add_metadata(
        {
            "/Title": name.removesuffix(".pdf").replace("-", " ").title(),
            "/Author": "",
            "/Creator": "free-sitter-info-pack",
            "/Producer": "free-sitter-info-pack",
        }
    )

    dest = dest_dir / name
    with dest.open("wb") as fh:
        writer.write(fh)
    return dest


def build_all(dest_dir: Path) -> list[Path]:
    try:
        import weasyprint  # noqa: F401
    except ImportError:
        sys.exit("WeasyPrint is required: pip install weasyprint")
    try:
        import pypdf  # noqa: F401
    except ImportError:
        sys.exit("pypdf is required: pip install pypdf")

    dest_dir.mkdir(parents=True, exist_ok=True)
    built = []
    for doc in DOCS:
        built.append(build_pdf(doc["name"], doc["sources"], doc["pages"], dest_dir))
    return built


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build printable sitter-packet PDFs from HTML/CSS sources."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "printables",
        help="output directory (default: printables/)",
    )
    args = parser.parse_args()

    built = build_all(args.out.resolve())
    for path in built:
        print(f"built {path.relative_to(path.parents[1])} ({path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
