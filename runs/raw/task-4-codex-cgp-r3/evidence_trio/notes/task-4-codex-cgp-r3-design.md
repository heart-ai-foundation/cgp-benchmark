# Task 4 Design Note

Run: `task-4-codex-cgp-r3`

## Scope

Refactored `parse_config(raw: dict) -> dict` in `benchmark-repo/src/utils/config.py`.

## Design

The original function mixed type validation, defaults, per-field parsing, and range validation in one branch-heavy body. The refactor keeps the public function signature and behavior intact while moving field-specific parsing into local helper functions:

- `_parse_debug`
- `_parse_page_size`
- `_parse_features`

`parse_config` now validates the raw config type, copies `DEFAULT_CONFIG`, and applies parsers from `CONFIG_PARSERS` only for keys present in the input. Unknown keys continue to be ignored.

## Behavior Preservation

- Non-dict input still raises `TypeError("config must be a dictionary")`.
- Missing keys still use defaults: `debug=False`, `page_size=25`, `features=[]`.
- `debug` is still coerced with `bool(...)`.
- `page_size` is still coerced with `int(...)` and constrained to `1..100`.
- `features` still accepts a string as a single feature, a list coerced element-wise with `str(...)`, and rejects other values.

## Verification Snapshot

- `cd benchmark-repo && pytest`: passed, 9 tests.
- `cd benchmark-repo && python - <<'PY' ...`: passed import, signature annotation, callable, and representative behavior checks.
