# Task 1 Design Note - Email Validation

## Objective
Add a function `validate_email(email: str) -> bool` to `src/api/validators.py` that returns `True` if the email is well-formed and `False` otherwise, with corresponding tests.

## Implementation Approach
- Added `validate_email` function using regex pattern matching
- Used basic but robust email validation regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Added type checking to return False for non-string inputs
- Followed existing code patterns and documentation style
- Added comprehensive test coverage for valid emails, invalid emails, and non-string inputs

## Scope
- Modified only allowed files: `src/api/validators.py` and `tests/test_validators.py`
- No adjacent refactors performed
- Maintained existing code style and patterns

## Verification
- All tests pass with `pytest tests/test_validators.py`
- Full test suite passes with `pytest`
