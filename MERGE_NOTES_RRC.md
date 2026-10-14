# Merge-Notizen: site/rrc-go-live (2026-10-14)

Basis: `origin/site/repo-reality-beta`, gemergt mit `origin/main` (`--allow-unrelated-histories`).

## Konflikte und Entscheidungen
- `index.html`: Branch-Version behalten (Bestellblöcke, Rechtsseiten-Links, Konzept-Bilder). Die englische Main-Version (Hero-Metrikleiste, Fault-Injection-Simulator, PID-Doku) ersetzt die Startseite nicht; sie kann später gezielt übernommen werden.
- `sitemap.xml`: Branch-Version behalten, weil sie alle 13 Seiten inkl. Impressum, Datenschutz, Widerruf und Repo-Check listet (main listet nur 2 Seiten). Main-Metadaten (lastmod/changefreq) bewusst nicht übernommen.
- `styles.css`: Branch-Version behalten; Main-only Styles gehören zur Main-Startseite und werden hier nicht gebraucht.
- Alle anderen Dateien aus main ohne Konflikt übernommen.

## Mac-Patch
`rrc_uncommitted_2026-10-13.patch` (Customer Proof Card) angewendet; Konflikt in `styles.css` per Vereinigung gelöst (bestehende Mitmachen/Order-Styles + neue Proof-Card-Styles).

## Angebot
- Pakete nur mit dem, was `scripts/repo_reality_check.py` (2026-courier) liefert: Free 0 € (Anzahl nach Schwere + Top 3 per Mail), Basis 1,99 € (report.md), Plus 2,99 € (+ report.pdf/report.json + kurze Einordnung), Großes Paket 4,99 €/Monat Einführungspreis (monatlicher Re-Scan, kündbar zum Monatsende, regulärer Preis später höher).
- Entfernt: Reality-Score 0–100, „5 wichtigste nächste Schritte“, Test-/TODO-Zählung (liefert das Skript nicht), 5-€-Preis, Stripe-Testlink.
- Bestellung per mailto an founder@couriersymphony.de mit Paket, Zahlungsart (PayPal/Überweisung/Karte-Stripe), Repo-URL. „Zahlung erst nach Bestätigung, Zahlungsdetails per Mail“.
- § 19 UStG-Hinweis vorbereitet, aber per `SHOW_USTG19_NOTE = False` ausgeschaltet (Dennis muss Steuerstatus bestätigen).
- Datenschutz Abschnitt 6 nennt jetzt PayPal und Stripe.
