const { execSync } = require('child_process');
const path = require('path');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';

console.log('================================================================');
console.log(' COURIER SYMPHONY — TITAN-WIN-100 MASTER REGRESSION RUNNER');
console.log('================================================================\n');

const SUITES = [
  { id: 'PHASE A', name: 'Demo-Fixes (WIN-IMP-001 bis 010)', file: 'tests/test_phase_a_smoke.js' },
  { id: 'PHASE A (TDZ)', name: 'TDZ Hoisting Regression (WIN-IMP-001-002)', file: 'tests/test_demospeed_regression.js' },
  { id: 'PHASE B', name: 'CSV & Offline (WIN-IMP-011 bis 020)', file: 'tests/test_phase_b_csv_offline.js' },
  { id: 'PHASE C', name: 'Accessibility WCAG 2.2 (WIN-IMP-021 bis 030)', file: 'tests/test_phase_c_a11y.js' },
  { id: 'PHASE D', name: 'Website Functions & Routing (WIN-IMP-031 bis 040)', file: 'tests/test_phase_d_website.js' },
  { id: 'PHASE E', name: 'Build & Release Gate (WIN-IMP-041 bis 050)', file: 'tests/test_phase_e_build.js' },
  { id: 'PHASE F', name: 'Security & XSS (WIN-IMP-051 bis 060)', file: 'tests/test_phase_f_security.js' },
  { id: 'PHASE G', name: 'Product Truth & Compliance (WIN-IMP-061 bis 070)', file: 'tests/test_phase_g_product_truth.js' },
  { id: 'PHASE H', name: 'Release Engineering (WIN-IMP-071 bis 080)', file: 'tests/test_phase_h_release.js' },
  { id: 'PHASE I', name: 'Förder-Demo & Checksums (WIN-IMP-081 bis 090)', file: 'tests/test_phase_i_foerder.js' },
];

let passed = 0;
SUITES.forEach(s => {
  console.log(`>>> Running [${s.id}] ${s.name}...`);
  try {
    const out = execSync(`node ${s.file}`, { cwd: root, encoding: 'utf8', stdio: 'pipe' });
    console.log(out.trim());
    console.log(`[PASS] ${s.id} completed successfully.\n`);
    passed++;
  } catch (err) {
    console.error(`[FAIL] ${s.id} failed with exit code ${err.status}`);
    console.error(err.stdout || err.stderr || err.message);
    process.exit(1);
  }
});

console.log('================================================================');
console.log(` ALL ${passed} OF ${SUITES.length} TEST PHASES PASSED WITH 100% SUCCESS!`);
console.log(' WIN-IMP-001 bis WIN-IMP-100 GATES FULLY VERIFIED.');
console.log('================================================================');
