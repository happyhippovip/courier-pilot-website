#!/usr/bin/env python3
"""Production build for couriersymphony.de (static, no dependencies).

    python3 build.py            # build dist/ and courier-site-dist.zip, warn on placeholders
    python3 build.py --release  # same, but FAIL while legal or payment placeholders remain
    python3 build.py --sync     # rewrite Repo Reality Check order blocks from the constants below

Output: dist/  -> upload the CONTENTS of this folder to the web root (see DEPLOY_STRATO.md).
"""
import html, pathlib, re, shutil, sys, zipfile
from urllib.parse import quote
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
PAGES = [
    "index.html",
    "konzept.html",
    "repo-reality-check.html",
    "architecture.html",
    "security.html",
    "use-cases.html",
    "developers.html",
    "company.html",
    "widerruf.html",
    "impressum.html",
    "datenschutz.html",
    "privacy.html",
    "404.html",
]
ASSETS = ["styles.css", "favicon.svg", "apple-touch-icon.png", "og-cover.png", "robots.txt", "sitemap.xml"]
ASSET_DIRS = ["assets"]
OFFER_PAGE = "repo-reality-check.html"
# Every page here must carry at least one synced order block (same button everywhere).
ORDER_PAGES = [OFFER_PAGE, "index.html"]
ORDER_BLOCK_BEGIN = "<!-- BEGIN:order-block -->"
ORDER_BLOCK_END = "<!-- END:order-block -->"

# Single source for the Repo Reality Check order button and contact line.
# TODO_PAYMENT_LINK keeps optional "Sofort bezahlen" disabled; Überweisung mailto is the live path.
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
    """Order slot: Überweisung via mailto (primary) + optional Sofort-bezahlen link.

    Bank details are never inlined; the reply mail carries them. A missing
    PAYMENT_LINK_REPO_REALITY keeps Sofort bezahlen disabled for later.
    """
    pay = payment_state(payment)
    mail = email_state(email)

    copy = (
        '<p class="order-pay">Bezahlung per Überweisung (5&nbsp;€). '
        'Bestelle per Mail an <strong>founder@couriersymphony.de</strong> mit deinem '
        'öffentlichen GitHub-Link – du bekommst die Bankverbindung in der Antwort. '
        'Der Report startet nach Zahlungseingang, Lieferung innerhalb von 48&nbsp;Stunden.</p>'
    )

    if mail == "live":
        esc = html.escape(email, quote=True)
        subject = quote("Repo Reality Check bestellen")
        body = quote(
            "Hallo Courier Symphony,\n\n"
            "ich möchte einen Repo Reality Check (Beta, 5 EUR per Überweisung) bestellen.\n\n"
            "Öffentlicher GitHub-Link: https://github.com/OWNER/REPO\n\n"
            "Bitte schickt mir die Bankverbindung zur Überweisung.\n\n"
            "Danke"
        )
        mailto_cta = (
            f'<a class="btn" href="mailto:{esc}?subject={subject}&amp;body={body}">'
            'Per Mail bestellen — 5&nbsp;EUR</a>'
        )
        contact = f'<p class="fine">Fragen: <a href="mailto:{esc}">{esc}</a></p>'
    elif mail == "placeholder":
        mailto_cta = '<button type="button" class="btn is-disabled" disabled>Per Mail bestellen — 5&nbsp;EUR</button>'
        contact = '<p class="fine">Fragen zur Bestellung: die Kontaktadresse ist noch nicht hinterlegt.</p>'
    else:
        mailto_cta = "<!-- invalid ORDER_CONTACT_EMAIL -->"
        contact = "<!-- invalid ORDER_CONTACT_EMAIL -->"

    if pay == "placeholder":
        instant = (
            '<button type="button" class="btn btn-ghost is-disabled" disabled>Sofort bezahlen</button>\n'
            '<p class="fine">Sofort bezahlen (Zahlungslink) ist optional und später verfügbar.</p>'
        )
    elif pay == "live":
        href = html.escape(payment, quote=True)
        instant = f'<a class="btn btn-ghost" href="{href}">Sofort bezahlen</a>'
    else:
        instant = "<!-- invalid PAYMENT_LINK_REPO_REALITY -->"

    return "\n".join([copy, mailto_cta, instant, contact])


