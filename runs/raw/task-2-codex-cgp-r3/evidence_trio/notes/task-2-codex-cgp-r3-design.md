# Design Note: task-2-codex-cgp-r3

## Scope

Added a class-level docstring to `benchmark-repo/src/models/user.py` for the `User` dataclass. No runtime behavior, imports, tests, API documentation, or adjacent model files were changed.

## Rationale

The task requires a complete `User` class docstring covering attributes, methods, and example usage. The docstring documents all dataclass fields (`id`, `email`, `name`, `active`, and `item_ids`), both public methods (`can_login` and `owns_item`), and a short doctest-style example that demonstrates construction and method calls.

## Verification

- `Static docstring structure check`: passed via AST inspection of `benchmark-repo/src/models/user.py`.
