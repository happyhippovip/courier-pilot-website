# Courier Symphony — Queue Definition: WIN-NEXT-121 bis WIN-NEXT-140
**Autor:** Google Antigravity Windows  
**Datum:** 23. Oktober 2026  
**Ziel:** PWA-Offline-Exzellenz, Erweiterte CSV-Engine (Währungen, Dezimaltrennzeichen, Deduplizierung) & CSP-Sicherheit

---

## 1. Arbeitsaufträge im Detail

### Block 1: PWA & Offline-Infrastruktur (121–125)
- **121:** Definition, Scope-Eingrenzung und Priorisierung.
- **122:** `sw.js` Service Worker für 100% netzunabhängigen Offline-Betrieb (Cache-First-Strategie).
- **123:** `manifest.json` Web App Manifest für Standalone-Messe- und Notebook-Vorführung.
- **124:** Einbindung des Manifests und Apple-Touch-Icon in `demo.html` und `index.html`.
- **125:** Performance-Optimierung: Null Render-Blocking, font-display: swap und instant Cache-Hits.

### Block 2: Erweiterte CSV-Engine (126–130)
- **126:** Internationales Datumsformat (ISO YYYY-MM-DD, US MM/DD/YYYY, EU DD.MM.YYYY).
- **127:** Dezimaltrennzeichen-Konvertierung (deutsches Komma `1.250,50 €` zu standardisiertem Float).
- **128:** Währungssymbol-Harmonisierung (€, EUR, $, USD, CHF).
- **129:** Erkennung und Zählung doppelter Datensätze (Deduplizierungs-Statistik).
- **130:** Detaillierter Audit-Log-Download (JSON mit Vorher/Nachher-Differenzen jeder Zelle).

### Block 3: Barrierefreiheit & Sicherheit (131–135)
- **131:** Screenreader Live-Region (`aria-live="polite"`) für Filter- und Sortieraktionen.
- **132:** High-Contrast Mode Support (`@media (forced-colors: active)`).
- **133:** Semantische Tabellenattribute (`scope="col"` auf allen Kopfzeilen).
- **134:** Strenge Content-Security-Policy (CSP) in `deploy/strato/htaccess` und `dist/.htaccess`.
- **135:** Strict Referrer Policy und Sicherheits-Header (`X-Content-Type-Options: nosniff`).

### Block 4: Build, Test & Handoff (136–140)
- **136:** `build.py` Erweiterung zur automatischen Einbindung von `sw.js` und `manifest.json`.
- **137:** Offline-Betriebsanleitung für Evaluatoren und Förderprüfer.
- **138:** Automatisierte Testsuite `tests/test_next_121_140.js`.
- **139:** Aktualisierung von GitHub PR #11 mit den neuen Commits.
- **140:** Master-Checkpoint und konsolidierte Übergabe.
