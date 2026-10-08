# Deploy: couriersymphony.de (STRATO)

Status: **vorbereitet, nicht veröffentlicht.** Nichts in diesem Repo lädt automatisch zu STRATO hoch.

## 0. Wichtig vorab: Welches STRATO-Paket?

| Paket | Webspace / SFTP | Was geht |
|---|---|---|
| **STRATO Domain** (nur Domain + Postfach) | **Nein** – laut STRATO-FAQ kein Speicherplatz, keine SFTP-Verbindung | Seite woanders hosten (z. B. GitHub Pages, kostenlos) und die Domain per DNS dorthin zeigen → **Weg B** |
| **STRATO Hosting** (Starter/Basic/Plus …) | Ja, SFTP (Port 22), Apache mit `.htaccess`, PHP | Dateien hochladen → **Weg A** |

Node.js läuft auf STRATO-Webhosting nicht (nur V-Server/Dedicated). Diese Seite braucht kein Node und kein PHP: reines HTML/CSS, kein JavaScript.

## 1. Build (beide Wege)

```bash
python3 build.py            # baut dist/ und courier-site-dist.zip, prüft Links/Anker/Assets
python3 build.py --release  # wie oben, schlägt aber fehl, solange Impressum/Datenschutz Platzhalter enthalten
```

Ergebnis: Ordner `dist/` (12 Dateien inkl. `.htaccess`). Den fertigen Ordner gibt es auch als CI-Artefakt `courier-site-dist` im Workflow **site-check**.

**Vor dem Go-live:** in `impressum.html` und `datenschutz.html` alle gelben `[…]`-Platzhalter ersetzen, den gestrichelten Hinweiskasten (`data-placeholder="true"`) löschen, dann `python3 build.py --release` muss `RESULT OK` zeigen.

## Weg A – STRATO Hosting-Paket (SFTP-Upload)

1. STRATO-Login → Paket → **Datenbanken und Webspace → SFTP & SSH** → Zugang anlegen oder vorhandenen nutzen. Notiere Server (Form `5xxxxxxxx.ssh.w2.strato.hosting`), Benutzername, Port 22. Passwort nur im Passwortmanager, **nie** ins Repo.
2. STRATO-Login → **Domains → Domainverwaltung**: prüfen, auf welches Zielverzeichnis `couriersymphony.de` zeigt (z. B. `/` oder `/couriersymphony`). Dieses Verzeichnis ist der Web-Root.
3. FileZilla (Protokoll **SFTP**, nicht FTP) verbinden, in den Web-Root wechseln.
4. **Den Inhalt** von `dist/` hochladen (nicht den Ordner selbst): `index.html`, `impressum.html`, `datenschutz.html`, `privacy.html`, `404.html`, `styles.css`, `favicon.svg`, `apple-touch-icon.png`, `og-cover.png`, `robots.txt`, `sitemap.xml` **und `.htaccess`** (in FileZilla „Versteckte Dateien anzeigen“ aktivieren).
5. HTTPS: STRATO-Login → **SSL** → Zertifikat der Domain zuweisen (inklusive www) → **„SSL erzwingen“ → permanente Weiterleitung (301)**. Die `.htaccess` leitet zusätzlich http→https und www→ohne www um.
6. Prüfen: `https://couriersymphony.de/` lädt, `http://` und `https://www.` leiten auf `https://couriersymphony.de/` um, `/gibtsnicht` zeigt die 404-Seite.
7. Erst wenn alles über HTTPS funktioniert: in `.htaccess` die HSTS-Zeile einkommentieren und erneut hochladen.

Bei GitHub-Pages-Wechsel zu STRATO: in `datenschutz.html` unter „Hosting“ STRATO stehen lassen und GitHub löschen.

## Weg B – Nur STRATO Domain (kostenlos, aktueller Stand)

Die Seite wird bereits von GitHub Pages aus dem Branch `main` dieses Repos ausgeliefert (`CNAME` = `couriersymphony.de`). Es fehlt nur der DNS-Eintrag bei STRATO (Stand 2026-10-08 zeigt die Domain noch auf die STRATO-Standard-IP):

1. STRATO-Login → **Domains → Domainverwaltung** → Zahnrad bei `couriersymphony.de` → **DNS**.
2. **A-Record** → „Eigene IP-Adresse“ → GitHub-Pages-IPs: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (falls nur eine IP möglich ist: eine davon).
3. **www**: Subdomain `www` anlegen und als **CNAME** auf `happyhippovip.github.io` setzen.
4. **MX-Records nicht ändern** (sonst bricht `founder@couriersymphony.de`).
5. Nach der DNS-Umstellung: GitHub → Repo **Settings → Pages** → „Enforce HTTPS“ aktivieren, sobald das Zertifikat bereitsteht.
6. Hinweis: GitHub Pages ignoriert `.htaccess`; HTTPS und Caching regelt dort GitHub.

## Was nicht automatisch passiert

- Kein Upload, kein DNS-Wechsel, kein Kauf. Login, 2FA, Passwörter und DNS-Änderungen macht Dennis selbst oder gibt sie ausdrücklich frei.
- Ein Merge nach `main` veröffentlicht über GitHub Pages sofort – deshalb erst Platzhalter füllen, dann mergen.
