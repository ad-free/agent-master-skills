import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parse as parseYaml } from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const HARNESS_PATHS = {
  opencode: '~/.config/opencode/skills',
  claude: '~/.claude/skills',
  cursor: '~/.cursor/skills',
  codex: '~/.codex/skills',
};

function expandHome(path) {
  return path.replace('~', process.env.HOME || process.env.USERPROFILE || '');
}

function getSkillsDir(harness) {
  const base = HARNESS_PATHS[harness];
  if (!base) throw new Error(`Unknown harness: ${harness}`);
  return expandHome(base);
}

function parseSkillFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  return parseYaml(match[1]);
}

const REQUIRED_KEYS = ['name', 'description', 'version', 'preamble-tier', 'allowed-tools', 'triggers'];
const ALLOWED_TOOLS = ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 'Agent', 'AskUserQuestion', 'WebSearch', 'Task'];

export async function doctor(options) {
  const { target } = options;
  const targets = target === 'all' ? Object.keys(HARNESS_PATHS) : [target];
  
  let totalIssues = 0;
  
  for (const harness of targets) {
    const skillsDir = getSkillsDir(harness);
    
    console.log(`\n=== ${harness.toUpperCase()} ===`);
    console.log(`Path: ${skillsDir}`);
    
    if (!existsSync(skillsDir)) {
      console.log('  ✗ Skills directory does not exist');
      totalIssues++;
      continue;
    }
    
    console.log('  ✓ Skills directory exists');
    
    const entries = readdirSync(skillsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);
    
    if (entries.length === 0) {
      console.log('  ⚠ No skills installed');
      continue;
    }
    
    console.log(`  Found ${entries.length} skill(s):`);
    
    for (const entry of entries) {
      const skillPath = join(skillsDir, entry, 'SKILL.md');
      console.log(`\n  Checking ${entry}...`);
      
      if (!existsSync(skillPath)) {
        console.log(`    ✗ Missing SKILL.md`);
        totalIssues++;
        continue;
      }
      
      try {
        const content = readFileSync(skillPath, 'utf-8');
        const fm = parseSkillFrontmatter(content);
        
        if (!fm) {
          console.log(`    ✗ Invalid YAML frontmatter`);
          totalIssues++;
          continue;
        }
        
        // Check required keys
        for (const key of REQUIRED_KEYS) {
          if (!(key in fm)) {
            console.log(`    ✗ Missing required frontmatter key: ${key}`);
            totalIssues++;
          }
        }
        
        // Check allowed-tools
        if (fm['allowed-tools']) {
          for (const tool of fm['allowed-tools']) {
            if (!ALLOWED_TOOLS.includes(tool)) {
              console.log(`    ⚠ Unknown tool in allowed-tools: ${tool}`);
            }
          }
        }
        
        // Check triggers
        if (fm['triggers'] && (!Array.isArray(fm['triggers']) || fm['triggers'].length === 0)) {
          console.log(`    ⚠ Triggers should be non-empty array`);
        }
        
        console.log(`    ✓ Valid skill (${fm.version || 'no version'})`);
        
      } catch (error) {
        console.log(`    ✗ Failed to parse: ${error.message}`);
        totalIssues++;
      }
    }
  }
  
  console.log(`\n=== SUMMARY ===`);
  if (totalIssues === 0) {
    console.log('✓ All checks passed!');
  } else {
    console.log(`✗ ${totalIssues} issue(s) found`);
    process.exit(1);
  }
}

import { readdirSync } from 'fs';