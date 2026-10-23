# Courier Symphony — Offline-Betriebsanleitung für Evaluatoren & Förderprüfer
**Version:** 1.0.0 (Release Candidate)  
**Autor:** Google Antigravity Windows  
**Datum:** 23. Oktober 2026  
**Zielgruppe:** NBank-Gutachter, Förderprüfer, Kanzlei-Evaluatoren, Messe-Demonstratoren

---

## 1. Zero-Cloud & 100% Offline-Garantie
Courier Symphony benötigt zur vollständigen Ausführung **keine Internetverbindung**, **keine externen APIs**, **keine Cloud-Server** und **keine Node.js/Python-Laufzeit** auf dem Zielgerät des Prüfers.

Alle Berechnungs-, Validierungs-, Normalisierungs- und kryptografischen Hashing-Vorgänge laufen lokal in der V8/SpiderMonkey/WebKit-Engine des Browsers:
- **Zero Third-Party Skripte:** Keine externen CDNs (kein Google Fonts, kein Bootstrap, kein CDNJS).
- **Keine Tracking-Pixel:** 100% DSGVO-konform ohne Cookie-Banner oder Datenübertragung.
- **Kryptografische Integrität:** Deterministische SHA-256 Receipts über WebCrypto API (`crypto.subtle.digest`).

---

## 2. Vorbereitung vor Ort (Messe / Förder-Präsentation)

### Option A: USB-Stick (Direktstart via `file://`)
1. Stecken Sie den freigegebenen USB-Stick an einen beliebigen Windows-, Mac- oder Linux-PC.
2. Öffnen Sie den Ordner `NBANK_PRAESENTATION_2026-10-26`.
3. Doppelklicken Sie auf `offline_demo.html`.
4. Der Standard-Browser öffnet die Demo im Offline-Modus.

### Option B: PWA-Offline-Installation (Webserver oder Localhost)
1. Wenn die Seite über einen lokalen HTTP-Server (`http://localhost:...`) oder HTTPS aufgerufen wurde, registriert der Service Worker (`sw.js`) automatisch alle 27 Kern-Assets im Browser-Cache.
2. Klicken Sie in der Browser-Adressleiste auf das Installations-Symbol ("App installieren").
3. Die Offline Reality Demo kann nun komplett ohne Netzwerkverbindung wie eine native Desktop-App gestartet werden.

---

## 3. Standard-Testabläufe für die Vorführung

### 90-Sekunden-Blitztest: "Vertriebs-Leads Bereinigen"
1. Klicken Sie auf den Button **"90s Leads"**.
2. Die Rohdaten mit gemischter Groß-/Kleinschreibung (`mAx MUSTERMANN`), unbereinigten Telefonnummern (`+49 (0) 89 1234567`) und Leerzeichen werden geladen.
3. Klicken Sie auf **"▶ Tabelle bereinigen & verifizieren"**.
4. **Ergebnis:**
   - Namen sind in sauberem Title-Case (`Max Mustermann`).
   - Telefonnummern sind normiert (`+49891234567`).
   - Ein SHA-256-Audit-Zertifikat wird generiert.

### 5-Minuten-Tiefenprüfung: "Buchhaltungsdaten & Währungen"
1. Klicken Sie auf **"5m Buchhaltung"**.
2. Die Rohdaten enthalten deutsche Währungsformate (`1.250,50 €`), uneinheitliche Datumsformate (`14.10.26`) und Zeilenduplikate.
3. Aktivieren Sie alle Bereinigungsregeln:
   - Leerzeichen trimmen
   - Telefon normieren
   - E-Mail lowercase
   - Namen Title-Case
   - Datum in ISO-8601 (`2026-10-14`)
   - Beträge & Währung normieren (`1250.50 EUR`)
   - Exakte Duplikate filtern
4. Klicken Sie auf **"▶ Tabelle bereinigen & verifizieren"**.
5. Klicken Sie auf **"Nur geänderte Zeilen"**, um sofort alle Korrekturen mit Durchstreichung der Originalwerte zu sehen.
6. Klicken Sie auf **"📑 Audit-Log (JSON)"** oder **"📜 Audit-Zertifikat (JSON)"**, um den manipulationssicheren Prüfnachweis herunterzuladen.

### Fehler-Resilienztest: "Defekte CSV / Semikolon-Trennzeichen"
1. Klicken Sie auf **"Fehlerfall"**.
2. Die Rohdaten simulieren einen unvollständigen Export mit fehlenden Spalten und abweichendem Trennzeichen.
3. Die Engine erkennt automatisch das Trennzeichen, füllt fehlende Spalten auf und blendet einen strukturierten Hinweiskasten ein, ohne abzustürzen.

---

## 4. Prüfsummen-Verifikation des Pakets
Auf dem USB-Stick oder im Evaluierungsordner kann die Unverfälschtheit aller Dateien jederzeit nachgewiesen werden:

```powershell
# Windows PowerShell
Get-FileHash -Algorithm SHA256 * | Format-Table -AutoSize
```

Vergleichen Sie die Ausgaben mit der mitgelieferten Datei `CHECKSUMS_SHA256.txt`. Jede Datei stimmt bis auf das letzte Byte überein.
