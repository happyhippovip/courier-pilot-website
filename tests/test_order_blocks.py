"""The Repo Reality Check order button comes only from build.py, on every order page."""

import importlib.util
import re
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


def test_ueberweisung_mailto_is_primary_and_no_checkout_without_link():
    block = build.render_order_block(build.PAYMENT_LINK_PLACEHOLDER, "founder@couriersymphony.de")
    assert "Bezahlung per Überweisung" in block
    assert "mailto:founder@couriersymphony.de" in block
    assert "Repo%20Reality%20Check%20bestellen" in block or "Repo Reality Check bestellen" in block
    assert "github.com/OWNER/REPO" in block or "OWNER%2FREPO" in block or "OWNER/REPO" in block
    assert "Sofort bezahlen" not in block  # no checkout/payment control without a live link
    assert "Repo-Check bestellen" in block and "5\u00a0€" in block
    assert "nach unserer Bestätigung" in block and "nur in dieser Antwort-Mail" in block
    assert "48&nbsp;Stunden" in block
    assert "Mein%20Name" in block and "gepr%C3%BCft" in block  # name + what to check prefilled
    assert "Widerrufsfrist" in block or "Widerrufsfrist" in __import__("urllib.parse").parse.unquote(block)
    assert "IBAN" not in block and "iban" not in block
    assert build.PAYMENT_LINK_PLACEHOLDER not in block


def test_live_payment_link_enables_sofort_bezahlen():
    live = build.render_order_block("https://pay.example/abc", "founder@couriersymphony.de")
    assert 'href="https://pay.example/abc"' in live
    assert "Sofort bezahlen" in live
    assert "disabled" not in live.split("Sofort bezahlen")[0][-80:]  # the sofort control is live
    assert "Bezahlung per Überweisung" in live  # mailto path stays


def test_no_third_party_forms_scripts_or_zip_offer_on_landing():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    # Antigravity's pilot form builds a mailto locally: no form action, no external script.
    assert not re.search(r"<form[^>]*\baction=", text)
    assert not re.search(r"<script[^>]*\bsrc=", text)
    assert "<iframe" not in text
    assert "or a ZIP" not in text
    assert "mailto:founder@couriersymphony.de" in text


def test_two_order_buttons_high_on_start_page():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    duo = text.index('id="bestellen"')
    assert duo < text.index('id="demo"'), "order buttons must sit right below the hero"
    updated, count = build.replace_video_blocks(text)
    assert count == 1 and updated == text, "run python3 build.py --sync"
    assert "Repo-Check bestellen" in text
    assert "Shorts-Paket – 10 Clips aus einem Langvideo: " + build.VIDEO_PRICE_LABEL in text
    assert "Erster Probe-Clip kostenlos." in text
    assert text.count("Konzept-Vorschau</span>") >= 2


def test_video_block_price_single_source_and_no_bank_data():
    block = build.render_video_block("founder@couriersymphony.de", "99\u00a0€")
    assert "99\u00a0€" in block and "99%20EUR" in block
    assert "79" not in block
    assert "IBAN" not in block and "nur in dieser Antwort-Mail" in block
    assert "mailto:founder@couriersymphony.de" in block
