#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { randomBytes } from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const LEARNING_DIR = join(PROJECT_ROOT, '.agent-master-skills', 'learning');

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

function generateId() {
  return 'inst-' + randomBytes(6).toString('hex');
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

function updateIndex(index, instinct) {
  if (!index.by_project[instinct.project_hash]) index.by_project[instinct.project_hash] = [];
  if (!index.by_project[instinct.project_hash].includes(instinct.id)) {
    index.by_project[instinct.project_hash].push(instinct.id);
  }
  
  instinct.context.tech_stack?.forEach(stack => {
    if (!index.by_stack[stack]) index.by_stack[stack] = [];
    if (!index.by_stack[stack].includes(instinct.id)) {
      index.by_stack[stack].push(instinct.id);
    }
  });
  
  instinct.context.task_types?.forEach(task => {
    if (!index.by_task[task]) index.by_task[task] = [];
    if (!index.by_task[task].includes(instinct.id)) {
      index.by_task[task].push(instinct.id);
    }
  });
  
  if (!index.by_status[instinct.status]) index.by_status[instinct.status] = [];
  if (!index.by_status[instinct.status].includes(instinct.id)) {
    index.by_status[instinct.status].push(instinct.id);
  }
  
  return index;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const pattern = args[0];
  const contextStr = args.includes('--context') ? args[args.indexOf('--context') + 1] : '{}';
  const confidenceStr = args.includes('--confidence') ? args[args.indexOf('--confidence') + 1] : '0.7';
  const tagsStr = args.includes('--tags') ? args[args.indexOf('--tags') + 1] : '';
  
  if (!pattern) {
    console.error('Usage: instinct-save "<pattern>" [--context <json>] [--confidence <0-1>] [--tags <csv>]');
    process.exit(1);
  }
  
  let context = {};
  try {
    context = JSON.parse(contextStr);
  } catch {
    console.error('Invalid --context JSON');
    process.exit(1);
  }
  
  const confidence = parseFloat(confidenceStr);
  if (isNaN(confidence) || confidence < 0 || confidence > 1) {
    console.error('Confidence must be 0-1');
    process.exit(1);
  }
  
  const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(Boolean) : [];
  
  return { pattern, context, confidence, tags };
}

function detectContext() {
  const context = {
    project_patterns: ['**'],
    tech_stack: [],
    task_types: ['feature'],
    file_patterns: ['**/*'],
    skills: [],
  };
  
  const packageJson = join(PROJECT_ROOT, 'package.json');
  if (existsSync(packageJson)) {
    const pkg = JSON.parse(readFileSync(packageJson, 'utf-8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.typescript) context.tech_stack.push('TypeScript');
    if (deps.react) context.tech_stack.push('React');
    if (deps.vue) context.tech_stack.push('Vue');
    if (deps.next) context.tech_stack.push('Next.js');
    if (deps.tailwindcss) context.tech_stack.push('Tailwind');
  }
  
  const devCraftState = join(PROJECT_ROOT, '.dev-craft', 'state.json');
  if (existsSync(devCraftState)) {
    context.skills.push('dev-craft');
  }
  const uiCraftState = join(PROJECT_ROOT, '.ui-craft', 'state.json');
  if (existsSync(uiCraftState)) {
    context.skills.push('ui-craft');
  }
  
  return context;
}

function main() {
  const { pattern, context: userContext, confidence, tags } = parseArgs();
  
  const projectHash = getProjectHash();
  const projectDir = join(LEARNING_DIR, 'project-learnings', projectHash);
  
  const instincts = loadInstincts(projectDir);
  const index = loadIndex(projectDir);
  
  // Merge user context with detected context
  const detectedContext = detectContext();
  const mergedContext = {
    project_patterns: userContext.project_patterns || detectedContext.project_patterns,
    tech_stack: [...new Set([...(userContext.tech_stack || []), ...detectedContext.tech_stack])],
    task_types: [...new Set([...(userContext.task_types || []), ...detectedContext.task_types])],
    file_patterns: [...new Set([...(userContext.file_patterns || []), ...detectedContext.file_patterns])],
    skills: [...new Set([...(userContext.skills || []), ...detectedContext.skills])],
  };
  
  const instinct = {
    id: generateId(),
    pattern,
    context: mergedContext,
    confidence,
    source: {
      session_id: 'explicit-save',
      timestamp: new Date().toISOString(),
      trigger: 'explicit',
      extracted_by: 'user'
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    applications: 1,
    last_used: new Date().toISOString(),
    status: confidence >= 0.5 ? 'active' : 'quarantined',
    project_hash: projectHash,
    tags,
  };
  
  instincts.push(instinct);
  updateIndex(index, instinct);
  
  saveInstincts(projectDir, instincts);
  saveIndex(projectDir, index);
  
  console.log(`✓ Saved instinct: ${instinct.id}`);
  console.log(`  Confidence: ${confidence} (${instinct.status})`);
  console.log(`  Pattern: ${pattern}`);
  console.log(`  Context: ${mergedContext.tech_stack.join(', ') || 'general'}`);
}

main();