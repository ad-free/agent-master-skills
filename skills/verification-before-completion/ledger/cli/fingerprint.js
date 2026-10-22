#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { createHash } from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = process.cwd();
const EVIDENCE_DIR = join(PROJECT_ROOT, '.dev-craft', 'evidence');
const FINGERPRINTS_DIR = join(EVIDENCE_DIR, 'fingerprints');

function computeFingerprint() {
  try {
    const tracked = execSync('git ls-files', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    const untracked = execSync('git ls-files --others --exclude-standard', { cwd: PROJECT_ROOT, encoding: 'utf-8' })
      .trim().split('\n').filter(Boolean);
    const sourceExts = ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.kt', '.cs', '.php', '.rb', '.json', '.yaml', '.yml', '.toml', '.md', '.sql'];
    const allFiles = [...tracked, ...untracked]
      .filter(f => sourceExts.some(ext => f.endsWith(ext)))
      .sort();
    
    const hasher = createHash('sha256');
    const fileHashes = [];
    
    for (const file of allFiles) {
      const filePath = join(PROJECT_ROOT, file);
      if (existsSync(filePath)) {
        const content = readFileSync(filePath);
        const fileHash = createHash('sha256').update(content).digest('hex');
        fileHashes.push({ file, hash: fileHash, size: content.length });
        hasher.update(file + ':' + fileHash);
      }
    }
    
    const fingerprint = 'sha256:' + hasher.digest('hex');
    
    // Cache
    mkdirSync(FINGERPRINTS_DIR, { recursive: true });
    writeFileSync(join(FINGERPRINTS_DIR, `${fingerprint.replace('sha256:', '')}.json`), JSON.stringify({
      fingerprint,
      timestamp: new Date().toISOString(),
      file_count: fileHashes.length,
      files: fileHashes,
    }, null, 2));
    
    return { fingerprint, fileHashes };
  } catch (error) {
    console.error('Error computing fingerprint:', error.message);
    try {
      const status = execSync('git status --porcelain', { cwd: PROJECT_ROOT, encoding: 'utf-8' });
      return { fingerprint: 'sha256:' + createHash('sha256').update(status).digest('hex'), fileHashes: [] };
    } catch {
      return { fingerprint: 'sha256:' + createHash('sha256').update(PROJECT_ROOT + Date.now()).digest('hex'), fileHashes: [] };
    }
  }
}

export async function fingerprint() {
  console.log('Computing working-tree fingerprint...');
  
  const { fingerprint, fileHashes } = computeFingerprint();
  
  console.log(`\nFingerprint: ${fingerprint}`);
  console.log(`Files: ${fileHashes.length}`);
  console.log(`Total size: ${fileHashes.reduce((sum, f) => sum + f.size, 0)} bytes`);
  
  // Show top 10 largest files
  const largest = fileHashes.sort((a, b) => b.size - a.size).slice(0, 10);
  if (largest.length > 0) {
    console.log('\nLargest files:');
    for (const f of largest) {
      console.log(`  ${f.file}: ${f.size} bytes`);
    }
  }
}