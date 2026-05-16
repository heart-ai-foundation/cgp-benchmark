# CGP Benchmark: Results and Consumer-Facing Remediation Changes Note

**Operational Coordination Note**
**Version:** 1.0
**Date:** 2026-05-16
**Author:** Mobley, D. D., Empathy Ethicist
**Canonical source for all changes herein:** `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md`
**Boundary governance:** Heart Foundation Charter v2.4 Section 3.6 (Dual-Entity Boundary Doctrine)

---

## 1. Why This Note Exists

The CGP Drift Reduction Benchmark returned a null result on its registered primary endpoint because baseline scope drift occurred at or near zero in the preregistered dataset. The operative findings the benchmark did produce, valid task completion and evidence-trail completeness, are the findings the commercial offer is actually built to sell, per Service Offer v1.1 Section 1 ("The durable value is auditability, reproducibility, and verifiable completion"). The exposure is not the data. The exposure is that the benchmark is named, reported, and cited for the one thing it did not show.

This note specifies the exact changes required so that the results document, the customer-facing artifact, the Foundation Publication Brief, the Service Offer, and the repository all resolve to the deviation note and stop promising the null. It specifies no new experiments. It specifies no methodology changes. It specifies no edit to the OSF registration.

Every change below resolves to the deviation note as canonical. Where a change depends on transcription fields still open in the deviation note Section 2, that dependency is marked BLOCKED.

---

## 2. Change Set A: Benchmark Results Document

**File:** `CGP_Drift_Reduction_Benchmark_Results.md`
**Problem:** The document leads with a blended all-agents validity figure and an upbeat headline, presents the drift null as a passing remark, and frames the manuscript direction softly. A reader takes "results are in, CGP passes" from it, which the registered endpoint does not support.

**Changes:**

A1. Add a status banner immediately under the title: a one-paragraph statement that the registered primary endpoint (scope drift) returned null at a baseline floor, that the operative findings concern valid completion and evidence completeness, and that epistemic status is governed by `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md`. Link the deviation note.

A2. Demote the "Headline Results" section. Rename it to "Result Against Registered Primary Endpoint." State the scope-drift null first (1 of 72 baseline, 1 of 72 CGP), state that the single baseline event was in the companion extension not the preregistered primary dataset, and state the floor-effect conclusion before any other number appears.

A3. Move valid-completion and evidence-trio findings into a separately titled section, "Observed Findings (Status Per Deviation Note)." Carry the raw proportions as recorded. Tag the section with the epistemic-status branch from deviation note Section 5. BLOCKED until deviation note Section 2 is transcribed and Section 5 status fixed.

A4. Reframe the Aider contrast as platform-specific and sample-limited. State explicitly: 18 runs per cell, one platform, no inferential statistics computed in the current snapshot, not a population claim.

A5. Report the verification-success movement (100.0% to 95.8%) in the body, not omitted, with a one-line note that it moved in the unfavorable direction and is within small-sample noise pending the registered analysis.

A6. Rewrite "Interpretation" and "Manuscript Direction" so the primary framing is reliability and auditability, drift is reported as null at floor, and the manuscript's contribution is stated as verifiable completion and non-submission detection rather than drift suppression. Remove any sentence that could be read as the benchmark validating CGP.

A7. Add an explicit limitations subsection: ceiling effects in three of four platforms, single-platform effect concentration, absence of inferential statistics in the snapshot, floor effect on the registered endpoint.

**Acceptance check:** A reader who reads only the first screen of the document concludes the registered endpoint was null and the operative result is completion and auditability, not drift reduction. No sentence in the document states or implies "passed" or "validated."

---

## 3. Change Set B: Customer-Facing Benchmark Artifact and Naming

**Targets:** the benchmark suite material referenced in Service Offer v1.1 Tier 3 deliverables ("Examples drawn from the published benchmark suite"), and the public artifact title.
**Problem:** A public artifact titled "Drift Reduction Benchmark" promises the null to any prospect who opens it. Service Offer v1.1 Section 6 permits sharing the offer and using benchmark examples in workshops.

**Changes:**

B1. Title the customer-facing artifact for what it demonstrates. Working title: "Continuity-Governed Prompting: Reliability and Auditability Benchmark." Do not retitle the OSF registration or the registered experiment design document. The registered internal name remains the historical record.

B2. Bind the OSF identifier (osf.io/fnmg5) and a link to the deviation note to the customer-facing artifact, so chain of custody is visible and a prospect who follows it reaches the honest record rather than a bare null.

B3. The customer-facing artifact carries the scope-drift result as a reported secondary, null at floor, with the floor effect explained in one sentence. It does not omit the null. Omitting it would reproduce the exposure in a more deniable form.

B4. Tier 3 workshop material presents the failure-mode walkthrough using non-submission and evidence-omission detection as the demonstrated catch, and presents drift as design intent with a documented floor-effect null, consistent with Service Offer v1.1 Section 3.1 and 3.5.

**Acceptance check:** No customer-facing artifact carries "Drift Reduction" as its operative title. Every customer-facing benchmark artifact links the deviation note. The drift null is present, not buried.

---

## 4. Change Set C: Foundation Publication Brief Reconciliation

**File:** `CGP_Foundation_Publication_Brief_v1_1.md`, Section 8 (claims boundary).
**Problem:** Service Offer v1.1 Section 3 states the HeartCore claims boundary is consistent with this brief's Section 8. If Section 8 currently frames the benchmark around drift reduction or states a drift outcome, it now disagrees with the deviation note.
**Status:** This brief has not been read into the current record. This note specifies conditions, not text.

