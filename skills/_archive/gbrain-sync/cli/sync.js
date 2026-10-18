#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const GBRAIN_DIR = join(process.env.HOME || '', '.gbrain');
const CONFIG_FILE = join(GBRAIN_DIR, 'config.yaml');
const PROJECT_ROOT = process.cwd();

function loadConfig() {
  if (!existsSync(CONFIG_FILE)) return null;
  const content = readFileSync(CONFIG_FILE, 'utf-8');
  const config = {};
  for (const line of content.split('\n')) {
    const match = line.match(/^(\w+):\s*(.+)$/);
    if (match) {
      config[match[1]] = match[2].replace(/^["']|["']$/g, '');
    }
  }
  return config;
}

function getChangedFiles(full = false) {
  if (full) {
    try {
      return execSync('git ls-files', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
        .trim().split('\n').filter(Boolean);
    } catch {
      return [];
    }
  }
  
  try {
    // Get files changed since last sync
    const lastSyncFile = join(GBRAIN_DIR, '.last-sync');
    let since = 'HEAD';
    if (existsSync(lastSyncFile)) {
      const lastSyncCommit = readFileSync(lastSyncFile, 'utf-8').trim();
      since = lastSyncCommit;
    }
    
    const output = execSync(`git diff --name-only ${since}..HEAD`, { cwd: PROJECT_ROOT, encoding: 'utf-8' });
    return output.trim().split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

function updateLastSync() {
  try {
    const commit = execSync('git rev-parse HEAD', { cwd: PROJECT_ROOT, encoding: 'utf-8' }).trim();
    writeFileSync(join(GBRAIN_DIR, '.last-sync'), commit);
  } catch {}
}

export async function sync(options) {
  const { full, dryRun, strategy } = options;
  
  const config = loadConfig();
  if (!config) {
    console.error('GBrain not configured. Run "gbrain-sync init" first.');
    process.exit(1);
  }
  
  console.log(`GBrain Sync (${config.backend})`);
  console.log('========================\n');
  
  const files = getChangedFiles(full);
  
  if (files.length === 0) {
    console.log('No changes to sync');
    return;
  }
  
  console.log(`${full ? 'Full reindex' : 'Incremental sync'} - ${files.length} file(s)`);
  console.log(`Strategy: ${strategy}\n`);
  
  if (dryRun) {
    console.log('Files to sync:');
    files.forEach(f => console.log(`  ${f}`));
    return;
  }
  
  // Filter by strategy
  let filteredFiles = files;
  if (strategy === 'code') {
    filteredFiles = files.filter(f => /\.(ts|tsx|js|jsx|py|go|rs|java|kt|cs|php|rb)$/.test(f));
  } else if (strategy === 'docs') {
    filteredFiles = files.filter(f => /\.(md|txt|rst|adoc)$/.test(f));
  }
  
  if (filteredFiles.length === 0) {
    console.log('No matching files for strategy');
    return;
  }
  
  console.log(`Processing ${filteredFiles.length} file(s)...`);
  
  // Use gbrain CLI to sync
  try {
    const args = ['sync', '--strategy', strategy];
    if (full) args.push('--full');
    
    execSync(`gbrain ${args.join(' ')}`, { 
      cwd: PROJECT_ROOT, 
      stdio: 'inherit',
      env: { ...process.env, GBRAIN_FILES: filteredFiles.join(',') }
    });
    
    updateLastSync();
    console.log('\n✓ Sync complete');
  } catch (error) {
    console.error('\n✗ Sync failed:', error.message);
    process.exit(1);
  }
}