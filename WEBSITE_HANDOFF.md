# Courier website — coordination handoff

Verified 2026-10-09 against `happyhippovip/courier-pilot-website` remotes, open PRs, CI, and cloud-agent metadata. No merges, no design replacement, no new site.

## WEBSITE_BASELINE

**PR #5** — draft, `cursor/copy-truth-pass-f9b1` → `site/repo-reality-beta`  
https://github.com/happyhippovip/courier-pilot-website/pull/5  
SHA `1ed1773` — honest Early Access copy; no 5 € / 79 € public prices; Repo Reality Check as labeled concept/demo; legal pages + `build.py` + tests inherited from PR #3.

Do **not** treat live `main` (`ed947dc`) as the customer baseline: it still ships “Production-Grade” / “mathematical guarantees” / Enterprise air-gapped claims, has no `impressum.html`, and is a thin static tree (no `build.py`).

## VERIFIED_EXISTING_PR

| Known item | Actual state |
|---|---|
| Customer-ready copy | **PR #5** open draft; agent IDLE; CI green |
| Repo Reality Check beta page | **PR #3** open draft (`site/repo-reality-beta`); page present; still has 5 € / 79 € mail-order CTAs; agent run **ERROR** but branch/PR saved |
| Launch-ready static site | **PR #2** open draft (`site/strato-launch-ready`); superseded/absorbed into PR #3 ancestry; conflicts with `main` |
| Test run — no changes | Agent `bc-01a12058-…` IDLE; no PR; no diff |

Related: **PR #4** DNS docs (`site/strato-domain-ready` → `site/strato-launch-ready`) — CI green, MERGEABLE; **not** in the PR #5 stack.

## CHECKS

| PR | `site-check` / build | Mergeability |
|---|---|---|
| #5 | **SUCCESS** | MERGEABLE into `site/repo-reality-beta` |
| #4 | **SUCCESS** | MERGEABLE into `site/strato-launch-ready` |
| #3 | **SUCCESS** | **CONFLICTING** vs `main` (`index.html`, `styles.css`, `sitemap.xml`) |
| #2 | **SUCCESS** | **CONFLICTING** vs `main` |
| #1 | no checks | **CONFLICTING**; superseded by #2 |

`main` Pages builds succeed; custom domain is set on GH Pages but public DNS is not cut over.

## FAILED_TASKS

1. **Agent “Repo Reality Check beta”** (`bc-97935103-…`) — lifecycle **ERROR**; PR #3 still exists and CI is green.
2. **Internal mobile walkthrough / video-review agents** — three runs **ERROR** (no usable site baseline from them).
3. **DNS / public domain** — `couriersymphony.de` → Strato `217.160.0.46` parking (“Domain reserved”); HTTPS handshake fails; GH Pages redirects project URL to the custom domain that is not live yet.
4. **PR #3 → `main`** — dirty/conflicting; also must **not** merge alone (would publish paid 5 € / 79 € buttons).
5. **MCP Outlook auth** soft-failed on the PR #5 agent run (non-blocking).

## CUSTOMER_READINESS

- **Live `main`:** not customer-honest (overclaims; missing DE legal pages).
- **Draft stack PR #3+#5:** customer-ready copy + legal/build tooling exist remotely; stacked; not on `main`; DNS/HTTPS go-live still owner-gated.
- **PR #5 alone** is the truth-pass; **PR #3 tip is its base**.

## NEXT_WEBSITE_ACTION

**Restack PR #5 onto current `main` (or merge #5→#3 tip first, then rebase that tip onto `main`), resolving conflicts in `index.html` / `styles.css` / `sitemap.xml`, keeping Early Access / prototype labeling and dropping paid CTAs + Production-Grade claims — then owner-only DNS per PR #4.**

Do not merge #3 without #5. Do not cut DNS until that restacked tip is the intended publish tree.

## HANDOFF_FOR_COURIER_PROJECT

Use **website PR #5** as the product-facing baseline for Courier Symphony coordination.

- Product evidence link already cited in PR #5: `2026-courier` PR #361 (hard kill / restart / 0 duplicate tasks / CI 12/12 / synthetic adapter).
- Public CTA: Early Access mailto `founder@couriersymphony.de` only — no checkout, no prices on public pages.
- Coordinator decisions still required: (1) approve restack-to-`main` + merge order #5 then #3 tip; (2) owner Strato DNS + GH Pages Enforce HTTPS (PR #4 / `docs/STRATO_DNS.md`); (3) tax/approval before un-hiding support section.
- Preserve design; do not spawn parallel new website workstreams.
