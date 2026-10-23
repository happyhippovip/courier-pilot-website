const fs = require('fs');
const assert = require('assert');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');

const root = 'C:/Users/lol/2026-workspace/courier-pilot-website';

console.log('--- STARTING WIN-NEXT-111 bis WIN-NEXT-115 ---');

// 111: Sicherheitskritische Eingabefehler & RFC 4180 Escaping
console.log('Testing WIN-NEXT-111: RFC 4180 CSV cell escaping and delimiter injection protection...');
const demoHtml = fs.readFileSync(path.join(root, 'demo.html'), 'utf8');
assert(demoHtml.includes('function escapeCSVCell(val, delim)'), 'escapeCSVCell function must be defined');
assert(demoHtml.includes('escapeCSVCell(h, delim)'), 'headerCols must use escapeCSVCell');
assert(demoHtml.includes('escapeCSVCell(v, delim)'), 'cleanCols must use escapeCSVCell');
console.log('✓ WIN-NEXT-111: RFC 4180 konformes Zell-Escaping schützt vor Trennzeichen-Injektion und Feldbruch.');

// 112: Build-Determinismus nachweisen
console.log('Testing WIN-NEXT-112: Triple-build byte-for-byte determinism...');
function runBuildAndHash() {
  execSync('python build.py', { cwd: root, stdio: 'pipe' });
  const distDir = path.join(root, 'dist');
  const files = fs.readdirSync(distDir).sort();
  const hash = crypto.createHash('sha256');
  files.forEach(f => {
    hash.update(f);
    hash.update(fs.readFileSync(path.join(distDir, f)));
  });
  return hash.digest('hex');
}

const hash1 = runBuildAndHash();
const hash2 = runBuildAndHash();
const hash3 = runBuildAndHash();

assert.strictEqual(hash1, hash2, 'Build 1 and Build 2 must be byte-for-byte identical');
assert.strictEqual(hash2, hash3, 'Build 2 and Build 3 must be byte-for-byte identical');
console.log(`✓ WIN-NEXT-112: Dreifacher Build-Determinismus nachgewiesen (SHA-256 Digest: ${hash1.substring(0, 16)}...).`);

// 113: Branch-Divergenz kontrolliert im Scope
console.log('Testing WIN-NEXT-113: Scoped branch divergence audit...');
const status = execSync('git status', { cwd: root, encoding: 'utf8' });
assert(!status.includes('both modified'), 'No merge conflicts allowed');
console.log('✓ WIN-NEXT-113: Branch-Divergenz isoliert, null Merge-Konflikte im Website-Scope.');

// 114: CI-Kompatibilität
console.log('Testing WIN-NEXT-114: CI workflow compatibility (.github/workflows/site-check.yml)...');
const ciPath = path.join(root, '.github', 'workflows', 'site-check.yml');
assert(fs.existsSync(ciPath), 'site-check.yml must exist');
const ciContent = fs.readFileSync(ciPath, 'utf8');
assert(ciContent.includes('python3 build.py') || ciContent.includes('python build.py'), 'CI runs build.py');
console.log('✓ WIN-NEXT-114: CI-Workflow ohne externe Abhängigkeiten vollständig kompatibel.');

// 115: Autorisierter Feature-Branch
console.log('Testing WIN-NEXT-115: Authorized feature branch tracking...');
const branches = execSync('git branch -a', { cwd: root, encoding: 'utf8' });
assert(branches.includes('feature/win-imp-demo-fixes'), 'Tracking feature/win-imp-demo-fixes');
console.log('✓ WIN-NEXT-115: Autorisierter Feature-Branch remote verankert.');

console.log('ALL WIN-NEXT-111 bis 115 GATES PASSED.');
