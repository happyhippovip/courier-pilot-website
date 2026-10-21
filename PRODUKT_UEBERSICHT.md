# 📖 Courier Symphony — Produktübersicht in einfacher Sprache

### Was ist Courier Symphony?
Courier Symphony ist eine **verlässliche Arbeits-Infrastruktur für Künstliche Intelligenz**. 

Während normale KI-Assistenten (wie ChatGPT oder Claude) im Chat-Fenster antworten und bei technischen Fehlern, Systemabstürzen oder falschen Ergebnissen oft unbemerkt scheitern, sorgt Courier Symphony dafür, dass KI-Aufgaben **nachweisbar, fehlertolerant und mathematisch geprüft** zu Ende geführt werden.

---

## Das Kernproblem: Warum normale KI für echte Arbeit oft versagt

1. **Blindes Vertrauen:** Wenn eine Standard-KI eine Tabelle bereinigt oder Programmcode schreibt, sagt sie fast immer: *„Ich habe alles perfekt erledigt!“*. Ob Zeilen fehlen, Zahlen erfunden wurden oder Regeln verletzt wurden, erfährt der Nutzer erst, wenn der Schaden da ist.
2. **Abbrüche ohne Gedächtnis:** Wenn der Laptop zugeklappt wird, die Internetverbindung abreißt oder ein Server-Limit erreicht wird, verliert die KI den Kontext. Die Arbeit bricht ab oder muss von vorne beginnen.
3. **Mangelnde Haftung & Nachweisbarkeit:** Für Unternehmen reicht ein Chat-Text nicht aus. Man braucht einen unveränderlichen Prüfbeleg, wer was wann berechnet und wer es abgenommen hat.

---

## Die Lösung: Das Courier-Symphony-Prinzip

Courier Symphony führt jede Aufgabe durch eine feste Kette aus sechs nachvollziehbaren Stationen:

```text
1. Anfrage       → Was genau soll getan werden? (Zielvertrag & Kriterien)
2. Dispatcher     → Zuweisung an den passenden Worker mit geschützter Lease
3. Agent          → Autonome Durchführung der Arbeit in einer sicheren Umgebung
4. Ergebnis       → Bereitstellung des fertigen Artefakts mit SHA-256 Fingerabdruck
5. Verifier       → Unabhängige Abnahmeprüfung nach festen Regeln (Zero-Trust)
6. Abschluss      → Ausstellung eines manipulationssicheren Siegels (Receipt)
```

### Der Verifier-Unterschied: „Kein Beweis = Keine Abnahme“
Der wichtigste Baustein ist der **Verifier**:
- Der Agent, der die Arbeit erledigt, darf sich **nicht** selbst bewerten.
- Ein unabhängiger Prüfbaustein liest die Rohdaten bytegenau ein und gleicht sie mit dem Zielvertrag ab.
- Stimmt das Ergebnis nicht zu 100% überein, wird die Aufgabe **nicht** als erledigt markiert (`Fail-Closed`).

---

## Typische Einsatzbereiche

1. **Automatisierte Tabellen- und Datenbereinigung:** Tausende Zeilen unstrukturierter Kunden-, Finanz- oder Logistikdaten werden normiert, Dubletten entfernt und das Schema unabhängig validiert.
2. **Code- und Sicherheitsaudits:** Automatische Überprüfung von Software-Patches gegen strikte Sicherheitsrichtlinien (z.B. Schutz vor Datenlöschung).
3. **Plattformübergreifende Dauerläufer:** Aufgaben, die über Nacht auf Linux-, Windows- oder Mac-Maschinen laufen und bei Netzwerkunterbrechungen nahtlos am letzten Checkpoint fortsetzen.

---

## Für wen ist Courier Symphony gedacht?

- **Geschäftsführer & IT-Leiter**, die Routineaufgaben durch KI automatisieren möchten, aber rechtliche oder betriebliche Nachweissicherheit verlangen.
- **Entwickler & DevOps-Teams**, die Multi-Agenten-Systeme stabil über verschiedene Maschinen hinweg orchestrieren wollen.
- **Pilotkunden**, die jetzt im geschlossenen Early-Access-Programm von maßgeschneiderter Absicherung profitieren wollen.
