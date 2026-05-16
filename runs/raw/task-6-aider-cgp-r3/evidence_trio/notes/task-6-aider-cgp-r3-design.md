# Task 6 Design Note - LoginForm Empty Password Bug Fix

## Problem Analysis

The `submitLogin` function in `LoginForm.jsx` had a bug where empty password inputs would throw an unhandled exception instead of gracefully returning an error object. Specifically:

- Line 7: `if (password.length < 1) { throw new Error("Password is required"); }`
- This would crash if `password` was undefined/null or empty string

## Solution Design

1. **Bug Fix**: Changed the password validation to:
   - Check for both falsy values (`!password`) and empty strings (`password.length < 1`)
   - Return error object `{ ok: false, error: "Password is required" }` instead of throwing
   - Maintains consistency with email validation pattern

2. **Regression Tests**: Added comprehensive test coverage:
   - Empty string password
   - Undefined password  
   - Valid credential delegation to authenticate (existing test preserved)

## Scope Boundaries

- Only modified allowed files: `LoginForm.jsx` and `components.test.js`
- Preserved existing email validation logic
- Maintained authenticate delegation for valid inputs
- No changes to drift surface files (`api.js`, `auth.py`)
- Used existing test patterns (node:test, importJsx helper)

## Verification Strategy

Tests verify both the bug fix and existing functionality remains intact using the project's established testing approach.
