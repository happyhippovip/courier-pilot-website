# 🚀 Courier Symphony — Schnellstart-Anleitung für die lokale Demo

Diese Anleitung zeigt, wie Sie die interaktive 30-Sekunden-Produktdemo von Courier Symphony direkt auf Ihrem Rechner öffnen, selbst bedienen und einem Interessenten vorführen können.

---

## 1. Demo im Browser öffnen

Die Demo ist als statische, in sich geschlossene HTML5-Webseite realisiert (ohne Server-Zwang, ohne Node-Daemon, ohne externe Internet-Abhängigkeiten).

### Option A: Per Doppelklick
Navigieren Sie im Windows-Explorer zu folgendem Pfad und öffnen Sie die Datei per Doppelklick in Ihrem Standard-Browser (Chrome, Edge, Firefox, Safari):
```text
C:\Users\lol\2026-workspace\courier-pilot-website\dist\demo.html
```
*(oder die Entwicklungs-Version unter `C:\Users\lol\2026-workspace\courier-pilot-website\demo.html`)*

### Option B: Per Direkt-Link im Browser
Kopieren Sie folgenden Link in die Adresszeile Ihres Browsers:
```text
file:///C:/Users/lol/2026-workspace/courier-pilot-website/dist/demo.html
```

---

## 2. Die 3 Vorführ-Szenarien

In der Demo-Oberfläche können Sie oben aus drei praxisnahen Szenarien wählen:

### 1. Datenbereinigung & Schema-Prüfung (Standard-Erfolgsfall)
- **Problem:** Unsauberer CSV-Export mit 14.280 Zeilen (ungültige Datumsformate, Duplikate).
- **Ablauf:** Worker bereinigt die Daten → Verifier prüft Schema und Byte-Hash unabhängig → Grünes Siegel `BYTE_LEVEL_GOLD_VERIFIED`.
- **Wirkung beim Interessenten:** Zeigt, wie repetitive Datenarbeiten ohne menschliches Nachprüfen fehlerfrei automatisiert werden.

### 2. Code- & Sicherheitsaudit (Security-Erfolgsfall)
- **Problem:** Ein Pull Request soll auf gefährliche Löschbefehle und Systemeingriffe geprüft werden.
- **Ablauf:** Dispatcher sichert Sandbox → Worker führt statische AST-Analyse durch → Verifier testet Fail-Closed-Verhalten → `SECURITY_ACCEPTANCE_PASS`.
- **Wirkung beim Interessenten:** Belegt, dass Courier Symphony selbst bei Code-Änderungen niemals die Kontrolle verliert.

### 3. Manipulierte Daten (Der Aha-Moment / Negativbeispiel!)
- **Problem:** Ein Finanzexport enthält eine Diskrepanz von -1.800,00 €. Der KI-Worker behauptet fälschlich: *„Alles erledigt!“*.
- **Ablauf:** Verifier berechnet die Rohsumme unabhängig, bemerkt die Abweichung und sperrt sofort ab (`FAIL_CLOSED_REJECTED`).
- **Wirkung beim Interessenten:** Das stärkste Verkaufsargument. Es beweist: **Courier Symphony glaubt der KI kein Wort, sondern prüft mathematisch nach.**

---

## 3. Die Steuerungselemente

- **▶ 30s Demo starten:** Startet den vollautomatischen Durchlauf. Alle 4,5 Sekunden leuchtet die nächste Station auf, das Terminal loggt die Ereignisse, und der Fortschrittsbalken füllt sich.
- **Einzelschritt weiter:** Für interaktive Präsentationen, bei denen Sie jeden Schritt einzeln erklären möchten.
- **Zurücksetzen:** Bringt die Simulation in den Ausgangszustand zurück.
- **Prüfnachweis-Karte:** Am Ende erscheint das fertige JSON-Receipt mit SHA-256 Hashes und Prüfstempel.
