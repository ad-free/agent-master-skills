---
name: visual-regression
description: Use when you need Playwright or Cypress screenshot comparison for visual testing and regression detection. Includes baseline management, diff visualization, threshold configuration, and CI integration.
model: big-pickle
version: 2.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "visual regression"
  - "screenshot test"
  - "visual test"
  - "ui snapshot"
  - "pixel diff"
  - "baseline"
  - "visual diff"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
---

<!-- TOKEN CEILING: ~3K -->

# Visual Regression Plugin (v2 — Baseline Management)

Automated visual comparison testing. Captures screenshots at defined breakpoints and compares against baselines to detect unintended visual changes.

---

## 1. BASELINE MANAGEMENT

### Baseline Directory Structure
```
.baselines/
  ├── mobile-375/
  │   ├── hero.png
  │   ├── features.png
  │   └── footer.png
  ├── tablet-768/
  │   ├── hero.png
  │   ├── features.png
  │   └── footer.png
  ├── desktop-1024/
  │   ├── hero.png
  │   ├── features.png
  │   └── footer.png
  └── desktop-1440/
      ├── hero.png
      ├── features.png
      └── footer.png
```

### Create Baseline
```bash
# Capture baselines at all breakpoints
npx playwright test --update-snapshots

# Or capture specific breakpoint
npx playwright test --update-snapshots --project=mobile-375
```

### Update Baseline
When intentional changes are made, update the baseline:
```bash
# Update all baselines
npx playwright test --update-snapshots

# Update specific test
npx playwright test --update-snapshots --grep="hero"
```

### Delete Baseline
```bash
# Remove specific baseline
rm .baselines/mobile-375/hero.png

# Remove all baselines for a breakpoint
rm -rf .baselines/mobile-375/
```

---

## 2. BREAKPOINTS

Default breakpoints (configurable in `state.json`):
- **Mobile:** 375px (iPhone SE)
- **Mobile:** 390px (iPhone 14)
- **Tablet:** 768px (iPad)
- **Desktop:** 1024px (laptop)
- **Desktop:** 1440px (monitor)
- **Wide:** 1920px (large monitor)

### Configure Breakpoints
```json
{
  "plugins": ["visual-regression"],
  "pluginConfig": {
    "visual-regression": {
      "breakpoints": [375, 768, 1024, 1440, 1920],
      "threshold": 0.001,
      "tool": "playwright"
    }
  }
}
```

---

## 3. THRESHOLD CONFIGURATION

### Threshold Levels
- **Strict:** 0.001 (0.1% — catches even minor changes)
- **Normal:** 0.01 (1% — catches significant changes)
- **Loose:** 0.05 (5% — only catches major changes)

### Configure Threshold
```json
{
  "pluginConfig": {
    "visual-regression": {
      "threshold": 0.001,
      "thresholdType": "percent"
    }
  }
}
```

### Per-Test Threshold
```javascript
expect(await page.screenshot()).toMatchSnapshot('hero.png', {
  threshold: 0.001,
  maxDiffPixelRatio: 0.01,
});
```

---

## 4. DIFF VISUALIZATION

### Generate Diff Images
When a test fails, generate a diff image showing the changes:
```javascript
const { toMatchSnapshot } = require('playwright/test');

expect(await page.screenshot()).toMatchSnapshot('hero.png', {
  maxDiffPixelRatio: 0.01,
});
```

### Diff Output
```
.baselines/
  ├── mobile-375/
  │   ├── hero.png (baseline)
  │   ├── hero-actual.png (current)
  │   └── hero-diff.png (diff visualization)
```

### Diff Image Legend
- **Green:** Pixels that match
- **Red:** Pixels that differ
- **Blue:** Pixels that are new/missing

---

## 5. TEST SCRIPTS

### Basic Visual Test
```javascript
const { test, expect } = require('@playwright/test');

test('homepage visual regression', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    threshold: 0.001,
  });
});
```

