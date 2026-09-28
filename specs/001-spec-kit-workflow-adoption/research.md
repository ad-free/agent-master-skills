# Research: Spec Kit Workflow Adoption

## Decisions

### Install the supported CLI with the existing `uv` tool

- **Decision**: Install `specify-cli` via `uv tool install specify-cli`.
- **Rationale**: Spec Kit documents this as a persistent PyPI install; `uv` and
  Python 3.13.15 are already available. Installation succeeded as CLI version 1.0.12.
- **Alternatives considered**: A release-pinned source install or one-shot `uvx`.
  Neither was necessary for the requested local persistent setup.

### Install integrations per project

- **Decision**: Initialize this repository for OpenCode, then install Claude Code
  and Oh My Pi integrations through Spec Kit's integration manager.
- **Rationale**: Agent commands and the shared `.specify/` feature state are
  project-scoped. The integration status reports all three integrations as
  multi-install safe and healthy, with no missing or locally modified managed files.
- **Alternatives considered**: A global copy of all command prompts. This would
  duplicate commands across agent homes and would not provide project-local feature
  state or safe integration tracking.

### Keep one shared global policy source

- **Decision**: Extend `~/.config/opencode/AGENTS.md`; point Claude's global
  `AGENTS.md` at that canonical file. OMP already loads the OpenCode global
  `AGENTS.md` through its compatibility instructions provider; keep its own global
  `AGENTS.md` as a brief pointer rather than copying the full policy.
- **Evidence**: OMP `src/discovery/opencode.ts:167-182` reads
  `~/.config/opencode/AGENTS.md`; `src/discovery/builtin.ts:913-943` reads
  `~/.omp/agent/AGENTS.md`. Claude's user `CLAUDE.md` imports its adjacent
  `AGENTS.md`; Claude Code supports recursive `@path` imports.
- **Rationale**: One policy avoids drift and excessive repeated prompt context.

### Use Spec Kit as the feature workflow, not as the entire engineering gate

- **Decision**: For substantial features in initialized projects, use Spec Kit's full
  constitution → specify → clarify → plan → checklist → tasks → analyze → implement
  → converge lifecycle. Keep normal tests, security checks, review, and
  project-specific implementation skills.
- **Rationale**: This follows the official SDD quickstart and the repository's
  evidence/verification requirements without forcing full SDD onto routine bugs.
- **Alternatives considered**: Installing the optional bug and idea-assessment
  extensions. Existing repository skills already cover debugging and product
  discovery, so installing them would duplicate workflows.

## Sources

- Spec Kit [Installation Guide](https://github.github.io/spec-kit/installation.html)
- Spec Kit [SDD Quickstart](https://github.github.io/spec-kit/quickstart.html)
- Spec Kit [Existing Project Guide](https://github.github.io/spec-kit/guides/existing-projects.html)
- Spec Kit [Agent Integrations](https://github.github.io/spec-kit/reference/integrations.html)
- Claude Code [Memory and AGENTS.md documentation](https://code.claude.com/docs/en/memory)
- Installed OMP discovery sources listed above
