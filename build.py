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
    "mitmachen.html",
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
LEGAL_PAGES = ["impressum.html", "datenschutz.html", "widerruf.html"]
# Public contact is e-mail only: no phone numbers, private mailboxes or bank data on any page.
PRIVATE_DATA_RES = [
    ("IBAN-like account number", re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[0-9A-Z]{4}){3,7}")),
    ("tel: link", re.compile(r"href=[\"']tel:", re.I)),
    ("mobile phone number", re.compile(r"(?:\+49[\s/-]?|\b0)1[5-7]\d[\s/-]?\d{3,4}[\s/-]?\d{3,5}\b")),
    ("private GMX/web.de mailbox", re.compile(r"@(?:gmx|web)\.(?:de|net|com)\b", re.I)),
]


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


REPO_PRICE_LABEL = "5 €"
# Shorts-Paket price: single source, change here and run python3 build.py --sync.
VIDEO_PRICE_LABEL = "79 €"
VIDEO_PAGES = ["index.html"]
VIDEO_BLOCK_BEGIN = "<!-- BEGIN:video-block -->"
VIDEO_BLOCK_END = "<!-- END:video-block -->"

PAY_COPY = (
    "Bezahlung per Überweisung erst nach unserer Bestätigung per Mail. "
    "Die Bankverbindung steht nur in dieser Antwort-Mail – nie auf der Website."
)


def _mailto(email: str, subject: str, body: str) -> str:
    esc = html.escape(email, quote=True)
    return f"mailto:{esc}?subject={quote(subject)}&amp;body={quote(body)}"


def render_order_block(payment: str = PAYMENT_LINK_REPO_REALITY, email: str = ORDER_CONTACT_EMAIL) -> str:
    """Repo-Check order slot: mailto (primary), bank transfer after confirmation.

    Bank details are never inlined; the reply mail carries them. No checkout:
    the optional Sofort-bezahlen link renders only when PAYMENT_LINK_REPO_REALITY is live.
    """
    pay = payment_state(payment)
    mail = email_state(email)
    copy = (
        f'<p class="order-pay">{PAY_COPY} Lieferung des Reports innerhalb von 48&nbsp;Stunden '
        'nach Zahlungseingang.</p>'
    )
    if mail == "live":
        esc = html.escape(email, quote=True)
        body = (
            "Hallo Courier Symphony,\n\n"
            "ich möchte einen Repo Reality Check (Beta, 5 EUR per Überweisung) bestellen.\n\n"
            "Öffentlicher GitHub-Link: https://github.com/OWNER/REPO\n"
            "Was soll geprüft werden (optional): \n"
            "Mein Name: \n\n"
            "Ich stimme ausdrücklich zu, dass ihr vor Ablauf der Widerrufsfrist mit dem Report beginnt, "
            "und weiß, dass ich mit Beginn der Ausführung mein Widerrufsrecht verliere "
            "(siehe Widerrufsbelehrung auf couriersymphony.de).\n\n"
            "Bitte bestätigt die Bestellung und schickt mir die Bankverbindung.\n\n"
            "Danke"
        )
        mailto_cta = (
            f'<a class="btn" href="{_mailto(email, "Repo Reality Check bestellen", body)}">'
            f'Repo-Check bestellen – {REPO_PRICE_LABEL}</a>'
        )
        contact = f'<p class="fine">Fragen: <a href="mailto:{esc}">{esc}</a></p>'
    elif mail == "placeholder":
        mailto_cta = f'<button type="button" class="btn is-disabled" disabled>Repo-Check bestellen – {REPO_PRICE_LABEL}</button>'
        contact = '<p class="fine">Fragen zur Bestellung: die Kontaktadresse ist noch nicht hinterlegt.</p>'
    else:
        mailto_cta = "<!-- invalid ORDER_CONTACT_EMAIL -->"
        contact = "<!-- invalid ORDER_CONTACT_EMAIL -->"
    parts = [copy, mailto_cta]
    if pay == "live":
        parts.append(f'<a class="btn btn-ghost" href="{html.escape(payment, quote=True)}">Sofort bezahlen</a>')
    elif pay == "invalid":
        parts.append("<!-- invalid PAYMENT_LINK_REPO_REALITY -->")
    parts.append(contact)
    return "\n".join(parts)


