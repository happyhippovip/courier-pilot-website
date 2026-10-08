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


def test_gallery_assets_exist_and_stay_small():
    import re

    konzept = ROOT / "assets" / "konzept"
    for name in ("index.html", "konzept.html"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for ref in re.findall(r'/assets/konzept/([\w.-]+)', text):
            assert (konzept / ref).is_file(), f"{name}: missing {ref}"
    for f in konzept.glob("*.webp"):
        assert f.stat().st_size <= 300_000, f"{f.name} over 300 KB"
    total = sum(f.stat().st_size for f in konzept.iterdir())
    assert total < 6_000_000, f"konzept assets {total} bytes >= 6 MB"


def test_new_x_concept_images_listed_on_both_pages():
    for name in ("index.html", "konzept.html"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for slug in ("hub-launch", "so-funktionierts"):
            assert f'href="#lb-{slug}"' in text, (name, slug)
            assert f'id="lb-{slug}"' in text, (name, slug)
