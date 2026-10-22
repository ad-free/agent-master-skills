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

function clusterInstincts(instincts) {
  // Simple clustering by context similarity
  const clusters = [];
  const used = new Set();
  
  for (const i of instincts) {
    if (used.has(i.id)) continue;
    
    const cluster = [i];
    used.add(i.id);
    
    for (const j of instincts) {
      if (used.has(j.id)) continue;
      
      const contextSim = contextSimilarity(i, j);
      const patternSim = jaccardSimilarity(i.pattern.toLowerCase(), j.pattern.toLowerCase());
      
      if (contextSim > 0.5 && patternSim > 0.3) {
        cluster.push(j);
        used.add(j.id);
      }
    }
    
    if (cluster.length >= 2) {
      clusters.push(cluster);
    }
  }
  
  return clusters;
}

function contextSimilarity(a, b) {
  let matches = 0, total = 0;
  
  // Tech stack
  const aStack = new Set(a.context.tech_stack || []);
  const bStack = new Set(b.context.tech_stack || []);
  const stackIntersection = [...aStack].filter(x => bStack.has(x)).length;
  const stackUnion = new Set([...aStack, ...bStack]).size;
  if (stackUnion > 0) {
    matches += stackIntersection / stackUnion;
    total++;
  }
  
  // Task types
  const aTask = new Set(a.context.task_types || []);
  const bTask = new Set(b.context.task_types || []);
  const taskIntersection = [...aTask].filter(x => bTask.has(x)).length;
  const taskUnion = new Set([...aTask, ...bTask]).size;
  if (taskUnion > 0) {
    matches += taskIntersection / taskUnion;
    total++;
  }
  
  // Skills
  const aSkills = new Set(a.context.skills || []);
  const bSkills = new Set(b.context.skills || []);
  const skillsIntersection = [...aSkills].filter(x => bSkills.has(x)).length;
  const skillsUnion = new Set([...aSkills, ...bSkills]).size;
  if (skillsUnion > 0) {
    matches += skillsIntersection / skillsUnion;
    total++;
  }
  
  return total > 0 ? matches / total : 0;
}

function jaccardSimilarity(a, b) {
  const setA = new Set(a.split(/\s+/).filter(w => w.length > 3));
  const setB = new Set(b.split(/\s+/).filter(w => w.length > 3));
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return union.size > 0 ? intersection.size / union.size : 0;
}

function generateSkillFromCluster(cluster) {
  // Generate a skill name from the cluster
  const commonWords = getCommonWords(cluster.map(c => c.pattern));
  const name = commonWords.slice(0, 3).join('-').toLowerCase().replace(/[^a-z0-9-]/g, '');
  
  const avgConfidence = cluster.reduce((sum, c) => sum + c.confidence, 0) / cluster.length;
  const totalApps = cluster.reduce((sum, c) => sum + c.applications, 0);
  
  // Determine skill type from context
  const allStacks = new Set();
  const allTasks = new Set();
  const allSkills = new Set();
  
  for (const c of cluster) {
    c.context.tech_stack?.forEach(s => allStacks.add(s));
    c.context.task_types?.forEach(t => allTasks.add(t));
    c.context.skills?.forEach(s => allSkills.add(s));
  }
  
  return {
    suggested_name: name || `skill-${cluster[0].id.slice(0, 6)}`,
    description: `Auto-generated from ${cluster.length} related instincts (avg confidence: ${avgConfidence.toFixed(2)}, total apps: ${totalApps})`,
    patterns: cluster.map(c => c.pattern),
    context: {
      tech_stack: [...allStacks],
      task_types: [...allTasks],
      skills: [...allSkills],
    },
    confidence: avgConfidence,
    instinct_ids: cluster.map(c => c.id),
  };
}

function getCommonWords(patterns) {
  const wordCounts = {};
  for (const p of patterns) {
    const words = p.toLowerCase().split(/\s+/).filter(w => w.length > 4);
    for (const w of words) {
      wordCounts[w] = (wordCounts[w] || 0) + 1;
    }
  }
  return Object.entries(wordCounts)
    .filter(([_, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .map(([word]) => word);
}

function main() {
  const args = process.argv.slice(2);
  const minConfidence = args.includes('--min-confidence') ? parseFloat(args[args.indexOf('--min-confidence') + 1]) : 0.6;
  const minClusterSize = args.includes('--min-size') ? parseInt(args[args.indexOf('--min-size') + 1]) : 3;
  const projectHash = args.includes('--project') ? args[args.indexOf('--project') + 1] : null;
  
  let allInstincts = [];
  
  if (projectHash) {
    const projectDir = join(GLOBAL_LEARNING_DIR, 'project-learnings', projectHash);
    if (existsSync(projectDir)) {
      allInstincts = loadInstincts(projectDir);
    }
  } else {
    // Global promoted instincts
    const globalDir = join(GLOBAL_LEARNING_DIR, 'global-promoted');
    if (existsSync(globalDir)) {
      allInstincts = loadInstincts(globalDir);
    }
  }
  
  // Filter by confidence
  allInstincts = allInstincts.filter(i => i.confidence >= minConfidence && i.status !== 'archived');
  
  if (allInstincts.length < minClusterSize) {
    console.log(`Not enough instincts (${allInstincts.length}) to form clusters (min: ${minClusterSize})`);
    return;
  }
  
  const clusters = clusterInstincts(allInstincts);
  
  console.log(`\n=== Skill Evolution Candidates (${clusters.length} clusters) ===\n`);
  
  for (const cluster of clusters) {
    if (cluster.length < minClusterSize) continue;
    
    const skill = generateSkillFromCluster(cluster);
    
    console.log(`## ${skill.suggested_name}`);
    console.log(`  ${skill.description}`);
    console.log(`  Context: ${skill.context.tech_stack.join(', ') || 'any'}, ${skill.context.task_types.join(', ') || 'any'}`);
    console.log(`  Avg confidence: ${skill.confidence.toFixed(2)} | Instincts: ${skill.instinct_ids.length}`);
    console.log(`  Patterns:`);
    for (const p of skill.patterns.slice(0, 3)) {
      console.log(`    - ${p.slice(0, 100)}${p.length > 100 ? '...' : ''}`);
    }
    if (skill.patterns.length > 3) console.log(`    ... and ${skill.patterns.length - 3} more`);
    console.log('');
  }
  
  console.log('Run skill-creator to generate SKILL.md from these clusters.');
}

main();