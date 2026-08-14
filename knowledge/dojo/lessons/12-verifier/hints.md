# Hints — 12 verifier

## Hint 1

Run the pieces you already have: `python3 -c "import re; print(re.findall(r'^\s*\d+\.\s+(.+)$', open('fixtures/builder_report.md').read(), re.MULTILINE))"` shows you what extract_claims should return. Then look at the dispatch in `verify_claim`: each branch already tells you which stdlib tool proves that claim class — `ast` for docstrings, an actual function call for behavior, `pathlib` for existence. The verifier never edits; it only observes and reports.

## Hint 2

- `extract_claims`: one line — `re.findall(r"^\s*\d+\.\s+(.+)$", report_text, re.MULTILINE)`.
- Docstring branch: `ast.parse` the file text, walk the tree, collect `n.name` for every `ast.FunctionDef` where `ast.get_docstring(n)` is falsy; verdict is `not missing`.
- Behavior branch: `actual = getattr(mod, fn)(a, b)`; verdict is `actual == want`; the evidence string must include `actual` — the checker looks for the real observed number (9) in the multiply evidence.
- Existence branch: `CALC.exists()` for both verdict and evidence.
- Report: `REPORT_OUT.write_text(json.dumps({"claims": results, "all_verified": all_verified}, indent=2))`.
- Exit: `sys.exit(0 if all_verified else 1)`.

## Hint 3

Near-answer — the six blanks in order:

```python
# extract_claims
return re.findall(r"^\s*\d+\.\s+(.+)$", report_text, re.MULTILINE)

# docstring branch
tree = ast.parse(CALC.read_text(encoding="utf-8"))
missing = [n.name for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef) and not ast.get_docstring(n)]
return (not missing, f"ast docstring scan of {CALC.name}: missing={missing or 'none'}")

# behavior branch
actual = getattr(mod, fn)(a, b)
return (actual == want, f"called {fn}({a}, {b}) -> got {actual}, builder claimed {want}")

# existence branch
return (CALC.exists(), f"pathlib: {CALC.relative_to(ROOT)} exists -> {CALC.exists()}")

# report contract + exit code (in main)
REPORT_OUT.write_text(
    json.dumps({"claims": results, "all_verified": all_verified}, indent=2),
    encoding="utf-8",
)
# ...
sys.exit(0 if all_verified else 1)
```
