"""Mitmachen page: LFG/LFM mailto only, honest beta preview, nav + teaser wired."""

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "mitmachen.html"
EMAIL = "founder@couriersymphony.de"
FORBIDDEN = ("Patent", "Claim", "Schutzpaket", "FIG.", "Moat", "Erfindung")
TEMPLATE_FIELDS = (
    "Name / Handle",
    "Rolle (Builder, Agent-Builder, Tester, Designer, Video)",
    "Sprachen / Tools",
    "GitHub-Profil oder verifizierbare Arbeit (Link)",
    "Verfügbarkeit",
    "Was ich beweisen will",
)


class Hrefs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.forms, self.scripts = [], 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "form":
            self.forms += 1
        if tag == "script":
            self.scripts += 1


def _text():
    return PAGE.read_text(encoding="utf-8")


def _mailtos():
    p = Hrefs()
    p.feed(_text())
    return [h for h in p.hrefs if h.startswith("mailto:")], p


def test_page_exists_and_in_build():
    assert PAGE.is_file()
    assert '"mitmachen.html"' in (ROOT / "build.py").read_text(encoding="utf-8")
    assert "https://couriersymphony.de/mitmachen.html" in (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_lfg_and_lfm_mailtos_valid():
    links, _ = _mailtos()
    subjects = {}
    for href in links:
        parts = urlsplit(href)
        if parts.path != EMAIL or not parts.query:
            continue
        q = parse_qs(parts.query)
        subj = q["subject"][0]
        body = q["body"][0]
        subjects[subj[:4]] = (subj, body)
    assert set(subjects) == {"LFG:", "LFM:"}, subjects.keys()
    for subj, body in subjects.values():
        assert " " not in urlsplit(next(h for h in links if unquote(h).find(subj) >= 0)).query
        for field in TEMPLATE_FIELDS:
            assert field in body, (subj, field)


def test_no_forms_scripts_or_third_party_targets():
    links, p = _mailtos()
    assert p.forms == 0 and p.scripts == 0
    for h in p.hrefs:
        assert h.startswith(("/", "#", "mailto:" + EMAIL)), h


def test_honest_beta_and_unpaid_wording():
    t = _text()
    assert "Beta-Vorschau – Gruppenfinder und Level-System sind noch nicht live; wir melden uns persönlich." in t
    assert "Keine Bezahlung zugesagt, keine Kosten für dich." in t
    assert "Einmal gelöst, für alle freigeschaltet:" in t
    assert "Die Anerkennung bleibt beim Ersten, der es gelöst hat." in t
    assert "noch nicht live" in t
    assert "Level&nbsp;1" in t and "60" in t
    assert "Ledger" in t
    for word in ("verdienst", "Verdienst", "garantiert"):
        assert word not in t, word


def test_no_forbidden_terms_on_new_or_touched_pages():
    for name in ("mitmachen.html", "index.html", "datenschutz.html"):
        t = (ROOT / name).read_text(encoding="utf-8")
        for word in FORBIDDEN:
            assert word not in t, (name, word)


def test_nav_link_and_index_teaser():
    for name in ("index.html", "konzept.html", "architecture.html", "use-cases.html",
                 "developers.html", "company.html", "mitmachen.html"):
        t = (ROOT / name).read_text(encoding="utf-8")
        nav = re.search(r'<nav class="nav" id="[^"]+"[^>]*>.*?</nav>', t, re.S).group(0)
        assert 'href="/mitmachen.html"' in nav and ">Mitmachen</a>" in nav, name
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="mitmachen-teaser"' in index
    assert '<a class="btn" href="/mitmachen.html">Mitmachen</a>' in index


def test_datenschutz_mentions_lfg_lfm():
    t = (ROOT / "datenschutz.html").read_text(encoding="utf-8")
    assert "Looking for Group / Looking for Member" in t
    assert "nur, um Ihnen zu antworten und passende" in t
    assert "Auf Wunsch löschen wir Ihre Angaben jederzeit" in t
    assert "kein Tracking" in t
