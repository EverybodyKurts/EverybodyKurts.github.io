---
name: create-fsharp-post
description: Create a new F# Jupyter notebook blog post with correct Quarto-compatible metadata. Prevents rendering issues caused by incorrect cell types or language identifiers.
argument-hint: "[slug]"
---

Create a new F# notebook blog post under `posts/` with correct Quarto-compatible metadata.

## Important Guidelines

- **Always use AskUserQuestion tool** when asking the user anything
- **Never use `F#` as a language identifier** — Pandoc doesn't recognize it; always use `fsharp`
- **No raw frontmatter cell in the notebook** — VS Code's Polyglot Notebooks extension converts raw cells to code cells on open, breaking Quarto rendering. Use `_quarto.yml` + an h1 cell instead (see below).

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

### Step 2: Create `_quarto.yml` for the post

Create `posts/{slug}/_quarto.yml` with the post metadata:

```yaml
title: "{title}"
description: "{description}"
author: "Kurt Mueller"
date: "{YYYY-MM-DD}"
categories:
  - fsharp
```

Quarto merges this into the document at render time, so no frontmatter cell is needed in the notebook.

### Step 3: Generate the Notebook

Create `posts/{slug}/index.ipynb` with this exact structure:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# {title}"
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

**Why the `# {title}` h1 cell?** Quarto extracts the document title from the first level-1 heading when there is no raw frontmatter cell. All other metadata (description, author, date, categories) comes from `_quarto.yml`.

### Critical Metadata Rules

These rules prevent known rendering failures with Quarto + Pandoc:

| Field | Correct | Wrong (breaks rendering) |
|---|---|---|
| `kernelspec.language` | `"fsharp"` | `"F#"` |
| `language_info.name` | `"fsharp"` | `"polyglot-notebook"` |
| Title source | `# h1` markdown cell | raw frontmatter cell (VS Code mangles it) |

**Why:** Pandoc doesn't recognize `f#` as a language class — the `#` corrupts fenced code block syntax, causing code to render as inline text. Using `"polyglot-notebook"` has the same effect.

### Step 4: Confirm

```
Created:
  posts/{slug}/_quarto.yml   ← post metadata
  posts/{slug}/index.ipynb   ← notebook (h1 title cell + starter cells)

Open it in VS Code or Jupyter to start writing. The notebook is safe to edit
without any metadata getting mangled.

To preview: quarto preview posts/{slug}/index.ipynb
```

## Tips

- **Add categories** in `_quarto.yml` to organize posts on the blog index
- **Use `execute: freeze: auto`** in the root `_quarto.yml` (already configured) so notebooks don't need to be re-executed during CI
- After writing, run `/validate-notebooks` to catch any issues before publishing
