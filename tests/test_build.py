"""Tests for the Free Sitter Info Pack.

Every sheet must build a valid, unbranded PDF, and the finished
printables/ must match the expected page counts.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(name="build_module")
def fixture_build_module():
    spec = importlib.util.spec_from_file_location("sittpack_build", ROOT / "build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sheet_paths():
    return sorted((ROOT / "sheets").glob("*.html"))


def test_sheets_exist():
    paths = sheet_paths()
    assert len(paths) == 8
    assert all(p.name == p.name.lower() and " " not in p.name for p in paths)


@pytest.mark.parametrize("path", sheet_paths(), ids=lambda p: p.name)
def test_every_sheet_builds_a_valid_pdf(build_module, path, tmp_path):
    document = build_module.render_part(path.name)
    out = tmp_path / (path.stem + ".pdf")
    document.write_pdf(out)

    assert out.exists() and out.stat().st_size > 0
    assert out.read_bytes()[:5] == b"%PDF-"
    reader = PdfReader(str(out))
    assert len(reader.pages) >= 1
    text = (reader.pages[0].extract_text() or "").lower()
    assert len(text) > 40
    assert "counter" in text


def test_full_build_via_cli(tmp_path):
    out_dir = tmp_path / "printables"
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--out", str(out_dir)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    assert len(list(out_dir.glob("*.pdf"))) == 5


def test_each_pdf_has_expected_pages_and_title(build_module, tmp_path):
    out_dir = tmp_path / "out"
    built = build_module.build_all(out_dir)
    assert {p.name for p in built} == {d["name"] for d in build_module.DOCS}

    for doc in build_module.DOCS:
        pdf_path = out_dir / doc["name"]
        assert pdf_path.read_bytes()[:5] == b"%PDF-"
        reader = PdfReader(str(pdf_path))
        assert len(reader.pages) == doc["pages"]
        expected_title = doc["name"].removesuffix(".pdf").replace("-", " ").title()
        assert reader.metadata.title == expected_title


def test_packets_keep_intro_and_details_distinct(build_module, tmp_path):
    out_dir = tmp_path / "out"
    build_module.build_all(out_dir)
    cases = [
        ("babysitter-packet.pdf", "welcome in", "babysitter details"),
        ("pet-sitter-packet.pdf", "animal clock", "pet sitter details"),
        ("house-sitter-packet.pdf", "temporary roommate", "house sitter details"),
    ]
    for name, first_hint, second_hint in cases:
        reader = PdfReader(str(out_dir / name))
        first = " ".join((reader.pages[0].extract_text() or "").lower().split())
        second = " ".join((reader.pages[1].extract_text() or "").lower().split())
        assert "leave this packet on the counter" in first
        assert first_hint in first
        assert second_hint in second


def test_extras_cover_treat_card_and_certificate(build_module, tmp_path):
    out_dir = tmp_path / "out"
    build_module.build_all(out_dir)

    card = PdfReader(str(out_dir / "treat-fairness-card.pdf"))
    card_text = " ".join((p.extract_text() or "") for p in card.pages).lower()
    for phrase in ("treat-fairness card", "ground rules", "today's tally"):
        assert phrase in card_text

    cert = PdfReader(str(out_dir / "thank-you-certificate.pdf"))
    cert_text = " ".join((p.extract_text() or "") for p in cert.pages).lower()
    for phrase in ("certificate of outstanding sittering", "grateful household"):
        assert phrase in cert_text


def test_pdfs_are_unbranded(build_module, tmp_path):
    out_dir = tmp_path / "out"
    build_module.build_all(out_dir)
    banned = ("asdale", "dylan", "dynamics")
    for doc in build_module.DOCS:
        reader = PdfReader(str(out_dir / doc["name"]))
        metadata_blob = " ".join(str(v) for v in (reader.metadata or {}).values()).lower()
        for word in banned:
            assert word not in metadata_blob
        for page in reader.pages:
            text = (page.extract_text() or "").lower()
            for word in banned:
                assert word not in text


def test_sources_have_no_secrets():
    banned_patterns = (
        "AK" + "IA",
        "sk" + "-",
        "ghp" + "_",
        "BEGIN OPENSSH PRIVATE" + " KEY",
        "BEGIN RSA PRIVATE" + " KEY",
        "BEGIN EC PRIVATE" + " KEY",
    )
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix in {".pdf", ".pyc"}:
            continue
        if any(part in {"__pycache__", ".git", ".pytest_cache"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in banned_patterns:
            assert pattern not in text, f"possible secret in {path.name}"
