#!/usr/bin/env python3
"""Production build for couriersymphony.de (static, no dependencies).

    python3 build.py            # build dist/ and courier-site-dist.zip, warn on placeholders
    python3 build.py --release  # same, but FAIL while legal placeholders remain

Output: dist/  -> upload the CONTENTS of this folder to the web root (see DEPLOY_STRATO.md).
"""
import html.parser, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
PAGES = ["index.html", "impressum.html", "datenschutz.html", "privacy.html", "404.html"]
ASSETS = ["styles.css", "favicon.svg", "apple-touch-icon.png", "og-cover.png", "robots.txt", "sitemap.xml"]


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])


def main() -> int:
    release = "--release" in sys.argv
    errors, warnings = [], []
    parsed = {}
    for page in PAGES:
        text = (ROOT / page).read_text(encoding="utf-8")
        p = Links()
        p.feed(text)
        parsed[page] = (text, p)
        if 'data-placeholder="true"' in text or 'class="ph"' in text:
            (errors if release else warnings).append(f"{page}: legal placeholders still present (fill before launch)")
    for page, (text, p) in parsed.items():
        for ref in p.refs:
            if re.match(r"^(https?:|mailto:|tel:)", ref):
                continue
            path, _, frag = ref.partition("#")
            target = page if path == "" else path.lstrip("/") or "index.html"
            if not (ROOT / target).is_file():
                errors.append(f"{page}: broken link {ref}")
            elif frag and frag not in parsed.get(target, (None, Links()))[1].ids:
                errors.append(f"{page}: missing anchor {ref}")
    for asset in ASSETS:
        if not (ROOT / asset).is_file():
            errors.append(f"missing asset {asset}")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for name in PAGES + ASSETS:
        shutil.copy2(ROOT / name, DIST / name)
    shutil.copy2(ROOT / "deploy" / "strato" / "htaccess", DIST / ".htaccess")
    zpath = ROOT / "courier-site-dist.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(DIST.rglob("*")):
            z.write(f, f.relative_to(DIST))

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    files = sorted(f.name for f in DIST.iterdir())
    size = sum(f.stat().st_size for f in DIST.iterdir())
    print(f"dist/: {len(files)} files, {size} bytes -> {', '.join(files)}")
    print("RESULT", "FAIL" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
