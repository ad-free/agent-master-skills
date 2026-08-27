---
name: playwright-skill
description: |
  Use when you want to test websites, automate browser interactions, validate web functionality,
  or perform any browser-based testing including screenshots, forms, responsive design, and UX validation.
  Enhanced with real browser QA: accessibility checks, performance metrics, console error detection,
  visual regression, and automated interaction testing.
model: gpt-5-nano
version: 2.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "test website"
  - "browser automation"
  - "playwright"
  - "browser test"
  - "automate browser"
  - "take screenshot"
  - "check responsive"
  - "qa"
  - "browser qa"
  - "accessibility check"
  - "a11y test"
metadata:
  origin: agent-master-skills
  version: 2.0.0
  ports: playwright-skill, taste-skill qa
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Playwright Browser Automation (v2 — Real Browser QA)

Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task.

---

## 1. AUTO-DETECT DEV SERVER

Before running any browser test, detect if a dev server is running:

```bash
# Check common dev server ports
for port in 3000 3001 5173 5174 8080 8888 4200 9000; do
  if lsof -i :$port -sTCP:LISTEN -t 2>/dev/null; then
    echo "Dev server running on port $port"
    break
  fi
done
```

If no server is running, start one:
- **Next.js:** `npm run dev` or `npx next dev`
- **Vite:** `npm run dev` or `npx vite`
- **React (CRA):** `npm start`
- **Static files:** `npx serve .` or `python -m http.server`

Wait for server to be ready before testing.

---

## 2. QA COMMAND (/qa)

The `/qa` command triggers a comprehensive browser QA pass. Run these checks in order:

### 2.1 Page Load Test
- Navigate to the target URL
- Check for HTTP errors (4xx, 5xx)
- Verify page title is present
- Check for console errors
- Measure page load time

### 2.2 Accessibility Check (a11y)
- Run Playwright's built-in accessibility snapshot
- Check for:
  - Missing alt text on images
  - Missing form labels
  - Missing heading hierarchy
  - Color contrast issues
  - Missing ARIA attributes
  - Keyboard navigation issues
- Output accessibility violations with severity

### 2.3 Responsive Design Test
Test at these breakpoints:
- Mobile: 375px (iPhone SE)
- Mobile: 390px (iPhone 14)
- Tablet: 768px (iPad)
- Desktop: 1024px (laptop)
- Desktop: 1440px (monitor)
- Wide: 1920px (large monitor)

For each breakpoint:
- Check layout doesn't overflow horizontally
- Verify text is readable (no tiny text)
- Check touch targets are ≥44px on mobile
- Verify navigation works (hamburger menu on mobile)
- Take a screenshot

### 2.4 Interaction Test
- Click all navigation links
- Fill and submit forms
- Test hover states on buttons
- Test focus states for keyboard navigation
- Verify modals/dialogs open and close
- Test scroll behavior

### 2.5 Console Error Detection
Monitor console for:
- JavaScript errors
- Failed network requests
- CORS errors
- Mixed content warnings
- Deprecation warnings

### 2.6 Performance Check
Measure:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- Time to Interactive (TTI)
- Total page weight

---

## 3. SCREENSHOT CAPTURE

### Full Page Screenshot
```javascript
await page.screenshot({ path: '/tmp/qa-screenshot-full.png', fullPage: true });
```

### Viewport Screenshot
```javascript
await page.screenshot({ path: '/tmp/qa-screenshot-viewport.png' });
```

### Element Screenshot
```javascript
const element = await page.locator('.hero');
await element.screenshot({ path: '/tmp/qa-screenshot-hero.png' });
```

### Responsive Screenshots
Take screenshots at every breakpoint and save with breakpoint label:
```bash
# Named screenshots
/tmp/qa-mobile-375.png
/tmp/qa-mobile-390.png
/tmp/qa-tablet-768.png
/tmp/qa-desktop-1024.png
/tmp/qa-desktop-1440.png
/tmp/qa-wide-1920.png
```

---

## 4. FORM TESTING

### Contact Form Test
```javascript
// Fill form
await page.fill('input[name="name"]', 'Test User');
await page.fill('input[name="email"]', 'test@example.com');
await page.fill('textarea[name="message"]', 'Test message');

// Submit
await page.click('button[type="submit"]');

// Verify success
await page.waitForSelector('.success-message');
```

### Form Validation Test
```javascript
// Submit empty form
await page.click('button[type="submit"]');

// Check for validation errors
const errors = await page.locator('.error-message').count();
console.log(`Validation errors: ${errors}`);
```

---

## 5. LINK CHECKING

