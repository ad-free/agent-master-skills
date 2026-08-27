#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const LEARNING_DIR = join(PROJECT_ROOT, '.agent-master-skills', 'learning');
const GLOBAL_LEARNING_DIR = join(process.env.HOME || '', '.agent-master-skills', 'learning');

function getProjectHash() {
  // Simple hash from git remote or directory name
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

function loadIndex(dir) {
  const file = join(dir, 'index.json');
  if (!existsSync(file)) return { by_project: {}, by_stack: {}, by_task: {}, by_status: {} };
  return JSON.parse(readFileSync(file, 'utf-8'));
}

function matchContext(instinct, context) {
  let score = 0;
  let matches = 0;
  
  // Project match
  if (instinct.context.project_patterns?.some(p => minimatch(context.projectPath, p))) {
    score += 0.3; matches++;
  }
  
  // Tech stack match
  if (instinct.context.tech_stack?.some(s => context.techStack.includes(s))) {
    score += 0.25; matches++;
  }
  
  // Task type match
  if (instinct.context.task_types?.includes(context.taskType)) {
    score += 0.2; matches++;
  }
  
  // File pattern match
  if (instinct.context.file_patterns?.some(p => context.filePatterns.some(f => minimatch(f, p)))) {
    score += 0.15; matches++;
  }
  
  // Skill match
  if (instinct.context.skills?.some(s => context.activeSkills.includes(s))) {
    score += 0.1; matches++;
  }
  
  return matches > 0 ? score / matches : 0;
}

// Simple minimatch implementation
function minimatch(str, pattern) {
  const regex = new RegExp('^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$');
  return regex.test(str);
}

function getRecencyFactor(lastUsed) {
  const days = (Date.now() - new Date(lastUsed).getTime()) / (1000 * 60 * 60 * 24);
  if (days < 7) return 1.0;
  if (days < 30) return 0.8;
  if (days < 90) return 0.5;
  return 0.2;
}

function detectContext() {
  const context = {
    projectPath: PROJECT_ROOT,
    techStack: [],
    taskType: 'feature',
    filePatterns: [],
    activeSkills: [],
  };
  
  // Detect tech stack
  const packageJson = join(PROJECT_ROOT, 'package.json');
  if (existsSync(packageJson)) {
    const pkg = JSON.parse(readFileSync(packageJson, 'utf-8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.typescript) context.techStack.push('TypeScript');
    if (deps.react) context.techStack.push('React');
    if (deps.vue) context.techStack.push('Vue');
    if (deps.next) context.techStack.push('Next.js');
    if (deps.tailwindcss) context.techStack.push('Tailwind');
    if (deps.python || deps.pytest) context.techStack.push('Python');
    if (deps.go) context.techStack.push('Go');
    if (deps.rust) context.techStack.push('Rust');
  }
  
  const pyproject = join(PROJECT_ROOT, 'pyproject.toml');
  if (existsSync(pyproject)) {
    context.techStack.push('Python');
  }
  
  const goMod = join(PROJECT_ROOT, 'go.mod');
  if (existsSync(goMod)) {
    context.techStack.push('Go');
  }
  
  // Detect active skills from .dev-craft / .ui-craft
  const devCraftState = join(PROJECT_ROOT, '.dev-craft', 'state.json');
  if (existsSync(devCraftState)) {
    const state = JSON.parse(readFileSync(devCraftState, 'utf-8'));
    context.activeSkills.push('dev-craft');
    if (state.currentPhase) context.taskType = state.currentPhase.toLowerCase();
  }
  
  const uiCraftState = join(PROJECT_ROOT, '.ui-craft', 'state.json');
  if (existsSync(uiCraftState)) {
    context.activeSkills.push('ui-craft');
  }
  
  return context;
}

function main() {
  const projectHash = getProjectHash();
  const context = detectContext();
  
  // Load project instincts
  const projectDir = join(LEARNING_DIR, 'project-learnings', projectHash);
  const projectInstincts = loadInstincts(projectDir);
  
  // Load global promoted instincts
  const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
  const globalInstincts = loadInstincts(globalDir);
  
  // Combine and filter active+ instincts
  const allInstincts = [...projectInstincts, ...globalInstincts]
    .filter(i => ['active', 'reliable', 'promoted'].includes(i.status));
  
  // Score and rank
  const ranked = allInstincts
    .map(i => {
      const relevance = matchContext(i, context);
      const recency = getRecencyFactor(i.last_used);
      const injectionScore = i.confidence * relevance * recency;
      return { ...i, relevance, recency, injectionScore };
    })
    .filter(i => i.injectionScore > 0.3)
    .sort((a, b) => b.injectionScore - a.injectionScore)
    .slice(0, 5);
  
  if (ranked.length > 0) {
    console.log('\n## Injected Instincts (from continuous-learning-v2)');
    ranked.forEach((instinct, idx) => {
      console.log(`${idx + 1}. [${instinct.confidence.toFixed(2)}] ${instinct.pattern.slice(0, 100)}${instinct.pattern.length > 100 ? '...' : ''}`);
      console.log(`   Context: ${instinct.context.tech_stack?.join(', ') || 'general'}, ${instinct.context.task_types?.join(', ') || 'any'}`);
      console.log(`   Source: ${instinct.source.session_id}, ${instinct.applications} applications`);
      console.log('');
    });
  }
}

main();