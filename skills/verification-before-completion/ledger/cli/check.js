#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { createHash } from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const EVIDENCE_DIR = join(PROJECT_ROOT, '.dev-craft', 'evidence');
const LEDGER_FILE = join(EVIDENCE_DIR, 'ledger.jsonl');
const INDEX_FILE = join(EVIDENCE_DIR, 'index.json');

function getFingerprint() {
  try {
    const { execSync } = require('child_process');
    const tracked = execSync('git ls-files', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    const untracked = execSync('git ls-files --others --exclude-standard', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    const sourceExts = ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.kt', '.cs', '.php', '.rb', '.json', '.yaml', '.yml', '.toml', '.md', '.sql'];
    const allFiles = [...tracked, ...untracked]
      .filter(f => sourceExts.some(ext => f.endsWith(ext)))
      .sort();
    const hasher = createHash('sha256');
    for (const file of allFiles) {
      const filePath = join(PROJECT_ROOT, file);
      const { existsSync } = require('fs');
      if (existsSync(filePath)) {
        const content = readFileSync(filePath);
        const fileHash = createHash('sha256').update(content).digest('hex');
        hasher.update(file + ':' + fileHash);
      }
    }
    return 'sha256:' + hasher.digest('hex');
  } catch {
    try {
      const { execSync } = require('child_process');
      const status = execSync('git status --porcelain', { cwd: PROJECT_ROOT, encoding: 'utf-8' });
      return 'sha256:' + createHash('sha256').update(status).digest('hex');
    } catch {
      return 'sha256:' + createHash('sha256').update(PROJECT_ROOT + Date.now()).digest('hex');
    }
  }
}

function parseMaxAge(maxAge) {
  const match = maxAge.match(/^(\d+)([hms])$/);
  if (!match) return 3600000;
  const value = parseInt(match[1]);
  const unit = match[2];
  if (unit === 'h') return value * 3600000;
  if (unit === 'm') return value * 60000;
  if (unit === 's') return value * 1000;
  return 3600000;
}

function loadLedger() {
  if (!existsSync(LEDGER_FILE)) return [];
  const content = readFileSync(LEDGER_FILE, 'utf-8');
  return content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

function loadIndex() {
  if (!existsSync(INDEX_FILE)) return {};
  return JSON.parse(readFileSync(INDEX_FILE, 'utf-8'));
}

function fingerprintMatches(entry, currentFingerprint, allowPaths = []) {
  if (entry.fingerprint === currentFingerprint) return true;
  
  // If fingerprints differ, check if only allowed paths changed
  if (allowPaths.length === 0) return false;
  
  try {
    const { execSync } = require('child_process');
    const diff = execSync('git diff --name-only', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    
    const changedFiles = new Set(diff);
    const allowedSet = new Set(allowPaths);
    
    for (const file of changedFiles) {
      let allowed = false;
      for (const pattern of allowedSet) {
        if (minimatch(file, pattern)) {
          allowed = true;
          break;
        }
      }
      if (!allowed) return false;
    }
    return true;
  } catch {
    return false;
  }
}

function minimatch(str, pattern) {
  const regex = new RegExp('^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$');
  return regex.test(str);
}

export async function check(options) {
  const { label, expectCmd, maxAge, allowPaths } = options;
  
  const index = loadIndex();
  const entryId = index[label];
  
  if (!entryId) {
    console.log(`MISSING: No evidence for label "${label}"`);
    process.exit(1);
  }
  
  const ledger = loadLedger();
  const entry = ledger.find(e => e.id === entryId);
  
  if (!entry) {
    console.log(`MISSING: Index points to non-existent entry ${entryId}`);
    process.exit(1);
  }
  
  const currentFingerprint = getFingerprint();
  const maxAgeMs = parseMaxAge(maxAge);
  const ageMs = Date.now() - new Date(entry.timestamp).getTime();
  
  // Check command match
  const cmdMatch = !expectCmd || entry.command === expectCmd;
  
  // Check age
  const ageOk = ageMs <= maxAgeMs;
  
  // Check fingerprint
  const fpMatch = fingerprintMatches(entry, currentFingerprint, allowPaths ? allowPaths.split(',').map(p => p.trim()) : entry.allow_paths || []);
  
  console.log(`\nEvidence Check: ${label}`);
  console.log('========================');
  console.log(`Entry: ${entry.id}`);
  console.log(`Timestamp: ${entry.timestamp} (${Math.floor(ageMs / 1000)}s ago)`);
  console.log(`Command: ${entry.command}`);
  console.log(`Expected: ${expectCmd || '(none)'} ${cmdMatch ? '✓' : '✗'}`);
  console.log(`Max age: ${maxAge} (${maxAgeMs}ms) ${ageOk ? '✓' : '✗'}`);
  console.log(`Fingerprint: ${entry.fingerprint.slice(0, 16)}... vs ${currentFingerprint.slice(0, 16)}... ${fpMatch ? '✓' : '✗'}`);
  console.log(`Passed: ${entry.passed ? '✓' : '✗'}`);
  
  let grade = 'FRESH';
  if (!cmdMatch) grade = 'STALE';
  else if (!ageOk) grade = 'STALE';
  else if (!fpMatch) grade = 'STALE';
  else if (!entry.passed) grade = 'STALE';
  
  console.log(`\nGrade: ${grade}`);
  
  if (grade === 'FRESH') {
    console.log('✓ Evidence is FRESH');
    process.exit(0);
  } else {
    console.log('✗ Evidence is STALE or INVALID');
    process.exit(1);
  }
}