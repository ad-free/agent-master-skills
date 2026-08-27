---
name: tdd-seam
description: TDD seam-based testing enforcement. Ensures tests are written at pre-agreed public seams, not against internals. Enforces red-green-refactor loop with vertical slices. Ported from mattpocock/engineering/tdd.
version: 1.0.0
triggers:
  - "tdd"
  - "test driven"
  - "red green"
  - "seam"
  - "test first"
metadata:
  origin: agent-master-skills
  ports: mattpocock/engineering/tdd
---

# TDD Seam-Based Testing

Test-driven development with seam-based testing. Tests verify behavior through public interfaces, not implementation details.

---

## 1. WHAT A GOOD TEST IS

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

---

## 2. SEAMS: WHERE TESTS GO

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

### Test Only at Pre-Agreed Seams

Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam.

Ask: **"What's the public interface, and which seams should we test?"**

### Seam Types

- **Function/Method seams**: test the public function signature
- **API seams**: test HTTP endpoints
- **Database seams**: test through repository interfaces
- **CLI seams**: test command-line input/output
- **Event seams**: test event publication and handling
- **Message seams**: test message queue publish/subscribe

### Seam Identification

```typescript
// BAD: Testing internal implementation
test('validateInput calls checkLength and checkFormat', () => {
  const validateInput = jest.spyOn(internal, 'checkLength');
  validateInput(input);
  expect(validateInput).toHaveBeenCalled();
});

// GOOD: Testing through public seam
test('validateInput rejects empty strings', () => {
  expect(validateInput('')).rejects.toThrow('Input required');
});
```

---

## 3. ANTI-PATTERNS

### Implementation-Coupled
Mocks internal collaborators, tests private methods, or verifies through a side channel. The tell: the test breaks when you refactor but behavior hasn't changed.

```typescript
// BAD: Implementation-coupled
test('user service hashes password', () => {
  const userService = new UserService();
  jest.spyOn(bcrypt, 'hash');
  await userService.create(user);
  expect(bcrypt.hash).toHaveBeenCalled();
});

// GOOD: Behavior-focused
test('user service creates user with hashed password', async () => {
  const user = await userService.create({ password: 'secret' });
  const stored = await db.users.findById(user.id);
  expect(stored.password).not.toBe('secret');
  expect(stored.password).toMatch(/^\$2[aby]?\$/);
});
```

### Tautological
The assertion recomputes the expected value the way the code does. Expected values must come from an independent source of truth.

```typescript
// BAD: Tautological
test('add returns sum', () => {
  expect(add(2, 3)).toBe(2 + 3);
});

// GOOD: Known-good literal
test('add returns sum', () => {
  expect(add(2, 3)).toBe(5);
});
```

### Horizontal Slicing
Writing all tests first, then all implementation. Bulk tests verify imagined behavior. Work in vertical slices instead: one test → one implementation → repeat.

---

## 4. RULES OF THE LOOP

### Red Before Green
Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.

```typescript
// RED: Write failing test
test('calculator adds two numbers', () => {
  const calc = new Calculator();
  expect(calc.add(2, 3)).toBe(5);
});

// GREEN: Minimal implementation
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
```

### One Slice at a Time
One seam, one test, one minimal implementation per cycle.

### Refactoring Is Not Part of the Loop
It belongs to the review stage, not the red → green implementation cycle.

---

## 5. TDD WORKFLOW

### Step 1: Identify Seam
```typescript
// What's the public interface?
// What seam should we test?
// → Calculator.add(a: number, b: number): number
```

### Step 2: Write Failing Test (RED)
```typescript
test('calculator adds two numbers', () => {
  const calc = new Calculator();
  expect(calc.add(2, 3)).toBe(5);
});
// ❌ FAIL: Calculator.add is not a function
```

### Step 3: Minimal Implementation (GREEN)
```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
// ✅ PASS: test passes
```

### Step 4: Next Slice
```typescript
// RED: New test
test('calculator handles negative numbers', () => {
  const calc = new Calculator();
  expect(calc.add(-1, 1)).toBe(0);
});

// GREEN: Minimal implementation
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
// ✅ PASS: already works
```

---

## 6. SEAM CONFIRMATION CHECKLIST

Before writing any test, confirm:

- [ ] What is the public interface?
- [ ] Which seams should we test?
- [ ] What behavior are we verifying?
- [ ] Where does the seam start and end?
- [ ] What's the independent source of truth for expected values?

---

## 7. TEST NAMING CONVENTION

Use behavior-focused names:

```typescript
// BAD: Implementation-focused
test('UserService.create hashes password', () => {});

// GOOD: Behavior-focused
test('user service creates user with hashed password', () => {});
test('user service rejects duplicate email', () => {});
test('user service requires password of at least 8 characters', () => {});
```

---

## 8. VERTICAL SLICES

Work in vertical slices, not horizontal layers:

```typescript
// BAD: Horizontal slicing
// Write all tests for Calculator
test('add works', () => {});
test('subtract works', () => {});
test('multiply works', () => {});
test('divide works', () => {});
// Then implement everything

// GOOD: Vertical slicing
// Cycle 1: Addition
test('add returns sum', () => {});
// Implement add

// Cycle 2: Subtraction
test('subtract returns difference', () => {});
// Implement subtract

// Cycle 3: Multiplication
test('multiply returns product', () => {});
// Implement multiply
```

---

## 9. INTEGRATION WITH DEV-CRAFT

In the dev-craft pipeline:
- **PHASE 0 (TDD_SEAM)**: Identify seams, confirm with user
- **PHASE 2 (TEST_PLAN)**: Write test plan based on seams
- **PHASE 3 (BUILD)**: Implement with red-green-refactor
- **PHASE 4 (VERIFY)**: Run tests, capture evidence

---

## 10. QUICK TDD CHECKLIST

For a fast TDD pass:

- [ ] Seam identified and confirmed
- [ ] Failing test written first
- [ ] Minimal implementation to pass
- [ ] Test passes
- [ ] No implementation-coupled tests
- [ ] No tautological assertions
- [ ] Vertical slice complete
- [ ] Ready for next slice