def render_video_block(email: str = ORDER_CONTACT_EMAIL, price: str = VIDEO_PRICE_LABEL) -> str:
    """Video-Schnitt (Shorts-Paket) request slot: mailto only, same payment rule."""
    price_txt = price.replace("\u00a0", " ").replace("€", "EUR")
    body = (
        "Hallo Courier Symphony,\n\n"
        f"ich möchte das Shorts-Paket anfragen (10 Clips aus einem Langvideo, {price_txt}, Überweisung nach Bestätigung).\n\n"
        "Link zum langen Video (z. B. YouTube, Cloud-Ordner): \n"
        "Länge des Videos: \n"
        "Plattform (YouTube Shorts / Instagram Reels / TikTok): \n"
        "Wünsche zum Stil (optional): \n"
        "Mein Name: \n\n"
        "Ich bestätige, dass ich die Rechte am Videomaterial habe und die gezeigten Personen einverstanden sind.\n\n"
        "Ich stimme ausdrücklich zu, dass ihr vor Ablauf der Widerrufsfrist mit dem Schnitt beginnt, "
        "und weiß, dass ich mit Beginn der Ausführung mein Widerrufsrecht verliere "
        "(siehe Widerrufsbelehrung auf couriersymphony.de).\n\n"
        "Bitte bestätigt den Auftrag mit Lieferzeit und schickt mir dann die Bankverbindung.\n\n"
        "Danke"
    )
    return "\n".join([
        f'<p class="order-pay">{price} pro Paket, verbindlich erst mit unserer Bestätigung per Mail; '
        f'die Lieferzeit nennen wir in der Bestätigung. {PAY_COPY}</p>',
        f'<a class="btn" href="{_mailto(email, f"Video-Schnitt anfragen (Shorts-Paket {price_txt})", body)}">'
        f'Shorts-Paket – 10 Clips aus einem Langvideo: {price}</a>',
        '<p class="fine">Erster Probe-Clip kostenlos.</p>',
    ])


def marked_video_block() -> str:
    return f"{VIDEO_BLOCK_BEGIN}\n{render_video_block()}\n{VIDEO_BLOCK_END}"


def replace_video_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(re.escape(VIDEO_BLOCK_BEGIN) + r".*?" + re.escape(VIDEO_BLOCK_END), re.DOTALL)
    count = len(pattern.findall(text))
    return pattern.sub(lambda _: marked_video_block(), text), count


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
        if "Sofort bezahlen" in rendered:
            errors.append("internal: no checkout/payment control may render without a live payment link")
        if "TODO_PAYMENT_LINK" in rendered:
            errors.append("internal: placeholder payment must not leak TODO_PAYMENT_LINK into HTML")
        if 'href="https://' in rendered:
            errors.append("internal: placeholder payment must not render a live payment URL")
    elif pay == "live" and html.escape(PAYMENT_LINK_REPO_REALITY, quote=True) not in rendered:
        errors.append("internal: live payment URL missing from Sofort bezahlen")
    if pay == "live":
        warnings.append(
            "PAYMENT_LINK_REPO_REALITY is live: name that payment provider in datenschutz.html section 6 before release"
        )
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

    for vpage in VIDEO_PAGES:
        vpath = ROOT / vpage
        vtext = vpath.read_text(encoding="utf-8") if vpath.is_file() else ""
        vupd, vcount = replace_video_blocks(vtext)
        if vcount < 1:
            errors.append(f"{vpage}: missing video-block markers")
        elif sync and vupd != vtext:
            vpath.write_text(vupd, encoding="utf-8")
            print(f"SYNC  {vpage}: wrote {vcount} video block(s) from build.py")
        elif vupd != vtext:
            errors.append(f"{vpage}: video block out of sync with VIDEO_PRICE_LABEL (run python3 build.py --sync)")
        if "IBAN" in render_video_block():
            errors.append("internal: bank data must never appear in the video block")

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
        for label, rx in PRIVATE_DATA_RES:
            if rx.search(text):
                errors.append(f"{page}: {label} must not appear on the public site")
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
