#!/usr/bin/env python3
"""Validate Jupyter notebooks for Quarto rendering compatibility.

Checks for metadata issues that cause broken code block rendering:
- kernelspec.language must be "fsharp" (not "F#")
- language_info.name must be "fsharp" (not "polyglot-notebook")
- Frontmatter cells must be raw (not code)
"""

import json
import glob
import sys


def validate_notebook(path):
    with open(path) as f:
        nb = json.load(f)

    issues = []
    meta = nb.get("metadata", {})

    ks_lang = meta.get("kernelspec", {}).get("language", "")
    if ks_lang.lower() == "f#":
        issues.append(
            f'kernelspec.language is "{ks_lang}" — must be "fsharp". '
            f"Pandoc cannot parse f# as a language class."
        )

    li_name = meta.get("language_info", {}).get("name", "")
    if li_name == "polyglot-notebook":
        issues.append(
            f'language_info.name is "{li_name}" — must be "fsharp". '
            f"Quarto uses this to determine the code cell language."
        )

    if nb.get("cells"):
        cell0 = nb["cells"][0]
        src = "".join(cell0.get("source", []))
        if src.strip().startswith("---") and cell0["cell_type"] != "raw":
            issues.append(
                f'Frontmatter cell is "{cell0["cell_type"]}" — must be "raw". '
                f"Code cells execute YAML as F#, producing parse errors."
            )

    return issues


def main():
    notebooks = sorted(glob.glob("posts/**/index.ipynb", recursive=True))

    if not notebooks:
        print("No notebooks found to validate.")
        return 0

    total_issues = 0

    for path in notebooks:
        issues = validate_notebook(path)
        if issues:
            print(f"\n❌ {path}")
            for issue in issues:
                print(f"   • {issue}")
            total_issues += len(issues)
        else:
            print(f"✅ {path}")

    if total_issues:
        print(f"\n{total_issues} issue(s) found. Fix before publishing.")
        return 1

    print(f"\nAll {len(notebooks)} notebook(s) passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
