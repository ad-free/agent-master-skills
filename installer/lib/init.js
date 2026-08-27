import { existsSync, mkdirSync, writeFileSync, cpSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = resolve(__dirname, '..', '..');

const TEMPLATES = {
  minimal: {
    skills: ['dev-craft', 'verification-before-completion'],
    agents: ['implementer', 'verifier'],
  },
  fullstack: {
    skills: ['dev-craft', 'ui-craft', 'planning-and-task-breakdown', 'verification-before-completion', 'debugging-and-error-recovery', 'code-review-and-quality'],
    agents: ['planner', 'implementer', 'frontend-engineer', 'verifier', 'debugger', 'code-reviewer'],
  },
  frontend: {
    skills: ['ui-craft', 'planning-and-task-breakdown', 'verification-before-completion', 'design-system-validate', 'accessibility-deep'],
    agents: ['planner', 'frontend-engineer', 'verifier'],
  },
  backend: {
    skills: ['dev-craft', 'planning-and-task-breakdown', 'verification-before-completion', 'backend-patterns', 'database-migrations'],
    agents: ['planner', 'implementer', 'verifier', 'database-engineer'],
  },
};

const HARNESS_CONFIGS = {
  opencode: {
    configDir: '.opencode',
    agentsDir: '.opencode/agents',
    skillsDir: '.opencode/skills',
  },
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

Project-level OpenCode configuration. Extends global \`~/.config/opencode/AGENTS.md\`.

---

## Skill Router — decide before acting

Route by task type, not by tech stack. Skills chain — follow the arrow.

| Task signal | Route |
|---|---|
| Vague idea, "how should we..." | product-thinking → planning-and-task-breakdown → dev-craft | ui-craft |
| Spec files (xlsx/csv/md/pdf) | project-discovery → planning-and-task-breakdown → dev-craft |
| New feature / new project | planning-and-task-breakdown → dev-craft | ui-craft |
| Bug / failing test / weird behavior | debugging-and-error-recovery → verification-before-completion |
| Frontend / UI work | ui-craft (+ frontend-design for visual polish) → verification-before-completion |
| Screenshot / image reference | image-to-design-spec → ui-craft |
| Infra / IaC / deploy change | dev-craft → Infra Safety → verification-before-completion |
| Large multi-module project | dev-craft + agent-orchestration |
| Multiple independent tasks | dispatching-parallel-agents |
| Review code | code-review-and-quality |
| Security audit / vuln discovery | bug-hunting → verification-before-completion |
| About to claim "done" | verification-before-completion (mandatory) |

**Unsure which skill?** Start with \`planning-and-task-breakdown\` — it produces a plan every other skill can execute against.

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