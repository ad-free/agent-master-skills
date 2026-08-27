#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';

const PROJECT_ROOT = process.cwd();
const DEV_CRAFT_DIR = join(PROJECT_ROOT, '.dev-craft');
const UI_CRAFT_DIR = join(PROJECT_ROOT, '.ui-craft');

function loadState(craftDir) {
  const statePath = join(craftDir, 'state.json');
  if (existsSync(statePath)) {
    try {
      return JSON.parse(readFileSync(statePath, 'utf-8'));
    } catch {
      return null;
    }
  }
  return null;
}

function saveState(craftDir, state) {
  mkdirSync(craftDir, { recursive: true });
  writeFileSync(join(craftDir, 'state.json'), JSON.stringify(state, null, 2));
}

function getCurrentSessionFile(craftDir) {
  const state = loadState(craftDir);
  if (state?.sessionFile) {
    return join(craftDir, state.sessionFile);
  }
  return null;
}

function appendToSession(craftDir, content) {
  const sessionFile = getCurrentSessionFile(craftDir);
  if (sessionFile && existsSync(sessionFile)) {
    const existing = readFileSync(sessionFile, 'utf-8');
    writeFileSync(sessionFile, existing + '\n\n' + content);
  }
}

function main() {
  console.log('[agent-master-skills] SessionStart: Loading project state...');
  
  // Load dev-craft state
  const devState = loadState(DEV_CRAFT_DIR);
  if (devState) {
    console.log(`[agent-master-skills] dev-craft: Phase ${devState.currentPhase}, Branch: ${devState.activeBranch || 'none'}`);
    if (devState.sessionFile) {
      appendToSession(DEV_CRAFT_DIR, `## Session Resumed: ${new Date().toISOString()}\nResumed from phase: ${devState.currentPhase}`);
    }
  }
  
  // Load ui-craft state
  const uiState = loadState(UI_CRAFT_DIR);
  if (uiState) {
    console.log(`[agent-master-skills] ui-craft: Phase ${uiState.currentPhase || 'unknown'}`);
    if (uiState.sessionFile) {
      appendToSession(UI_CRAFT_DIR, `## Session Resumed: ${new Date().toISOString()}\nResumed from phase: ${uiState.currentPhase || 'unknown'}`);
    }
  }
  
  // Check for skill updates (throttled to once per hour)
  const updateFlag = join(PROJECT_ROOT, '.agent-skills-last-update');
  const now = Date.now();
  const ONE_HOUR = 60 * 60 * 1000;
  
  if (existsSync(updateFlag)) {
    const lastUpdate = parseInt(readFileSync(updateFlag, 'utf-8'), 10);
    if (now - lastUpdate < ONE_HOUR) {
      console.log('[agent-master-skills] Skipping update check (throttled)');
    } else {
      writeFileSync(updateFlag, String(now));
      console.log('[agent-master-skills] Checking for skill updates...');
      // Non-blocking update check - would run in background
    }
  } else {
    writeFileSync(updateFlag, String(now));
  }
  
  // Load context.md files for shared language
  const devContext = join(DEV_CRAFT_DIR, 'context.md');
  const uiContext = join(UI_CRAFT_DIR, 'context.md');
  
  if (existsSync(devContext)) {
    console.log('[agent-master-skills] Loaded dev-craft context.md');
  }
  if (existsSync(uiContext)) {
    console.log('[agent-master-skills] Loaded ui-craft context.md');
  }
}

main();