**Required conditions (verify, then edit only as needed):**

C1. Section 8 must not state or imply a drift-reduction result. If it does, correct it to the deviation note's defensible-claims set (Section 6 of the deviation note).

C2. Section 8 must reference `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md` as the governing evidence record for any benchmark claim.

C3. Section 8's claims boundary must remain the parent of Service Offer v1.1 Section 3. Edit the brief first, then propagate to the Service Offer, never the reverse, per the Dual-Entity Boundary (Foundation evidence is parent; commercial citation is child).

**Acceptance check:** Reading Section 8 and deviation note Section 6 side by side yields no contradiction. Section 8 points to the deviation note.

---

## 5. Change Set D: HeartCore Service Offer

**File:** `CGP_HeartCore_Service_Offer_v1_1.md` → version bump to v1.2.
**Problem:** Section 3.1 cites `CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md` as the empirical basis for the drift claim. That citation now resolves to a null. Section 3.6 enforcement requires quantitative claims trace to published evidence.

**Changes:**

D1. Section 3.1: change the drift bullet citation from the experiment design document to `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md`. Keep the existing wording "design intent, with empirical testing in progress," which is already correctly non-confirmatory. The wording survives; only the citation target changes.

D2. Section 3.1: add a bullet permitting the supported operative claim, phrased to the deviation note's defensible set, that an open preregistered benchmark produced an observed improvement in valid completion and evidence completeness in a baseline-unreliable agent platform, with epistemic status per the deviation note. BLOCKED until deviation note Section 5 status is fixed.

D3. Section 3.4: review every acceptable-language example against the deviation note. The four current examples do not assert a drift outcome and appear to survive. Confirm and record the confirmation. Add one example reflecting the reliability-and-auditability framing so sales language has a positive claim that is actually supported.

D4. Section 3.5: add "CGP reduced drift in our benchmark" and "benchmark-proven drift reduction" to the not-acceptable list, with the violation note "registered primary endpoint null at floor; see deviation note."

D5. Section 7 Companion Documents: add `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md` to Foundation methodology references.

D6. Revision note for v1.2: "Benchmark citation corrected to preregistration deviation note following null result on registered primary endpoint. Reliability-and-auditability claim added per deviation note defensible set. Drift-outcome language added to prohibited examples."

D7. Apply Pattern C signature unchanged (HeartCore, heartcoreventures.com). The entity boundary is not affected by this remediation; only the cited evidence changes.

**Acceptance check:** No HeartCore document cites the experiment design document as proof of a drift result. Every benchmark-derived claim in the Service Offer resolves to the deviation note. Section 3.6 enforcement passes against the corrected text.

---

## 6. Change Set E: Repository and OSF Surfaces

**Targets:** `github.com/heart-ai-foundation/cgp-benchmark` repository and the OSF registration page.

**Changes:**

E1. Commit `CGP_Benchmark_Preregistration_Deviation_Note_v1_0.md` to the repository alongside `runs/processed/` and `docs/paper/`.

E2. Add a top-of-README epistemic-status section: registered primary endpoint null at floor, operative findings concern completion and auditability, deviation note is the governing record, link it.

E3. From the OSF registration page, add a link to the deviation note as an associated component. Do not edit the registration body.

E4. `docs/paper/` working manuscript: apply the Change Set A framing to the manuscript draft so the paper and the results document do not diverge. The manuscript's contribution statement becomes verifiable completion and non-submission detection, drift reported as null at floor.

**Acceptance check:** Anyone arriving at the repository or the OSF page from a Service Offer or workshop citation reaches the deviation note within one click.

---

## 7. Sequencing and Dependencies

Strict order. Foundation evidence is parent; commercial citation is child; the registration is frozen.

1. Close deviation note Section 2 (transcribe from OSF) and Section 5 (fix epistemic status). Everything marked BLOCKED depends on this.
2. Run or commission the registered analysis with test statistics, effect sizes, and intervals. Attach to repository.
3. Change Set A (results document) and Change Set E (repository, OSF link).
4. Change Set C (Foundation Publication Brief Section 8).
5. Change Set B (customer-facing artifact and naming).
6. Change Set D (Service Offer v1.2).

Steps 4 through 6 must not precede step 3. A commercial citation must never resolve to a Foundation document that has not yet been corrected.

---

## 8. Validation Before Any Step Is Marked Done

Per Voice-DNA v2.1 pre-delivery checklist plus claims-boundary self-test:

- Grep each edited document for em dashes. Zero outside the Academic carve-out. Corpus footer separator preserved.
- Grep for banned phrases. Register match verified per document.
- Signature pattern verified per entity: results document and Foundation Publication Brief and customer-facing artifact carry Pattern A; Service Offer carries Pattern C; this note and the deviation note carry their stated patterns.
- Claims-boundary self-test: for every benchmark-derived sentence in every touched document, name the evidence it resolves to. If it resolves to the registered drift endpoint, it is non-compliant and is rewritten or removed.
- Sidewalk test on the results document headline and the Service Offer Section 3 language.

---

## 9. Out of Scope

- No new experiments. The deviation note Section 4 separately notes that a future drift benchmark would need engineered baseline drift; that is a different project and is not authorized by this note.
- No edit to the OSF registration body or to raw run records.
- No change to the CGP methodology or the Next-Prompt Protocol scaffold.
- No change to the Dual-Entity Boundary or to entity signature patterns.

---

*© 2026 Dylan D. Mobley. All Rights Reserved.*
*CGP Benchmark: Results and Consumer-Facing Remediation Changes Note v1.0*
*empathyethicist.ai*
