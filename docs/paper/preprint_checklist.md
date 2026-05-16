# Preprint Checklist

## Required Before Public Preprint

- Confirm `CGP_Benchmark_Preregistration_Deviation_Note_v1_1.md` is attached or linked from OSF.
- Confirm the repository README points to the v1.1 deviation note.
- Confirm `runs/processed/registered_analysis.md` and `runs/processed/registered_analysis.json` are present and pushed.
- Confirm `docs/paper/manuscript_draft.md` uses the reliability-and-auditability title.
- Confirm the abstract states the registered drift endpoint null at floor.
- Confirm no public-facing paper text says or implies CGP reduced drift in this benchmark.
- Confirm figure captions label validity as an operational composite rather than the registered primary endpoint.
- Confirm references are complete enough for preprint release.
- Confirm code/data license statement is visible.
- Confirm conflict-of-interest and AI-assistance disclosures are visible.

## Recommended Preprint Files

- `docs/paper/manuscript_draft.md`
- `docs/paper/figure_and_table_captions.md`
- `docs/paper/submission_package.md`
- `docs/paper/references.bib`
- `docs/paper/figures/`
- `docs/paper/tables/`
- `docs/research_integrity/CGP_Benchmark_Preregistration_Deviation_Note_v1_1.md`
- `runs/processed/registered_analysis.md`
- `runs/processed/registered_analysis.json`

## Build Note

Pandoc and Quarto were not available in the local environment when this checklist was created. The current package is Markdown-native and can be converted later with Pandoc, Quarto, or a venue-specific LaTeX template.

Recommended future build command after installing Pandoc:

```bash
pandoc docs/paper/manuscript_draft.md \
  --bibliography docs/paper/references.bib \
  --citeproc \
  -o docs/paper/preprint.pdf
```

## Preprint Abstract Boundary

The abstract must preserve this boundary:

The registered primary endpoint was scope drift and returned a null result at a baseline floor. The observed practical contribution concerns verifiable completion, work submission, evidence production, and failure-mode visibility.
