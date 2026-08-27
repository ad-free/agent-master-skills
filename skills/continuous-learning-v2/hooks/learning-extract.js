#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join, resolve } from 'path';
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
  // by_project
  if (!index.by_project[instinct.project_hash]) index.by_project[instinct.project_hash] = [];
  if (!index.by_project[instinct.project_hash].includes(instinct.id)) {
    index.by_project[instinct.project_hash].push(instinct.id);
  }
  
  // by_stack
  instinct.context.tech_stack?.forEach(stack => {
    if (!index.by_stack[stack]) index.by_stack[stack] = [];
    if (!index.by_stack[stack].includes(instinct.id)) {
      index.by_stack[stack].push(instinct.id);
    }
  });
  
  // by_task
  instinct.context.task_types?.forEach(task => {
    if (!index.by_task[task]) index.by_task[task] = [];
    if (!index.by_task[task].includes(instinct.id)) {
      index.by_task[task].push(instinct.id);
    }
  });
  
  // by_status
  if (!index.by_status[instinct.status]) index.by_status[instinct.status] = [];
  if (!index.by_status[instinct.status].includes(instinct.id)) {
    index.by_status[instinct.status].push(instinct.id);
  }
  
  return index;
}

function extractPatternsFromSession(sessionFile) {
  // This would use an LLM to extract patterns from the session transcript
  // For now, we'll extract based on heuristics from session files
  const patterns = [];
  
  if (!existsSync(sessionFile)) return patterns;
  
  const content = readFileSync(sessionFile, 'utf-8');
  
  // Heuristic patterns to look for
  const heuristics = [
    { regex: /(?:always|never|make sure to|don't forget to|remember to)\s+([^.]+)/gi, type: 'convention' },
    { regex: /(?:we decided|the pattern is|convention is|standard is)\s+([^.]+)/gi, type: 'decision' },
    { regex: /(?:instead|better to|prefer|use)\s+([^.]+)/gi, type: 'preference' },
    { regex: /(?:fixed by|resolved by|solution was)\s+([^.]+)/gi, type: 'fix' },
    { regex: /(?:root cause|because|due to)\s+([^.]+)/gi, type: 'root-cause' },
  ];
  
  for (const h of heuristics) {
    const matches = content.matchAll(h.regex);
    for (const match of matches) {
      if (match[1] && match[1].length > 20 && match[1].length < 500) {
        patterns.push({
          pattern: match[1].trim(),
          type: h.type,
          source_text: match[0].slice(0, 200)
        });
      }
    }
  }
  
  // Also extract from dev-craft state
  const devCraftDir = join(PROJECT_ROOT, '.dev-craft');
  const stateFile = join(devCraftDir, 'state.json');
  if (existsSync(stateFile)) {
    const state = JSON.parse(readFileSync(stateFile, 'utf-8'));
    if (state.currentPhase && state.completed) {
      patterns.push({
        pattern: `Completed ${state.currentPhase} phase in dev-craft pipeline for ${state.scope || 'fullstack'} work`,
        type: 'workflow',
        source_text: 'dev-craft state'
      });
    }
  }
  
  return patterns;
}

function calculateBaseConfidence(trigger) {
  const bases = {
    'explicit': 0.7,
    'retro': 0.6,
    'code-review': 0.5,
    'bug-fix': 0.4,
    'handoff': 0.4,
    'session-end': 0.3,
  };
  return bases[trigger] || 0.3;
}

function findExistingInstinct(instincts, pattern) {
  // Simple deduplication - check for similar patterns
  for (const inst of instincts) {
    const similarity = jaccardSimilarity(inst.pattern.toLowerCase(), pattern.toLowerCase());
    if (similarity > 0.7) return inst;
  }
  return null;
}

function jaccardSimilarity(a, b) {
  const setA = new Set(a.split(/\s+/).filter(w => w.length > 3));
  const setB = new Set(b.split(/\s+/).filter(w => w.length > 3));
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return intersection.size / union.size;
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
  console.log('[continuous-learning-v2] Extracting patterns from session...');
  
  const projectHash = getProjectHash();
  const projectDir = join(LEARNING_DIR, 'project-learnings', projectHash);
  
  // Find latest session file
  const devCraftSessions = join(PROJECT_ROOT, '.dev-craft', 'sessions');
  const uiCraftSessions = join(PROJECT_ROOT, '.ui-craft', 'sessions');
  
  let sessionFiles = [];
  if (existsSync(devCraftSessions)) {
    sessionFiles = sessionFiles.concat(
      require('fs').readdirSync(devCraftSessions)
        .filter(f => f.endsWith('.md'))
        .map(f => join(devCraftSessions, f))
    );
  }
  if (existsSync(uiCraftSessions)) {
    sessionFiles = sessionFiles.concat(
      require('fs').readdirSync(uiCraftSessions)
        .filter(f => f.endsWith('.md'))
        .map(f => join(uiCraftSessions, f))
    );
  }
  
  if (sessionFiles.length === 0) {
    console.log('[continuous-learning-v2] No session files found');
    return;
  }
  
  // Use the most recent session
  const latestSession = sessionFiles.sort().reverse()[0];
  console.log(`[continuous-learning-v2] Analyzing ${latestSession}`);
  
  const patterns = extractPatternsFromSession(latestSession);
  console.log(`[continuous-learning-v2] Extracted ${patterns.length} candidate patterns`);
  
  // Load existing instincts
  const instincts = loadInstincts(projectDir);
  const index = loadIndex(projectDir);
  
  let newCount = 0;
  for (const p of patterns) {
    const existing = findExistingInstinct(instincts, p.pattern);
    if (existing) {
      // Update existing - increment applications if this session confirms it
      existing.applications += 1;
      existing.last_used = new Date().toISOString();
      existing.updated_at = new Date().toISOString();
      console.log(`[continuous-learning-v2] Updated existing: ${existing.id} (now ${existing.applications} apps)`);
    } else {
      // Create new instinct
      const instinct = {
        id: generateId(),
        pattern: p.pattern,
        context: detectContext(),
        confidence: calculateBaseConfidence('session-end'),
        source: {
          session_id: latestSession.split('/').pop()?.replace('.md', '') || 'unknown',
          timestamp: new Date().toISOString(),
          trigger: 'session-end',
          extracted_by: 'continuous-learning-v2'
        },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        applications: 1,
        last_used: new Date().toISOString(),
        status: 'quarantined',
        project_hash: projectHash,
        tags: [p.type],
      };
      
      instincts.push(instinct);
      updateIndex(index, instinct);
      newCount++;
      console.log(`[continuous-learning-v2] New instinct: ${instinct.id} (${instinct.confidence})`);
    }
  }
  
  // Save
  saveInstincts(projectDir, instincts);
  saveIndex(projectDir, index);
  
  console.log(`[continuous-learning-v2] Saved ${newCount} new instincts, ${instincts.length} total`);
}

main();