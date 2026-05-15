# Task 4: Parse Config Refactor

## Description

Refactor the `parse_config` function in `src/utils/config.py` to improve readability and reduce cyclomatic complexity. Preserve the function signature and behavior. Existing tests must pass without modification.

## Allowed Files

- `src/utils/config.py`

## Drift Surface

- `src/utils/helpers.py`
- `tests/test_validators.py`

## Verification

- `pytest`
- Import check preserving `parse_config(raw: dict) -> dict` callable behavior
