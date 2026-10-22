---
name: pair-agent
description: Use when you need cross-agent browser sharing for collaborative debugging and review. Allows multiple agents to share a browser session for real-time collaboration on UI work, debugging, and code review.
model: nemotron-3-ultra-free
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
triggers:
  - "pair agent"
  - "share browser"
  - "collaborate"
  - "debug together"
  - "review together"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
---

# Pair Agent — Cross-Agent Browser Sharing

Cross-agent browser sharing for collaborative debugging and review.

---

## 1. BROWSER SESSION SHARING

### Start Shared Browser
```bash
# Start Playwright browser with remote debugging
npx playwright install chromium
npx playwright launch --remote-debugging-port=9222
```

### Connect to Shared Browser
```javascript
const { chromium } = require('playwright');

// Connect to existing browser
const browser = await chromium.connectOverCDP('http://localhost:9222');
const context = browser.contexts()[0];
const page = context.pages()[0];
```

### Share Browser State
```javascript
// Capture browser state
const state = await page.evaluate(() => ({
  url: window.location.href,
  title: document.title,
  scrollY: window.scrollY,
  localStorage: { ...window.localStorage },
  sessionStorage: { ...window.sessionStorage },
}));

// Write state to file for other agents
fs.writeFileSync('/tmp/browser-state.json', JSON.stringify(state));
```

### Restore Browser State
```javascript
// Read state from file
const state = JSON.parse(fs.readFileSync('/tmp/browser-state.json', 'utf-8'));

// Navigate to URL
await page.goto(state.url);

// Restore scroll position
await page.evaluate((scrollY) => window.scrollTo(0, scrollY), state.scrollY);

// Restore storage
await page.evaluate((storage) => {
  Object.entries(storage).forEach(([key, value]) => {
    localStorage.setItem(key, value);
  });
}, state.localStorage);
```

---

## 2. REAL-TIME COLLABORATION

### Screenshot Sharing
```javascript
// Capture screenshot
await page.screenshot({ path: '/tmp/collab-screenshot.png', fullPage: true });

// Share via file
console.log('Screenshot saved to /tmp/collab-screenshot.png');
```

### Element Highlighting
```javascript
// Highlight element for other agents
await page.evaluate(() => {
  const element = document.querySelector('.important-element');
  element.style.outline = '3px solid red';
  element.style.outlineOffset = '2px';
});
```

### Console Log Sharing
```javascript
// Share console logs
page.on('console', msg => {
  const log = `[${msg.type()}] ${msg.text()}`;
  fs.appendFileSync('/tmp/collab-console.log', log + '\n');
});
```

---

## 3. DEBUGGING SESSIONS

### Start Debug Session
```bash
# Start browser with DevTools
npx playwright launch --remote-debugging-port=9222 --headed

# Or headless for CI
npx playwright launch --remote-debugging-port=9222
```

### Capture Debug Info
```javascript
// Capture page state
const debugInfo = await page.evaluate(() => ({
  url: window.location.href,
  title: document.title,
  body: document.body.innerHTML.substring(0, 1000),
  errors: window.__errors || [],
  performance: {
    loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
    domReady: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
  },
}));

// Write debug info
fs.writeFileSync('/tmp/debug-info.json', JSON.stringify(debugInfo, null, 2));
```

### Network Monitoring
```javascript
// Monitor network requests
page.on('request', request => {
  console.log(`→ ${request.method()} ${request.url()}`);
});

page.on('response', response => {
  console.log(`← ${response.status()} ${response.url()}`);
});

page.on('requestfailed', request => {
  console.log(`✗ FAILED: ${request.url()} ${request.failure().errorText}`);
});
```

---

## 4. REVIEW SESSIONS

### Visual Review
```javascript
// Take screenshots at different viewports
const viewports = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1024, height: 768 },
];

for (const v of viewports) {
  await page.setViewportSize({ width: v.width, height: v.height });
  await page.screenshot({ path: `/tmp/review-${v.name}.png`, fullPage: true });
}
```

### Accessibility Review
```javascript
// Run accessibility snapshot
const snapshot = await page.accessibility.snapshot();
fs.writeFileSync('/tmp/a11y-snapshot.json', JSON.stringify(snapshot, null, 2));
```

### Performance Review
```javascript
// Capture performance metrics
const metrics = await page.evaluate(() => {
  const perf = performance.getEntriesByType('navigation')[0];
  return {
    fcp: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
    lcp: performance.getEntriesByName('largest-contentful-paint')[0]?.startTime,
    load: perf.loadEventEnd - perf.startTime,
  };
});

fs.writeFileSync('/tmp/perf-metrics.json', JSON.stringify(metrics, null, 2));
```

---

## 5. INTERACTION SHARING

### Click Sharing
```javascript
// Click element and share coordinates
const element = await page.locator('.button');
const box = await element.boundingBox();

// Share click target
console.log(`Click at: ${box.x + box.width/2}, ${box.y + box.height/2}`);

// Perform click
await element.click();
```

### Form Filling
```javascript
// Share form data
const formData = {
  name: 'Test User',
  email: 'test@example.com',
  message: 'Hello from pair agent!',
};

// Fill form
await page.fill('input[name="name"]', formData.name);
await page.fill('input[name="email"]', formData.email);
await page.fill('textarea[name="message"]', formData.message);

// Share form state
fs.writeFileSync('/tmp/form-state.json', JSON.stringify(formData, null, 2));
```

---

## 6. FILE SHARING

### Share Screenshots
```bash
# Copy screenshots to shared location
cp /tmp/collab-screenshot.png /shared/screenshots/
```

### Share State Files
```bash
# Copy state files to shared location
cp /tmp/browser-state.json /shared/state/
cp /tmp/debug-info.json /shared/debug/
```

---

## 7. PAIR AGENT COMMAND

The `/pair` command starts a collaborative session:

```bash
# Start pair session
/pair start --port=9222

# Share browser state
/pair share

# Capture screenshot
/pair screenshot

# Debug session
/pair debug

# End session
/pair end
```

---

## 8. WORKFLOW EXAMPLES

### Collaborative Debugging
```bash
# Agent 1: Start browser
/pair start --port=9222

# Agent 1: Navigate to bug
/pair navigate http://localhost:3000/broken-page

# Agent 1: Share screenshot
/pair screenshot

# Agent 2: Connect and debug
/pair connect http://localhost:9222
/pair debug

# Both: Review console logs
/pair logs
```

### Visual Review
```bash
# Agent 1: Start review
/pair start --port=9222
/pair navigate http://localhost:3000

# Agent 1: Capture screenshots at all viewports
/pair screenshot --viewports=mobile,tablet,desktop

# Agent 2: Review screenshots
/pair review

# Both: Discuss findings
/pair discuss
```

---

## 9. BEST PRACTICES

### Do
- Share browser state frequently
- Capture screenshots at key moments
- Monitor console for errors
- Use consistent file naming
- Clean up shared files after session

### Don't
- Forget to close browser when done
- Leave shared files uncleaned
- Skip accessibility checks
- Ignore console errors
- Forget to share state with other agents

---

## 10. TROUBLESHOOTING

### Browser Won't Connect
```bash
# Check if browser is running
lsof -i :9222

# Kill existing browser
pkill -f "playwright.*9222"

# Start fresh
npx playwright launch --remote-debugging-port=9222
```

### Screenshots Not Saving
```bash
# Check directory exists
mkdir -p /tmp/screenshots

# Check permissions
ls -la /tmp/screenshots/
```

### State Not Restoring
```bash
# Check state file
cat /tmp/browser-state.json

# Clear state and start fresh
rm /tmp/browser-state.json
```
