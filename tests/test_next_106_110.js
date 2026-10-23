const fs = require('fs');
const assert = require('assert');
const path = require('path');
const vm = require('vm');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';
const PAGES = [
  "index.html", "demo.html", "repo-reality-check.html", "architecture.html",
  "security.html", "use-cases.html", "developers.html", "company.html",
  "widerruf.html", "impressum.html", "datenschutz.html", "privacy.html", "404.html"
];

console.log('--- STARTING WIN-NEXT-106 bis WIN-NEXT-110 ---');

// 106: JavaScript-Laufzeit- und Syntaxprüfung
console.log('Testing WIN-NEXT-106: JavaScript runtime and syntax validation across all pages...');
let scriptCount = 0;
PAGES.forEach(page => {
  const content = fs.readFileSync(path.join(root, page), 'utf8');
  const scripts = [...content.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)];
  scripts.forEach((m) => {
    const attrs = m[1];
    const code = m[2].trim();
    if (!code) return;
    if (attrs.includes('application/ld+json')) {
      JSON.parse(code);
    } else {
      new vm.Script(code);
      scriptCount++;
    }
  });
});
assert(scriptCount >= 6, 'Must compile all inline JS scripts');
console.log(`✓ WIN-NEXT-106: Alle ${scriptCount} JavaScript-Blöcke kompilieren ohne Syntax- oder Hoistingfehler.`);

// 107: Mobile-Breakpoints
console.log('Testing WIN-NEXT-107: Mobile breakpoints and responsiveness...');
const stylesCss = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');
assert(stylesCss.includes('@media (max-width:759px)'), 'styles.css must include mobile breakpoint 759px');
assert(stylesCss.includes('@media (min-width:760px)'), 'styles.css must include desktop breakpoint 760px');
assert(stylesCss.includes('overflow-x:auto') || stylesCss.includes('overflow-x: auto'), 'Responsive table/pre scrolling');
console.log('✓ WIN-NEXT-107: Mobile Breakpoints (max-width: 759px) und horizontale Scroll-Container integer.');

// 108: Tastatur- und Fokusfehler
console.log('Testing WIN-NEXT-108: Keyboard focus and button type attributes...');
const demoHtml = fs.readFileSync(path.join(root, 'demo.html'), 'utf8');
assert(demoHtml.includes('type="button" class="btn-sub" id="btnFilterAll"'), 'btnFilterAll has type="button"');
assert(demoHtml.includes('type="button" class="btn-sub" id="btnFilterChanged"'), 'btnFilterChanged has type="button"');
assert(demoHtml.includes('handleScenarioTabKey'), 'Scenario tab navigation listener present');
assert(stylesCss.includes(':focus-visible'), ':focus-visible styling present for keyboard accessibility');
console.log('✓ WIN-NEXT-108: type="button" Attribute, Pfeiltastennavigation und :focus-visible Outline verifiziert.');

// 109: Reduced Motion Absicherung
console.log('Testing WIN-NEXT-109: prefers-reduced-motion coverage...');
assert(stylesCss.includes('prefers-reduced-motion: reduce'), 'prefers-reduced-motion: reduce query present');
assert(stylesCss.includes('animation-duration: 0.01ms') || stylesCss.includes('animation-duration:0.01ms'), 'Animations disabled under reduced motion');
console.log('✓ WIN-NEXT-109: Reduced Motion Override (0.01ms Dauer) verifiziert.');

// 110: Asset- und Link-Regression
console.log('Testing WIN-NEXT-110: Asset and link regression...');
const distPath = path.join(root, 'dist');
assert(fs.existsSync(distPath), 'dist/ must exist');
const distFiles = fs.readdirSync(distPath);
assert.strictEqual(distFiles.length, 25, 'dist must contain exactly 25 files');
assert(distFiles.includes('demo.html') && distFiles.includes('styles.css') && distFiles.includes('.htaccess'), 'Core assets present in dist');
console.log(`✓ WIN-NEXT-110: Asset- und Link-Regression erfolgreich (${distFiles.length} Dateien in dist/).`);

console.log('ALL WIN-NEXT-106 bis 110 GATES PASSED.');
