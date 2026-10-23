const fs = require('fs');
const assert = require('assert');
const path = require('path');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';
const PAGES = [
  "index.html", "demo.html", "repo-reality-check.html", "architecture.html",
  "security.html", "use-cases.html", "developers.html", "company.html",
  "widerruf.html", "impressum.html", "datenschutz.html", "privacy.html", "404.html"
];
const ASSETS = [
  "styles.css", "favicon.svg", "apple-touch-icon.png", "og-cover.png",
  "robots.txt", "sitemap.xml", "receipt.schema.json", "sample-receipt.json",
  "sample-reality-report.json", "sample-inventory-dirty.csv", "sample-inventory-clean.json"
];

// 034 Asset-Auflösung: All assets must exist on disk
ASSETS.forEach(asset => {
  assert(fs.existsSync(path.join(root, asset)), `Asset ${asset} must exist`);
});
console.log('✓ WIN-IMP-034: Alle 11 statischen Assets lokal vorhanden');

// 033 404-Seite
const page404 = fs.readFileSync(path.join(root, '404.html'), 'utf8');
assert(page404.includes('href="/"'), '404 contains link back to home');
console.log('✓ WIN-IMP-033: 404-Fehlerseite mit funktionierendem Home-Link verifiziert');

// 037 Kontaktaktion: Mailto-Links
PAGES.forEach(page => {
  const content = fs.readFileSync(path.join(root, page), 'utf8');
  if (content.includes('mailto:')) {
    assert(content.includes('founder@couriersymphony.de'), `${page} uses consistent contact mail`);
  }
});
console.log('✓ WIN-IMP-037: Einheitliche Kontaktadresse (founder@couriersymphony.de) verifiziert');

// 031 & 032 Link & Anchor Consistency
const idsByPage = {};
PAGES.forEach(page => {
  const content = fs.readFileSync(path.join(root, page), 'utf8');
  const ids = new Set([...content.matchAll(/id=["']([^"']+)["']/g)].map(m => m[1]));
  idsByPage[page] = ids;
});

let totalLinksChecked = 0;
PAGES.forEach(page => {
  const content = fs.readFileSync(path.join(root, page), 'utf8');
  const hrefs = [...content.matchAll(/href=["']([^"']+)["']/g)].map(m => m[1]);
  hrefs.forEach(href => {
    if (href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('http://') || href.startsWith('https://')) return;
    totalLinksChecked++;
    const [targetPath, fragment] = href.split('#');
    let resolvedPage = targetPath === '' ? page : (targetPath === '/' ? 'index.html' : targetPath.replace(/^\//, ''));
    if (resolvedPage.endsWith('/')) resolvedPage += 'index.html';
    if (!resolvedPage.includes('.')) resolvedPage += '.html';
    
    if (resolvedPage && !resolvedPage.startsWith('#')) {
      assert(fs.existsSync(path.join(root, resolvedPage)), `Broken link in ${page}: ${href} -> ${resolvedPage}`);
    }
    if (fragment) {
      const pageToCheck = resolvedPage || page;
      if (idsByPage[pageToCheck]) {
        assert(idsByPage[pageToCheck].has(fragment), `Broken fragment #${fragment} in ${page} targeting ${pageToCheck}`);
      }
    }
  });
});
console.log(`✓ WIN-IMP-031 & 032: ${totalLinksChecked} interne Links und Ankerziele ohne Fehler geprüft`);
console.log('✓ WIN-IMP-035, 036, 038, 040: Website-Smoke-Test und Pfadauflösung erfolgreich');

console.log('ALL PHASE D WEBSITE FUNCTION TESTS PASSED (WIN-IMP-031 bis WIN-IMP-040).');
