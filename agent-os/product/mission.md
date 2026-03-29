# Product Mission

## Problem

Creating a blog on GitHub Pages powered by Jupyter notebooks with F# language support. The F# notebook ecosystem is fragile: dotnet-interactive is deprecated (though still functional), Verso is too immature to rely on, and IfSharp is abandoned. A reliable authoring and publishing workflow is needed despite this tooling instability.

## Target Users

Personal technical blog for sharing ideas, experiments, and writing about F# and functional programming.

## Solution

The "freeze" strategy: decouple F# execution from CI/CD publishing. Author notebooks locally using dotnet-interactive's `.net-fsharp` Jupyter kernel, execute all cells before committing, and publish through Quarto with `freeze: true` so GitHub Actions never needs the F# kernel. This isolates the fragile dependency (F# notebook runtime) to the local authoring environment while keeping the publishing pipeline stable and kernel-agnostic.
