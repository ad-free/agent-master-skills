import { execSync } from 'child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync, cpSync } from 'fs';
import { join, dirname, basename, resolve } from 'path';
import { fileURLToPath } from 'url';
import { parse as parseYaml } from 'yaml';
import { globSync } from 'glob';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = resolve(__dirname, '..', '..');

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

function findSkillsInRepo(repoPath) {
  const skillFiles = globSync('**/SKILL.md', { cwd: repoPath, absolute: true });
  const skills = [];
  
  for (const file of skillFiles) {
    try {
      const content = readFileSync(file, 'utf-8');
      const frontmatter = parseSkillFrontmatter(content);
      if (frontmatter?.name) {
        skills.push({
          name: frontmatter.name,
          description: frontmatter.description,
          version: frontmatter.version,
          path: file,
          relPath: file.replace(repoPath + '/', ''),
        });
      }
    } catch (e) {
      console.warn(`Warning: Failed to parse ${file}: ${e.message}`);
    }
  }
  
  return skills;
}

async function cloneRepo(source, targetDir) {
  const isUrl = source.startsWith('http') || source.startsWith('git@');
  
  if (isUrl) {
    execSync(`git clone --depth 1 "${source}" "${targetDir}"`, { stdio: 'pipe' });
  } else {
    cpSync(source, targetDir, { recursive: true });
  }
}

export async function installSkill(source, options) {
  const { skill: skillName, target, force, dryRun } = options;
  const targets = target === 'all' ? Object.keys(HARNESS_PATHS) : [target];
  
  const tempDir = join('/tmp', '.agent-skills-temp-' + Date.now());
  
  try {
    console.log(`Cloning ${source}...`);
    if (!dryRun) {
      await cloneRepo(source, tempDir);
      console.log(`Cloned to ${tempDir}, checking contents...`);
      const { readdirSync } = await import('fs');
      console.log(`Temp dir contents:`, readdirSync(tempDir));
    } else {
      // For dry-run, we still need to clone to analyze
      await cloneRepo(source, tempDir);
      console.log(`Cloned to ${tempDir} for analysis`);
    }
    
    const skills = findSkillsInRepo(tempDir);
    console.log(`Found ${skills.length} skills in repo`);
    
    if (skills.length === 0) {
      throw new Error('No skills found in repository (no SKILL.md files with name frontmatter)');
    }
    
    console.log(`Found ${skills.length} skill(s):`);
    skills.forEach(s => console.log(`  - ${s.name} (${s.version || 'no version'})`));
    
    let skillsToInstall = skills;
    if (skillName) {
      skillsToInstall = skills.filter(s => s.name === skillName);
      if (skillsToInstall.length === 0) {
        throw new Error(`Skill "${skillName}" not found. Available: ${skills.map(s => s.name).join(', ')}`);
      }
    }
    
    for (const harness of targets) {
      const skillsDir = getSkillsDir(harness);
      console.log(`\nInstalling to ${harness} (${skillsDir})...`);
      
      if (!dryRun) {
        mkdirSync(skillsDir, { recursive: true });
      }
      
      for (const skill of skillsToInstall) {
        const targetSkillDir = join(skillsDir, skill.name);
        
        if (existsSync(targetSkillDir) && !force) {
          console.log(`  ⚠ ${skill.name} already exists, use --force to overwrite`);
          continue;
        }
        
        if (dryRun) {
          console.log(`  [dry-run] Would install ${skill.name} to ${targetSkillDir}`);
          continue;
        }
        
        if (existsSync(targetSkillDir)) {
          rmSync(targetSkillDir, { recursive: true });
        }
        
        mkdirSync(targetSkillDir, { recursive: true });
        
        const skillSrcDir = dirname(skill.path);
        cpSync(skillSrcDir, targetSkillDir, { recursive: true });
        
        console.log(`  ✓ Installed ${skill.name}`);
      }
    }
    
    if (!dryRun) {
      console.log('\n✓ Installation complete!');
      console.log('Run "agent-skills doctor" to verify installation.');
    }
    
  } catch (error) {
    console.error(`\n✗ Installation failed: ${error.message}`);
    process.exit(1);
  } finally {
    if (existsSync(tempDir)) {
      rmSync(tempDir, { recursive: true, force: true });
    }
  }
}