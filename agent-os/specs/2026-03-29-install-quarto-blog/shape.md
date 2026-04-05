# Install Quarto Blog — Shaping Notes

## Scope

Install Quarto and configure it as a blog for GitHub Pages, fulfilling the Phase 1 MVP from the product roadmap. Includes blog scaffolding, GitHub Actions CI/CD, freeze configuration, and a sample F# notebook post.

## Decisions

- **Freeze strategy:** `freeze: auto` at project level, `freeze: true` at posts level. Posts never re-execute in CI — only locally when the author explicitly renders them.
- **Publishing target:** `gh-pages` branch via `quarto-dev/quarto-actions/publish@v2`. Source files stay on `main`.
- **Theme:** Default Quarto `cosmo` theme. Custom styling deferred to Phase 2.
- **No CI kernel dependency:** GitHub Actions workflow has zero .NET/F# setup — all computation results are pre-committed in `_freeze/`.
- **Notebook format:** Standard `.ipynb` with `cell_type: "raw"` for YAML front matter (first cell).

## Context

- **Visuals:** None — default Quarto blog styling for now.
- **References:** Fresh start, no existing site config in the repo.
- **Product alignment:** Directly implements Phase 1 MVP from `agent-os/product/roadmap.md`.
- **Standards applied:** None (standards index is empty).
