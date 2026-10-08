"""Mitmachen 'Gemeinsames Ziel (Vorschau)': non-binding pledges by mail only, no money flow."""

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "mitmachen.html"
EMAIL = "founder@couriersymphony.de"


def _section():
    t = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<section class="section ziel" id="ziel".*?</section>', t, re.S)
    assert m, "ziel section missing"
    return m.group(0)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.tags, self.tiers = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if "ziel-tier" in (a.get("class") or "").split():
            self.tiers += 1


def _parsed():
    p = Tags()
    p.feed(_section())
    return p


def test_heading_and_preview_marker():
    s = _section()
    assert '<h2 id="ziel-title">Gemeinsames Ziel (Vorschau)</h2>' in s
    assert "Vorschau, nicht live" in s


def test_two_or_three_goal_tiers_starting_at_1000():
    p = _parsed()
    assert 2 <= p.tiers <= 3, p.tiers
    s = _section()
    assert "ab 1.000 € Zusagen" in s
    amounts = re.findall(r"ab ([\d.]+) € Zusagen", s)
    assert len(amounts) == p.tiers
    values = [int(a.replace(".", "")) for a in amounts]
    assert values == sorted(values) and values[0] == 1000


def test_honest_no_money_human_decides():
    s = _section()
    for phrase in (
        "Nur unverbindliche Zusagen per E-Mail.",
        "Es wird kein Geld eingesammelt, du zahlst jetzt nichts.",
        "Über jede Ausgabe entscheidet Dennis als Gründer persönlich, nicht eine KI.",
        "Nichts wird automatisch gekauft.",
        "Wir sammeln kein Geld ein.",
    ):
        assert phrase in s, phrase


def test_only_pledge_mailto_no_forms_scripts_or_payment_links():
    p = _parsed()
    assert "form" not in p.tags and "script" not in p.tags and "input" not in p.tags
    assert p.hrefs, "pledge mailto missing"
    for h in p.hrefs:
        assert h.startswith("mailto:" + EMAIL + "?"), h
    parts = urlsplit(p.hrefs[0])
    assert " " not in parts.query
    q = parse_qs(parts.query)
    assert q["subject"][0].startswith("ZIEL:")
    body = q["body"][0]
    for field in ("Name / Handle", "Unverbindlicher Betrag (EUR)", "unverbindliche Zusage",
                  "Es wird jetzt kein Geld eingesammelt"):
        assert field in body, field
    for word in ("IBAN", "BIC", "Kontonummer", "Bankverbindung:", "PayPal"):
        assert word not in body, word


def test_no_bank_data_or_revenue_claims_in_section():
    s = _section()
    assert not re.search(r"\b[A-Z]{2}\d{2}(?:\s?[0-9A-Z]{4}){3,7}", s), "IBAN-like string"
    for word in ("IBAN", "PayPal", "Stripe", "Rendite", "Gewinn", "garantiert", "verdienst",
                 "Patent", "Claim", "Schutzpaket", "Erfindung", "Moat"):
        assert word not in s, word


def test_datenschutz_covers_pledges():
    t = (ROOT / "datenschutz.html").read_text(encoding="utf-8")
    assert "unverbindliche Zusage" in t
    assert "kein Geld eingezogen" in t
