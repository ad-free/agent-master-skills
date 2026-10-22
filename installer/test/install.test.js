import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { findSkillsInRepo } from '../lib/install.js';

function skill(root, rel, name) {
  mkdirSync(join(root, rel), { recursive: true });
  writeFileSync(join(root, rel, 'SKILL.md'), `---\nname: ${name}\ndescription: test\n---\n`);
}

test('nested plugin, archived and synced skills are not installed as separate skills', () => {
  const root = mkdtempSync(join(tmpdir(), 'skills-'));
  skill(root, 'skills/dev-craft', 'dev-craft');
  skill(root, 'skills/dev-craft/plugins/tdd-enforcer', 'tdd-enforcer');
  skill(root, 'skills/ui-craft', 'ui-craft');
  skill(root, 'skills/_archive/handoff', 'handoff');
  skill(root, 'skills/synced/abc/pdf', 'pdf');

  const names = findSkillsInRepo(root).map((s) => s.name).sort();
  assert.deepEqual(names, ['dev-craft', 'ui-craft']);
});

test('a single skill folder installs as one skill', () => {
  const root = mkdtempSync(join(tmpdir(), 'skills-'));
  skill(root, '', 'dev-craft');
  skill(root, 'plugins/tdd-enforcer', 'tdd-enforcer');

  assert.deepEqual(findSkillsInRepo(root).map((s) => s.name), ['dev-craft']);
});
