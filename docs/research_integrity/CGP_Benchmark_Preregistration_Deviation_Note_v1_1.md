# CGP Drift Reduction Benchmark: Preregistration Deviation Note

**Heart AI Foundation Research Integrity Document**
**Document Type:** Preregistration Deviation Note (appended record, non-destructive)
**Version:** 1.1
**Date:** 2026-05-16
**Principal:** Mobley, D. D., Founder
**OSF Registration:** https://osf.io/fnmg5
**Associated Experiment Design:** `CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`
**Associated Results Document:** `CGP_Drift_Reduction_Benchmark_Results.md` (recorded 2026-05-16)
**Associated Repository:** https://github.com/heart-ai-foundation/cgp-benchmark
**Foundation Relationship:** Open methodology and open benchmark published by the Heart AI Foundation. Commercial implementation services are operated separately by HeartCore Ventures LLC under Heart Foundation Charter v2.4 Section 3.6 (Dual-Entity Boundary Doctrine).

**Validity Condition:** This note fills the transcription fields specified in v1.0 using the repository's OSF preregistration packet, `docs/osf_preregistration/OSF_PREREGISTRATION.md`, which was prepared for the frozen OSF registration at https://osf.io/fnmg5. It is an evidentiary deviation note for repository and manuscript use. If the public OSF-rendered registration text differs from the repository packet, the OSF-rendered text controls and this note must be corrected in a later version.

---

## 1. Purpose

This note records, without altering the original registration, the relationship between the preregistered analysis plan for the Continuity-Governed Prompting (CGP) Drift Reduction Benchmark and the results obtained in the first processed analysis. It exists to discharge a research-integrity obligation and a commercial-claims obligation simultaneously.

The research-integrity obligation: a preregistered experiment whose registered primary endpoint did not move must say so plainly, in a record attached to the registration, before any downstream artifact characterizes the experiment as successful.

The commercial-claims obligation: HeartCore Ventures LLC's Service Offer v1.1 Section 3.1 cites the Foundation's preregistered benchmark experiment as the empirical basis for stating that workflow drift reduction is the methodology's design intent with testing in progress. Section 3.6 of that same document requires that quantitative claims trace to published evidence. This note is the evidence record that the citation must resolve to, and it must be honest enough that a technically literate reader following the citation reaches the same conclusion the Foundation reached.

This note does not change the methodology. It does not change the registration. It does not add or rerun experiments. It classifies what was found against what was registered.

---

## 2. The Registered Design

The following fields are transcribed from the OSF preregistration packet stored in `docs/osf_preregistration/OSF_PREREGISTRATION.md`.

> **Registered primary hypothesis:**
>
> H1, the primary hypothesis, is that CGP reduces scope drift in agent-assisted coding workflows compared to ordinary summary-based prompting.

> **Registered primary endpoint and its operational definition:**
>
> Primary metrics are:
>
> M1, scope drift count, defined as the number of files modified outside the allowed-files set per run.
>
> M2, reproducibility variance, defined as variance in scope drift, completion success, and files touched across three replications of each task-agent-condition cell.
>
> M3, verification-command compliance, defined as whether the agent executed the named verification command before declaring completion.

The preregistration packet does not define composite run validity as a primary endpoint. It defines inclusion and exclusion as follows:

> A run is included if it starts from the correct task tag, uses the assigned condition prompt, and reaches a declared completion or stop condition.
>
> A run is excluded or flagged if the repository cannot be reset cleanly, the agent platform changes materially mid-run, required verification cannot run for environmental reasons unrelated to the agent output, or the condition prompt is accidentally mixed with the other condition. Exclusions and flags will be documented in the run record and final report.

> **Registered secondary or exploratory endpoints, if any:**
>
> The CGP-only scaffold adherence metric is M4, evidence trio completeness, scored 0 to 3 based on structural presence of design note, run record, and evidence JSON.
>
> Secondary metrics are M5, task verification success, and M8, human correction burden.
>
> Exploratory metrics are M6, token cost per task; M7, wall-clock time per task; M9, clarification loops; M10, retry attempts; and M11, unauthorized file access if telemetry supports it.

Work submission and composite run validity are not named as registered primary, secondary, or exploratory endpoints in the preregistration packet. They are operational analysis fields derived from run capture and should be reported as observed operational findings rather than confirmatory preregistered endpoints.

> **Registered analysis population and sample plan:**
>
> The experiment has four factors.
>
> Condition has two levels: baseline summary-based prompting and CGP via the Next-Prompt Protocol scaffold.
>
> Agent platform has two levels: Claude Code and Aider.
>
> Task has six levels: input validation, user docstring, user-items endpoint, parse-config refactor, favorite-items feature, and LoginForm empty-password bug fix.
>
> Replication has three levels per task, condition, and agent cell.
>
> The study uses 72 total runs:
>
> 6 tasks x 2 conditions x 2 agents x 3 replications.
>
> This is an initial controlled benchmark, not a full-scale field validation.

