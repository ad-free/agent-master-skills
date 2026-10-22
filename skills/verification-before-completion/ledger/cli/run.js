#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { createHash, randomBytes } from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const EVIDENCE_DIR = join(PROJECT_ROOT, '.dev-craft', 'evidence');
const LEDGER_FILE = join(EVIDENCE_DIR, 'ledger.jsonl');
const RUNS_DIR = join(EVIDENCE_DIR, 'runs');
const INDEX_FILE = join(EVIDENCE_DIR, 'index.json');
const FINGERPRINTS_DIR = join(EVIDENCE_DIR, 'fingerprints');

function getFingerprint() {
  // Compute working-tree fingerprint
  // Uses git ls-files + untracked source files, excludes gitignored
  try {
    // Get tracked files
    const tracked = execSync('git ls-files', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    
    // Get untracked source files (not gitignored)
    const untracked = execSync('git ls-files --others --exclude-standard', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    
    // Filter to source files only
    const sourceExts = ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.kt', '.cs', '.php', '.rb', '.json', '.yaml', '.yml', '.toml', '.md', '.sql'];
    const allFiles = [...tracked, ...untracked]
      .filter(f => sourceExts.some(ext => f.endsWith(ext)))
      .sort();
    
    // Hash content of each file
    const hasher = createHash('sha256');
    for (const file of allFiles) {
      const filePath = join(PROJECT_ROOT, file);
      if (existsSync(filePath)) {
        const content = readFileSync(filePath);
        const fileHash = createHash('sha256').update(content).digest('hex');
        hasher.update(file + ':' + fileHash);
      }
    }
    
    return 'sha256:' + hasher.digest('hex');
  } catch {
    // Fallback: hash of git status
    try {
      const status = execSync('git status --porcelain', { cwd: PROJECT_ROOT, encoding: 'utf-8' });
      return 'sha256:' + createHash('sha256').update(status).digest('hex');
    } catch {
      return 'sha256:' + createHash('sha256').update(PROJECT_ROOT + Date.now()).digest('hex');
    }
  }
}

function generateId() {
  return 'evt-' + randomBytes(4).toString('hex');
}

function parseMaxAge(maxAge) {
  const match = maxAge.match(/^(\d+)([hms])$/);
  if (!match) return 3600000; // 1 hour default
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

function saveIndex(index) {
  mkdirSync(EVIDENCE_DIR, { recursive: true });
  writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2));
}

function getLastHash() {
  const ledger = loadLedger();
  if (ledger.length === 0) return null;
  const last = ledger[ledger.length - 1];
  return createHash('sha256').update(JSON.stringify(last)).digest('hex');
}

export async function run(command, options) {
  const { label, expectCmd, maxAge, allowPaths } = options;
  
  console.log(`[evidence] Running: ${command}`);
  console.log(`[evidence] Label: ${label}`);
  
  const fingerprint = getFingerprint();
  const startTime = Date.now();
  
  let exitCode = 0;
  let output = '';
  let passed = false;
  let summary = '';
  
  try {
    output = execSync(command, { 
      cwd: PROJECT_ROOT, 
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 300000 // 5 min timeout
    });
    exitCode = 0;
    passed = true;
  } catch (error) {
    exitCode = error.status || 1;
    output = error.stdout?.toString() || error.stderr?.toString() || error.message;
    passed = false;
  }
  
  const durationMs = Date.now() - startTime;
  
  // Extract summary from output
  const lines = output.trim().split('\n');
  summary = lines.slice(-3).join(' | ').slice(0, 200);
  
  // Output hash
  const outputHash = 'sha256:' + createHash('sha256').update(output).digest('hex');
  
  // Previous entry hash
  const prevHash = getLastHash();
  
  // Create evidence entry
  const entry = {
    id: generateId(),
    label,
    timestamp: new Date().toISOString(),
    command: expectCmd || command,
    exit_code: exitCode,
    duration_ms: durationMs,
    fingerprint,
    output_hash: outputHash,
    passed,
    summary,
    prev_hash: prevHash,
    max_age_ms: parseMaxAge(maxAge),
    allow_paths: allowPaths ? allowPaths.split(',').map(p => p.trim()) : [],
  };
  
  // Save to ledger
  mkdirSync(EVIDENCE_DIR, { recursive: true });
  appendFileSync(LEDGER_FILE, JSON.stringify(entry) + '\n');
  
  // Save detailed run log (capped at 2MB)
  mkdirSync(RUNS_DIR, { recursive: true });
  const runFile = join(RUNS_DIR, `${entry.id}.log`);
  const truncatedOutput = output.length > 2000000 ? output.slice(0, 2000000) + '\n... [truncated]' : output;
  writeFileSync(runFile, truncatedOutput, { mode: 0o600 });
  
  // Update index
  const index = loadIndex();
  index[label] = entry.id;
  saveIndex(index);
  
  // Cache fingerprint
  mkdirSync(FINGERPRINTS_DIR, { recursive: true });
  writeFileSync(join(FINGERPRINTS_DIR, `${fingerprint.replace('sha256:', '')}.json`), JSON.stringify({
    fingerprint,
    timestamp: entry.timestamp,
    label,
  }, null, 2));
  
  console.log(`[evidence] ${passed ? '✓ PASSED' : '✗ FAILED'} (${durationMs}ms)`);
  console.log(`[evidence] Summary: ${summary}`);
  console.log(`[evidence] Fingerprint: ${fingerprint.slice(0, 16)}...`);
  console.log(`[evidence] Entry: ${entry.id}`);
  
  if (!passed) {
    process.exit(exitCode);
  }
}