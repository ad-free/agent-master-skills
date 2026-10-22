#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
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

function loadProjectInstincts() {
  const projectsDir = join(GLOBAL_LEARNING_DIR, 'project-learnings');
  if (!existsSync(projectsDir)) return [];
  
  const projects = require('fs').readdirSync(projectsDir);
  let all = [];
  for (const proj of projects) {
    const instincts = loadInstincts(join(projectsDir, proj));
    all.push(...instincts.map(i => ({ ...i, project_dir: proj })));
  }
  return all;
}

function main() {
  const args = process.argv.slice(2);
  const filterStatus = args.includes('--status') ? args[args.indexOf('--status') + 1] : null;
  const filterProject = args.includes('--project') ? args[args.indexOf('--project') + 1] : null;
  const minConfidence = args.includes('--min-confidence') ? parseFloat(args[args.indexOf('--min-confidence') + 1]) : 0;
  const showGlobal = args.includes('--global');
  
  let instincts = loadProjectInstincts();
  
  if (showGlobal) {
    const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
    instincts = instincts.concat(loadInstincts(globalDir).map(i => ({ ...i, project_dir: 'global' })));
  }
  
  if (filterStatus) {
    instincts = instincts.filter(i => i.status === filterStatus);
  }
  
  if (filterProject) {
    instincts = instincts.filter(i => i.project_dir === filterProject || i.project_hash === filterProject);
  }
  
  instincts = instincts.filter(i => i.confidence >= minConfidence);
  
  // Sort by confidence desc, then applications desc
  instincts.sort((a, b) => b.confidence - a.confidence || b.applications - a.applications);
  
  console.log(`\n=== Instincts (${instincts.length} total) ===`);
  
  const byStatus = {};
  for (const i of instincts) {
    if (!byStatus[i.status]) byStatus[i.status] = [];
    byStatus[i.status].push(i);
  }
  
  for (const status of ['promoted', 'reliable', 'active', 'quarantined', 'archived']) {
    const list = byStatus[status] || [];
    if (list.length === 0) continue;
    
    console.log(`\n## ${status.toUpperCase()} (${list.length})`);
    for (const i of list) {
      const age = Math.floor((Date.now() - new Date(i.last_used).getTime()) / (1000 * 60 * 60 * 24));
      console.log(`  [${i.confidence.toFixed(2)}] ${i.id} - ${i.pattern.slice(0, 80)}${i.pattern.length > 80 ? '...' : ''}`);
      console.log(`    Project: ${i.project_dir} | Apps: ${i.applications} | Last used: ${age}d ago | Tags: ${i.tags?.join(', ') || 'none'}`);
    }
  }
}

main();