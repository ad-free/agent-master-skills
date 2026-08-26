---
name: playwright-skill
description: |
  Use when you want to test websites, automate browser interactions, validate web functionality,
  or perform any browser-based testing including screenshots, forms, responsive design, and UX validation.
model: gpt-5-nano
version: 1.0.1
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
metadata:
  origin: external (playwright-skill)
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Playwright Browser Automation

Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task.
