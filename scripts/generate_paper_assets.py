#!/usr/bin/env python3
"""Generate manuscript tables and figures from processed benchmark metrics."""

from __future__ import annotations

from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", ".matplotlib-cache")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams["svg.hashsalt"] = "cgp-benchmark-paper-assets"

PROCESSED = Path("runs/processed")
PAPER = Path("docs/paper")
TABLES = PAPER / "tables"
FIGURES = PAPER / "figures"


def pct(value: float | str) -> str:
    if value == "" or pd.isna(value):
        return "n/a"
    return f"{float(value) * 100:.1f}%"


def write_markdown_table(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(df.to_markdown(index=False) + "\n", encoding="utf-8")


def make_tables() -> None:
    summary = pd.read_csv(PROCESSED / "summary_by_dataset_agent_condition.csv")
    table1 = summary[
        [
            "dataset",
            "agent",
            "condition",
            "n",
            "valid_n",
            "valid_rate",
            "work_submitted_rate",
            "task_success_rate",
            "scope_drift_any_rate",
            "evidence_trio_complete_rate",
        ]
    ].copy()
    table1.columns = [
        "Dataset",
        "Agent",
        "Condition",
        "n",
        "Valid n",
        "Valid rate",
        "Work submitted",
        "Task success",
        "Scope drift any",
        "Evidence trio complete",
    ]
    for column in ["Valid rate", "Work submitted", "Task success", "Scope drift any", "Evidence trio complete"]:
        table1[column] = table1[column].apply(pct)
    write_markdown_table(TABLES / "table1_summary_by_dataset_agent_condition.md", table1)

    runs = pd.read_csv(PROCESSED / "run_level_metrics.csv").fillna("")
    invalid = runs[runs["run_validity"] == "invalid"].copy()
    invalid["Failure mechanism"] = invalid.apply(classify_failure, axis=1)
    table2 = (
        invalid.groupby(["dataset", "agent", "condition", "Failure mechanism"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["dataset", "agent", "condition", "Failure mechanism"])
    )
    table2.columns = ["Dataset", "Agent", "Condition", "Failure mechanism", "n"]
    write_markdown_table(TABLES / "table2_invalid_run_mechanisms.md", table2)


def classify_failure(row: pd.Series) -> str:
    if int(row.get("work_submitted") or 0) == 0:
        return "No work submitted"
    if int(row.get("scope_drift_any") or 0) == 1:
        return "Scope drift"
    if int(row.get("task_success") or 0) == 0:
        return "Verification failure"
    if row.get("condition") == "cgp" and str(row.get("evidence_trio_complete")) not in {"1", "1.0"}:
        return "Evidence incomplete"
    return "Other invalid"


def save_figure(path_base: Path) -> None:
    path_base.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path_base.with_suffix(".png"), dpi=220, metadata={"Software": "cgp-benchmark"})
    plt.savefig(path_base.with_suffix(".svg"), metadata={"Date": None})
    plt.close()


def make_validity_figure() -> None:
    summary = pd.read_csv(PROCESSED / "summary_by_dataset_agent_condition.csv")
    summary["Agent"] = summary["agent"].replace({"claude-code": "Claude Code", "gemini-cli": "Gemini CLI"})
    summary["Condition"] = summary["condition"].replace({"baseline": "Baseline", "cgp": "CGP"})
    summary["Valid rate (%)"] = summary["valid_rate"] * 100

    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(data=summary, x="Agent", y="Valid rate (%)", hue="Condition", palette=["#6B7280", "#2563EB"])
    ax.set_ylim(0, 105)
    ax.set_xlabel("")
    ax.set_ylabel("Valid runs (%)")
    ax.set_title("Run validity by agent and prompt condition")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", padding=3, fontsize=10)
    save_figure(FIGURES / "figure2_validity_by_agent_condition")


def make_failure_figure() -> None:
    runs = pd.read_csv(PROCESSED / "run_level_metrics.csv").fillna("")
    invalid = runs[runs["run_validity"] == "invalid"].copy()
    invalid["Agent"] = invalid["agent"].replace({"claude-code": "Claude Code", "gemini-cli": "Gemini CLI"})
    invalid["Condition"] = invalid["condition"].replace({"baseline": "Baseline", "cgp": "CGP"})
    invalid["Failure mechanism"] = invalid.apply(classify_failure, axis=1)
    counts = invalid.groupby(["Agent", "Condition", "Failure mechanism"]).size().reset_index(name="n")

    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(13, 7))
    ax = sns.barplot(data=counts, x="Agent", y="n", hue="Failure mechanism")
    ax.set_xlabel("")
    ax.set_ylabel("Invalid run count")
    ax.set_title("Invalid run mechanisms")
    save_figure(FIGURES / "figure3_invalid_run_mechanisms")


