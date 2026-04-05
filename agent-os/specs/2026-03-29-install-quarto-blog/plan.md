# Plan: Install Quarto and Configure Blog MVP

## Context

Setting up a Quarto-powered blog on GitHub Pages with F# Jupyter notebook support. This is the Phase 1 MVP from the product roadmap. The key architectural insight is the "freeze" strategy: author notebooks locally with the `.net-fsharp` kernel, execute all cells, commit the `_freeze/` directory, and let CI render HTML without ever needing the F# kernel.

The repo is a fresh start — no existing site config, workflows, or blog files.

---

## Task 1: Save Spec Documentation

Create `agent-os/specs/2026-03-29-install-quarto-blog/` with:

- `plan.md` — This full plan
- `shape.md` — Shaping notes (scope, decisions, context)
- `references.md` — Quarto docs references

## Task 2: Create Quarto Blog Scaffolding

Create these files in the repo root:

**`_quarto.yml`**
```yaml
project:
  type: website

website:
  title: "Kurt Mueller"
  site-url: https://everybodykurts.github.io
  description: "A blog about F# and functional programming"
  navbar:
    right:
      - about.qmd
      - icon: github
        href: https://github.com/everybodykurts
      - icon: rss
        href: index.xml

format:
  html:
    theme: cosmo
    css: styles.css

execute:
  freeze: auto
```

**`index.qmd`**
```yaml
---
title: "Kurt Mueller"
listing:
  contents: posts
  sort: "date desc"
  type: default
  categories: true
  feed: true
---
```

**`about.qmd`**
```yaml
---
title: "About"
---

Welcome to my blog. I write about F# and functional programming.
```

**`styles.css`** — Empty placeholder for custom styles.

**`.nojekyll`** — Empty file to skip Jekyll processing on GitHub Pages.

**`posts/_metadata.yml`**
```yaml
# Options shared across all posts
freeze: true
```

Note: `freeze: true` (not `auto`) at posts level means posts are NEVER re-executed unless you explicitly render that specific post. The project-level `freeze: auto` applies to non-post content.

## Task 3: Update `.gitignore`

Add these entries:
```
/.quarto/
/_site/
```

Do NOT ignore `_freeze/` — it must be committed for the freeze strategy to work in CI.

## Task 4: Create GitHub Actions Workflow

**`.github/workflows/publish.yml`**
```yaml
on:
  workflow_dispatch:
  push:
    branches: main

name: Quarto Publish

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render and Publish
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

No Python, R, or .NET setup needed — `freeze` means all computation results are already committed.

## Task 5: Create Sample F# Blog Post

**`posts/hello-fsharp/index.ipynb`**

A Jupyter notebook with:
- Cell 1: Raw cell with YAML front matter (title, description, author, date, categories)
- Cell 2: Markdown cell with introduction
- Cell 3: F# code cell with a simple example
- Kernel metadata: `.net-fsharp`

The `.ipynb` JSON must have `"cell_type": "raw"` for the front matter cell (not markdown).

## Task 6: Local Render and Freeze (Manual Steps)

After implementation, the user needs to:

1. **Install prerequisites locally:**
   ```bash
   # Install Quarto from https://quarto.org/docs/get-started/
   brew install --cask quarto

   # Install dotnet-interactive and register the F# kernel
   dotnet tool install -g Microsoft.dotnet-interactive
   dotnet interactive jupyter install
   # Verify: jupyter kernelspec list should show .net-fsharp
   ```

2. **Render locally:**
   ```bash
   quarto render
   ```
   This executes notebook cells and creates `_freeze/` and `_site/`.

3. **Preview locally:**
   ```bash
   quarto preview
   ```

4. **Initial publish (creates `gh-pages` branch and `_publish.yml`):**
   ```bash
   quarto publish gh-pages
   ```
   Commit the generated `_publish.yml` to the repo.

5. **Configure GitHub repo settings:**
   - Settings > Pages > Source: "Deploy from a branch"
   - Branch: `gh-pages` / `/ (root)`
   - Settings > Actions > General > Workflow permissions: "Read and write permissions"

6. **Commit and push** all files including `_freeze/` directory.

---

## Critical Files

- `_quarto.yml` — Project config with freeze strategy
- `index.qmd` — Blog listing page
- `posts/_metadata.yml` — Per-post freeze override
- `.github/workflows/publish.yml` — CI/CD pipeline
- `posts/hello-fsharp/index.ipynb` — Sample F# notebook post
- `.gitignore` — Exclude build artifacts, keep `_freeze/`

## Verification

1. Run `quarto render` locally — should produce `_site/` with rendered blog
2. Run `quarto preview` — should open browser with working blog
3. Verify `_freeze/posts/hello-fsharp/` exists after render
4. Push to main — GitHub Actions should deploy to gh-pages
5. Visit https://everybodykurts.github.io — blog should be live
