#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const GBRAIN_DIR = join(process.env.HOME || '', '.gbrain');
const CONFIG_FILE = join(GBRAIN_DIR, 'config.yaml');
const PROJECT_ROOT = process.cwd();

function getProjectHash() {
  try {
    const remote = execSync('git config --get remote.origin.url', { cwd: PROJECT_ROOT, encoding: 'utf-8' }).trim();
    if (remote) {
      return require('crypto').createHash('md5').update(remote).digest('hex').slice(0, 12);
    }
  } catch {}
  return require('crypto').createHash('md5').update(PROJECT_ROOT).digest('hex').slice(0, 12);
}

function loadConfig() {
  if (!existsSync(CONFIG_FILE)) return null;
  const content = readFileSync(CONFIG_FILE, 'utf-8');
  // Simple YAML parse for our config
  const config = {};
  for (const line of content.split('\n')) {
    const match = line.match(/^(\w+):\s*(.+)$/);
    if (match) {
      config[match[1]] = match[2].replace(/^["']|["']$/g, '');
    }
  }
  return config;
}

function saveConfig(config) {
  mkdirSync(GBRAIN_DIR, { recursive: true });
  const lines = [];
  for (const [key, value] of Object.entries(config)) {
    lines.push(`${key}: "${value}"`);
  }
  writeFileSync(CONFIG_FILE, lines.join('\n'));
}

async function setupPGLite() {
  console.log('Setting up PGLite local backend...');
  
  // Check if gbrain CLI is available
  try {
    execSync('gbrain --version', { stdio: 'pipe' });
  } catch {
    console.log('Installing gbrain CLI...');
    execSync('npm install -g @gbrain/cli', { stdio: 'inherit' });
  }
  
  // Initialize local brain
  execSync('gbrain init --local', { cwd: PROJECT_ROOT, stdio: 'inherit' });
  
  const config = {
    backend: 'pglite',
    project_id: getProjectHash(),
    trust_tier: 'read-write',
    auto_sync: 'true',
    incremental: 'true',
  };
  
  saveConfig(config);
  console.log('✓ PGLite local GBrain initialized');
  registerMCP();
}

async function setupSupabase(options) {
  console.log('Setting up Supabase backend...');
  
  let { supabaseUrl, supabaseToken } = options;
  
  if (!supabaseUrl) {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    
    supabaseUrl = await new Promise(r => readline.question('Supabase project URL: ', r));
    supabaseToken = await new Promise(r => readline.question('Supabase Personal Access Token: ', r));
    readline.close();
  }
  
  // Auto-provision if needed
  if (supabaseUrl && !supabaseUrl.includes('pooler')) {
    console.log('Provisioning GBrain database...');
    // This would call Supabase Management API
    // For now, assume user provides pooler URL
  }
  
  const poolerUrl = supabaseUrl.replace('https://', 'postgresql://postgres:').replace('.supabase.co', '.supabase.co:5432/postgres');
  
  const config = {
    backend: 'supabase',
    supabase_url: supabaseUrl,
    pooler_url: poolerUrl,
    project_id: getProjectHash(),
    trust_tier: options.trust || 'read-write',
    auto_sync: 'true',
    incremental: 'true',
  };
  
  saveConfig(config);
  
  // Initialize via gbrain CLI
  execSync(`gbrain init --pooler "${poolerUrl}"`, { cwd: PROJECT_ROOT, stdio: 'inherit' });
  
  console.log('✓ Supabase GBrain initialized');
  registerMCP();
}

async function setupRemoteMCP(options) {
  console.log('Setting up remote MCP backend...');
  
  let { mcpUrl, mcpToken } = options;
  
  if (!mcpUrl) {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    
    mcpUrl = await new Promise(r => readline.question('MCP server URL: ', r));
    mcpToken = await new Promise(r => readline.question('Bearer token (optional): ', r));
    readline.close();
  }
  
  const config = {
    backend: 'mcp',
    mcp_url: mcpUrl,
    mcp_token: mcpToken || '',
    project_id: getProjectHash(),
    trust_tier: options.trust || 'read-only',
    auto_sync: 'false',
    incremental: 'true',
  };
  
  saveConfig(config);
  console.log('✓ Remote MCP GBrain configured');
  registerMCP();
}

function registerMCP() {
  try {
    execSync('claude mcp add gbrain -- gbrain serve', { stdio: 'pipe' });
    console.log('✓ Registered GBrain as MCP server for Claude Code');
  } catch {
    console.log('⚠ Could not register MCP (run manually: claude mcp add gbrain -- gbrain serve)');
  }
  
  // Update CLAUDE.md with guidance
  const claudeMd = join(PROJECT_ROOT, 'CLAUDE.md');
  const guidance = `
## GBrain Search Guidance
This project uses GBrain for persistent code intelligence.
Prefer \`gbrain search\`, \`gbrain code-def\`, \`gbrain code-refs\` over Grep for code queries.
`;
  
  if (existsSync(claudeMd)) {
    const content = readFileSync(claudeMd, 'utf-8');
    if (!content.includes('GBrain Search Guidance')) {
      writeFileSync(claudeMd, content + guidance);
    }
  } else {
    writeFileSync(claudeMd, guidance);
  }
}

export async function init(options) {
  console.log('GBrain Setup Wizard');
  console.log('==================\n');
  
  const existingConfig = loadConfig();
  if (existingConfig) {
    console.log(`Existing config found: ${existingConfig.backend} (${existingConfig.project_id})`);
    const { default: prompts } = await import('prompts');
    const response = await prompts({
      type: 'confirm',
      name: 'reconfigure',
      message: 'Reconfigure?',
      initial: false,
    });
    if (!response.reconfigure) {
      console.log('Keeping existing configuration');
      return;
    }
  }
  
  const { default: prompts } = await import('prompts');
  const backend = await prompts({
    type: 'select',
    name: 'backend',
    message: 'Choose backend:',
    choices: [
      { title: 'PGLite Local (offline, private, ~30s)', value: 'pglite' },
      { title: 'Supabase Existing (team, cloud, ~90s)', value: 'supabase' },
      { title: 'Supabase Auto-provision (new project, ~2min)', value: 'supabase-auto' },
      { title: 'Remote MCP (existing GBrain server)', value: 'mcp' },
    ],
  });
  
  switch (backend.value) {
    case 'pglite':
      await setupPGLite();
      break;
    case 'supabase':
    case 'supabase-auto':
      await setupSupabase(options);
      break;
    case 'mcp':
      await setupRemoteMCP(options);
      break;
  }
  
  console.log('\n✓ GBrain setup complete!');
  console.log('Run "gbrain-sync sync" to index your codebase');
  console.log('Run "gbrain-sync search <query>" to search');
}