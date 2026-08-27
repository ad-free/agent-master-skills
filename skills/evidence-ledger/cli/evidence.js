#!/usr/bin/env node
import { program } from 'commander';
import { run } from './run.js';
import { check } from './check.js';
import { verify } from './verify.js';
import { list } from './list.js';
import { fingerprint } from './fingerprint.js';

program
  .name('evidence')
  .description('Tamper-evident verification evidence ledger')
  .version('1.0.0');

program
  .command('run')
  .description('Run a verification command and record evidence')
  .requiredOption('--label <label>', 'Evidence label (e.g., test-unit, lint, typecheck)')
  .option('--expect-cmd <cmd>', 'Expected command for grading')
  .option('--max-age <duration>', 'Max age for fresh evidence (e.g., 1h, 30m)', '1h')
  .option('--allow-paths <globs>', 'Comma-separated paths that can change without staleness')
  .argument('<command...>', 'Command to run')
  .action(async (command, options) => {
    await run(command.join(' '), options);
  });

program
  .command('check')
  .description('Check evidence freshness for a label')
  .requiredOption('--label <label>', 'Evidence label')
  .option('--expect-cmd <cmd>', 'Expected command')
  .option('--max-age <duration>', 'Max age for fresh evidence', '1h')
  .option('--allow-paths <globs>', 'Comma-separated allowed paths')
  .action(async (options) => {
    await check(options);
  });

program
  .command('verify')
  .description('Verify hash chain integrity')
  .action(async () => {
    await verify();
  });

program
  .command('list')
  .description('List evidence entries')
  .option('--label <label>', 'Filter by label')
  .option('--since <time>', 'Filter since timestamp')
  .option('--limit <n>', 'Max entries', '50')
  .action(async (options) => {
    await list(options);
  });

program
  .command('fingerprint')
  .description('Compute working-tree fingerprint')
  .action(async () => {
    await fingerprint();
  });

program.parse();