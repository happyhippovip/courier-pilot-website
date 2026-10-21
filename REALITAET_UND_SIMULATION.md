# ⚖️ Courier Symphony — Realität vs. Simulation (Transparenz-Matrix)

Im Sinne der Grundregeln von Project Memory und der internen Governance dokumentiert dieses Dokument lückenlos und ungeschönt, welche Komponenten von Courier Symphony **bereits real implementiert und getestet** sind und welche Aspekte in der Web-Demo **deterministisch simuliert** werden.

---

## 1. Die Transparenz-Matrix

| Komponente | Status | Reale Implementierung im Codebase | Rolle in der Web-Demo (`demo.html`) |
| :--- | :--- | :--- | :--- |
| **Zielvertrag (Goal Contract)** | **REAL** | `courier_core/goal_contract.py` definiert strenge Schema-, Hash- und Kriterien-Bindungen. | Simuliert als interaktives JSON-Szenario. |
| **Dispatcher & TaskLease** | **REAL** | `scripts/task_lease_manager.py` sichert atomare Sperren gegen parallele Doppelarbeit mit Fail-Closed bei Konflikten. | Simuliert (Worker-Zuweisung im Log ohne OS-Prozesse). |
| **Worker-Isolation** | **REAL** | Windows-Worker (`scripts/windows_worker/`) und Candidate-Sandboxen sichern isolierte Pfade ohne Zugriff auf Live-Daten. | Simuliert (kein echter Windows-Prozess auf dem PC gestartet). |
| **Unabhängiger Verifier** | **REAL** | `scripts/courier_verifier.py`, `courier_core/verifier.py` sowie Testsuiten prüfen Byte-Level-Hashes gegen Erwartungswerte. | Deterministisch im JavaScript abgebildet (zeigt echte Logik: Hash-Vergleich & Abweichungserkennung). |
| **Fail-Closed Abnahme** | **REAL** | Bei Diskrepanzen, unlesbaren Locks oder fehlendem Beweis wird `UNKNOWN` / `FAIL` ausgegeben; niemals „Blindes Grün“. | Real im Szenario 3 demonstriert (Erkennung von Differenzen und Abbruch). |
| **Prüfnachweis (Receipt)** | **REAL** | `model.py`, `acceptance_evidence()` bauen 6-Tupel aus Journal-Events; tamper-proof versiegelt. | Simuliert als formatiertes JSON-Ergebnisobjekt mit echten Datenstrukturen. |
| **Provider-LLM-Aufrufe** | **BLOCKIERT** | Reale API-Aufrufe an externe Modelle sind im aktuellen Modus durch `AUTONOMOUS_SPEND_LIMIT_EUR=0.00` bewusst gesperrt. | 100% deterministische Beispieldaten, **0,00 € Kosten**. |
| **Öffentliche Zahlungsannahme** | **OFFEN** | Stripe/Zahlungs-Links stehen auf `TODO_PAYMENT_LINK`. Keine automatischen Abbuchungen. | Reine Kontaktanfrage per E-Mail für Pilotpartner. |

---

## 2. Warum diese Trennung wichtig ist

1. **Sicherheit:** Der Interessent kann die Demo gefahrlos auf jedem Rechner öffnen, ohne dass Software installiert wird, Ports geöffnet werden oder Netzwerkverkehr anfällt.
2. **Reproduzierbarkeit:** Die Vorführung funktioniert immer gleich, verzögerungsfrei und unabhängig von Serverausfällen, Rate-Limits oder schwankender KI-Laune.
3. **Echtheit des Kerns:** Die in der Demo gezeigten 6 Stationen und Log-Nachrichten sind keine Marketing-Erfindung, sondern spiegeln exakt die Schnittstellen wider, die im Python-Backend von `2026-courier` implementiert und durch über 228 automatisierte Tests abgesichert sind.
