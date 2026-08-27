# Fingerprint Algorithm

## Purpose

Compute a deterministic hash of the working-tree source code that:
- Identical content = identical fingerprint (across commits, rebases, squashes)
- Includes untracked source files
- Excludes gitignored, binary, and large files
- Fast computation via stat cache (~40x faster than full re-hash)

## Algorithm

```
1. Get file list:
   - Tracked: `git ls-files`
   - Untracked (non-gitignored): `git ls-files --others --exclude-standard`
   
2. Filter to source files by extension:
   .ts, .tsx, .js, .jsx, .py, .go, .rs, .java, .kt, .cs, .php, .rb
   .json, .yaml, .yml, .toml, .md, .sql

3. Sort file paths lexicographically

4. For each file:
   - Read content
   - Compute SHA256(content)
   - Accumulate: SHA256(path + ':' + content_hash)

5. Final fingerprint = "sha256:" + accumulated_hash
```

## Caching

Cache key: `(mtime_ns, size)` → `file_hash`
- Invalidate on mtime or size change
- Stored in `.dev-craft/evidence/fingerprints/`

## Properties

| Property | Value |
|----------|-------|
| Deterministic | Yes |
| Git-history independent | Yes |
| Untracked files included | Yes |
| Gitignored excluded | Yes |
| Binary files excluded | By extension filter |
| Large file handling | Extension filter excludes most |
| Speed (10k files) | ~200ms (cached) vs ~8s (full) |

## Use Cases

- Evidence entry binding (detect tree changes since verification)
- Staleness detection in `evidence check`
- Cross-machine verification consistency