```javascript
// Get all links
const links = await page.locator('a[href]').all();

// Check each link
for (const link of links) {
  const href = await link.getAttribute('href');
  if (href && href.startsWith('http')) {
    const response = await page.request.get(href);
    console.log(`${href}: ${response.status()}`);
  }
}
```

---

## 6. CONSOLE MONITORING

```javascript
const errors = [];
page.on('console', msg => {
  if (msg.type() === 'error') {
    errors.push(msg.text());
  }
});

page.on('pageerror', error => {
  errors.push(error.message);
});

// After test
if (errors.length > 0) {
  console.log('Console errors found:');
  errors.forEach(e => console.log(`  - ${e}`));
}
```

---

## 7. ACCESSIBILITY TESTING

```javascript
// Run accessibility snapshot
const snapshot = await page.accessibility.snapshot();

// Check for issues
function checkA11y(node, issues = []) {
  if (node.role === 'img' && !node.name) {
    issues.push('Image missing alt text');
  }
  if (node.role === 'button' && !node.name) {
    issues.push('Button missing accessible name');
  }
  if (node.role === 'link' && !node.name) {
    issues.push('Link missing accessible name');
  }
  if (node.children) {
    node.children.forEach(child => checkA11y(child, issues));
  }
  return issues;
}

const issues = checkA11y(snapshot);
console.log(`Accessibility issues: ${issues.length}`);
```

---

## 8. RESPONSIVE TESTING

```javascript
const viewports = [
  { name: 'mobile-375', width: 375, height: 812 },
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'desktop-1024', width: 1024, height: 768 },
  { name: 'desktop-1440', width: 1440, height: 900 },
  { name: 'wide-1920', width: 1920, height: 1080 },
];

for (const viewport of viewports) {
  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  await page.goto(url);
  
  // Check for horizontal overflow
  const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
  const viewportWidth = await page.evaluate(() => window.innerWidth);
  
  if (bodyWidth > viewportWidth) {
    console.log(`Overflow detected at ${viewport.name}: ${bodyWidth}px > ${viewportWidth}px`);
  }
  
  // Take screenshot
  await page.screenshot({ path: `/tmp/qa-${viewport.name}.png` });
}
```

---

## 9. PERFORMANCE TESTING

```javascript
// Measure performance metrics
const metrics = await page.evaluate(() => {
  const perf = performance.getEntriesByType('navigation')[0];
  return {
    fcp: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
    load: perf.loadEventEnd - perf.startTime,
    domContentLoaded: perf.domContentLoadedEventEnd - perf.startTime,
    responseTime: perf.responseEnd - perf.requestStart,
  };
});

console.log('Performance metrics:', metrics);
```

---

## 10. TEST REPORT GENERATION

After running all tests, generate a report:

```markdown
# QA Report — [URL]

## Summary
- **Tests Run:** X
- **Passed:** X
- **Failed:** X
- **Accessibility Issues:** X
- **Console Errors:** X
- **Performance Score:** X/100

## Test Results

### 1. Page Load
- Status: ✅/❌
- Load Time: Xms
- Title: [title]

### 2. Accessibility
- Issues Found: X
- Critical: X
- Warning: X
- Details: [list]

### 3. Responsive Design
- Mobile (375px): ✅/❌
- Tablet (768px): ✅/❌
- Desktop (1024px): ✅/❌
- Wide (1920px): ✅/❌

### 4. Console Errors
- Errors: X
- Warnings: X
- Details: [list]

### 5. Performance
- FCP: Xms
- LCP: Xms
- CLS: X
- TTI: Xms

### 6. Screenshots
- [List of captured screenshots]
```

---

## 11. QUICK QA CHECKLIST

For a fast QA pass, run these checks:

- [ ] Page loads without errors
- [ ] No console errors
- [ ] No broken links
- [ ] Forms work correctly
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Navigation works
- [ ] Images load
- [ ] Fonts load
- [ ] No horizontal overflow
- [ ] Touch targets ≥44px on mobile
- [ ] Focus states visible
- [ ] Alt text present on images
- [ ] Page title present
- [ ] Meta description present

---

## 12. EXAMPLE USAGE

### Full QA Pass
```bash
# Start dev server if needed
npm run dev &

# Wait for server
sleep 5

# Run QA
npx playwright test qa-test.js
```

### Quick Screenshot
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');
  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  await browser.close();
})();
```

### Responsive Test
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const viewports = [
    { width: 375, height: 812, name: 'mobile' },
    { width: 768, height: 1024, name: 'tablet' },
    { width: 1024, height: 768, name: 'desktop' },
  ];
  
  for (const v of viewports) {
    await page.setViewportSize({ width: v.width, height: v.height });
    await page.goto('http://localhost:3000');
    await page.screenshot({ path: `/tmp/${v.name}.png` });
  }
  
  await browser.close();
})();
```
