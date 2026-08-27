#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PROJECT_ROOT = process.cwd();
const GLOBAL_LEARNING_DIR = join(process.env.HOME || '', '.agent-master-skills', 'learning');

function getProjectHash() {
  try {
    const { execSync } = require('child_process');
    const remote = execSync('git config --get remote.origin.url', { cwd: PROJECT_ROOT, encoding: 'utf-8' }).trim();
    if (remote) {
      return require('crypto').createHash('md5').update(remote).digest('hex').slice(0, 12);
    }
  } catch {}
  return require('crypto').createHash('md5').update(PROJECT_ROOT).digest('hex').slice(0, 12);
}

function loadInstincts(dir) {
  const file = join(dir, 'instincts.jsonl');
  if (!existsSync(file)) return [];
  const content = readFileSync(file, 'utf-8');
  return content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

function saveInstincts(dir, instincts) {
  mkdirSync(dir, { recursive: true });
  const file = join(dir, 'instincts.jsonl');
  const content = instincts.map(i => JSON.stringify(i)).join('\n') + '\n';
  writeFileSync(file, content);
}

function loadIndex(dir) {
  const file = join(dir, 'index.json');
  if (!existsSync(file)) return { by_project: {}, by_stack: {}, by_task: {}, by_status: {} };
  return JSON.parse(readFileSync(file, 'utf-8'));
}

function saveIndex(dir, index) {
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'index.json'), JSON.stringify(index, null, 2));
}

function rebuildIndex(instincts) {
  const index = { by_project: {}, by_stack: {}, by_task: {}, by_status: {} };
  for (const i of instincts) {
    if (!index.by_project[i.project_hash]) index.by_project[i.project_hash] = [];
    index.by_project[i.project_hash].push(i.id);
    
    i.context.tech_stack?.forEach(stack => {
      if (!index.by_stack[stack]) index.by_stack[stack] = [];
      index.by_stack[stack].push(i.id);
    });
    
    i.context.task_types?.forEach(task => {
      if (!index.by_task[task]) index.by_task[task] = [];
      index.by_task[task].push(i.id);
    });
    
    if (!index.by_status[i.status]) index.by_status[i.status] = [];
    index.by_status[i.status].push(i.id);
  }
  return index;
}

function findExisting(instincts, pattern) {
  for (const i of instincts) {
    const similarity = jaccardSimilarity(i.pattern.toLowerCase(), pattern.toLowerCase());
    if (similarity > 0.7) return i;
  }
  return null;
}

function jaccardSimilarity(a, b) {
  const setA = new Set(a.split(/\s+/).filter(w => w.length > 3));
  const setB = new Set(b.split(/\s+/).filter(w => w.length > 3));
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return union.size > 0 ? intersection.size / union.size : 0;
}

function main() {
  const args = process.argv.slice(2);
  const inputFile = args[0];
  const mergeStrategy = args.includes('--strategy') ? args[args.indexOf('--strategy') + 1] : 'merge';
  // strategies: merge (update existing, add new), replace (replace all), skip-existing
  
  if (!inputFile || !existsSync(inputFile)) {
    console.error('Usage: instinct-import <file.jsonl> [--strategy merge|replace|skip-existing]');
    process.exit(1);
  }
  
  const content = readFileSync(inputFile, 'utf-8');
  const imported = content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
  
  const projectHash = getProjectHash();
  const projectDir = join(GLOBAL_LEARNING_DIR, 'project-learnings', projectHash);
  
  const instincts = loadInstincts(projectDir);
  const index = loadIndex(projectDir);
  
  let added = 0, updated = 0, skipped = 0;
  
  for (const imp of imported) {
    // Update project hash to current project
    imp.project_hash = projectHash;
    imp.updated_at = new Date().toISOString();
    imp.source = {
      ...imp.source,
      trigger: 'import',
      extracted_by: 'instinct-import'
    };
    
    const existing = findExisting(instincts, imp.pattern);
    
    if (existing) {
      if (mergeStrategy === 'skip-existing') {
        skipped++;
        continue;
      } else if (mergeStrategy === 'merge') {
        // Merge: keep higher confidence, sum applications
        existing.confidence = Math.max(existing.confidence, imp.confidence);
        existing.applications += imp.applications;
        existing.last_used = new Date().toISOString();
        existing.tags = [...new Set([...(existing.tags || []), ...(imp.tags || [])])];
        updated++;
      } else if (mergeStrategy === 'replace') {
        // Replace with imported
        Object.assign(existing, imp);
        updated++;
      }
    } else {
      instincts.push(imp);
      added++;
    }
  }
  
  // Rebuild index
  const newIndex = rebuildIndex(instincts);
  
  saveInstincts(projectDir, instincts);
  saveIndex(projectDir, newIndex);
  
  console.log(`✓ Import complete: ${added} added, ${updated} updated, ${skipped} skipped`);
}

main();