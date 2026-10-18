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

export async function search(query, options) {
  const { type, limit, project } = options;
  
  const config = loadConfig();
  if (!config) {
    console.error('GBrain not configured. Run "gbrain-sync init" first.');
    process.exit(1);
  }
  
  console.log(`Searching GBrain (${config.backend})...`);
  
  try {
    const args = ['search', query, '--limit', limit];
    if (type !== 'all') args.push('--type', type);
    if (project) args.push('--project', project);
    
    const output = execSync(`gbrain ${args.join(' ')}`, { 
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    });
    
    console.log(output);
  } catch (error) {
    if (error.stdout) console.log(error.stdout.toString());
    if (error.stderr) console.error(error.stderr.toString());
    console.error('\nSearch failed:', error.message);
  }
}