def make_pipeline_svg() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="420" viewBox="0 0 1400 420">
  <style>
    .box { fill: #f8fafc; stroke: #1f2937; stroke-width: 2; rx: 12; }
    .cgp { fill: #dbeafe; stroke: #1d4ed8; stroke-width: 2; rx: 12; }
    .text { font-family: Arial, sans-serif; font-size: 24px; fill: #111827; text-anchor: middle; }
    .small { font-family: Arial, sans-serif; font-size: 18px; fill: #374151; text-anchor: middle; }
    .arrow { stroke: #111827; stroke-width: 3; marker-end: url(#arrowhead); }
  </style>
  <defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#111827"/></marker></defs>
  <rect class="box" x="40" y="120" width="190" height="120"/>
  <text class="text" x="135" y="165">Task spec</text><text class="small" x="135" y="200">allowed files</text>
  <line class="arrow" x1="230" y1="180" x2="310" y2="180"/>
  <rect class="cgp" x="310" y="90" width="230" height="180"/>
  <text class="text" x="425" y="140">Prompt condition</text><text class="small" x="425" y="178">baseline or CGP</text><text class="small" x="425" y="210">manifest + lock</text><text class="small" x="425" y="242">evidence trio</text>
  <line class="arrow" x1="540" y1="180" x2="620" y2="180"/>
  <rect class="box" x="620" y="120" width="190" height="120"/>
  <text class="text" x="715" y="165">Agent run</text><text class="small" x="715" y="200">isolated worktree</text>
  <line class="arrow" x1="810" y1="180" x2="890" y2="180"/>
  <rect class="box" x="890" y="120" width="190" height="120"/>
  <text class="text" x="985" y="165">Capture</text><text class="small" x="985" y="200">diff + transcript</text>
  <line class="arrow" x1="1080" y1="180" x2="1160" y2="180"/>
  <rect class="box" x="1160" y="90" width="200" height="180"/>
  <text class="text" x="1260" y="140">Metrics</text><text class="small" x="1260" y="178">validity</text><text class="small" x="1260" y="210">drift</text><text class="small" x="1260" y="242">verification</text>
</svg>
"""
    (FIGURES / "figure1_benchmark_pipeline.svg").write_text(svg, encoding="utf-8")


def make_graphical_abstract_svg() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650" viewBox="0 0 1400 650">
  <style>
    .title { font-family: Arial, sans-serif; font-size: 34px; font-weight: 700; fill: #111827; text-anchor: middle; }
    .label { font-family: Arial, sans-serif; font-size: 25px; font-weight: 700; fill: #111827; text-anchor: middle; }
    .body { font-family: Arial, sans-serif; font-size: 19px; fill: #374151; text-anchor: middle; }
    .metric { font-family: Arial, sans-serif; font-size: 44px; font-weight: 700; fill: #1d4ed8; text-anchor: middle; }
    .box { fill: #f8fafc; stroke: #1f2937; stroke-width: 2; rx: 14; }
    .cgp { fill: #dbeafe; stroke: #1d4ed8; stroke-width: 3; rx: 14; }
    .baseline { fill: #f3f4f6; stroke: #4b5563; stroke-width: 2; rx: 14; }
    .accent { fill: #ecfdf5; stroke: #047857; stroke-width: 2; rx: 14; }
    .warn { fill: #fff7ed; stroke: #c2410c; stroke-width: 2; rx: 14; }
    .arrow { stroke: #111827; stroke-width: 3; marker-end: url(#arrowhead); }
  </style>
  <defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#111827"/></marker></defs>
  <rect width="1400" height="650" fill="#ffffff"/>
  <text class="title" x="700" y="60">Continuity-Governed Prompting: Reliability and Auditability Benchmark</text>

  <rect class="box" x="50" y="150" width="255" height="170"/>
  <text class="label" x="177.5" y="198">Controlled Tasks</text>
  <text class="body" x="177.5" y="236">6 coding tasks</text>
  <text class="body" x="177.5" y="266">allowed files</text>
  <text class="body" x="177.5" y="296">verification commands</text>

  <line class="arrow" x1="305" y1="235" x2="375" y2="235"/>

  <rect class="baseline" x="375" y="115" width="250" height="115"/>
  <text class="label" x="500" y="158">Baseline</text>
  <text class="body" x="500" y="194">ordinary task prompt</text>
  <rect class="cgp" x="375" y="255" width="250" height="145"/>
  <text class="label" x="500" y="298">CGP</text>
  <text class="body" x="500" y="334">manifest, lock, non-goals</text>
  <text class="body" x="500" y="364">stop rules, evidence trio</text>

  <line class="arrow" x1="625" y1="235" x2="695" y2="235"/>

  <rect class="box" x="695" y="150" width="255" height="170"/>
  <text class="label" x="822.5" y="198">144 Runs</text>
  <text class="body" x="822.5" y="236">4 agent platforms</text>
  <text class="body" x="822.5" y="266">isolated git worktrees</text>
  <text class="body" x="822.5" y="296">diff + transcript capture</text>

  <line class="arrow" x1="950" y1="235" x2="1020" y2="235"/>

  <rect class="accent" x="1020" y="110" width="330" height="250"/>
  <text class="label" x="1185" y="155">Observed Reliability</text>
  <text class="body" x="1185" y="193">valid completed runs</text>
  <text class="metric" x="1185" y="255">77.8% to 94.4%</text>
  <text class="body" x="1185" y="296">baseline to CGP, all agents</text>
  <text class="body" x="1185" y="326">primary: 58.3% to 88.9%</text>

  <rect class="warn" x="175" y="460" width="1050" height="105"/>
  <text class="label" x="700" y="500">Main Mechanism</text>
  <text class="body" x="700" y="538">Registered drift endpoint was null at floor; CGP improved task engagement and evidence completeness.</text>
</svg>
"""
    (FIGURES / "graphical_abstract.svg").write_text(svg, encoding="utf-8")


def main() -> int:
    make_tables()
    make_validity_figure()
    make_failure_figure()
    make_pipeline_svg()
    make_graphical_abstract_svg()
    print(f"wrote tables to {TABLES}")
    print(f"wrote figures to {FIGURES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
