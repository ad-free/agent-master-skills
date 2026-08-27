#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();

function main() {
  const toolName = process.env.OPENCODE_TOOL_NAME || '';
  const toolArgs = process.env.OPENCODE_TOOL_ARGS || '{}';
  const toolResult = process.env.OPENCODE_TOOL_RESULT || '';
  
  // Auto-capture evidence for verification commands
  if (toolName === 'Bash') {
    try {
      const args = JSON.parse(toolArgs);
      const command = args.command || '';
      
      // Patterns that indicate verification commands
      const patterns = [
        { label: 'test', regex: /\b(pytest|vitest|jest|npm test|go test|cargo test)\b/ },
        { label: 'lint', regex: /\b(ruff check|eslint|golangci-lint|mypy --strict|tsc --noEmit)\b/ },
        { label: 'typecheck', regex: /\b(mypy|tsc --noEmit|go vet)\b/ },
        { label: 'build', regex: /\b(npm run build|go build|cargo build|python -m build)\b/ },
      ];
      
      for (const p of patterns) {
        if (p.regex.test(command)) {
          console.log(`[evidence-ledger] Auto-capturing evidence for ${p.label}: ${command}`);
          // The evidence CLI will be called by the agent explicitly
          // This hook just logs for awareness
          break;
        }
      }
    } catch {
      // Ignore parse errors
    }
  }
}

main();