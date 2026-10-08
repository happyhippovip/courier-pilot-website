"""Konzept-Vorschau gallery: disclaimer must be present on gallery pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCLAIMER = (
    "Konzeptbilder und KI-Clips. Zahlen, Namen und Avatare darin "
    "sind Beispiele, keine echten Nutzer- oder Umsatzdaten."
)


def test_disclaimer_on_gallery_pages():
    for name in ("index.html", "konzept.html"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert DISCLAIMER in text, f"{name} missing gallery disclaimer"
        assert 'id="konzept"' in text, f"{name} missing #konzept section"
        assert "/assets/konzept/" in text, f"{name} missing konzept assets"
