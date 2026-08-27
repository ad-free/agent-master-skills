#!/usr/bin/env node
import { program } from 'commander';
import { installSkill } from '../lib/install.js';
import { listSkills } from '../lib/list.js';
import { updateSkills } from '../lib/update.js';
import { doctor } from '../lib/doctor.js';
import { initProject } from '../lib/init.js';

program
  .name('agent-skills')
  .description('Install and manage agent skills across harnesses (OpenCode, Claude Code, Cursor, Codex)')
  .version('1.0.0');

program
  .command('add <source>')
  .description('Install a skill from a GitHub repo or local path')
  .option('--skill <name>', 'Install a specific skill by name (from SKILL.md frontmatter)')
  .option('--target <harness>', 'Target harness: opencode, claude, cursor, codex, all', 'all')
  .option('--force', 'Overwrite existing skill')
  .option('--dry-run', 'Show what would be installed without making changes')
  .action(async (source, options) => {
    await installSkill(source, options);
  });

program
  .command('list')
  .description('List installed skills')
  .option('--target <harness>', 'Target harness: opencode, claude, cursor, codex, all', 'all')
  .action(async (options) => {
    await listSkills(options);
  });

program
  .command('update')
  .description('Update all installed skills to latest versions')
  .option('--target <harness>', 'Target harness: opencode, claude, cursor, codex, all', 'all')
  .option('--dry-run', 'Show what would be updated')
  .action(async (options) => {
    await updateSkills(options);
  });

program
  .command('doctor')
  .description('Check installation health and diagnose issues')
  .option('--target <harness>', 'Target harness: opencode, claude, cursor, codex, all', 'all')
  .action(async (options) => {
    await doctor(options);
  });

program
  .command('init')
  .description('Initialize agent skills in current project')
  .option('--target <harness>', 'Target harness: opencode, claude, cursor, codex, all', 'all')
  .option('--template <name>', 'Project template: minimal, fullstack, frontend, backend', 'fullstack')
  .action(async (options) => {
    await initProject(options);
  });

program.parse();