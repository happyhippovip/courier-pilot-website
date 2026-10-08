"""Founder fields filled; remaining legal TODOs still block --release."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "Dennis Ricardo Hobbiejanßen"
EMAIL = "founder@couriersymphony.de"
LEGAL = ("impressum.html", "datenschutz.html", "widerruf.html")


def test_founder_name_email_city_on_legal_pages():
    for name in LEGAL:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert NAME in text, name
        assert f"mailto:{EMAIL}" in text, name
        assert "Oldenburg" in text, name


def test_street_and_plz_remain_explicit_placeholders():
    for name in LEGAL:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert 'class="ph">[Straße und Hausnummer]' in text, name
        assert 'class="ph">[PLZ]' in text, name


def test_datenschutz_section6_github_only_no_zip_upload():
    text = (ROOT / "datenschutz.html").read_text(encoding="utf-8")
    assert "öffentlicher GitHub-Repo-Link" in text
    assert "keine ZIP-Uploads" in text
    assert "Repo-Link oder ZIP" not in text
    assert "Zahlungsdienstleister" in text  # payment provider still TODO


def test_no_invented_company_vat_or_register():
    impressum = (ROOT / "impressum.html").read_text(encoding="utf-8")
    assert "GmbH" not in impressum
    assert "UG (" not in impressum
    assert "DE123" not in impressum  # no fake VAT
    assert "Umsatzsteuer-Identifikationsnummer" in impressum  # section stays as TODO
    assert "Registergericht und Registernummer" in impressum


def test_release_still_fails_on_address_and_payment_placeholders():
    proc = subprocess.run(
        [sys.executable, "build.py", "--release"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    # Überweisung mailto is live; optional Sofort-bezahlen link may still warn.
    assert "impressum.html: legal placeholders still present" in out
    assert "datenschutz.html: legal placeholders still present" in out
    assert "widerruf.html: legal placeholders still present" in out
    assert "Straße und Hausnummer" in (ROOT / "impressum.html").read_text(encoding="utf-8")
    assert "RESULT FAIL" in out
    # Must not fail solely for missing payment link once legal TODOs are gone:
    # payment placeholder is a WARN, not an ERROR line.
    assert "ERROR PAYMENT_LINK_REPO_REALITY" not in out
