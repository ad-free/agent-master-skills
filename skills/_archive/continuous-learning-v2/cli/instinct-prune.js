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

function main() {
  const args = process.argv.slice(2);
  const days = args.includes('--days') ? parseInt(args[args.indexOf('--days') + 1]) : 90;
  const minConfidence = args.includes('--min-confidence') ? parseFloat(args[args.indexOf('--min-confidence') + 1]) : 0.3;
  const dryRun = args.includes('--dry-run');
  const projectOnly = args.includes('--project-only');
  
  const dirs = [];
  const projectsDir = join(GLOBAL_LEARNING_DIR, 'project-learnings');
  if (existsSync(projectsDir)) {
    for (const proj of require('fs').readdirSync(projectsDir)) {
      dirs.push(join(projectsDir, proj));
    }
  }
  
  if (!projectOnly) {
    const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
    if (existsSync(globalDir)) dirs.push(globalDir);
  }
  
  let totalRemoved = 0;
  let totalArchived = 0;
  
  for (const dir of dirs) {
    const instincts = loadInstincts(dir);
    if (instincts.length === 0) continue;
    
    const now = Date.now();
    const dayMs = 24 * 60 * 60 * 1000;
    
    const kept = [];
    const archived = [];
    
    for (const i of instincts) {
      const daysSinceUse = (now - new Date(i.last_used).getTime()) / dayMs;
      const shouldArchive = daysSinceUse > days || i.confidence < minConfidence;
      const shouldRemove = i.status === 'archived' && daysSinceUse > days * 2;
      
      if (shouldRemove) {
        totalRemoved++;
        console.log(`  REMOVE: ${i.id} (archived ${daysSinceUse.toFixed(0)}d ago, conf: ${i.confidence.toFixed(2)})`);
      } else if (shouldArchive && i.status !== 'archived') {
        i.status = 'archived';
        i.updated_at = new Date().toISOString();
        archived.push(i);
        totalArchived++;
        console.log(`  ARCHIVE: ${i.id} (unused ${daysSinceUse.toFixed(0)}d, conf: ${i.confidence.toFixed(2)})`);
      } else {
        kept.push(i);
      }
    }
    
    if (!dryRun) {
      saveInstincts(dir, [...kept, ...archived]);
      saveIndex(dir, rebuildIndex([...kept, ...archived]));
    }
  }
  
  console.log(`\n${dryRun ? '[DRY RUN] ' : ''}Complete: ${totalArchived} archived, ${totalRemoved} removed`);
}

main();