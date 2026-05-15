# Phase 0 Initial Benchmark Scaffold

## Why this exists

The locked CGP drift-reduction experiment requires a canonical open repository before benchmark execution. This slice creates the initial repository scaffold and executable controlled benchmark app without starting the experiment or drafting results.

## Macro delta alignment

This slice reduces the gap between locked experiment design and executable repository by creating the repo layout, baseline benchmark app, and protocol scaffold.

## Next objective

Create the initial `cgp-benchmark` repository with a passing Python and frontend benchmark app, orientation docs, raw and processed run directories, paper placeholder, and Next-Prompt Protocol scaffold.

## Files in play

- `README.md`
- `LICENSE`
- `CITATION.cff`
- `.gitignore`
- `benchmark-repo/**`
- `docs/**`
- `analysis/**`
- `paper/**`
- `runs/**`
- `next-prompt-protocols/**`

## Non-goals

- Do not run the 72-run experiment.
- Do not claim benchmark results.
- Do not publish a paper draft with fabricated or expected results.
- Do not change the locked Heart Corpus v1.1 experiment design.

## Acceptance

- `python -m pytest` passes from `benchmark-repo/`.
- `npm test` passes from `benchmark-repo/`.
- `node next-prompt-protocols/tools/sync-protocols.mjs --check` passes from repository root.
- Repository has an initial commit ready for publication under `heart-ai-foundation/cgp-benchmark`.
