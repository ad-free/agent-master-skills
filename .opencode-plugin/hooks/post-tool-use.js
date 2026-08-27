#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

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
  const toolName = process.env.OPENCODE_TOOL_NAME || '';
  const toolArgs = process.env.OPENCODE_TOOL_ARGS || '{}';
  const toolResult = process.env.OPENCODE_TOOL_RESULT || '';
  
  // Auto-save dev-craft state on phase transitions
  if (toolName === 'Bash') {
    try {
      const args = JSON.parse(toolArgs);
      const command = args.command || '';
      
      // Detect phase transitions in dev-craft
      if (command.includes('dev-craft') || command.includes('Phase')) {
        const devState = loadState(DEV_CRAFT_DIR);
        if (devState) {
          appendToSession(DEV_CRAFT_DIR, `### Tool: ${toolName}\n\`\`\`bash\n${command}\n\`\`\`\nResult: ${toolResult.slice(0, 500)}`);
        }
      }
    } catch {
      // Ignore
    }
  }
  
  // Track test runs for verification evidence
  if (toolName === 'Bash') {
    try {
      const args = JSON.parse(toolArgs);
      const command = args.command || '';
      if (command.includes('test') || command.includes('pytest') || command.includes('vitest') || command.includes('jest')) {
        const evidenceDir = join(PROJECT_ROOT, '.dev-craft', 'evidence');
        mkdirSync(evidenceDir, { recursive: true });
        const evidenceFile = join(evidenceDir, `test-${Date.now()}.json`);
        writeFileSync(evidenceFile, JSON.stringify({
          timestamp: new Date().toISOString(),
          command,
          result: toolResult.slice(0, 2000),
        }, null, 2));
      }
    } catch {
      // Ignore
    }
  }
}

main();