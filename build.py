#!/usr/bin/env python3
"""Production build for couriersymphony.de (static, no dependencies).

    python3 build.py            # build dist/ and courier-site-dist.zip, warn on placeholders
    python3 build.py --release  # same, but FAIL while legal or payment placeholders remain
    python3 build.py --sync     # rewrite Repo Reality Check order blocks from the constants below

Output: dist/  -> upload the CONTENTS of this folder to the web root (see DEPLOY_STRATO.md).
"""
import html, pathlib, re, shutil, sys, zipfile
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
PAGES = [
    "index.html",
    "repo-reality-check.html",
    "impressum.html",
    "datenschutz.html",
    "privacy.html",
    "404.html",
]
ASSETS = ["styles.css", "favicon.svg", "apple-touch-icon.png", "og-cover.png", "robots.txt", "sitemap.xml"]
OFFER_PAGE = "repo-reality-check.html"
ORDER_BLOCK_BEGIN = "<!-- BEGIN:order-block -->"
ORDER_BLOCK_END = "<!-- END:order-block -->"

# Single source for the Repo Reality Check order button and contact line.
# TODO_PAYMENT_LINK disables the button ("Bald verfügbar") and fails --release.
PAYMENT_LINK_REPO_REALITY = "TODO_PAYMENT_LINK"
# Strato alias on couriersymphony.de. TODO_ORDER_EMAIL would fail --release.
ORDER_CONTACT_EMAIL = "founder@couriersymphony.de"

PAYMENT_LINK_PLACEHOLDER = "TODO_PAYMENT_LINK"
ORDER_EMAIL_PLACEHOLDER = "TODO_ORDER_EMAIL"
EMAIL_RE = re.compile(r"^[^@\s<>\"]+@[^@\s<>\"]+\.[^@\s<>\"]+$")


class Links(HTMLParser):
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


def payment_state(url: str) -> str:
    if url == PAYMENT_LINK_PLACEHOLDER:
        return "placeholder"
    if url.startswith("https://") and not any(c in url for c in " \t\r\n\"'<>"):
        return "live"
    return "invalid"


def email_state(email: str) -> str:
    if email == ORDER_EMAIL_PLACEHOLDER:
        return "placeholder"
    if EMAIL_RE.fullmatch(email):
        return "live"
    return "invalid"


def render_order_block(payment: str = PAYMENT_LINK_REPO_REALITY, email: str = ORDER_CONTACT_EMAIL) -> str:
    """HTML for one order slot. Placeholder payment renders a disabled button, no href."""
    if payment_state(payment) == "placeholder":
        action = '<button type="button" class="btn is-disabled" disabled>Bald verfügbar</button>\n<p class="fine">Die Bestellung ist noch nicht freigeschaltet.</p>'
    elif payment_state(payment) == "live":
        href = html.escape(payment, quote=True)
        action = f'<a class="btn" href="{href}">Als Beta-Tester bestellen — 5 EUR</a>'
    else:
        action = "<!-- invalid PAYMENT_LINK_REPO_REALITY -->"

    if email_state(email) == "placeholder":
        contact = "<p class=\"fine\">Fragen zur Bestellung: die Kontaktadresse ist noch nicht hinterlegt.</p>"
    elif email_state(email) == "live":
        esc = html.escape(email, quote=True)
        contact = f'<p class="fine">Fragen zur Bestellung: <a href="mailto:{esc}">{esc}</a></p>'
    else:
        contact = "<!-- invalid ORDER_CONTACT_EMAIL -->"
    return action + "\n" + contact


def marked_order_block() -> str:
    return f"{ORDER_BLOCK_BEGIN}\n{render_order_block()}\n{ORDER_BLOCK_END}"


def replace_order_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(
        re.escape(ORDER_BLOCK_BEGIN) + r".*?" + re.escape(ORDER_BLOCK_END),
        re.DOTALL,
    )
    count = len(pattern.findall(text))
    return pattern.sub(marked_order_block(), text), count


def main() -> int:
    release = "--release" in sys.argv
    sync = "--sync" in sys.argv
    errors, warnings = [], []

    pay = payment_state(PAYMENT_LINK_REPO_REALITY)
    mail = email_state(ORDER_CONTACT_EMAIL)
    if pay == "invalid":
        errors.append("PAYMENT_LINK_REPO_REALITY must be TODO_PAYMENT_LINK or an https:// URL")
    elif pay == "placeholder":
        (errors if release else warnings).append(
            "PAYMENT_LINK_REPO_REALITY is still TODO_PAYMENT_LINK (set the payment URL in build.py before release)"
        )
    if mail == "invalid":
        errors.append("ORDER_CONTACT_EMAIL must be TODO_ORDER_EMAIL or a plain email address")
    elif mail == "placeholder":
        (errors if release else warnings).append(
            "ORDER_CONTACT_EMAIL is still TODO_ORDER_EMAIL (set a real contact address in build.py before release)"
        )

    rendered = render_order_block()
    if pay == "placeholder":
        button_line = rendered.splitlines()[0]
        if button_line != '<button type="button" class="btn is-disabled" disabled>Bald verfügbar</button>':
            errors.append("internal: placeholder payment must render a disabled Bald verfügbar button")
        if "TODO_PAYMENT_LINK" in rendered or "href=" in button_line:
            errors.append("internal: placeholder payment must not render a payment URL")
    elif pay == "live" and html.escape(PAYMENT_LINK_REPO_REALITY, quote=True) not in rendered:
        errors.append("internal: live payment URL missing from the order button")
    if mail == "live" and f"mailto:{html.escape(ORDER_CONTACT_EMAIL, quote=True)}" not in rendered:
        errors.append("internal: ORDER_CONTACT_EMAIL missing from the order block")

    offer_path = ROOT / OFFER_PAGE
    if not offer_path.is_file():
        errors.append(f"missing page {OFFER_PAGE}")
    else:
        offer_text = offer_path.read_text(encoding="utf-8")
        updated, count = replace_order_blocks(offer_text)
        if count < 1:
            errors.append(f"{OFFER_PAGE}: missing order-block markers")
        elif sync and updated != offer_text:
            offer_path.write_text(updated, encoding="utf-8")
            print(f"SYNC  {OFFER_PAGE}: wrote {count} order block(s) from build.py")
        elif updated != offer_text:
            errors.append(
                f"{OFFER_PAGE}: order block out of sync with PAYMENT_LINK_REPO_REALITY / "
                "ORDER_CONTACT_EMAIL (run python3 build.py --sync)"
            )

    parsed = {}
    for page in PAGES:
        path = ROOT / page
        if not path.is_file():
            errors.append(f"missing page {page}")
            continue
        text = path.read_text(encoding="utf-8")
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
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, DIST / name)
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
