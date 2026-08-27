#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const PROJECT_ROOT = process.cwd();

function main() {
  const toolName = process.env.OPENCODE_TOOL_NAME || '';
  const toolArgs = process.env.OPENCODE_TOOL_ARGS || '{}';
  
  // Track file edits for context engineering
  if (['Write', 'Edit', 'Bash'].includes(toolName)) {
    // Could log to context-engineering for context rotation
  }
  
  // Prevent commits to protected branches
  if (toolName === 'Bash') {
    try {
      const args = JSON.parse(toolArgs);
      const command = args.command || '';
      if (command.includes('git commit') || command.includes('git push')) {
        const branch = execSync('git branch --show-current', { cwd: PROJECT_ROOT, encoding: 'utf-8' }).trim();
        if (['main', 'master', 'develop'].includes(branch)) {
          console.error('[agent-master-skills] BLOCKED: Cannot commit/push to protected branch:', branch);
          console.error('Create a feature branch first: git checkout -b feat/your-feature');
          process.exit(1);
        }
      }
    } catch {
      // Ignore parse errors
    }
  }
}

function execSync(command, options) {
  const { spawnSync } = require('child_process');
  const result = spawnSync(command, { shell: true, ...options });
  return result.stdout.toString();
}

main();