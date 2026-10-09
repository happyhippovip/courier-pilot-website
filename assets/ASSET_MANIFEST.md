# Website visual asset manifest

Recovered from the existing PR #3 / PR #5 stack on `courier-pilot-website`.
Machine-readable hashes: `ASSET_MANIFEST.json`.

## Access note

```
IMAGE_ACCESS_REQUIRED: Robfort / Grokbot prepared images (provider unverified from this session)
EXACT_PROVIDER: unknown — founder reports “Robfort”; not accessible here
REQUIRED_EXPORT: approved original image files + usage rights note
DESTINATION: assets/ (source of truth) → copied into release via build.py
```

Private memory repo `happyhippovip/2026-project-memory` was not readable (404).
No authorized Robfort/Grok artifact channel was available to this session.

## Courier-owned assets already in-repo

| Path | Used on | Rights |
|---|---|---|
| `assets/konzept/*.webp` | `konzept.html` gallery + thumbs | Courier Konzept / concept preview |
| `assets/konzept/*.mp4` + posters | `konzept.html` clips | Courier Konzept / concept preview |
| `og-cover.png` | Open Graph | Courier site chrome |
| `favicon.svg`, `apple-touch-icon.png` | Site chrome | Courier site chrome |

Do not treat Konzept images as customer metrics, revenue proof, or shipped product UI.
Originals stay under `assets/`; `python3 build.py --release` copies them into `dist/assets/`.
