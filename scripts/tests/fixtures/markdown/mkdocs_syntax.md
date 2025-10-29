# Test: MkDocs-Specific Syntax

This file contains valid MkDocs extensions that should NOT trigger errors.

!!! warning
    This is an admonition block
    - These list items are inside an admonition
    - They should not trigger validation errors

!!! info "Information"
    Another admonition with a title
    - More list items
    - Still valid

## Code Blocks

Code blocks should also be ignored:

```python
# This looks like a comment
- But it's in a code block
- Should not trigger errors
```

## Definition Lists

Term 1
:   Definition for term 1
:   Another definition

These are all valid MkDocs syntax and should pass validation.
