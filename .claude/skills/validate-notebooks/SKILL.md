---
name: validate-notebooks
description: Validate Jupyter notebook metadata for Quarto compatibility. Catches rendering issues (wrong cell types, bad language identifiers) before publishing.
argument-hint: "[path]"
---

Validate `.ipynb` notebooks for Quarto rendering compatibility.

## Important Guidelines

- **Report all issues found** — Don't stop at the first one
- **Offer to auto-fix** — After reporting, ask if the user wants fixes applied
- **Never change cell content** — Only fix metadata and cell types

## Process

### Step 1: Find Notebooks

If `$ARGUMENTS` contains a path, validate that specific notebook.

Otherwise, find all notebooks:

```bash
find posts/ -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*'
```

### Step 2: Validate Each Notebook

For each `.ipynb` file, run these checks using a script or inline Python:

```python
import json, sys

def validate_notebook(path):
    with open(path) as f:
        nb = json.load(f)

    issues = []
    meta = nb.get('metadata', {})

    # Check 1: kernelspec.language must be "fsharp", not "F#"
    ks_lang = meta.get('kernelspec', {}).get('language', '')
    if ks_lang.lower() == 'f#':
        issues.append({
            'severity': 'error',
            'check': 'kernelspec.language',
            'message': f'kernelspec.language is "{ks_lang}" — must be "fsharp". '
                       f'Pandoc cannot parse "f#" as a language class (the # breaks fenced code blocks).',
            'fix': ('metadata.kernelspec.language', 'fsharp')
        })

    # Check 2: language_info.name must be "fsharp", not "polyglot-notebook"
    li_name = meta.get('language_info', {}).get('name', '')
    if li_name == 'polyglot-notebook':
        issues.append({
            'severity': 'error',
            'check': 'language_info.name',
            'message': f'language_info.name is "{li_name}" — must be "fsharp". '
                       f'Quarto uses this to determine the code cell language.',
            'fix': ('metadata.language_info.name', 'fsharp')
        })

    # Check 3: First cell should be raw (frontmatter)
    if nb['cells']:
        cell0 = nb['cells'][0]
        src = ''.join(cell0.get('source', []))
        if src.strip().startswith('---') and cell0['cell_type'] != 'raw':
            issues.append({
                'severity': 'error',
                'check': 'frontmatter cell type',
                'message': f'Frontmatter cell is "{cell0["cell_type"]}" — must be "raw". '
                           f'Code cells execute frontmatter as F#, producing parse errors.',
                'fix': ('cells[0].cell_type', 'raw')
            })

    # Check 4: Frontmatter code cell should not have outputs or execution_count
    if nb['cells']:
        cell0 = nb['cells'][0]
        src = ''.join(cell0.get('source', []))
        if src.strip().startswith('---') and cell0['cell_type'] == 'raw':
            if 'execution_count' in cell0 or cell0.get('outputs'):
                issues.append({
                    'severity': 'warning',
                    'check': 'frontmatter cell artifacts',
                    'message': 'Raw frontmatter cell has leftover execution_count or outputs fields.',
                    'fix': ('cells[0]: remove execution_count and outputs', None)
                })

    return issues
```

### Step 3: Report Results

Present findings grouped by file:

```
## Notebook Validation Results

### posts/hello-fsharp/index.ipynb
✅ All checks passed

### posts/new-post/index.ipynb
❌ kernelspec.language is "F#" — must be "fsharp"
❌ language_info.name is "polyglot-notebook" — must be "fsharp"
❌ Frontmatter cell is "code" — must be "raw"

---
Found 3 issues in 1 of 2 notebooks.
```

### Step 4: Offer Auto-Fix

If issues were found, use AskUserQuestion:

```
Found {n} issues. Should I auto-fix them?

1. **Fix all** — Apply all fixes automatically
2. **Review each** — Show me each fix before applying
3. **Skip** — Don't fix, just report
```

### Applying Fixes

When fixing, use Python/JSON manipulation (not text editing) to avoid corruption:

- **kernelspec.language**: Set to `"fsharp"`
- **language_info.name**: Set to `"fsharp"`
- **cell_type change**: Set `cell_type` to `"raw"`, remove `execution_count` and `outputs` keys
- **Write back** with `json.dump(nb, f, indent=1, ensure_ascii=False)` and trailing newline

After fixes, re-validate to confirm all issues are resolved.

## Checks Reference

| Check | Severity | What | Why |
|---|---|---|---|
| `kernelspec.language` | Error | Must be `"fsharp"` | `"F#"` → `.f#` class → `#` breaks Pandoc fenced code blocks |
| `language_info.name` | Error | Must be `"fsharp"` | `"polyglot-notebook"` is not a Pandoc language |
| Frontmatter cell type | Error | Must be `"raw"` | Code cells execute YAML as F#, producing errors |
| Frontmatter artifacts | Warning | No outputs/execution_count on raw cells | Leftover fields from when cell was a code cell |

## Tips

- Run before committing new or edited notebooks
- The .NET Interactive kernel defaults to `"F#"` and `"polyglot-notebook"` — these must be corrected every time
- Pair with `create-fsharp-post` skill to avoid issues from the start
