#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const GLOBAL_LEARNING_DIR = join(process.env.HOME || '', '.agent-master-skills', 'learning');

function loadInstincts(dir) {
  const file = join(dir, 'instincts.jsonl');
  if (!existsSync(file)) return [];
  const content = readFileSync(file, 'utf-8');
  return content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

function main() {
  const args = process.argv.slice(2);
  const projectHash = args.includes('--project') ? args[args.indexOf('--project') + 1] : null;
  const promotedOnly = args.includes('--promoted-only');
  const outputFile = args.includes('--output') ? args[args.indexOf('--output') + 1] : null;
  
  let allInstincts = [];
  
  if (promotedOnly) {
    const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
    if (existsSync(globalDir)) {
      allInstincts = loadInstincts(globalDir);
    }
  } else if (projectHash) {
    const projectDir = join(GLOBAL_LEARNING_DIR, 'project-learnings', projectHash);
    if (existsSync(projectDir)) {
      allInstincts = loadInstincts(projectDir);
    }
  } else {
    // Export all projects
    const projectsDir = join(GLOBAL_LEARNING_DIR, 'project-learnings');
    if (existsSync(projectsDir)) {
      for (const proj of require('fs').readdirSync(projectsDir)) {
        const instincts = loadInstincts(join(projectsDir, proj));
        allInstincts.push(...instincts);
      }
    }
    // Also include global promoted
    const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
    if (existsSync(globalDir)) {
      allInstincts.push(...loadInstincts(globalDir));
    }
  }
  
  // Filter to only export active+ instincts by default
  const toExport = allInstincts.filter(i => 
    promotedOnly ? i.status === 'promoted' : ['active', 'reliable', 'promoted'].includes(i.status)
  );
  
  const output = toExport.map(i => JSON.stringify(i)).join('\n') + '\n';
  
  if (outputFile) {
    writeFileSync(outputFile, output);
    console.log(`✓ Exported ${toExport.length} instincts to ${outputFile}`);
  } else {
    process.stdout.write(output);
  }
}

main();