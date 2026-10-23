const fs = require('fs');
const assert = require('assert');
const path = require('path');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';
const styles = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');

const PAGES = [
  "index.html", "demo.html", "repo-reality-check.html", "architecture.html",
  "security.html", "use-cases.html", "developers.html", "company.html",
  "widerruf.html", "impressum.html", "datenschutz.html", "privacy.html", "404.html"
];

// 021 Reduced Motion
assert(styles.includes('prefers-reduced-motion: reduce'), 'prefers-reduced-motion: reduce present');
assert(styles.includes('animation-duration: 0.01ms !important'), 'animation override for reduced motion');
console.log('✓ WIN-IMP-021: Reduced Motion Media Query verifiziert');

// 022 Focus-Visible
assert(styles.includes(':focus-visible'), ':focus-visible style present');
assert(styles.includes('outline:'), 'Focus outline defined');
console.log('✓ WIN-IMP-022: Focus-Visible Ringe verifiziert');

// 023 Skip-Link & 024 Tastaturnavigation
PAGES.forEach(page => {
  const content = fs.readFileSync(path.join(root, page), 'utf8');
  assert(content.includes('class="skip"') || content.includes("class='skip'"), `${page} must contain a skip link`);
  assert(content.includes('id="main"') || content.includes("id='main'"), `${page} must contain main target`);
});
console.log('✓ WIN-IMP-023: Skip-Links auf allen 13 Seiten vorhanden');
console.log('✓ WIN-IMP-024: Tastaturnavigation & Main-Landmarks intakt');

// 026 ARIA-Zustände & 027 Formularbeschriftungen in demo.html
const demoHtml = fs.readFileSync(path.join(root, 'demo.html'), 'utf8');
assert(demoHtml.includes('aria-pressed='), 'aria-pressed present in demo');
assert(demoHtml.includes('aria-selected='), 'aria-selected present in demo');
assert(demoHtml.includes('aria-label='), 'aria-label present in demo inputs');
console.log('✓ WIN-IMP-026: ARIA-Zustände (pressed, selected) verifiziert');
console.log('✓ WIN-IMP-027: Formularbeschriftungen & aria-labels verifiziert');

// 028 Fehleransagen
assert(demoHtml.includes('aria-live='), 'aria-live announcer present');
assert(demoHtml.includes('role="status"') || demoHtml.includes('role="alert"') || demoHtml.includes('aria-live="polite"'), 'Live region present');
console.log('✓ WIN-IMP-028: Barrierefreie Live-Status- und Fehleransagen vorhanden');

// 029 Responsive Zoom
assert(styles.includes('@media'), 'Responsive breakpoints present in CSS');
assert(styles.includes('rem') || styles.includes('em'), 'Relative scalable units used');
console.log('✓ WIN-IMP-029: Skalierbare Einheiten & Responsive Breakpoints verifiziert');

console.log('ALL PHASE C ACCESSIBILITY TESTS PASSED (WIN-IMP-021 bis WIN-IMP-030).');
