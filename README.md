# couriersymphony.de

Static site for Courier Symphony — *Ideas travel further.* Plain HTML/CSS, no JavaScript, no cookies, no build dependencies.

- `python3 build.py` → `dist/` (Strato-ready, includes `.htaccess`) and `courier-site-dist.zip`
- `python3 build.py --release` → fails while legal placeholders remain, and while `PAYMENT_LINK_REPO_REALITY` in `build.py` is still `TODO_PAYMENT_LINK`
- Order button and contact line on `repo-reality-check.html` are generated from `PAYMENT_LINK_REPO_REALITY` and `ORDER_CONTACT_EMAIL` in `build.py` (`python3 build.py --sync` rewrites the marked blocks)
- Deployment: see [DEPLOY_STRATO.md](DEPLOY_STRATO.md)
