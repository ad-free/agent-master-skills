import { existsSync, readFileSync, rmSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parse as parseYaml } from 'yaml';
import { installSkill } from './install.js';

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

function getInstalledSkillSource(skillsDir, skillName) {
  const skillPath = join(skillsDir, skillName, 'SKILL.md');
  if (!existsSync(skillPath)) return null;
  
  try {
    const content = readFileSync(skillPath, 'utf-8');
    const fm = parseSkillFrontmatter(content);
    return fm?.origin || fm?.repository || null;
  } catch {
    return null;
  }
}

export async function updateSkills(options) {
  const { target, dryRun } = options;
  const targets = target === 'all' ? Object.keys(HARNESS_PATHS) : [target];
  
  console.log('Checking for skill updates...\n');
  
  for (const harness of targets) {
    const skillsDir = getSkillsDir(harness);
    
    if (!existsSync(skillsDir)) {
      console.log(`${harness}: not installed`);
      continue;
    }
    
    const entries = readdirSync(skillsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);
    
    for (const entry of entries) {
      const source = getInstalledSkillSource(skillsDir, entry);
      if (!source) {
        console.log(`  ${entry}: no source info, skipping`);
        continue;
      }
      
      console.log(`  Updating ${entry} from ${source}...`);
      
      if (dryRun) {
        console.log(`    [dry-run] Would update ${entry}`);
        continue;
      }
      
      try {
        const tempDir = join('/tmp', '.agent-skills-update-' + Date.now());
        
        // Clone fresh copy
        const { execSync } = await import('child_process');
        execSync(`git clone --depth 1 "${source}" "${tempDir}"`, { stdio: 'pipe' });
        
        // Find the skill in the fresh repo
        const { globSync } = await import('glob');
        const skillFiles = globSync('**/SKILL.md', { cwd: tempDir, absolute: true });
        let found = false;
        
        for (const file of skillFiles) {
          const content = readFileSync(file, 'utf-8');
          const fm = parseSkillFrontmatter(content);
          if (fm?.name === entry) {
            // Update it
            const targetSkillDir = join(skillsDir, entry);
            rmSync(targetSkillDir, { recursive: true });
            const { cpSync } = await import('fs');
            cpSync(dirname(file), targetSkillDir, { recursive: true });
            console.log(`    ✓ Updated ${entry}`);
            found = true;
            break;
          }
        }
        
        if (!found) {
          console.log(`    ⚠ Skill ${entry} not found in source repo`);
        }
        
        rmSync(tempDir, { recursive: true, force: true });
        
      } catch (error) {
        console.log(`    ✗ Failed to update ${entry}: ${error.message}`);
      }
    }
  }
  
  console.log('\n✓ Update check complete');
}