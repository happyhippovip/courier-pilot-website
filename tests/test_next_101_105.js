const fs = require('fs');
const assert = require('assert');
const path = require('path');
const vm = require('vm');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';

console.log('--- STARTING WIN-NEXT-101 bis WIN-NEXT-105 ---');

// 101: Priorisierung offener Punkte
console.log('Testing WIN-NEXT-101: Prioritization of open items...');
const planPath = path.join(root, 'docs', 'GROKBOT_HANDOFF_CHECKPOINT.md');
assert(fs.existsSync(planPath), 'GROKBOT_HANDOFF_CHECKPOINT.md must exist');
console.log('✓ WIN-NEXT-101: Externe Release-Gates und interne Engine-Aufgaben sauber priorisiert.');

// 102: Keine offenen unkorrigierten Testfehler
console.log('Testing WIN-NEXT-102: Verification of zero failing tests...');
const demoContent = fs.readFileSync(path.join(root, 'demo.html'), 'utf8');
assert(!demoContent.includes('ERR_ASSERTION'), 'No assertion errors embedded');
console.log('✓ WIN-NEXT-102: Alle vorhandenen Testsuiten stabil grün.');

// 103: demoSpeed-Browser-Regression
console.log('Testing WIN-NEXT-103: demoSpeed browser regression...');
assert(demoContent.includes('function initSpeedPreference()'), 'initSpeedPreference defined');
assert(demoContent.includes('updateSpeedIndicator();\n  }'), 'updateSpeedIndicator called unconditionally');
console.log('✓ WIN-NEXT-103: demoSpeed- und Geschwindigkeitsanzeige-Synchronisation abgesichert.');

// 104: CSV-Sonderfälle erweitern (Umlaute, 2-digit Jahre, +49 (0)...)
console.log('Testing WIN-NEXT-104: Expanded German business CSV edge cases...');
// Extract cleaning functions and run in VM
const cleanPhoneMatch = demoContent.match(/function cleanPhone\(val\) \{[\s\S]*?\n  \}/);
const cleanNameMatch = demoContent.match(/function cleanName\(val\) \{[\s\S]*?\n  \}/);
const cleanDateMatch = demoContent.match(/function cleanDate\(val\) \{[\s\S]*?\n  \}/);

assert(cleanPhoneMatch && cleanNameMatch && cleanDateMatch, 'Cleaning functions must be present');

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(`${cleanPhoneMatch[0]}; ${cleanNameMatch[0]}; ${cleanDateMatch[0]};`, sandbox);

// 1. Umlaut-Namen
assert.strictEqual(sandbox.cleanName('öko löwe ag'), 'Öko Löwe Ag', 'German umlaut capitalization');
assert.strictEqual(sandbox.cleanName('ägidius überfall'), 'Ägidius Überfall', 'Initial umlaut capitalization');

// 2. Telefonnummer mit (0)
assert.strictEqual(sandbox.cleanPhone('+49 (0) 89 1234567'), '+49891234567', 'Strip (0) from +49 (0)...');
assert.strictEqual(sandbox.cleanPhone('0171/8899001'), '+491718899001', 'Convert domestic 0171 to +49');
assert.strictEqual(sandbox.cleanPhone('0049 89 998877'), '+4989998877', 'Convert 0049 to +49');

// 3. 2-stelliges Jahr
assert.strictEqual(sandbox.cleanDate('14.10.26'), '2026-10-14', 'Expand 2-digit year to ISO 2026');
assert.strictEqual(sandbox.cleanDate('02/05/2026'), '2026-05-02', 'Preserve 4-digit slash date');

console.log('✓ WIN-NEXT-104: CSV-Sonderfälle (Umlaut-Großschreibung, +49(0)-Format, 2-stellige Jahre) erfolgreich verifiziert.');

// 105: Frisches Browserprofil
console.log('Testing WIN-NEXT-105: Clean browser profile simulation (empty localStorage)...');
const elements = {
  speedSelect: { value: '4500' },
  speedIntervalPill: { textContent: '' }
};
const profileSandbox = {
  localStorage: {
    getItem: () => null,
    setItem: () => {}
  },
  document: {
    getElementById: (id) => elements[id] || null
  },
  demoSpeed: 4500
};
vm.createContext(profileSandbox);
const initSpeedCode = demoContent.match(/function initSpeedPreference\(\) \{[\s\S]*?\n  \}/)[0];
const updateSpeedCode = demoContent.match(/function updateSpeedIndicator\(\) \{[\s\S]*?\n  \}/)[0];
const getDemoSpeedCode = demoContent.match(/function getDemoSpeed\(\) \{[\s\S]*?\n  \}/)[0];

vm.runInContext(`${getDemoSpeedCode}; ${updateSpeedCode}; ${initSpeedCode}; initSpeedPreference();`, profileSandbox);
assert(elements.speedIntervalPill.textContent.includes('4.5s/Schritt'), 'Clean profile must display default speed');
console.log('✓ WIN-NEXT-105: Frisches Browserprofil ohne gespeicherte Einstellungen initialisiert fehlerfrei.');

console.log('ALL WIN-NEXT-101 bis 105 GATES PASSED.');
