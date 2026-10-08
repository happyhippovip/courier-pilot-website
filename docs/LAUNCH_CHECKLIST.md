# Launch-Checkliste: von „DNS gesetzt“ bis „live“

- [ ] DNS im STRATO-Panel gesetzt ([STRATO_DNS.md](STRATO_DNS.md), Schritte 1–3).
- [ ] DNS-Prüfung bestanden: `dig`-/`nslookup`-Ergebnisse wie in
  [STRATO_DNS.md](STRATO_DNS.md), Schritt 6 beschrieben.
- [ ] GitHub → **Settings → Pages** → Custom domain `couriersymphony.de`
  eingetragen und DNS-Check grün.
- [ ] **Enforce HTTPS** aktiviert (Zertifikat kann bis zu ca. 1 Stunde dauern).
- [ ] Impressum (`impressum.html`) und Datenschutz (`datenschutz.html`) mit den
  echten Inhaberdaten ausgefüllt: alle `[…]`-Platzhalter ersetzt, den
  gestrichelten Hinweiskasten (`data-placeholder="true"`) gelöscht.
  Die Daten trägt der Inhaber selbst ein — hier stehen keine Namen/Adressen.
- [ ] `python3 build.py --release` zeigt `RESULT OK`.
- [ ] Erst dann: in `main` mergen. **Der Merge nach `main` ist der Go-live**
  (GitHub Pages veröffentlicht sofort). Vorher nichts mergen.
- [ ] Nach dem Go-live: `https://couriersymphony.de/` lädt, `http://` und
  `https://www.` landen auf der kanonischen Adresse.
