const fs = require('fs');
const assert = require('assert');

const html = fs.readFileSync('C:/Users/lol/2026-workspace/courier-pilot-website/demo.html', 'utf8');
const scriptMatches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert(scriptMatches.length >= 1, 'Script tag found');

const code = scriptMatches[0][1];

// Test 1: Cold start with stored preference
let speedSetInStorage = null;
const window = {
  location: { hash: '', search: '' },
  addEventListener: () => {},
  history: { replaceState: () => {} }
};
const document = {
  addEventListener: () => {},
  querySelectorAll: () => [],
  getElementById: (id) => {
    if (id === 'speedSelect') return { value: '2500' };
    if (id === 'speedIntervalPill') return { textContent: '' };
    return null;
  }
};
const localStorage = {
  getItem: (key) => (key === 'courier_demo_speed' ? '2500' : null),
  setItem: (key, val) => { speedSetInStorage = val; }
};

try {
  const fn = new Function('window', 'document', 'localStorage', code);
  fn(window, document, localStorage);
  console.log('PASS: demo.html executed without TDZ errors on load with stored speed preference.');
} catch (e) {
  console.error('FAIL: Script evaluation threw error:', e);
  process.exit(1);
}
