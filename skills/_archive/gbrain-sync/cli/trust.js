#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

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

function saveConfig(config) {
  mkdirSync(GBRAIN_DIR, { recursive: true });
  const lines = [];
  for (const [key, value] of Object.entries(config)) {
    lines.push(`${key}: "${value}"`);
  }
  writeFileSync(CONFIG_FILE, lines.join('\n'));
}

export async function trust(tier) {
  const validTiers = ['read-write', 'read-only', 'deny'];
  
  if (!validTiers.includes(tier)) {
    console.error(`Invalid trust tier. Must be one of: ${validTiers.join(', ')}`);
    process.exit(1);
  }
  
  const config = loadConfig();
  if (!config) {
    console.error('GBrain not configured. Run "gbrain-sync init" first.');
    process.exit(1);
  }
  
  config.trust_tier = tier;
  saveConfig(config);
  
  console.log(`✓ Trust tier set to: ${tier}`);
  console.log('This applies to the current repository.');
  
  // If using MCP backend, this would be sent to the server
  if (config.backend === 'mcp') {
    console.log('Note: For remote MCP, trust tier is enforced server-side.');
  }
}