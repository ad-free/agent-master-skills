import { readFileSync, existsSync, readdirSync } from 'fs';
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

export async function listSkills(options) {
  const { target } = options;
  const targets = target === 'all' ? Object.keys(HARNESS_PATHS) : [target];
  
  for (const harness of targets) {
    const skillsDir = getSkillsDir(harness);
    
    console.log(`\n${harness.toUpperCase()} (${skillsDir}):`);
    
    if (!existsSync(skillsDir)) {
      console.log('  (not installed)');
      continue;
    }
    
    const entries = readdirSync(skillsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);
    
    if (entries.length === 0) {
      console.log('  (no skills installed)');
      continue;
    }
    
    for (const entry of entries) {
      const skillPath = join(skillsDir, entry, 'SKILL.md');
      if (existsSync(skillPath)) {
        try {
          const content = readFileSync(skillPath, 'utf-8');
          const fm = parseSkillFrontmatter(content);
          const version = fm?.version ? ` v${fm.version}` : '';
          const desc = fm?.description ? ` - ${fm.description.split('\n')[0]}` : '';
          console.log(`  ✓ ${entry}${version}${desc}`);
        } catch {
          console.log(`  ✓ ${entry} (invalid SKILL.md)`);
        }
      } else {
        console.log(`  ? ${entry} (no SKILL.md)`);
      }
    }
  }
}