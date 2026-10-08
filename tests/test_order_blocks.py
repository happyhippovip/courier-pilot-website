"""The Repo Reality Check order button comes only from build.py, on every order page."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("site_build", ROOT / "build.py")
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)


def test_every_order_page_carries_the_synced_block():
    assert "index.html" in build.ORDER_PAGES
    for page in build.ORDER_PAGES:
        text = (ROOT / page).read_text(encoding="utf-8")
        updated, count = build.replace_order_blocks(text)
        assert count >= 1, page
        assert updated == text, f"{page}: run python3 build.py --sync"


def test_placeholder_keeps_button_disabled_and_live_link_enables_it():
    placeholder = build.render_order_block(build.PAYMENT_LINK_PLACEHOLDER, "founder@couriersymphony.de")
    assert "disabled" in placeholder and "href=\"https" not in placeholder
    assert build.PAYMENT_LINK_PLACEHOLDER not in placeholder
    live = build.render_order_block("https://pay.example/abc", "founder@couriersymphony.de")
    assert 'href="https://pay.example/abc"' in live and "disabled" not in live


def test_no_third_party_forms_or_zip_offer_on_landing():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "<form" not in text
    assert "<script" not in text
    assert "or a ZIP" not in text
    assert "mailto:founder@couriersymphony.de" in text
