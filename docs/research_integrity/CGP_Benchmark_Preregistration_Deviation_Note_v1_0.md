# CGP Drift Reduction Benchmark: Preregistration Deviation Note

**Heart AI Foundation Research Integrity Document**
**Document Type:** Preregistration Deviation Note (appended record, non-destructive)
**Version:** 1.0
**Date:** 2026-05-16
**Principal:** Mobley, D. D., Founder
**OSF Registration:** https://osf.io/fnmg5
**Associated Experiment Design:** `CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`
**Associated Results Document:** `CGP_Drift_Reduction_Benchmark_Results.md` (recorded 2026-05-16)
**Associated Repository:** https://github.com/heart-ai-foundation/cgp-benchmark
**Foundation Relationship:** Open methodology and open benchmark published by the Heart AI Foundation. Commercial implementation services are operated separately by HeartCore Ventures LLC under Heart Foundation Charter v2.4 Section 3.6 (Dual-Entity Boundary Doctrine).

**Validity Condition:** This note is structurally complete but not yet evidentiary. It contains marked transcription fields that must be populated verbatim from the OSF registration record at https://osf.io/fnmg5 before the note is cited as an authoritative record. A deviation note that reconstructs a registration from memory is not a deviation note. The transcription fields are the load-bearing content. Until they are filled from the frozen registration, treat this document as a draft instrument.

---

## 1. Purpose

This note records, without altering the original registration, the relationship between the preregistered analysis plan for the Continuity-Governed Prompting (CGP) Drift Reduction Benchmark and the results obtained in the first processed analysis. It exists to discharge a research-integrity obligation and a commercial-claims obligation simultaneously.

The research-integrity obligation: a preregistered experiment whose registered primary endpoint did not move must say so plainly, in a record attached to the registration, before any downstream artifact characterizes the experiment as successful.

The commercial-claims obligation: HeartCore Ventures LLC's Service Offer v1.1 Section 3.1 cites the Foundation's preregistered benchmark experiment as the empirical basis for stating that workflow drift reduction is the methodology's design intent with testing in progress. Section 3.6 of that same document requires that quantitative claims trace to published evidence. This note is the evidence record that the citation must resolve to, and it must be honest enough that a technically literate reader following the citation reaches the same conclusion the Foundation reached.

This note does not change the methodology. It does not change the registration. It does not add or rerun experiments. It classifies what was found against what was registered.

---

## 2. The Registered Design

The following fields must be transcribed verbatim from the frozen OSF registration at https://osf.io/fnmg5. Do not paraphrase. Do not summarize. Copy the registered text exactly, including any registered ambiguity.

> **[TRANSCRIBE VERBATIM. Registered primary hypothesis:]**
> _<insert the exact registered primary hypothesis statement>_

> **[TRANSCRIBE VERBATIM. Registered primary endpoint and its operational definition:]**
> _<insert the exact registered primary endpoint, including how scope drift was operationally defined and how a run was scored valid or invalid>_

> **[TRANSCRIBE VERBATIM. Registered secondary or exploratory endpoints, if any:]**
> _<insert any registered secondary endpoints exactly as registered, including work submission, verification success, and evidence-trio completeness if and only if they appear in the registration; if they do not appear, state "Not registered" here>_

> **[TRANSCRIBE VERBATIM. Registered analysis population and sample plan:]**
> _<insert the exact registered analysis set, the registered agent platforms, the registered run counts, and any registered rule distinguishing a primary preregistered dataset from a companion or extension dataset>_

> **[TRANSCRIBE VERBATIM. Registered analysis plan and any registered inferential tests:]**
> _<insert the registered statistical or descriptive analysis plan exactly as registered, including any registered test, effect size, or interval reporting>_

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

Epistemic-status determination, to be completed against Section 2:

- **If work submission, non-submission, verification success, or evidence-trio completeness were registered as secondary endpoints:** report them as preregistered secondary findings, subject to the registered analysis plan, and apply any registered correction for multiple endpoints.
- **If they were not registered:** report them as exploratory findings, label every downstream use of them as exploratory, and state explicitly that they were not preregistered. Exploratory findings generated after observing the data may motivate a future confirmatory benchmark. They may not be presented as confirmatory results of this one.

No effect in Section 5 may be reported with inferential confidence absent the analysis the registration specifies. The results document records raw proportions only. It reports no confidence intervals, no exact tests, and no effect sizes. Any inferential claim, including any claim that the Aider contrast is statistically reliable, requires the registered analysis (or, if the registration specified none for these endpoints, an explicitly exploratory analysis labeled as such) and must report test statistic, effect size, and interval. A contrast resting on 18 runs per cell in one platform is not a population-level claim and must not be written as one.

---

## 6. Impact on Claims

Until Section 2 is transcribed and Section 5 status is fixed, the following claim positions hold.

**Defensible now:**

- The CGP methodology's design intent includes workflow drift reduction. This is a statement of design intent and is not contingent on the benchmark.
- A preregistered benchmark of the drift hypothesis was conducted, returned a null result on the registered primary endpoint due to a baseline floor effect, and the floor effect is documented.
- The benchmark produced an observed improvement in valid task completion and in evidence-trail completeness, concentrated in a baseline-unreliable agent platform, with epistemic status pending Section 2.

**Not defensible and prohibited until corrected:**

- Any statement that CGP "passed the benchmark," "reduced drift," or was "validated" by this experiment.
- Any quantitative completion, reliability, or auditability figure presented as a confirmatory benchmark outcome before Section 5 status is fixed and the registered analysis is reported.
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

## 9. Required Actions Before This Note Is Authoritative

1. Transcribe all marked fields in Section 2 verbatim from https://osf.io/fnmg5.
2. Fix the epistemic-status branch in Section 5 against the transcribed registration.
3. Run or commission the registered analysis (or an explicitly labeled exploratory analysis if the registration specified none for the non-drift endpoints), reporting test statistics, effect sizes, and intervals, and attach those outputs to the repository.
4. Execute the companion Changes Note so that the results document, the customer-facing benchmark artifact, the Foundation Publication Brief, and Service Offer v1.1 resolve to this record.
5. Version this note to v1.1 once Sections 2 and 5 are closed, and link it from the OSF registration and from `runs/processed/` and `docs/paper/` in the repository.

---

*© 2026 The Heart AI Foundation. All Rights Reserved.*
*Author: Mobley, D. D. | Published under CC BY 4.0*
*The Heart AI Foundation™ — CGP Drift Reduction Benchmark: Preregistration Deviation Note v1.0*
*heartaifoundation.org*
