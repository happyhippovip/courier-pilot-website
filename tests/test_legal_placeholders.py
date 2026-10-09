"""Legal pages filled with Dennis's confirmed public facts; --release has no legal blocker."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "Dennis Ricardo Hobbiejanßen"
EMAIL = "founder@couriersymphony.de"
STREET = "Siebenbürger Straße 13c"
PLZ_CITY = "26127 Oldenburg"
LEGAL = ("impressum.html", "datenschutz.html", "widerruf.html")


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_founder_name_email_address_on_legal_pages():
    for name in LEGAL:
        text = _read(name)
        assert NAME in text, name
        assert f"mailto:{EMAIL}" in text, name
        assert STREET in text, name
        assert PLZ_CITY in text, name


def test_no_placeholders_left_on_legal_pages():
    for name in LEGAL:
        text = _read(name)
        assert 'class="ph"' not in text, name
        assert 'data-placeholder="true"' not in text, name
        assert "TODO" not in text, name
        assert "[Straße und Hausnummer]" not in text, name


def test_impressum_ddg_mstv_and_email_only_contact():
    text = _read("impressum.html")
    assert "Angaben gemäß § 5 DDG" in text
    assert "Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV" in text
    assert text.count(STREET) == 2  # § 5 DDG block + MStV block
    assert "Telefon" not in text  # phone is not public; e-mail is the contact channel
    assert "tel:" not in text


def test_no_invented_company_vat_or_register():
    impressum = _read("impressum.html")
    assert "Gründung in Vorbereitung" in impressum
    assert "Privatperson" in impressum
    for word in ("GmbH", "UG (", "Geschäftsführer", "Umsatzsteuer", "USt-ID", "Handelsregister",
                 "Registergericht", "Kleinunternehmer"):
        assert word not in impressum, word


def test_datenschutz_factual_items():
    text = _read("datenschutz.html")
    assert "GitHub Pages" in text and "GitHub, Inc." in text
    assert "https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" in text
    assert "STRATO GmbH" in text
    assert "Der Landesbeauftragte für den Datenschutz Niedersachsen" in text
    assert "https://www.lfd.niedersachsen.de/" in text
    assert "Banküberweisung" in text
    assert "ausschließlich in unserer Antwort-E-Mail" in text
    assert "Stand: 8. Oktober 2026" in text
    assert "öffentliche GitHub-Links" in text and "keine ZIP-Uploads" in text
    assert "Repo-Link oder ZIP" not in text
    assert "7 Tage" not in text  # no invented log retention period


def test_no_private_contact_or_bank_data_anywhere():
    sys.path.insert(0, str(ROOT))
    import build  # noqa: E402

    for page in sorted(ROOT.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        assert "IBAN" not in text, page.name
        for label, rx in build.PRIVATE_DATA_RES:
            assert not rx.search(text), (page.name, label)


def test_offer_page_no_longer_points_to_placeholders():
    text = _read("repo-reality-check.html")
    assert "als Platzhalter markiert" not in text


def test_release_passes_with_only_payment_link_warning():
    proc = subprocess.run(
        [sys.executable, "build.py", "--release"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "RESULT OK" in out
    assert "ERROR" not in out
    assert "legal placeholders still present" not in out
    assert "WARN  PAYMENT_LINK_REPO_REALITY is still TODO_PAYMENT_LINK" in out


def test_release_guard_rejects_private_data():
    sys.path.insert(0, str(ROOT))
    import build  # noqa: E402

    hits = lambda s: [label for label, rx in build.PRIVATE_DATA_RES if rx.search(s)]
    assert hits("Konto DE00 1234 5678 9012 3456 78")
    assert hits('<a href="tel:+49000">')
    assert hits("max@gmx.de")
    assert hits("Tel. 0151 2345678") and hits("+49 160 1234567")
    assert not hits("Stand: 8. Oktober 2026, 26127 Oldenburg")
    assert not hits(_read("impressum.html"))
    assert not hits(_read("datenschutz.html"))
