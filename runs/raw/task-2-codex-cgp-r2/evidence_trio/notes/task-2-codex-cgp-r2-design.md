# Design Note: task-2-codex-cgp-r2

## Scope

Added documentation only to `benchmark-repo/src/models/user.py`, preserving the existing `User` dataclass fields and method behavior.

## Rationale

The class docstring documents the model purpose, all public dataclass attributes, both public methods, and a short interactive example. This satisfies the task requirement without changing runtime behavior or touching drift-surface files.

## Verification Snapshot

- Command: `cd benchmark-repo && python - <<'PY' ... PY`
- Result: `Static docstring structure check passed`
