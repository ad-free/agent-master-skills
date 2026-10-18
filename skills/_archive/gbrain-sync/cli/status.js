#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const GBRAIN_DIR = join(process.env.HOME || '', '.gbrain');
const CONFIG_FILE = join(GBRAIN_DIR, 'config.yaml');

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

export async function status() {
  const config = loadConfig();
  
  console.log('GBrain Status');
  console.log('=============\n');
  
  if (!config) {
    console.log('Not configured. Run "gbrain-sync init" to set up.');
    return;
  }
  
  console.log(`Backend: ${config.backend}`);
  console.log(`Project: ${config.project_id}`);
  console.log(`Trust tier: ${config.trust_tier}`);
  console.log(`Auto-sync: ${config.auto_sync}`);
  console.log(`Incremental: ${config.incremental}`);
  
  if (config.backend === 'supabase') {
    console.log(`Supabase URL: ${config.supabase_url}`);
  } else if (config.backend === 'mcp') {
    console.log(`MCP URL: ${config.mcp_url}`);
  }
  
  // Last sync info
  const lastSyncFile = join(GBRAIN_DIR, '.last-sync');
  if (existsSync(lastSyncFile)) {
    const commit = readFileSync(lastSyncFile, 'utf-8').trim();
    console.log(`Last sync commit: ${commit.slice(0, 8)}`);
  }
  
  // Try to get index stats from gbrain CLI
  try {
    const output = execSync('gbrain status', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'] });
    console.log('\nIndex stats:');
    console.log(output);
  } catch {
    console.log('\n(gbrain CLI not available for detailed stats)');
  }
  
  // Check MCP registration
  try {
    execSync('claude mcp list', { stdio: 'pipe' });
    console.log('\nMCP: Registered');
  } catch {
    console.log('\nMCP: Not registered (run: claude mcp add gbrain -- gbrain serve)');
  }
}