The companion extension using Codex and Gemini CLI is not part of the primary preregistered confirmatory dataset described in the core OSF preregistration packet. It is treated as a companion extension in downstream analysis.

> **Registered analysis plan and any registered inferential tests:**
>
> For M1, paired Wilcoxon signed-rank tests will compare Baseline and CGP conditions.
>
> For M3 and M5, McNemar's test will compare paired binary outcomes.
>
> For M2, variance ratios will compare reproducibility across conditions by task and agent cell.
>
> Effect sizes and 95 percent bootstrapped confidence intervals will be reported. The significance threshold is alpha = 0.05 with Bonferroni correction for the three primary hypotheses.
>
> M4 will be reported only within the CGP condition to characterize scaffold adherence and flag partial-compliance runs.
>
> M6 through M11 will be reported descriptively as exploratory metrics and will not be used for primary hypothesis testing.

What is independently established by the results document, and therefore stated here without transcription, is the dataset partition the analysis used. The processed analysis treats Claude Code and Aider as the primary preregistered dataset (72 runs, 36 baseline and 36 CGP) and Codex and Gemini CLI as a companion extension dataset (72 runs, 36 baseline and 36 CGP). Eight harness-defect records were archived and excluded from planned-run analysis. Any claim about whether the companion extension was registered as confirmatory, registered as exploratory, or added after registration must be resolved against the transcription fields above and must not be inferred from the results document alone.

---

## 3. Observed Result Against the Registered Primary Endpoint

The registered primary endpoint concerns scope drift. The observed scope-drift incidence was:

- Baseline prompting: 1 invalid run attributable to scope drift, out of 72 baseline runs.
- Continuity-Governed Prompting: 1 invalid run attributable to scope drift, out of 72 CGP runs.

The single baseline scope-drift event occurred in the companion extension dataset (Gemini CLI, a run that drifted into `benchmark-repo/tests/test_config.py`). It did not occur in the primary preregistered dataset. Within the primary preregistered dataset (Claude Code and Aider), Claude Code completed all baseline and CGP runs validly, and Aider's invalid baseline runs were driven by non-submission rather than by scope drift.

The consequence is direct and must be stated without softening. Baseline scope-drift incidence in the preregistered primary dataset was at or near zero. An endpoint defined as the reduction of an event that did not meaningfully occur under the baseline condition cannot register a reduction. The registered primary endpoint returned a null result, and the null is a floor effect rather than evidence that CGP fails to reduce drift. The benchmark, as registered, lacked the conditions required to test its registered primary hypothesis.

---

## 4. Floor Effect: Why the Primary Endpoint Was Untestable as Registered

A reduction effect is only measurable when the quantity to be reduced occurs at a non-trivial rate in the comparison condition. Scope drift did not. Across 72 baseline runs spanning four agent platforms, exactly one run failed through scope drift, and that run was outside the preregistered primary dataset. The preregistered primary dataset recorded no baseline scope-drift failures of the kind the endpoint was written to detect.

This is a benchmark design limitation, not an analysis error and not a methodology failure. The agent platforms and task set selected for the preregistered dataset did not induce baseline scope drift at a detectable rate. Two of the four platforms (Claude Code, Codex) operated at ceiling validity in both conditions. A third (Gemini CLI) was near ceiling. Only one platform (Aider) showed condition-sensitive variation, and that variation occurred through a different failure mode entirely.

A future benchmark intended to test the registered drift hypothesis would require tasks and conditions engineered so that baseline scope drift occurs at a rate high enough to permit detection of a reduction. That work is out of scope for this note and must not be conflated with the present registration. The present registration's primary endpoint stands as null at the floor.

---

## 5. Observed Findings and Their Epistemic Status

The processed analysis surfaced effects on endpoints other than scope drift. Their evidentiary weight depends entirely on whether they were registered, which is resolved by the transcription fields in Section 2.

The observed effects, stated as found:

- Composite run validity rose from 56 of 72 baseline runs (77.8%) to 68 of 72 CGP runs (94.4%) across all four platforms.
- Within the preregistered primary dataset, composite run validity rose from 21 of 36 (58.3%) to 32 of 36 (88.9%).
- The primary-dataset contrast was concentrated in a single platform. Aider baseline runs were valid in 3 of 18 cases; Aider CGP runs were valid in 14 of 18 cases. Claude Code operated at ceiling in both conditions.
- Work submission rose from 79.2% under baseline to 100.0% under CGP. The dominant baseline failure mode was non-submission, an agent completing without changing files, which ordinary verification commands do not detect.
- Verification success was 100.0% under baseline and 95.8% under CGP, a small movement in the unfavorable direction that must be reported, not omitted.
- Evidence-trio completeness under CGP was 71 of 72 (98.6%) overall, 35 of 36 in the primary dataset, and 36 of 36 in the companion extension.

