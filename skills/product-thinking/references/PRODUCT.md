# PRODUCT.md — [Project Name]

## 1. Domain & Problem

**Domain:** [HRM / CRM / E-commerce / etc.]
**Context:** [Greenfield / Replacement / Prototype / Idea stage]

### Users
| Role | Description |
|------|-------------|
| [Role 1] | [What this user does in the system] |
| [Role 2] | [What this user does in the system] |

### Problem Statement
> [Single sentence: Who needs what and why]

---

## 2. Scope

### Modules
| Module | Purpose | In/Out |
|--------|---------|--------|
| [Module 1] | [1-line purpose] | ✅ In scope |
| [Module 2] | [1-line purpose] | ✅ In scope |
| [Module 3] | [1-line purpose] | ❌ Out of scope (future) |

### Integration Points
- [External service 1] — [purpose]
- [External service 2] — [purpose]

---

## 3. Features

### Module 1: [Name]
| ID | Feature | User Story | Acceptance Criteria | Priority |
|----|---------|------------|-------------------|----------|
| F1 | [Feature] | As a [role], I want to [action] so that [benefit]. | 1. [Condition] | G1 |
| F2 | [Feature] | As a [role], I want to [action] so that [benefit]. | 1. [Condition] | G2 |

### Module 2: [Name]
| ID | Feature | User Story | Acceptance Criteria | Priority |
|----|---------|------------|-------------------|----------|
| F3 | [Feature] | ... | ... | ... |

---

## 4. Priority & Sequencing

### Priority Map
| Module | Priority | Complexity | Depends On |
|--------|----------|------------|------------|
| [Module 1] | G1 | L | — |
| [Module 2] | G1 | M | Module 1 |
| [Module 3] | G2 | S | — |

### Build Sequence
1. **Phase 1 (G1):** Module 1 → Module 2 (core workflow)
2. **Phase 2 (G1/G2):** Module 3 + Module 4 (supporting features)
3. **Phase 3 (G2):** Module 5 + Module 6 (enhancements)
4. **Phase 4 (G3):** Module 7 (polish, analytics, reports)

### Dependency Graph
```
Module 1 ──→ Module 2 ──→ Module 4
                           │
Module 3 ──────────────────┘
                    Module 5 (standalone)
```

---

## 5. Open Questions

1. [Question about requirement ambiguity]
2. [Question about technical constraint]
3. [Question about user behavior assumption]

---

## 6. Glossary

| Term | Definition |
|------|------------|
| [Term] | [Definition] |
