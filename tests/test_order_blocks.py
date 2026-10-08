"""The Repo Reality Check order button comes only from build.py, on every order page."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("site_build", ROOT / "build.py")
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)


def test_paid_order_slots_are_off():
    assert build.ORDER_PAGES == []
    assert build.VIDEO_PAGES == []
    for name in ("index.html", "repo-reality-check.html"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "BEGIN:order-block" not in text, name
        assert "BEGIN:video-block" not in text, name
        assert "5\u00a0€" not in text and "79\u00a0€" not in text, name
        assert "5 EUR" not in text and "79 EUR" not in text, name
        assert "mailto:founder@couriersymphony.de" in text, name


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


def test_early_access_mailto_replaces_purchase_buttons():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    early = text.index('id="early-access"')
    assert early < text.index('id="demo"'), "Early Access sits with the hero, above the simulator"
    assert "Early Access per E-Mail" in text
    assert "Repo-Check bestellen" not in text
    assert "Shorts-Paket" not in text
    assert build.VIDEO_PRICE_LABEL not in text
    assert build.REPO_PRICE_LABEL not in text
    assert "Keine Bezahlung" in text or "keine Bezahlung" in text
    nav = text.split("<nav", 1)[1].split("</nav>", 1)[0]
    assert "support-development" not in nav
    start = text.index('id="support-development"')
    tag = text[text.rfind("<", 0, start):text.find(">", start)]
    assert "hidden" in tag and 'data-draft="support"' in tag
    assert "Support Courier Symphony's Development" in text
    assert "Hardware-Sponsoring" in text
    assert "founder@couriersymphony.de" in text
    # Activation stays a comment until the founder approves it and a tax check is done.
    assert "tax check" in text
    stripped = build.strip_draft_support(text)
    assert "Support Courier Symphony's Development" not in stripped
    assert "support-development" not in stripped


def test_video_block_price_single_source_and_no_bank_data():
    block = build.render_video_block("founder@couriersymphony.de", "99\u00a0€")
    assert "99\u00a0€" in block and "99%20EUR" in block
    assert "79" not in block
    assert "IBAN" not in block and "nur in dieser Antwort-Mail" in block
    assert "mailto:founder@couriersymphony.de" in block


def test_golive_blockers_fixed():
    from urllib.parse import unquote
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    offer = (ROOT / "repo-reality-check.html").read_text(encoding="utf-8")
    privacy = (ROOT / "datenschutz.html").read_text(encoding="utf-8")
    assert "Dr. Dennis Schmidt" not in index and "Tech Systems GmbH" not in index
    for page in ROOT.glob("*.html"):
        assert "99–149" not in page.read_text(encoding="utf-8"), page.name
    assert "Video-Schnitt (Shorts-Paket)" in privacy and "nach der Lieferung" in privacy
    video = unquote(build.render_video_block())
    assert "Rechte am Videomaterial" in video and "Widerrufsfrist" in video
    repo = build.render_order_block()
    assert repo.count("Bezahlung per Überweisung") == 1