### Responsive Visual Test
```javascript
const viewports = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1024, height: 768 },
  { name: 'wide', width: 1440, height: 900 },
];

for (const viewport of viewports) {
  test(`homepage ${viewport.name} visual regression`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto('http://localhost:3000');
    await expect(page).toHaveScreenshot(`homepage-${viewport.name}.png`, {
      fullPage: true,
    });
  });
}
```

### Component Visual Test
```javascript
test('button visual regression', async ({ page }) => {
  await page.goto('http://localhost:3000');
  const button = page.locator('.btn-primary');
  await expect(button).toMatchSnapshot('button-primary.png');
});
```

---

## 6. SELECTIVE TESTING

### Test Specific Pages
```bash
# Test only homepage
npx playwright test --grep="homepage"

# Test only mobile
npx playwright test --project=mobile-375

# Test only specific component
npx playwright test --grep="button"
```

### Ignore Regions
```javascript
// Ignore dynamic content
await expect(page).toHaveScreenshot('page.png', {
  mask: [page.locator('.dynamic-content')],
});

// Ignore multiple regions
await expect(page).toHaveScreenshot('page.png', {
  mask: [
    page.locator('.timestamp'),
    page.locator('.user-avatar'),
    page.locator('.ad-banner'),
  ],
});
```

---

## 7. CI INTEGRATION

### GitHub Actions
```yaml
name: Visual Regression
on: [push, pull_request]

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: visual-regression-results
          path: test-results/
```

### Store Baselines in CI
```yaml
- name: Store baselines
  uses: actions/upload-artifact@v3
  with:
    name: baselines
    path: .baselines/
```

---

## 8. CONFIGURATION

### Full Configuration Example
```json
{
  "plugins": ["visual-regression"],
  "pluginConfig": {
    "visual-regression": {
      "breakpoints": [375, 768, 1024, 1440],
      "threshold": 0.001,
      "thresholdType": "percent",
      "tool": "playwright",
      "baselineDir": ".baselines",
      "diffDir": ".baselines/diffs",
      "updateSnapshots": false,
      "fullPage": true,
      "maskDynamic": true,
      "maskSelectors": [".timestamp", ".user-avatar"],
      "ignoreRegions": []
    }
  }
}
```

### Environment Variables
```bash
# Update baselines
UPDATE_SNAPSHOTS=1 npx playwright test

# Strict mode
VISUAL_REGRESSION_STRICT=1 npx playwright test

# Custom threshold
VISUAL_REGRESSION_THRESHOLD=0.005 npx playwright test
```

---

## 9. TROUBLESHOOTING

### Test Fails But No Visual Change
- Check threshold settings (may be too strict)
- Check for dynamic content (timestamps, animations)
- Check for font rendering differences
- Check for anti-aliasing differences

### Baselines Out of Date
- Run `npx playwright test --update-snapshots`
- Commit updated baselines
- Verify changes are intentional

### Slow Tests
- Reduce breakpoint count
- Use component screenshots instead of full page
- Mask dynamic regions
- Run tests in parallel

### Flaky Tests
- Wait for animations to complete
- Mask dynamic content
- Use stable selectors
- Disable animations during testing

---

## 10. BEST PRACTICES

### Do
- Store baselines in version control
- Update baselines when intentional changes are made
- Mask dynamic content (timestamps, avatars, ads)
- Test at all relevant breakpoints
- Use component screenshots for focused testing
- Run visual tests in CI

### Don't
- Commit baselines without reviewing diffs
- Ignore failing visual tests
- Use too strict thresholds for pixel-perfect rendering
- Test at too many breakpoints (focus on key ones)
- Forget to mask dynamic content

### Threshold Guidelines
- **0.001 (0.1%):** Use for critical UI elements (buttons, forms, headers)
- **0.01 (1%):** Use for general page screenshots
- **0.05 (5%):** Use for complex layouts with dynamic content
