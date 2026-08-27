/**
 * Verify Gate Hook
 * 
 * Captures verification evidence when the agent tries to declare work complete.
 * Runs on PostToolUse when the agent calls completion-related tools.
 * 
 * Enforces: No "done" without fresh evidence of lint, typecheck, tests, and build passing.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const EVIDENCE_DIR = path.join(process.cwd(), '.dev-craft', 'evidence');

function ensureEvidenceDir() {
  if (!fs.existsSync(EVIDENCE_DIR)) {
    fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
  }
}

function captureEvidence(name, command) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `${name}-${timestamp}.txt`;
  const filepath = path.join(EVIDENCE_DIR, filename);

  try {
    const output = execSync(command, { 
      encoding: 'utf-8',
      timeout: 30000,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    const evidence = `[${new Date().toISOString()}] ${command}\n\nExit: 0\n\n${output}`;
    fs.writeFileSync(filepath, evidence);
    
    return { success: true, output, file: filepath };
  } catch (error) {
    const evidence = `[${new Date().toISOString()}] ${command}\n\nExit: ${error.status}\n\nstdout:\n${error.stdout || ''}\n\nstderr:\n${error.stderr || ''}`;
    fs.writeFileSync(filepath, evidence);
    
    return { success: false, output: error.stdout || error.stderr || error.message, file: filepath };
  }
}

function hook(context) {
  // Only run on PostToolUse
  if (context.tool !== 'task_complete' && context.tool !== 'claim_done') {
    return;
  }

  ensureEvidenceDir();

  console.log('[verify-gate] Running verification checks...');

  // Detect project type and run appropriate checks
  const checks = [];
  
  // Check for package.json (Node.js)
  if (fs.existsSync(path.join(process.cwd(), 'package.json'))) {
    const pkg = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'package.json'), 'utf-8'));
    
    if (pkg.scripts?.lint) {
      checks.push({ name: 'lint', command: 'npm run lint' });
    }
    if (pkg.scripts?.typecheck) {
      checks.push({ name: 'typecheck', command: 'npm run typecheck' });
    }
    if (pkg.scripts?.test) {
      checks.push({ name: 'test', command: 'npm test' });
    }
    if (pkg.scripts?.build) {
      checks.push({ name: 'build', command: 'npm run build' });
    }
  }
  
  // Check for pyproject.toml (Python)
  if (fs.existsSync(path.join(process.cwd(), 'pyproject.toml'))) {
    checks.push({ name: 'lint', command: 'uv run ruff check .' });
    checks.push({ name: 'typecheck', command: 'uv run mypy .' });
    checks.push({ name: 'test', command: 'uv run pytest' });
  }
  
  // Check for go.mod (Go)
  if (fs.existsSync(path.join(process.cwd(), 'go.mod'))) {
    checks.push({ name: 'lint', command: 'golangci-lint run' });
    checks.push({ name: 'test', command: 'go test ./...' });
    checks.push({ name: 'build', command: 'go build ./...' });
  }
  
  // Check for Cargo.toml (Rust)
  if (fs.existsSync(path.join(process.cwd(), 'Cargo.toml'))) {
    checks.push({ name: 'lint', command: 'cargo clippy' });
    checks.push({ name: 'test', command: 'cargo test' });
    checks.push({ name: 'build', command: 'cargo build --release' });
  }

  // Run all checks
  const results = [];
  for (const check of checks) {
    console.log(`[verify-gate] Running ${check.name}...`);
    const result = captureEvidence(check.name, check.command);
    results.push({ ...check, ...result });
  }

  // Generate summary
  const passed = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;

  console.log('\n[verify-gate] Verification Summary:');
  console.log(`  Passed: ${passed}`);
  console.log(`  Failed: ${failed}`);

  if (failed > 0) {
    console.log('\n[verify-gate] ❌ VERIFICATION FAILED');
    console.log('Fix failing checks before declaring done.');
    
    // List failed checks
    results.filter(r => !r.success).forEach(r => {
      console.log(`  - ${r.name}: ${r.output.split('\n')[0]}`);
    });
    
    // Block completion
    return {
      block: true,
      message: `Verification failed: ${failed} check(s) did not pass. Fix before declaring done.`
    };
  } else {
    console.log('\n[verify-gate] ✅ ALL CHECKS PASSED');
    return {
      block: false,
      message: 'All verification checks passed.'
    };
  }
}

module.exports = { hook };
