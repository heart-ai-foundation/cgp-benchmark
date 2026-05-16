#!/usr/bin/env python3
"""Build a preprint PDF from the CGP benchmark manuscript assets."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs" / "paper"
FIGURES = PAPER / "figures"
TABLES = PAPER / "tables"
OUT = PAPER / "preprint"
TEX = OUT / "cgp_reliability_auditability_preprint.tex"
PDF = OUT / "cgp_reliability_auditability_preprint.pdf"


CITATIONS = {
    "jimenez2023swebench": "Jimenez et al., 2023",
    "yang2024sweagent": "Yang et al., 2024",
    "swegym2024": "Pan et al., 2024",
    "chan2024mlebench": "Chan et al., 2024",
    "liu2023agentbench": "Liu et al., 2023",
    "yao2022react": "Yao et al., 2022",
    "shinn2023reflexion": "Shinn et al., 2023",
    "schick2023toolformer": "Schick et al., 2023",
}


REFERENCES = [
    r"Chan, J. S., Chowdhury, N., Jaffe, O., Aung, J., Sherburn, D., Mays, E., Starace, G., Liu, K., Maksin, L., Patwardhan, T., Weng, L., \& Mądry, A. (2024). \textit{MLE-bench: Evaluating machine learning agents on machine learning engineering}. arXiv:2410.07095. \url{https://arxiv.org/abs/2410.07095}",
    r"Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., \& Narasimhan, K. (2023). \textit{SWE-bench: Can language models resolve real-world GitHub issues?} arXiv:2310.06770. \url{https://arxiv.org/abs/2310.06770}",
    r"Liu, X., Yu, H., Zhang, H., Xu, Y., Lei, X., Lai, H., Gu, Y., Ding, H., Men, K., Yang, K., Zhang, S., Deng, X., Zeng, A., Du, Z., Zhang, C., Shen, S., Zhang, T., Su, Y., Sun, H., Huang, M., Dong, Y., \& Tang, J. (2023). \textit{AgentBench: Evaluating LLMs as agents}. arXiv:2308.03688. \url{https://arxiv.org/abs/2308.03688}",
    r"Pan, J., Wang, X., Neubig, G., Jaitly, N., Ji, H., Suhr, A., \& Zhang, Y. (2024). \textit{Training software engineering agents and verifiers with SWE-Gym}. arXiv:2412.21139. \url{https://arxiv.org/abs/2412.21139}",
    r"Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., \& Scialom, T. (2023). \textit{Toolformer: Language models can teach themselves to use tools}. arXiv:2302.04761. \url{https://arxiv.org/abs/2302.04761}",
    r"Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., \& Yao, S. (2023). \textit{Reflexion: Language agents with verbal reinforcement learning}. arXiv:2303.11366. \url{https://arxiv.org/abs/2303.11366}",
    r"Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., \& Press, O. (2024). \textit{SWE-agent: Agent-computer interfaces enable automated software engineering}. arXiv:2405.15793. \url{https://arxiv.org/abs/2405.15793}",
    r"Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., \& Cao, Y. (2022). \textit{ReAct: Synergizing reasoning and acting in language models}. arXiv:2210.03629. \url{https://arxiv.org/abs/2210.03629}",
]


SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex_escape(text: str) -> str:
    return "".join(SPECIAL.get(char, char) for char in text)


def format_inline(text: str) -> str:
    def citation(match: re.Match[str]) -> str:
        keys = [part.strip().lstrip("@") for part in match.group(1).split(";")]
        return "(" + "; ".join(CITATIONS.get(key, key) for key in keys) + ")"

    pieces: list[str] = []
    last = 0
    pattern = re.compile(r"`([^`]+)`|\[(@[^]]+)\]")
    for match in pattern.finditer(text):
        pieces.append(tex_escape(text[last : match.start()]))
        if match.group(1) is not None:
            pieces.append(r"\texttt{" + tex_escape(match.group(1)) + "}")
        else:
            keys = [part.strip().lstrip("@") for part in match.group(2).split(";")]
            pieces.append("(" + "; ".join(CITATIONS.get(key, key) for key in keys) + ")")
        last = match.end()
    pieces.append(tex_escape(text[last:]))
    return "".join(pieces)


def paragraphize(lines: list[str]) -> list[str]:
    out: list[str] = []
    para: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if para:
                out.append(format_inline(" ".join(para)))
                out.append("")
                para = []
            continue
        if line.startswith("|"):
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            if para:
                out.append(format_inline(" ".join(para)))
                out.append("")
                para = []
            heading = line[3:].strip()
            if heading == "Abstract":
                out.append(r"\section*{" + tex_escape(heading) + "}")
            elif heading == "Figures and Tables":
                continue
            elif heading == "References":
                continue
            else:
                out.append(r"\section{" + tex_escape(heading) + "}")
            continue
        if line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("affiliation:") or line.startswith("date:") or line.startswith("bibliography:") or line.startswith("repository:") or line.startswith("osf_registration:") or line.startswith("  - "):
            continue
        para.append(line)
    if para:
        out.append(format_inline(" ".join(para)))
        out.append("")
    return out


def read_main_body() -> list[str]:
    text = (PAPER / "preprint_manuscript.md").read_text(encoding="utf-8")
    body_lines = text.splitlines()
    start = next((idx for idx, line in enumerate(body_lines) if line.strip() == "## Abstract"), 0)
    # Stop before the source manuscript's collection block; this builder places displays inline.
    stop = next((idx for idx, line in enumerate(body_lines) if line.strip() == "## Figures and Tables"), len(body_lines))
    return place_displays_inline(paragraphize(body_lines[start:stop]))


def convert_svg(name: str) -> str:
    source = FIGURES / f"{name}.svg"
    target = OUT / f"{name}.pdf"
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(target), str(source)], check=True)
    return target.name


def copy_png(name: str) -> str:
    source = FIGURES / f"{name}.png"
    target = OUT / source.name
    shutil.copy2(source, target)
    return target.name


def latex_table_from_markdown(path: Path, caption: str, label: str) -> str:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = []
    for idx, line in enumerate(lines):
        if idx == 1:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(cells)
    header, body = rows[0], rows[1:]
    colspec = "l" * len(header)
    tex = [r"\begin{table}[H]", r"\centering", r"\small", r"\resizebox{\textwidth}{!}{%", rf"\begin{{tabular}}{{{colspec}}}", r"\toprule"]
    tex.append(" & ".join(tex_escape(cell) for cell in header) + r" \\")
    tex.append(r"\midrule")
    for row in body:
        tex.append(" & ".join(tex_escape(cell) for cell in row) + r" \\")
    tex.extend([r"\bottomrule", r"\end{tabular}%", r"}", rf"\caption{{{tex_escape(caption)}}}", rf"\label{{{label}}}", r"\end{table}"])
    return "\n".join(tex)


def latex_figure(filename: str, caption: str, *, width: str = r"\textwidth", numbered: bool = True) -> str:
    caption_command = "caption" if numbered else "caption*"
    return "\n".join(
        [
            r"\begin{figure}[H]\centering",
            rf"\includegraphics[width={width}]{{{filename}}}",
            rf"\{caption_command}{{{caption}}}",
            r"\end{figure}",
        ]
    )


def display_blocks() -> dict[str, str]:
    pipeline = convert_svg("figure1_benchmark_pipeline")
    validity = copy_png("figure2_validity_by_agent_condition")
    failures = copy_png("figure3_invalid_run_mechanisms")
    return {
        "pipeline": latex_figure(
            pipeline,
            r"Benchmark run-capture pipeline. Each benchmark run began with a task specification containing allowed files and verification commands, then proceeded through either a baseline prompt or a CGP prompt that added manifest, lock, stop-condition, and evidence-trio requirements. Runs were executed in isolated git worktrees, captured as transcripts and diffs, and scored into run-level metrics. CGP evidence files were treated as allowed operational evidence when computing scope drift.",
            width=r"0.92\textwidth",
        ),
        "validity": latex_figure(
            validity,
            r"Operational run validity by agent and prompt condition. Bars show the proportion of runs classified as valid under the operational composite endpoint for each agent platform and prompt condition. This figure should not be interpreted as the registered primary drift endpoint; registered scope drift was analyzed separately and returned a null result at a baseline floor.",
            width=r"0.86\textwidth",
        ),
        "failures": latex_figure(
            failures,
            r"Invalid-run mechanisms by agent and prompt condition. Bars count invalid planned runs by observed failure mechanism. The dominant failure mode was non-submission in Aider baseline runs, where the agent completed without changing files while repository verification still passed.",
            width=r"0.86\textwidth",
        ),
        "table1": latex_table_from_markdown(TABLES / "table1_summary_by_dataset_agent_condition.md", "Summary by dataset, agent, and condition.", "tab:summary"),
        "table2": latex_table_from_markdown(TABLES / "table2_invalid_run_mechanisms.md", "Invalid-run mechanisms.", "tab:failures"),
    }


def place_displays_inline(body: list[str]) -> list[str]:
    displays = display_blocks()
    out: list[str] = []
    inserted = {key: False for key in displays}

    for line in body:
        out.append(line)
        if "Figure 1" in line and not inserted["pipeline"]:
            out.extend(["", displays["pipeline"], ""])
            inserted["pipeline"] = True
        if "Table 1" in line and "Figure 2" in line and not inserted["table1"]:
            out.extend(["", displays["table1"], "", displays["validity"], ""])
            inserted["table1"] = True
            inserted["validity"] = True
        if "Table 2" in line and "Figure 3" in line and not inserted["table2"]:
            out.extend(["", displays["table2"], "", displays["failures"], ""])
            inserted["table2"] = True
            inserted["failures"] = True

    return out


def render_tex() -> str:
    body = "\n".join(read_main_body())
    refs = "\n".join(rf"\item {ref}" for ref in REFERENCES)
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{hyperref}}
\usepackage{{float}}
\usepackage{{caption}}
\setmainfont{{TeX Gyre Pagella}}
\emergencystretch=3em
\sloppy
\hypersetup{{colorlinks=true, linkcolor=blue, urlcolor=blue, citecolor=blue}}
\title{{Reliability and Auditability Effects of Continuity-Governed Prompting: A Controlled Benchmark of Agent-Assisted Coding Workflows}}
\author{{Dylan D. Mobley\\Heart AI Foundation}}
\date{{May 16, 2026}}
\begin{{document}}
\maketitle

\noindent Repository: \url{{https://github.com/heart-ai-foundation/cgp-benchmark}}\\
OSF registration: \url{{https://osf.io/fnmg5}}\\
Zenodo DOI: \url{{https://doi.org/10.5281/zenodo.20234367}}\\
ORCID: \url{{https://orcid.org/0009-0002-3560-3955}}

{body}

\clearpage
\section*{{References}}
\begin{{enumerate}}
{refs}
\end{{enumerate}}

\end{{document}}
"""


def build_pdf() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TEX.write_text(render_tex(), encoding="utf-8")
    for _ in range(2):
        subprocess.run(["xelatex", "-interaction=nonstopmode", TEX.name], cwd=OUT, check=True)
    print(PDF)


if __name__ == "__main__":
    build_pdf()
