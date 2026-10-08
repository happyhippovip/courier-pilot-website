"""Mobile menu dismiss guarantee (no-JS :target pattern).

State machine: on mobile the panel is visible exactly while the URL fragment
equals the nav element's id. Tapping any in-page link whose fragment differs
therefore closes the panel; tapping the opener (fragment == nav id) opens it.

Every page with a toggle-style header nav (class "nav", not "nav-static",
not "foot-nav") must use this pattern, otherwise the menu can neither open
nor provably close:
  - <a class="nav-burger" href="#<nav-id>"> opens it,
  - <nav class="nav" id="<nav-id>"> is the panel,
  - <a class="nav-close" href="#<other-existing-id>"> closes it,
  - every in-page href="#x" inside the nav has x != nav id, so the tap
    provably moves :target away and the panel closes.
"""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html"))


class Nav(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.header_navs = []
        self.burgers = []
        self._nav = None
        self._in_header = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "header":
            self._in_header = True
        if tag == "nav":
            classes = (attrs.get("class") or "").split()
            if "foot-nav" not in classes:
                self._nav = {"class": classes, "id": attrs.get("id"),
                             "links": [], "closes": []}
                self.header_navs.append(self._nav)
        elif tag == "a":
            href = attrs.get("href", "")
            classes = (attrs.get("class") or "").split()
            if "nav-burger" in classes and self._in_header:
                self.burgers.append(href)
            elif "nav-close" in classes and self._nav is not None:
                self._nav["closes"].append(href)
            elif self._nav is not None:
                self._nav["links"].append(href)

    def handle_endtag(self, tag):
        if tag == "nav":
            self._nav = None
        elif tag == "header":
            self._in_header = False


def _parse(page: Path) -> Nav:
    parser = Nav()
    parser.feed(page.read_text(encoding="utf-8"))
    return parser


def _frag(href: str):
    return href[1:] if href.startswith("#") and len(href) > 1 else None


def test_toggle_navs_use_dismiss_pattern():
    failures = []
    for page in PAGES:
        parsed = _parse(page)
        for nav in parsed.header_navs:
            classes = nav["class"]
            if "nav-static" in classes or "nav" not in classes:
                continue
            nav_id = nav["id"]
            label = f"{page.name} nav"
            if not nav_id or f"#{nav_id}" not in parsed.burgers:
                failures.append(f"{label}: no burger link opening the panel")
                continue
            good_close = [c for c in nav["closes"]
                          if _frag(c) and _frag(c) != nav_id and _frag(c) in parsed.ids]
            if not good_close:
                failures.append(f"{label}: no close link to a different existing id")
            for href in nav["links"]:
                frag = _frag(href)
                if frag is not None and frag == nav_id:
                    failures.append(f"{label}: in-page link {href} keeps :target on the panel")
    assert not failures, "mobile menu cannot provably close:\n" + "\n".join(failures)


def test_inpage_nav_links_reference_existing_ids():
    failures = []
    for page in PAGES:
        parsed = _parse(page)
        for nav in parsed.header_navs:
            if "nav" not in nav["class"]:
                continue
            for href in nav["links"] + nav["closes"]:
                frag = _frag(href)
                if frag is not None and frag not in parsed.ids:
                    failures.append(f"{page.name}: nav link {href} has no anchor")
    assert not failures, "dangling in-page nav links:\n" + "\n".join(failures)
