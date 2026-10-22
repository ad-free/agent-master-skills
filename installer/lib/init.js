import { existsSync, mkdirSync, writeFileSync, cpSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = resolve(__dirname, '..', '..');

const TEMPLATES = {
  minimal: {
    skills: ['dev-craft', 'verification-before-completion'],
    agents: ['verifier'],
  },
  fullstack: {
    skills: ['dev-craft', 'ui-craft', 'verification-before-completion', 'debugging-and-error-recovery', 'code-review-and-quality'],
    agents: ['verifier', 'debugger', 'code-reviewer', 'test-engineer'],
  },
  frontend: {
    skills: ['ui-craft', 'dev-craft', 'verification-before-completion', 'accessibility', 'fe-visual-loop'],
    agents: ['verifier', 'code-reviewer'],
  },
  backend: {
    skills: ['dev-craft', 'verification-before-completion', 'api-design', 'debugging-and-error-recovery'],
    agents: ['verifier', 'debugger', 'security-auditor'],
  },
};

const HARNESS_CONFIGS = {
  claude: {
    configDir: '.claude',
    agentsDir: '.claude/agents',
    skillsDir: '.claude/skills',
  },
  cursor: {
    configDir: '.cursor',
    agentsDir: '.cursor/agents',
    skillsDir: '.cursor/skills',
  },
  codex: {
    configDir: '.codex',
    agentsDir: '.codex/agents',
    skillsDir: '.codex/skills',
  },
};

export async function initProject(options) {
  const { target, template } = options;
  const targets = target === 'all' ? Object.keys(HARNESS_CONFIGS) : [target];
  const tmpl = TEMPLATES[template] || TEMPLATES.fullstack;
  
  console.log(`Initializing ${template} project for: ${targets.join(', ')}\n`);
  
  for (const harness of targets) {
    const config = HARNESS_CONFIGS[harness];
    const projectRoot = process.cwd();
    
    // Create config directory
    const configPath = join(projectRoot, config.configDir);
    const agentsPath = join(projectRoot, config.agentsDir);
    const skillsPath = join(projectRoot, config.skillsDir);
    
    mkdirSync(configPath, { recursive: true });
    mkdirSync(agentsPath, { recursive: true });
    mkdirSync(skillsPath, { recursive: true });
    
    console.log(`  ${harness}: Created ${config.configDir}/`);
    
    // Copy agents
    for (const agent of tmpl.agents) {
      const src = join(REPO_ROOT, 'agents', `${agent}.md`);
      const dest = join(agentsPath, `${agent}.md`);
      if (existsSync(src)) {
        cpSync(src, dest);
        console.log(`    ✓ Agent: ${agent}`);
      } else {
        console.log(`    ⚠ Agent not found: ${agent}`);
      }
    }
    
    // Copy skills (symlink or copy)
    for (const skill of tmpl.skills) {
      const src = join(REPO_ROOT, 'skills', skill);
      const dest = join(skillsPath, skill);
      if (existsSync(src)) {
        try {
          // Try symlink first (for updates)
          if (existsSync(dest)) {
            // Remove existing
            const { rmSync } = await import('fs');
            rmSync(dest, { recursive: true, force: true });
          }
          // Copy for now (symlinks can be problematic across platforms)
          cpSync(src, dest, { recursive: true });
          console.log(`    ✓ Skill: ${skill}`);
        } catch (e) {
          console.log(`    ✗ Failed to install skill ${skill}: ${e.message}`);
        }
      } else {
        console.log(`    ⚠ Skill not found: ${skill}`);
      }
    }
    
    // Create AGENTS.md if it doesn't exist
    const agentsMdPath = join(projectRoot, 'AGENTS.md');
    if (!existsSync(agentsMdPath)) {
      const agentsMd = `# AGENTS.md — Project Agent Instructions

Project-level agent instructions. Extend the user-level \`AGENTS.md\` if one exists.

---

## Skill Router — decide before acting

| Task | Entry skill | Add only when needed |
|---|---|---|
| Vague product idea | product-thinking | then dev-craft |
| Spec files (xlsx/csv/md/pdf) | project-discovery | then dev-craft |
| Feature, bug, refactor, migration, schema/API change | dev-craft | debugging-and-error-recovery (cause unknown), tdd-seam, api-design |
| Frontend / UI pipeline, redesign, motion | ui-craft | fe-visual-loop, image-to-design-spec, accessibility |
| Review code | code-review-and-quality | bug-hunting |
| Security audit | bug-hunting | code-review-and-quality |
| Completion check outside dev-craft | verification-before-completion | — |
| Long session, handoff, resume | context-engineering | — |
| Independent tasks in parallel | dispatching-parallel-agents | — |

Typos, one-line fixes, docs and config need no skill.

---

## Project-Specific Notes

- This project uses \`${template}\` template
- Primary skills: ${tmpl.skills.join(', ')}
- Primary agents: ${tmpl.agents.join(', ')}
`;
      writeFileSync(agentsMdPath, agentsMd);
      console.log(`    ✓ Created AGENTS.md`);
    }
  }
  
  console.log('\n✓ Project initialization complete!');
  console.log('Run "agent-skills doctor" to verify installation.');
}