def marked_order_block() -> str:
    return f"{ORDER_BLOCK_BEGIN}\n{render_order_block()}\n{ORDER_BLOCK_END}"


def replace_order_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(
        re.escape(ORDER_BLOCK_BEGIN) + r".*?" + re.escape(ORDER_BLOCK_END),
        re.DOTALL,
    )
    count = len(pattern.findall(text))
    return pattern.sub(lambda _: marked_order_block(), text), count


def main() -> int:
    release = "--release" in sys.argv
    sync = "--sync" in sys.argv
    errors, warnings = [], []

    pay = payment_state(PAYMENT_LINK_REPO_REALITY)
    mail = email_state(ORDER_CONTACT_EMAIL)
    if pay == "invalid":
        errors.append("PAYMENT_LINK_REPO_REALITY must be TODO_PAYMENT_LINK or an https:// URL")
    elif pay == "placeholder":
        warnings.append(
            "PAYMENT_LINK_REPO_REALITY is still TODO_PAYMENT_LINK (optional Sofort-bezahlen link; Überweisung via mailto is live)"
        )
    if mail == "invalid":
        errors.append("ORDER_CONTACT_EMAIL must be TODO_ORDER_EMAIL or a plain email address")
    elif mail == "placeholder":
        (errors if release else warnings).append(
            "ORDER_CONTACT_EMAIL is still TODO_ORDER_EMAIL (set a real contact address in build.py before release)"
        )

    rendered = render_order_block()
    if "Bezahlung per Überweisung" not in rendered:
        errors.append("internal: order block must state Überweisung payment")
    if "IBAN" in rendered or "iban" in rendered:
        errors.append("internal: bank/IBAN data must never appear in the order block")
    if pay == "placeholder":
        if "Sofort bezahlen" not in rendered or "disabled" not in rendered:
            errors.append("internal: placeholder payment must render a disabled Sofort bezahlen control")
        if "TODO_PAYMENT_LINK" in rendered:
            errors.append("internal: placeholder payment must not leak TODO_PAYMENT_LINK into HTML")
        if 'href="https://' in rendered:
            errors.append("internal: placeholder payment must not render a live payment URL")
    elif pay == "live" and html.escape(PAYMENT_LINK_REPO_REALITY, quote=True) not in rendered:
        errors.append("internal: live payment URL missing from Sofort bezahlen")
    if mail == "live":
        if f"mailto:{html.escape(ORDER_CONTACT_EMAIL, quote=True)}" not in rendered:
            errors.append("internal: ORDER_CONTACT_EMAIL missing from the order block")
        if "Repo%20Reality%20Check%20bestellen" not in rendered and "Repo Reality Check bestellen" not in rendered:
            errors.append("internal: mailto subject for order missing")

    for order_page in ORDER_PAGES:
        offer_path = ROOT / order_page
        if not offer_path.is_file():
            errors.append(f"missing page {order_page}")
            continue
        offer_text = offer_path.read_text(encoding="utf-8")
        updated, count = replace_order_blocks(offer_text)
        if count < 1:
            errors.append(f"{order_page}: missing order-block markers")
        elif sync and updated != offer_text:
            offer_path.write_text(updated, encoding="utf-8")
            print(f"SYNC  {order_page}: wrote {count} order block(s) from build.py")
        elif updated != offer_text:
            errors.append(
                f"{order_page}: order block out of sync with PAYMENT_LINK_REPO_REALITY / "
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
    for adir in ASSET_DIRS:
        if not (ROOT / adir).is_dir():
            errors.append(f"missing asset dir {adir}")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for name in PAGES + ASSETS:
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, DIST / name)
    for adir in ASSET_DIRS:
        src = ROOT / adir
        if src.is_dir():
            shutil.copytree(src, DIST / adir)
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
