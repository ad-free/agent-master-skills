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

function loadLedger() {
  if (!existsSync(LEDGER_FILE)) return [];
  const content = readFileSync(LEDGER_FILE, 'utf-8');
  return content.trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

export async function verify() {
  const ledger = loadLedger();
  
  if (ledger.length === 0) {
    console.log('Ledger is empty - nothing to verify');
    process.exit(0);
  }
  
  console.log(`Verifying hash chain (${ledger.length} entries)...`);
  
  let prevHash = null;
  let tampered = false;
  
  for (let i = 0; i < ledger.length; i++) {
    const entry = ledger[i];
    const entryHash = createHash('sha256').update(JSON.stringify(entry)).digest('hex');
    
    // Check prev_hash link
    if (i === 0) {
      if (entry.prev_hash !== null) {
        console.log(`  ✗ Entry ${i} (${entry.id}): First entry should have null prev_hash`);
        tampered = true;
      }
    } else {
      if (entry.prev_hash !== prevHash) {
        console.log(`  ✗ Entry ${i} (${entry.id}): Chain broken - prev_hash mismatch`);
        console.log(`    Expected: ${prevHash}`);
        console.log(`    Got:      ${entry.prev_hash}`);
        tampered = true;
      }
    }
    
    // Check fingerprint format
    if (!entry.fingerprint || !entry.fingerprint.startsWith('sha256:')) {
      console.log(`  ⚠ Entry ${i} (${entry.id}): Invalid fingerprint format`);
    }
    
    // Check output_hash format
    if (!entry.output_hash || !entry.output_hash.startsWith('sha256:')) {
      console.log(`  ⚠ Entry ${i} (${entry.id}): Invalid output_hash format`);
    }
    
    prevHash = entryHash;
  }
  
  if (tampered) {
    console.log('\n✗ TAMPER DETECTED: Hash chain integrity compromised');
    process.exit(3);
  } else {
    console.log('\n✓ Hash chain verified - no tampering detected');
    console.log(`  Chain head: ${prevHash}`);
    process.exit(0);
  }
}