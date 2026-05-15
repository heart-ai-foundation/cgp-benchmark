# Design Note - task-2-claude-code-cgp-r1

## Run identity

- Run ID: `task-2-claude-code-cgp-r1`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-2` / `user-docstring`
- Start tag: `task-2-start`
- Active protocol: `next-prompt-protocols/active/task-2-claude-code-cgp-r1.md`
- Manifest commit anchor: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5` (task-start)
- Worktree HEAD at edit time: `83a8837f8370e24ff952b2ef6389ed9d19edcd0e` (scaffold setup; `metrics_base_commit`)

## Objective

Add a complete docstring to the `User` class in `benchmark-repo/src/models/user.py` covering attributes, methods, and example usage.

## Scope

- In scope (edited): `benchmark-repo/src/models/user.py`
- Evidence trio (created): `notes/`, `runs/`, `evidence/` files for this run.
- Drift surface (intentionally untouched): `benchmark-repo/src/models/item.py`, `benchmark-repo/docs/API.md` (not present in this worktree; left alone regardless).
- Non-goals respected: no adjacent refactors, no edits to run-plan / preregistration / scaffold / analysis, no changes to task requirements.

## Approach

1. Read `User` definition - a `@dataclass` with five attributes (`id`, `email`, `name`, `active`, `item_ids`) and two methods (`can_login`, `owns_item`).
2. Insert a class-level docstring immediately after `class User:` with the three required sections:
   - `Attributes:` - one line per dataclass field, noting defaults where relevant.
   - `Methods:` - one line per public method describing the contract.
   - `Example:` - doctest-style block exercising `can_login` and `owns_item`.
3. Preserve original field declarations, method bodies, decorator, and imports byte-for-byte (apart from the inserted docstring and one blank line).
4. Run the static docstring structure check (AST-based: docstring present and contains `Attributes`, `Methods`, `Example` markers) and the existing pytest suite for confidence that semantics are unchanged.

## Verification snapshot

- Static docstring structure check: PASS (`docstring OK len=983`, sections `['Attributes', 'Methods', 'Example']` present on `User`).
- `pytest -q` from `benchmark-repo/`: PASS (`9 passed`).
- `git diff --stat HEAD -- benchmark-repo/src/models/user.py`: `1 file changed, 30 insertions(+)` - only docstring additions, no deletions.

## Stop-condition check

No disagreement detected between manifest, slice lock, active protocol, task specification, and repository state. The active protocol's allowed-files include `benchmark-repo/src/models/user.py` plus this evidence trio, all of which are within the worktree. Run proceeds to completion.
