# Courier Symphony — Release Engineering Plan V1
**Workkeys:** WIN-IMP-071 bis WIN-IMP-080  
**Autor:** Google Antigravity Windows  
**Datum:** 23. Oktober 2026  
**Zielbranch:** `site/repo-reality-beta`  
**Feature-Branch:** `feature/win-imp-demo-fixes`  
**Remote-URL:** `https://github.com/happyhippovip/courier-pilot-website.git`

---

## 1. WIN-IMP-071: Branch-Divergenz-Analyse
- **Gemeinsamer Vorfahre (Merge Base):** Ermittelt über Git-Historie.
- **Remote `origin/site/repo-reality-beta`:** 7 Commits voraus (`c25d6c0` bis `fd76931`). Fokus: `konzept.html`, Bildassets in `assets/konzept/`, mobile Navigation und Überweisungstext.
- **Lokal `feature/win-imp-demo-fixes`:** Beinhaltet Delta 100-183 sowie die gehärteten Fixes WIN-IMP-001 bis 070.
- **Konfliktanalyse (WIN-IMP-072):**
  - `demo.html` wurde im Remote-Branch **nicht verändert**.
  - Unsere Fixes (TDZ-Beseitigung, Mailto-Harmonisierung, 5MB Upload-Grenze) sind im Dateibaum isoliert.
  - Testdateien `tests/test_phase_*.js` existieren nur auf unserem Feature-Branch.
  - Konfliktrisiko beim Zusammenführen: **0% (Clean Fast-Forward / Merge)** für alle Demo-Dateien.

---

## 2. WIN-IMP-073: Commit-Inventar (Feature-Branch)
| Commit SHA | Typ / Scope | Beschreibung |
|---|---|---|
| `cd72e2c` | `fix(demo)` | Beseitigung der TDZ-Fehler für `demoSpeed` und `stopwatchTimerId` (WIN-IMP-001 bis 010) |
| `a668480` | `test(csv)` | Testsuite für Semikolon-Parsing, DATEV-Heuristik, BOM & UTF-8 (WIN-IMP-011 bis 020) |
| `00519cb` | `test(a11y)` | WCAG 2.2 Suite: Reduced Motion, Focus-Visible, Skip-Links, ARIA (WIN-IMP-021 bis 030) |
| `ebc6e49` | `fix(website)` | Einheitliche Kontaktadresse (`founder@couriersymphony.de`) & Routing (WIN-IMP-031 bis 040) |
| `2aa1d31` | `test(build)` | Build-Reproduzierbarkeit, Manifest, Release-Gate & Windows-Encoding (WIN-IMP-041 bis 050) |
| `1ffc22b` | `security(demo)` | 5MB Dateiupload-Grenze, XSS-Filterung & Security-Tests (WIN-IMP-051 bis 060) |
| `0fceb8a` | `docs(compliance)` | Produkt-Wahrheitsmatrix & Transparenzprüfungen (WIN-IMP-061 bis 070) |

---

## 3. WIN-IMP-074: Minimaler Integrationsplan
1. Alle Änderungen sind atomar auf `feature/win-imp-demo-fixes` gepusht.
2. Der Feature-Branch kann via GitHub PR `#<ID>` von Dennis oder GrokBot begutachtet werden.
3. Kein Force-Push (`--force` verboten).
4. Nach Review: Squash- oder Merge-Commit in `site/repo-reality-beta`.

---

## 4. WIN-IMP-076: Release Notes (`v0.9.3-beta.windows.1`)
### Behoben (Fixes)
- **Kritischer Laufzeitfehler (TDZ):** `ReferenceError: Cannot access 'demoSpeed' before initialization` in `demo.html` und `offline_demo.html` behoben.
- **Stopwatch-TDZ:** `stopwatchTimerId`, `stopwatchStartTime` und `stopwatchElapsed` in den oberen Skript-Scope verschoben.
- **Kontaktkonsistenz:** Veraltete Dummy-Domain `pilot@couriersymphony.com` durch die verifizierte Adresse `founder@couriersymphony.de` ersetzt.
- **Sicherheitsgrenze für Dateiuploads:** Browserseitiges Limit von 5 MB in `handleFile()` implementiert, um Speicherüberläufe und Browserabstürze zu verhindern.

### Neu (Features & Tests)
- **Automatisierte Testsuiten:** 7 neue JavaScript-Testsuiten unter `tests/` für Phasen A bis G.
- **Produkt-Wahrheitsmatrix:** Vollständige Dokumentation in `PRODUKT_WAHRHEITSMATRIX.md`.
- **Förderpaket-Prüfsummen:** Aktualisierte SHA-256 Hashes in `CHECKSUMS_SHA256.txt`.

---

## 5. WIN-IMP-077 & 078: Versionskennzeichnung & Rollback-Plan
- **Version:** `v0.9.3-beta.windows.1`
- **Rollback-Strategie:**
  - Da alle Commits atomar sind, kann jeder Einzelschritt via `git revert <SHA>` rückgängig gemacht werden.
  - Ausgangs-Commit: `b1dd142`.

---

## 6. WIN-IMP-079 & 080: PR-Vorbereitung & Release-Kandidat
- **PR-Titel:** `fix(demo): eliminate TDZ runtime errors, enforce 5MB limits and add regression test suites`
- **Zielbranch:** `site/repo-reality-beta`
- **Release-Gate Status:** Blockiert wie vorgesehen `build.py --release` bis zur Eintragung der Zahlungsdaten durch Dennis.
