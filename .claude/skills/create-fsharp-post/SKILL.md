---
name: create-fsharp-post
description: Create a new F# Jupyter notebook blog post with correct Quarto-compatible metadata. Prevents rendering issues caused by incorrect cell types or language identifiers.
argument-hint: "[slug]"
---

Create a new F# notebook blog post under `posts/` with correct Quarto-compatible metadata.

## Important Guidelines

- **Always use AskUserQuestion tool** when asking the user anything
- **Never use `F#` as a language identifier** — Pandoc doesn't recognize it; always use `fsharp`
- **Frontmatter must be a raw cell** — Not a code cell

## Process

### Step 1: Gather Post Details

If `$ARGUMENTS` contains a slug, use it. Otherwise, use AskUserQuestion:

```
What's the blog post about? I'll need:

1. A short slug for the URL (e.g., "pattern-matching-basics")
2. The title
3. A one-line description

Or just describe the topic and I'll suggest these.
```

### Step 2: Generate the Notebook

Create the file at `posts/{slug}/index.ipynb` with this exact structure:

```json
{
 "cells": [
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "---\n",
    "title: \"{title}\"\n",
    "description: \"{description}\"\n",
    "author: \"Kurt Mueller\"\n",
    "date: \"{YYYY-MM-DD}\"\n",
    "categories:\n",
    "  - fsharp\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Introduction\n",
    "\n",
    "TODO: Write introduction."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "dotnet_interactive": {
     "language": "fsharp"
    }
   },
   "outputs": [],
   "source": [
    "// Your F# code here\n",
    "printfn \"Hello from F#!\""
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".NET (F#)",
   "language": "fsharp",
   "name": ".net-fsharp"
  },
  "language_info": {
   "name": "fsharp"
  },
  "polyglot_notebook": {
   "kernelInfo": {
    "defaultKernelName": "fsharp",
    "items": [
     {
      "aliases": [],
      "name": "fsharp"
     }
    ]
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

### Critical Metadata Rules

These rules prevent known rendering failures with Quarto + Pandoc:

| Field | Correct | Wrong (breaks rendering) |
|---|---|---|
| Frontmatter cell type | `"cell_type": "raw"` | `"cell_type": "code"` |
| `kernelspec.language` | `"fsharp"` | `"F#"` |
| `language_info.name` | `"fsharp"` | `"polyglot-notebook"` |

**Why:** Pandoc doesn't recognize `f#` as a language class — the `#` corrupts fenced code block syntax, causing code to render as inline text. Using `"polyglot-notebook"` has the same effect. The frontmatter cell must be `raw` so Quarto treats it as metadata, not executable code.

### Step 3: Confirm

```
Created posts/{slug}/index.ipynb

Open it in VS Code or Jupyter to start writing. The notebook has:
- ✅ Raw frontmatter cell (won't render as code block)
- ✅ fsharp language identifiers (proper syntax highlighting)
- ✅ Starter markdown + code cells

To preview: quarto preview posts/{slug}/index.ipynb
```

## Tips

- **Add categories** in the frontmatter YAML to organize posts on the blog index
- **Use `execute: freeze: auto`** in `_quarto.yml` (already configured) so notebooks don't need to be re-executed during CI
- After writing, run `/validate-notebooks` to catch any issues before publishing
