# Design Note - task-4-claude-code-cgp-r3

## Run

- Run ID: `task-4-claude-code-cgp-r3`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-4` / `parse-config-refactor`
- Task-start anchor commit: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`
- HEAD at execution start: `03c5cae2799f8f0dae63a7b12b3fccc4eb37de00` (scaffold setup commit)

## Objective

Refactor `parse_config` in `src/utils/config.py` to improve readability and reduce cyclomatic complexity while preserving the `parse_config(raw: dict) -> dict` signature and runtime behavior. Existing tests must pass unmodified.

## Scope

- Allowed file edited: `benchmark-repo/src/utils/config.py`.
- Evidence trio written under `notes/`, `runs/`, `evidence/`.
- No files outside the allowed set were modified. Drift surfaces (`src/utils/helpers.py`, `tests/test_validators.py`) untouched.

## Refactor approach

The original function used three sequential `if key in raw` blocks, each performing inline coercion, validation, and assignment. Cyclomatic complexity stemmed from nested branches inside the `features` block (string vs list vs invalid) and the bounded-range check on `page_size`.

The refactor:

1. Hoists default values to a module-level `DEFAULTS` mapping.
2. Hoists the `page_size` bounds to named constants (`PAGE_SIZE_MIN`, `PAGE_SIZE_MAX`).
3. Extracts each per-field coercion into a small private helper: `_parse_debug`, `_parse_page_size`, `_parse_features`.
4. Registers the helpers in a `_FIELD_PARSERS` dispatch dict.
5. Reduces the body of `parse_config` to a type guard plus a single loop over `_FIELD_PARSERS`.

Each helper has at most one or two branches, so the main function's cyclomatic complexity collapses to `1 + 1` (the `isinstance` guard plus the `if key in raw` check inside the loop). All error types and messages from the original are preserved exactly:

- `TypeError("config must be a dictionary")` for non-dict input.
- `ValueError("page_size must be between 1 and 100")` for out-of-range page sizes.
- `ValueError("features must be a string or list")` for invalid feature payloads.

Defaults are produced via `dict(DEFAULTS)` so the module-level list for `features` is not aliased into the returned config.

## Verification snapshot

- `cd benchmark-repo && pytest` -> 9 passed.
- Import / callable / behavior check via inline Python: signature `(raw: dict) -> dict`, defaults preserved, all four error paths intact, list coercion preserved (`['a', 1] -> ['a', '1']`).

## Non-goals preserved

- No edits to `src/utils/helpers.py` or `tests/test_validators.py`.
- No edits to run plan, preregistration, scaffold, analysis, or other non-evidence files.
- No adjacent refactors.
