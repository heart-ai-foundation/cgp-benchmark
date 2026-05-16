#!/usr/bin/env python3
"""Run preregistered contrasts from processed CGP benchmark metrics."""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations
from math import comb, exp, log, sqrt
from pathlib import Path
import json
import random

import pandas as pd


PROCESSED = Path("runs/processed")
RUNS = PROCESSED / "run_level_metrics.csv"
OUT_JSON = PROCESSED / "registered_analysis.json"
OUT_MD = PROCESSED / "registered_analysis.md"
BOOTSTRAPS = 1000
RANDOM_SEED = 20260516


def binomial_two_sided_p(k: int, n: int, p: float = 0.5) -> float | None:
    if n == 0:
        return None
    observed = comb(n, k) * (p**k) * ((1 - p) ** (n - k))
    total = 0.0
    for i in range(n + 1):
        prob = comb(n, i) * (p**i) * ((1 - p) ** (n - i))
        if prob <= observed + 1e-15:
            total += prob
    return min(1.0, total)


def exact_wilcoxon_signed_rank(diffs: Iterable[float]) -> dict[str, float | int | None]:
    nonzero = [float(diff) for diff in diffs if float(diff) != 0.0]
    n = len(nonzero)
    if n == 0:
        return {"n_nonzero": 0, "w_plus": 0, "w_minus": 0, "p_two_sided": None}

    abs_values = [abs(diff) for diff in nonzero]
    sorted_unique = sorted(set(abs_values))
    ranks: list[float] = []
    for value in abs_values:
        positions = [idx + 1 for idx, ranked in enumerate(sorted(abs_values)) if ranked == value]
        ranks.append(sum(positions) / len(positions))

    w_plus = sum(rank for rank, diff in zip(ranks, nonzero, strict=True) if diff > 0)
    w_minus = sum(rank for rank, diff in zip(ranks, nonzero, strict=True) if diff < 0)
    observed = min(w_plus, w_minus)

    possible = []
    for r in range(n + 1):
        for positive_indices in combinations(range(n), r):
            positive = set(positive_indices)
            value = sum(rank for idx, rank in enumerate(ranks) if idx in positive)
            possible.append(min(value, sum(ranks) - value))
    p_value = sum(1 for value in possible if value <= observed + 1e-15) / len(possible)
    return {
        "n_nonzero": n,
        "w_plus": w_plus,
        "w_minus": w_minus,
        "p_two_sided": p_value,
    }


def pair_runs(df: pd.DataFrame) -> pd.DataFrame:
    index_cols = ["dataset", "agent", "task_id", "replication"]
    wide = df.pivot_table(
        index=index_cols,
        columns="condition",
        values=[
            "scope_drift_count",
            "verification_compliance",
            "task_success",
            "valid",
            "changed_file_count",
        ],
        aggfunc="first",
    )
    wide.columns = [f"{metric}_{condition}" for metric, condition in wide.columns]
    return wide.reset_index()


def odds_ratio_with_haldane(a: int, b: int, c: int, d: int) -> dict[str, float]:
    # Table orientation:
    # a = both success, b = baseline success / CGP fail,
    # c = baseline fail / CGP success, d = both fail.
    bh, ch = b + 0.5, c + 0.5
    odds = ch / bh
    se = sqrt((1 / bh) + (1 / ch))
    low = exp(log(odds) - 1.96 * se)
    high = exp(log(odds) + 1.96 * se)
    return {"discordant_odds_ratio_cgp_vs_baseline": odds, "ci95_low": low, "ci95_high": high}


def bootstrap_mean_diff(pairs: pd.DataFrame, baseline_col: str, cgp_col: str) -> dict[str, float]:
    rng = random.Random(RANDOM_SEED)
    diffs = [float(row[cgp_col]) - float(row[baseline_col]) for _, row in pairs.iterrows()]
    if not diffs:
        return {"mean_diff": 0.0, "ci95_low": 0.0, "ci95_high": 0.0}
    means = []
    for _ in range(BOOTSTRAPS):
        sample = [rng.choice(diffs) for _ in diffs]
        means.append(sum(sample) / len(sample))
    means.sort()
    return {
        "mean_diff": sum(diffs) / len(diffs),
        "ci95_low": means[int(0.025 * BOOTSTRAPS)],
        "ci95_high": means[int(0.975 * BOOTSTRAPS) - 1],
    }


def mcnemar(pairs: pd.DataFrame, variable: str) -> dict[str, int | float | None]:
    base = f"{variable}_baseline"
    cgp = f"{variable}_cgp"
    both_yes = int(((pairs[base] == 1) & (pairs[cgp] == 1)).sum())
    baseline_yes_cgp_no = int(((pairs[base] == 1) & (pairs[cgp] == 0)).sum())
    baseline_no_cgp_yes = int(((pairs[base] == 0) & (pairs[cgp] == 1)).sum())
    both_no = int(((pairs[base] == 0) & (pairs[cgp] == 0)).sum())
    discordant = baseline_yes_cgp_no + baseline_no_cgp_yes
    p_value = binomial_two_sided_p(min(baseline_yes_cgp_no, baseline_no_cgp_yes), discordant)
    odds = odds_ratio_with_haldane(both_yes, baseline_yes_cgp_no, baseline_no_cgp_yes, both_no)
    return {
        "both_yes": both_yes,
        "baseline_yes_cgp_no": baseline_yes_cgp_no,
        "baseline_no_cgp_yes": baseline_no_cgp_yes,
        "both_no": both_no,
        "discordant_n": discordant,
        "exact_mcnemar_p_two_sided": p_value,
        **odds,
    }