Epistemic-status determination:

- Scope drift count (M1) is the registered primary endpoint for H1. It returned a null result at a baseline floor in the primary preregistered dataset.
- Verification-command compliance (M3) is a registered primary metric for H3. In the primary dataset, baseline compliance was 100.0%, CGP compliance was 91.7%, and the exact McNemar two-sided p value was 0.2500.
- Task verification success (M5) is a registered secondary metric. In the primary dataset, baseline success was 100.0%, CGP success was 91.7%, and the exact McNemar two-sided p value was 0.2500.
- Evidence-trio completeness (M4) is a registered CGP-only scaffold adherence metric. It should be reported within the CGP condition, not as a between-condition effect.
- Work submission, non-submission, and composite run validity are not named as registered endpoints in the preregistration packet. They may be reported as observed operational findings and as motivation for future confirmatory work, but not as confirmatory evidence that the registered drift hypothesis succeeded.

The registered analysis has now been run and attached in `runs/processed/registered_analysis.md` and `runs/processed/registered_analysis.json`. Any inferential claim should resolve to those files or to a later corrected analysis file.

---

## 6. Impact on Claims

With Section 2 transcribed and Section 5 status fixed, the following claim positions hold.

**Defensible now:**

- The CGP methodology's design intent includes workflow drift reduction. This is a statement of design intent and is not contingent on the benchmark.
- A preregistered benchmark of the drift hypothesis was conducted, returned a null result on the registered primary endpoint due to a baseline floor effect, and the floor effect is documented.
- The benchmark produced an observed improvement in valid task completion and in evidence-trail completeness, concentrated in a baseline-unreliable agent platform. Composite run validity and work submission are operational findings, not confirmatory registered endpoints.

**Not defensible and prohibited until corrected:**

- Any statement that CGP "passed the benchmark," "reduced drift," or was "validated" by this experiment.
- Any quantitative completion, reliability, or auditability figure presented as a confirmatory registered endpoint for this benchmark.
- Any citation, in Service Offer v1.1 Section 3.1 or in `CGP_Foundation_Publication_Brief_v1_1.md` Section 8 or in customer-facing benchmark-suite material, that resolves to a drift-reduction result this experiment did not produce.

The reconciliation of Service Offer v1.1 Section 3.1, Service Offer v1.1 Section 3.4 acceptable-language examples, and `CGP_Foundation_Publication_Brief_v1_1.md` Section 8 against this note is specified in the companion Changes Note and is not duplicated here. The Foundation Publication Brief is referenced but not characterized in this note, because its current claims-boundary text has not been read into this record.

---

## 7. Chain of Custody and Integrity Statement

The OSF registration at https://osf.io/fnmg5 is not modified by this note. The registration remains the frozen statement of what was planned. This note is an appended, separately versioned record of how the executed analysis relates to that frozen plan.

The processed analysis artifacts under `runs/processed/` and the run-level records under `runs/raw/` (including the eight archived harness-defect records under `runs/raw/invalid/`) are the underlying evidence and are not altered by this note. Corrections to interpretation and to downstream documents are made in the documents themselves and in the companion Changes Note, never by editing the registration or the raw records.

This note is authored by the principal, who is also the methodology author and the founder of both the Heart AI Foundation and HeartCore Ventures LLC. That concurrence of roles is the precise reason this note exists and is written to a forensic standard rather than a promotional one. The Dual-Entity Boundary requires that the Foundation's evidence record be honest independent of any commercial interest in the outcome, and that the commercial entity cite the Foundation record rather than generate a parallel one.

---

## 8. Falsifiability Position

This note strengthens rather than weakens the program. The Next-Prompt Protocol Implementation Guide states the falsifiable claim plainly: a functioning scaffold should either prevent drift or make drift visible, and if it does neither it is only documentation. The present benchmark could not test prevention because baseline drift did not occur at a measurable rate. It did produce evidence relevant to visibility and to valid completion. Recording the null on the registered endpoint, rather than absorbing it into a favorable summary, is the behavior the falsifiability commitment requires. A program that reports its floor effects is more credible than one that does not, and credibility is the asset the associated services are built to sell.

---

## 9. Remaining Required Actions

1. Attach or link this v1.1 note from the OSF registration page as an associated deviation record.
2. Ensure the results document, customer-facing benchmark artifact, Foundation Publication Brief, and Service Offer resolve to this v1.1 record rather than to an unqualified drift-reduction claim.
3. If the public OSF-rendered registration text differs from the repository packet transcribed here, issue a v1.2 correction using the OSF-rendered text as controlling evidence.

---

*© 2026 The Heart AI Foundation. All Rights Reserved.*
*Author: Mobley, D. D. | Published under CC BY 4.0*
*The Heart AI Foundation™ — CGP Drift Reduction Benchmark: Preregistration Deviation Note v1.1*
*heartaifoundation.org*
