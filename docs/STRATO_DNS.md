# STRATO-DNS für couriersymphony.de (GitHub Pages)

Stand: vorbereitet, **nicht veröffentlicht**. Diese Anleitung ändert nichts
automatisch — alle Schritte im STRATO-Kundenbereich macht der Inhaber selbst.
Grundlagen zum SFTP-/Hosting-Weg stehen in [DEPLOY_STRATO.md](../DEPLOY_STRATO.md);
dort steht auch, welches STRATO-Paket welchen Weg braucht.

Die IP-Adressen unten sind gegen die offizielle GitHub-Pages-Dokumentation geprüft:
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Voraussetzung

- STRATO-Paket mit Domainverwaltung (reines Domain-Paket genügt, Webspace ist
  nicht nötig).
- Die Website wird von GitHub Pages ausgeliefert (Datei `CNAME` im Repo enthält
  `couriersymphony.de`).

## Schritt 1: Alte Einträge entfernen

1. Im STRATO-Kundenbereich anmelden → **Domains → Domainverwaltung** →
   Zahnrad bei `couriersymphony.de` → **DNS**.
2. Bestehende Einträge für `@` (manchmal „Root“ oder leer) vom Typ **A** und
   **AAAA** entfernen oder ersetzen — besonders STRATO-Standard- oder
   Parking-Einträge.
3. Bestehende Einträge für **www** vom Typ **A**/**AAAA** entfernen.
4. Grund: Übrig gebliebene Einträge leiten Besucher weiter auf die alte
   STRATO-Seite und verhindern, dass GitHub das HTTPS-Zertifikat ausstellt.

## Schritt 2: Apex-Einträge für couriersymphony.de anlegen

Vier **A-Records** für `@`:

- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

Vier **AAAA-Records** für `@`:

- `2606:50c0:8000::153`
- `2606:50c0:8001::153`
- `2606:50c0:8002::153`
- `2606:50c0:8003::153`

Falls das STRATO-Formular nur eine IP pro Feld zulässt: jede Adresse in ein
eigenes Feld bzw. einen eigenen Eintrag schreiben. Falls nur ein Eintrag
möglich ist, eine der vier A-Adressen nehmen (alle vier sind besser).

## Schritt 3: www-Subdomain anlegen

- Subdomain **www** als **CNAME** auf `happyhippovip.github.io` zeigen lassen.
- **MX-Records nicht ändern** — sonst funktioniert `founder@couriersymphony.de`
  nicht mehr (siehe [DEPLOY_STRATO.md](../DEPLOY_STRATO.md), Weg B).

## Schritt 4: GitHub-Seite einstellen

1. Im GitHub-Repo **Settings → Pages** → **Custom domain**:
   `couriersymphony.de` eintragen und speichern.
2. Warten, bis die DNS-Prüfung erfolgreich ist.
3. Danach **„Enforce HTTPS“** anhaken. Das Zertifikat kann bis zu ca.
   1 Stunde dauern. Erscheint es nicht: Custom Domain entfernen, kurz warten,
   erneut eintragen.
4. Hinweis: GitHub Pages ignoriert `.htaccess` — HTTPS und Caching regelt dort
   GitHub.

## Schritt 5 (empfohlen): Domain für das GitHub-Konto verifizieren

1. GitHub → Profil-**Settings → Pages → Verified domains** → Domain hinzufügen.
2. Den angezeigten **TXT-Record** im STRATO-DNS-Panel anlegen.
3. Schützt davor, dass andere Konten die Domain für ihre Pages-Sites nutzen.

## Schritt 6: Prüfen

```bash
dig +short A couriersymphony.de
dig +short AAAA couriersymphony.de
dig +short CNAME www.couriersymphony.de
curl -I https://couriersymphony.de
```

Auf Windows ohne `dig` stattdessen:

```cmd
nslookup couriersymphony.de
nslookup www.couriersymphony.de
```

Erwartete Ergebnisse:

- Die A-Abfrage listet die vier `185.199.10x.153`-Adressen.
- Die AAAA-Abfrage listet die vier `2606:50c0:800x::153`-Adressen.
- Die www-Abfrage zeigt `happyhippovip.github.io`.
- `curl -I` antwortet mit `HTTP/2 200` (nach kurzer DNS-Verbreitung; weltweit
  kann es bis zu ca. 24 Stunden dauern, meist geht es deutlich schneller).
