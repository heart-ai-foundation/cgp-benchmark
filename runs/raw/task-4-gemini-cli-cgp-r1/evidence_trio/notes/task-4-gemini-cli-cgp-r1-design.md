# Design Note - Task 4: Parse Config Refactor

## Rationale
The original `parse_config` function in `src/utils/config.py` handled multiple responsibilities (validation, type conversion, and default setting) for multiple configuration fields within a single function body. This increased cyclomatic complexity and reduced readability.

The refactoring extracts the logic for `page_size` and `features` into dedicated helper functions. This allows the main `parse_config` function to focus on the overall structure of the configuration object.

## Refactoring Plan
1.  Extract `page_size` parsing and validation into `_parse_page_size(value)`.
2.  Extract `features` parsing and validation into `_parse_features(value)`.
3.  Rewrite `parse_config` to use these helpers and `dict.get()` for cleaner default handling.
4.  Preserve the `parse_config(raw: dict) -> dict` signature.

## Verification Strategy
-   Run existing `pytest` suite in `benchmark-repo`.
-   Perform a manual import and execution test of `parse_config` with various inputs to ensure behavioral parity.
-   Ensure no changes were made to files outside the allowed set.
