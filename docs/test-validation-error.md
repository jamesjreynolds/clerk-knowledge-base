# Test Validation Error

This file is intentionally created with markdown formatting errors to verify that CI/CD validation blocks merge.

## Problem: Missing blank line before list
- This list item should trigger an error
- Because there's no blank line before it

**Another problem:**
1. This ordered list also has no blank line
2. Should trigger validation error too

This file should be deleted after testing T040.
