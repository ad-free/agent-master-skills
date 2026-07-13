# Plugin System

Both dev-craft and ui-craft support a plugin system for extending functionality.

## Plugin Architecture

```
skills/
├── dev-craft/
│   ├── SKILL.md                    # Core pipeline
│   ├── plugins/                    # dev-craft plugins
│   │   ├── security-audit/
│   │   ├── database-migrations/
│   │   ├── api-versioning/
│   │   ├── performance-profiling/
│   │   └── dependency-audit/
│   ├── scripts/
│   └── references/
├── ui-craft/
│   ├── SKILL.md                    # Core pipeline
│   ├── plugins/                    # ui-craft plugins
│   │   ├── figma-sync/
│   │   ├── visual-regression/
│   │   ├── design-system-validate/
│   │   ├── accessibility-deep/
│   │   └── animation-craft/
│   ├── scripts/
│   └── references/
└── PLUGIN-SYSTEM.md                # This file
```

## Plugin Format

Each plugin is a directory with:

```
plugin-name/
├── SKILL.md              # Plugin instructions
├── scripts/              # Optional scripts
└── references/           # Optional reference docs
```

## Plugin Registration

Plugins are registered in `state.json`:

```json
{
  "plugins": ["security-audit", "figma-sync"],
  "pluginConfig": {
    "security-audit": { "severity": "high" },
    "figma-sync": { "fileKey": "abc123" }
  }
}
```

## Available Plugins

### dev-craft Plugins

| Plugin | Description | Use Case |
|--------|-------------|----------|
| `security-audit` | Agent-driven STRIDE + OWASP audit | Production deployments |
| `database-migrations` | Safe migration patterns | Schema changes |
| `api-versioning` | API version management | Public APIs |
| `performance-profiling` | Performance bottleneck detection | Optimization |
| `dependency-audit` | Dependency vulnerability scanning | Security |

### ui-craft Plugins

| Plugin | Description | Use Case |
|--------|-------------|----------|
| `figma-sync` | Sync design tokens from Figma | Design-to-code |
| `visual-regression` | Playwright screenshot comparison | Visual testing |
| `design-system-validate` | Validate against design system | Consistency |
| `accessibility-deep` | WCAG 2.2 AAA compliance | Accessibility |
| `animation-craft` | Advanced animation patterns | Micro-interactions |

## Best Practices

1. **Single responsibility** — One plugin, one concern
2. **Idempotent** — Running twice should not change results
3. **Configurable** — Accept config via `state.json`
4. **Documented** — Clear SKILL.md with examples
5. **Tested** — Include test cases in plugin

---

See `SHARED.md` for the skill router and cross-skill communication protocol.
