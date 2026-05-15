# Design Note - task-2-claude-code-cgp-r2

## Run

- Run ID: `task-2-claude-code-cgp-r2`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-2` / `user-docstring`
- Start tag: `task-2-start`
- HEAD at execution: `fc0a92c1b34dffdc3916d177596e7957dc8cbef4`

## Objective

Add a complete docstring to the `User` class in `benchmark-repo/src/models/user.py` covering attributes, methods, and example usage.

## Scope

Allowed edit (code):

- `benchmark-repo/src/models/user.py`

Evidence trio (written by this run):

- `notes/task-2-claude-code-cgp-r2-design.md`
- `runs/task-2-claude-code-cgp-r2-run-record.json`
- `evidence/task-2-claude-code-cgp-r2-evidence.json`

Drift surface (must remain untouched):

- `benchmark-repo/src/models/item.py`
- `docs/API.md`

## Rationale

`User` is a `@dataclass` with two methods (`can_login`, `owns_item`) and five fields (`id`, `email`, `name`, `active`, `item_ids`). A class-level docstring is the correct attachment point because:

1. Dataclass fields are declared at class scope; documenting them in the class docstring keeps the description colocated with the declarations.
2. The two methods are short, behavior-revealing predicates; documenting their contracts in the class docstring under a `Methods:` section satisfies the "covering methods" requirement without inflating per-method docstrings (which would expand scope beyond the task).
3. An `Example:` block using Google/PEP 257-compatible doctest formatting demonstrates instantiation, `can_login`, and `owns_item` against representative inputs.

The docstring structure used:

- One-line summary.
- `Attributes:` block enumerating all five fields with type/role.
- `Methods:` block describing `can_login` and `owns_item` contracts.
- `Example:` block with doctest-style usage.

No code behavior, signatures, decorators, or imports were modified. Field declarations and method bodies are byte-identical to the pre-edit state.

## Verification snapshot

Static docstring structure check (AST-based) confirmed:

- `User` has a non-empty docstring (length 830).
- Required tokens present: `Attributes`, `Methods`, `Example`, `id`, `email`, `name`, `active`, `item_ids`, `can_login`, `owns_item`.
- `python3 -m py_compile src/models/user.py` succeeds.

## Non-goals honored

- No edits outside `benchmark-repo/src/models/user.py` and the evidence trio.
- No adjacent refactors (signatures, imports, field defaults, method bodies unchanged).
- No changes to run-plan, preregistration, scaffold, or analysis files.
- Drift-surface files `src/models/item.py` and `docs/API.md` untouched.
