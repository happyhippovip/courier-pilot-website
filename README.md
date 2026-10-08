# couriersymphony.de

Static site for Courier Symphony — *Ideas travel further.* Plain HTML/CSS, no JavaScript, no cookies, no build dependencies.

- `python3 build.py` → `dist/` (Strato-ready, includes `.htaccess`) and `courier-site-dist.zip`
- `python3 build.py --release` → fails while legal placeholders (`class="ph"` / `data-placeholder`) remain or a page carries private data (IBAN-like numbers, phone numbers, `tel:` links, GMX/web.de mailboxes); a missing optional `PAYMENT_LINK_REPO_REALITY` is only a warning (Überweisung via mailto is the live order path)
- Order button and contact line on `repo-reality-check.html` are generated from `PAYMENT_LINK_REPO_REALITY` and `ORDER_CONTACT_EMAIL` in `build.py` (`python3 build.py --sync` rewrites the marked blocks)
- Deployment: see [DEPLOY_STRATO.md](DEPLOY_STRATO.md)
