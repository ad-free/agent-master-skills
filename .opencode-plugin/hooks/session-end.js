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

function appendToSession(craftDir, content) {
  const state = loadState(craftDir);
  if (state?.sessionFile) {
    const sessionFile = join(craftDir, state.sessionFile);
    if (existsSync(sessionFile)) {
      const existing = readFileSync(sessionFile, 'utf-8');
      writeFileSync(sessionFile, existing + '\n\n' + content);
    }
  }
}

function main() {
  console.log('[agent-master-skills] SessionEnd: Saving project state...');
  
  // Save dev-craft session
  const devState = loadState(DEV_CRAFT_DIR);
  if (devState) {
    appendToSession(DEV_CRAFT_DIR, `## Session Ended: ${new Date().toISOString()}\nFinal phase: ${devState.currentPhase}\nCompleted phases: ${devState.completed?.join(', ') || 'none'}`);
    console.log('[agent-master-skills] dev-craft session saved');
  }
  
  // Save ui-craft session
  const uiState = loadState(UI_CRAFT_DIR);
  if (uiState) {
    appendToSession(UI_CRAFT_DIR, `## Session Ended: ${new Date().toISOString()}\nFinal phase: ${uiState.currentPhase || 'unknown'}`);
    console.log('[agent-master-skills] ui-craft session saved');
  }
  
  // Create handoff document if context is large
  // This would be triggered by context-engineering skill
}

main();