def variance_summary(df: pd.DataFrame) -> list[dict[str, str | float | int | None]]:
    rows = []
    metrics = ["scope_drift_count", "completed", "changed_file_count"]
    for (dataset, agent, task_id), cell in df.groupby(["dataset", "agent", "task_id"]):
        row: dict[str, str | float | int | None] = {"dataset": dataset, "agent": agent, "task_id": task_id}
        for metric in metrics:
            baseline = cell[cell["condition"] == "baseline"][metric].astype(float)
            cgp = cell[cell["condition"] == "cgp"][metric].astype(float)
            b_sd = float(baseline.std(ddof=1)) if len(baseline) > 1 else None
            c_sd = float(cgp.std(ddof=1)) if len(cgp) > 1 else None
            row[f"{metric}_baseline_sd"] = b_sd
            row[f"{metric}_cgp_sd"] = c_sd
            row[f"{metric}_variance_ratio_cgp_over_baseline"] = (
                (c_sd**2) / (b_sd**2) if b_sd and c_sd is not None else None
            )
        rows.append(row)
    return rows


def analyze_subset(name: str, df: pd.DataFrame) -> dict[str, object]:
    pairs = pair_runs(df)
    m1_diff = pairs["scope_drift_count_cgp"] - pairs["scope_drift_count_baseline"]
    return {
        "run_count": int(len(df)),
        "pair_count": int(len(pairs)),
        "scope_drift": {
            "baseline_total": int(df[df["condition"] == "baseline"]["scope_drift_count"].sum()),
            "cgp_total": int(df[df["condition"] == "cgp"]["scope_drift_count"].sum()),
            "wilcoxon": exact_wilcoxon_signed_rank(m1_diff),
            "bootstrap_mean_diff_cgp_minus_baseline": bootstrap_mean_diff(
                pairs, "scope_drift_count_baseline", "scope_drift_count_cgp"
            ),
        },
        "verification_compliance": {
            "baseline_rate": float(df[df["condition"] == "baseline"]["verification_compliance"].mean()),
            "cgp_rate": float(df[df["condition"] == "cgp"]["verification_compliance"].mean()),
            "mcnemar": mcnemar(pairs, "verification_compliance"),
            "bootstrap_mean_diff_cgp_minus_baseline": bootstrap_mean_diff(
                pairs, "verification_compliance_baseline", "verification_compliance_cgp"
            ),
        },
        "verification_success": {
            "baseline_rate": float(df[df["condition"] == "baseline"]["task_success"].mean()),
            "cgp_rate": float(df[df["condition"] == "cgp"]["task_success"].mean()),
            "mcnemar": mcnemar(pairs, "task_success"),
            "bootstrap_mean_diff_cgp_minus_baseline": bootstrap_mean_diff(
                pairs, "task_success_baseline", "task_success_cgp"
            ),
        },
        "reproducibility_variance": variance_summary(df),
    }


def fmt_p(value: float | None) -> str:
    if value is None:
        return "not defined"
    return f"{value:.4f}"


def write_markdown(results: dict[str, object]) -> None:
    lines = [
        "# Registered Analysis Results",
        "",
        "This file reports the preregistered contrasts from the frozen analysis plan using `runs/processed/run_level_metrics.csv`. Exact tests are used where the data are sparse. The primary confirmatory dataset is Claude Code plus Aider; Codex plus Gemini CLI are reported as a companion extension.",
        "",
    ]
    for subset_name in ["primary", "extension", "all_planned"]:
        subset = results[subset_name]
        scope = subset["scope_drift"]
        compliance = subset["verification_compliance"]
        success = subset["verification_success"]
        lines.extend(
            [
                f"## {subset_name.replace('_', ' ').title()}",
                "",
                f"Runs: {subset['run_count']}; paired baseline-CGP comparisons: {subset['pair_count']}.",
                "",
                "### H1 / M1: Scope Drift Count",
                "",
                f"Baseline total scope-drift count: {scope['baseline_total']}. CGP total scope-drift count: {scope['cgp_total']}. Exact paired Wilcoxon two-sided p value: {fmt_p(scope['wilcoxon']['p_two_sided'])}.",
                "",
                "### H3 / M3: Verification-Command Compliance",
                "",
                f"Baseline rate: {compliance['baseline_rate']:.1%}. CGP rate: {compliance['cgp_rate']:.1%}. Exact McNemar two-sided p value: {fmt_p(compliance['mcnemar']['exact_mcnemar_p_two_sided'])}.",
                "",
                "### M5: Verification Success",
                "",
                f"Baseline rate: {success['baseline_rate']:.1%}. CGP rate: {success['cgp_rate']:.1%}. Exact McNemar two-sided p value: {fmt_p(success['mcnemar']['exact_mcnemar_p_two_sided'])}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "The registered H1 scope-drift endpoint does not show a favorable reduction. In the primary dataset, baseline scope drift was zero, so the endpoint was at a floor. Completion, non-submission, and evidence-trio findings remain important operational observations, but they must be reported according to their registered or exploratory status rather than as proof of drift reduction.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    df = pd.read_csv(RUNS)
    results = {
        "primary": analyze_subset("primary", df[df["dataset"] == "primary"]),
        "extension": analyze_subset("extension", df[df["dataset"] == "extension"]),
        "all_planned": analyze_subset("all_planned", df),
        "bootstrap_iterations": BOOTSTRAPS,
        "random_seed": RANDOM_SEED,
    }
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_markdown(results)
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
