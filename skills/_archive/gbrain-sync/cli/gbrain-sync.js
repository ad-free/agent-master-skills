#!/usr/bin/env node
import { program } from 'commander';
import { init } from './init.js';
import { sync } from './sync.js';
import { search } from './search.js';
import { status } from './status.js';
import { trust } from './trust.js';

program
  .name('gbrain-sync')
  .description('GBrain integration - persistent vector knowledge base for AI agents')
  .version('1.0.0');

program
  .command('init')
  .description('Initialize GBrain for current project')
  .option('--local', 'Use PGLite local backend (no account needed)')
  .option('--supabase-url <url>', 'Supabase project URL')
  .option('--supabase-token <token>', 'Supabase Personal Access Token')
  .option('--mcp-url <url>', 'Remote GBrain MCP server URL')
  .option('--mcp-token <token>', 'MCP server bearer token')
  .option('--trust <tier>', 'Trust tier: read-write, read-only, deny', 'read-write')
  .action(async (options) => {
    await init(options);
  });

program
  .command('sync')
  .description('Sync current repo to GBrain')
  .option('--full', 'Full reindex (not incremental)')
  .option('--dry-run', 'Preview what would be synced')
  .option('--strategy <strategy>', 'Sync strategy: code | docs | all', 'code')
  .action(async (options) => {
    await sync(options);
  });

program
  .command('search <query>')
  .description('Search GBrain for code/knowledge')
  .option('--type <type>', 'Result type: code | symbols | docs | all', 'all')
  .option('--limit <n>', 'Max results', '10')
  .option('--project <hash>', 'Limit to specific project')
  .action(async (query, options) => {
    await search(query, options);
  });

program
  .command('status')
  .description('Show GBrain sync status')
  .action(async () => {
    await status();
  });

program
  .command('trust <tier>')
  .description('Set trust tier for current repo')
  .argument('<tier>', 'Trust tier: read-write, read-only, deny')
  .action(async (tier) => {
    await trust(tier);
  });

program.parse();