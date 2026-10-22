#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const EVIDENCE_DIR = join(PROJECT_ROOT, '.dev-craft', 'evidence');
const LEDGER_FILE = join(EVIDENCE_DIR, 'ledger.jsonl');

function loadLedger() {
  if (!existsSync(LEDGER_FILE)) return [];
  const content = readFileSync(LEDGER_FILE, 'utf-8');
  return content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

export async function list(options) {
  const { label, since, limit } = options;
  
  const ledger = loadLedger();
  
  if (ledger.length === 0) {
    console.log('No evidence entries');
    return;
  }
  
  let filtered = ledger;
  
  if (label) {
    filtered = filtered.filter(e => e.label === label);
  }
  
  if (since) {
    const sinceTime = new Date(since).getTime();
    filtered = filtered.filter(e => new Date(e.timestamp).getTime() >= sinceTime);
  }
  
  // Sort by timestamp descending
  filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  
  // Limit
  filtered = filtered.slice(0, parseInt(limit) || 50);
  
  console.log(`\nEvidence Entries (${filtered.length}/${ledger.length})`);
  console.log('==========================================');
  
  for (const entry of filtered) {
    const age = Math.floor((Date.now() - new Date(entry.timestamp).getTime()) / 1000);
    const status = entry.passed ? '✓' : '✗';
    console.log(`\n${status} ${entry.id} [${entry.label}]`);
    console.log(`  Time: ${entry.timestamp} (${age}s ago)`);
    console.log(`  Command: ${entry.command}`);
    console.log(`  Duration: ${entry.duration_ms}ms`);
    console.log(`  Fingerprint: ${entry.fingerprint.slice(0, 16)}...`);
    console.log(`  Summary: ${entry.summary}`);
  }
}