# Project Underdog - Security Master and Ticker Lineage Source Candidate Evaluation Framework v1

## 1. Executive Summary

This note defines the standardized framework for comparing future Security Master and Ticker Lineage source candidates before any real source is selected, loaded, ingested, accepted, or used for metadata construction.

Preferred candidate class from the prior survey:

`professional_or_institutional_security_master_with_point_in_time_or_dated_snapshot_ticker_lineage`

Framework purpose:

- Evaluate future candidate sources consistently.
- Preserve point-in-time integrity before source loading.
- Separate source comparison from source acceptance.
- Keep security identity and ticker lineage ahead of sector, industry, size, peer, and discovery work.

This is an evaluation-design artifact only. It does not identify vendors, evaluate real sources, ingest data, load source files, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run validation, mutate governance, register production outputs, or implement ML.

## 2. Evaluation Objectives

Primary objectives:

- Determine whether a candidate source can plausibly support `security_master_pit`.
- Determine whether a candidate source can plausibly support `ticker_lineage_pit`.
- Assess point-in-time safety before any source loading.
- Assess whether source history is reproducible, auditable, and date-safe.
- Identify blockers, manual-review items, and conditional-use limitations.
- Rank candidates using a consistent source-gate scorecard.

Non-objectives:

- Selecting a vendor.
- Accepting or rejecting a real source.
- Loading data samples.
- Ingesting metadata.
- Building security master or ticker lineage tables.
- Reconstructing sector, industry, size, or peer metadata.
- Enabling discovery or validation.

## 3. Candidate Comparison Criteria

| criterion | evaluation question | strong evidence | weak evidence |
| --- | --- | --- | --- |
| Effective-date support | Does the source provide effective dates, event dates, or known-as-of dates? | Explicit effective start/end and event as-of dates. | Current snapshot only or undated history. |
| PIT integrity | Can records be used without look-ahead? | Point-in-time records or retained dated snapshots. | Static profiles, backfilled current identity, or unknown timestamp policy. |
| Identifier continuity | Can the same economic security be tracked over time? | Stable security id, issuer id, share class, exchange, active/inactive windows. | Ticker-only identity or missing share-class/exchange context. |
| Ticker-lineage support | Does the source track ticker changes and windows? | Dated ticker windows, prior/next ticker, exchange changes, delistings, reuse handling. | Current ticker only or incomplete symbol-change history. |
| Corporate-action support | Does the source represent continuity events? | Mergers, acquisitions, spin-offs, delistings, relistings, predecessor/successor links. | Event gaps or event dates without security continuity. |
| Auditability | Can the source be reviewed and traced? | Source version, snapshot date, file hash/reference, review timestamp, reviewer notes. | Opaque feed, no retained source reference, no versioning. |
| Reproducibility | Can the evaluation and future construction be repeated? | Retained raw files or controlled references and deterministic normalization notes. | Manual extraction, changing API, no archive. |
| Coverage | Does it cover the target research universe by date? | Measurable active ticker-date coverage, ideally 95%+. | Unknown coverage or survivorship-biased active-only universe. |
| Lineage transparency | Are identity and ticker mappings explainable? | Source record ids, event ids, confidence fields, manual flags. | Black-box corrections with no rationale. |
| Maintenance burden | Is ongoing use manageable? | Stable schema, repeatable updates, bounded manual review. | Frequent schema drift, high manual repair burden. |
| Implementation complexity | How hard is the source to map safely? | Field model aligns with `security_master_pit` and `ticker_lineage_pit`. | Requires heavy inference, many joins, or ambiguous event logic. |
| Licensing uncertainty | Can source metadata be retained for research audit? | Clear retention and research-use permissions. | Unclear retention, redistribution, or audit restrictions. |

## 4. Scoring Framework

Use the existing source-gate score range:

| score | meaning |
| ---: | --- |
| 0 | Fails the criterion or evidence is absent. |
| 1 | Weak or partial evidence; likely blocks construction without manual review or narrow scope. |
| 2 | Acceptable evidence for controlled lineage evaluation with documented limitations. |
| 3 | Strong evidence; suitable for formal lineage-evaluation design if other gates pass. |

Core source-gate score fields:

- `pit_integrity_score`
- `coverage_score`
- `historical_depth_score`
- `identifier_quality_score`
- `update_feasibility_score`
- `source_stability_score`
- `implementation_complexity_score`
- `cost_manual_burden_score`
- `leakage_risk_score`

Supplemental qualitative criteria:

- effective-date support
- ticker-lineage support
- corporate-action support
- auditability
- reproducibility
- lineage transparency
- licensing uncertainty

Weighting approach:

| component | weight | rationale |
| --- | ---: | --- |
| PIT integrity | 20% | Look-ahead prevention is mandatory. |
| Identifier continuity | 20% | Security identity is the foundation for all downstream joins. |
| Ticker-lineage support | 15% | Historical ticker/date mapping is mandatory for Project Underdog panels. |
| Effective-date and as-of support | 15% | Date logic determines PIT usability. |
| Auditability and reproducibility | 15% | Source lineage must be retained and repeatable. |
| Coverage and historical depth | 10% | Coverage gaps can be blocked, but must be measured. |
| Maintenance, implementation, and licensing risk | 5% | High burden can make an otherwise strong source impractical. |

Minimum thresholds:

- `pit_integrity_score` must be at least 2.
- `identifier_quality_score` must be at least 2.
- `historical_depth_score` must be at least 2 for broad lineage evaluation.
- `coverage_score` must be at least 2 for broad lineage evaluation, or must include a narrow conditional scope.
- `leakage_risk_score` must be at least 2, interpreted as acceptable low-leakage risk.
- Any score of 0 in PIT integrity, identifier quality, effective-date support, auditability, or reproducibility is blocking.

Manual-review thresholds:

- Any required score field equal to 1 triggers manual review.
- Unknown licensing triggers manual review.
- Unknown source retention or reproducibility triggers manual review.
- Ticker-only identity triggers manual review unless stable security identifiers are separately documented.
- Conditional or inferred windows trigger manual review unless the conditional scope is machine-readable.

## 5. Acceptance Classes

These classes are candidate-comparison classes, not final source acceptance decisions.

| class | definition | allowed next step | blocked next step |
| --- | --- | --- | --- |
| `STRONG_CANDIDATE` | Meets all minimum thresholds, no critical red flags, strong PIT/date/identifier/ticker/audit evidence. | Prepare formal source-gate candidate evaluation package. | Loading, ingestion, construction, production use. |
| `CONDITIONAL_CANDIDATE` | Has promising evidence but requires narrow domain/date/universe scope or supplemental review. | Prepare conditional scope and formal evaluation package. | Broad lineage use, construction, reconstruction, discovery. |
| `MANUAL_REVIEW_REQUIRED` | Missing or ambiguous evidence prevents ranking or eligibility determination. | Request missing information and open manual-review item. | Loading, ingestion, construction, source acceptance. |
| `UNSUITABLE` | Fails critical PIT, identifier, lineage, reproducibility, or licensing criteria. | Retain survey/evaluation notes only. | Any PIT source use, loading, ingestion, construction. |

Class mapping guidance:

- `STRONG_CANDIDATE` may map to formal decision `ACCEPTED_FOR_LINEAGE_EVALUATION` only after source-gate evaluation.
- `CONDITIONAL_CANDIDATE` may map to `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` or a future conditional evaluation path.
- `MANUAL_REVIEW_REQUIRED` maps directly to source-gate manual review.
- `UNSUITABLE` may map to `REJECTED_FOR_PIT_USE` only after formal evaluation, not during framework design.

## 6. Red Flag Conditions

Blocking red flags:

- Static snapshot only.
- No effective dates and no source snapshot/as-of dates.
- Ticker-only identity with no stable security id, exchange/share-class resolution, or corporate-action support.
- No reproducible source archive, file hash, controlled reference, or version history.
- Licensing or usage terms prevent research retention or audit.
- Coverage cannot be measured by date.
- Source history silently backfills current identity.
- Ticker reuse is unresolved.
- Delisted or inactive securities are missing from history.
- Manual curation dominates the source without dated evidence and review trail.

Manual-review red flags:

- Effective windows must be inferred from sparse snapshots.
- Source has stable identifiers but weak event rationale.
- Source has ticker history but unclear issuer/security continuity.
- Source includes classification fields that may be current-state only.
- Update process is unclear.
- Source schema is unstable or undocumented.

Diagnostic-only red flags:

- Current profile API only.
- Public static reference snapshot.
- Manually curated list without dated evidence.
- Source intended only for cross-checking or coverage inspection.

## 7. Historical Integrity Assessment

Historical integrity assessment should answer:

- Does every record have a valid source snapshot date, known-as-of date, event as-of date, or effective window?
- Can source records be joined to a signal date without using future knowledge?
- Are event effective dates separated from event known dates?
- Are inactive, delisted, merged, and renamed securities present?
- Are ticker changes and ticker reuse represented as dated events or windows?
- Are inferred windows flagged and confidence-adjusted?
- Are missing periods explicitly blocked rather than filled with current state?

Historical integrity classes:

| class | definition | implication |
| --- | --- | --- |
| `PIT_STRONG` | Explicit point-in-time windows and as-of lineage. | Candidate can proceed if other gates pass. |
| `DATED_SNAPSHOT_USABLE` | Repeatable dated snapshots support inferred windows with audit trail. | Candidate may proceed with confidence penalties and scope limits. |
| `INFERRED_ONLY` | Windows require reconstruction from sparse evidence. | Manual review and conditional scope required. |
| `STATIC_OR_BACKFILLED` | Current/static metadata would populate history. | Blocks PIT source use. |

## 8. Reproducibility Assessment

Reproducibility assessment should answer:

- Can raw files or controlled references be retained?
- Are source versions and snapshot dates stable?
- Can records be hashed?
- Are normalization rules deterministic?
- Can row counts before and after cleaning be recorded?
- Is the update process repeatable?
- Can manual overrides be separated from automated source records?
- Does licensing permit research retention and audit artifacts?

Reproducibility classes:

| class | definition | implication |
| --- | --- | --- |
| `REPRODUCIBLE` | Raw/reference, version, hash, and rules can be retained. | Eligible for formal evaluation. |
| `REPRODUCIBLE_WITH_CONDITIONS` | Some constraints exist but can be represented in scope and lineage. | Conditional candidate. |
| `MANUAL_REPLAY_ONLY` | Requires manual steps that need review and bounded procedures. | Manual review required. |
| `UNREPRODUCIBLE` | Cannot retain or recreate source state. | Unsuitable. |

## 9. Candidate Ranking Methodology

Ranking process:

1. Confirm the candidate is in scope for security identity and ticker lineage.
2. Check blocking red flags before assigning a ranking.
3. Score all source-gate fields from 0 to 3.
4. Assign supplemental qualitative flags for effective dates, ticker lineage, corporate actions, auditability, reproducibility, and licensing.
5. Apply minimum thresholds.
6. Assign an acceptance class.
7. Rank candidates within each class by weighted score.
8. Break ties by stronger PIT integrity, then stronger identifier continuity, then stronger ticker-lineage support, then lower licensing uncertainty.
9. Document every missing field and manual-review item.
10. Preserve guardrails: ranking does not authorize source loading, ingestion, acceptance, construction, reconstruction, discovery, validation, production use, or ML.

Recommended weighted score formula:

`weighted_score = 0.20*pit_integrity + 0.20*identifier_continuity + 0.15*ticker_lineage + 0.15*effective_date_support + 0.15*audit_reproducibility + 0.10*coverage_depth + 0.05*operational_feasibility`

Where each component is normalized to the 0-3 score range.

Ranking interpretation:

| weighted score | interpretation |
| ---: | --- |
| 2.50 to 3.00 | Strong candidate if no red flags exist. |
| 2.00 to 2.49 | Conditional candidate or manual-review candidate depending on missing fields. |
| 1.00 to 1.99 | Manual review or diagnostic-only candidate. |
| below 1.00 | Unsuitable unless a narrow diagnostic use is explicitly documented. |

## 10. Final Recommendation

How should future source candidates be compared?

Future candidates should be compared with a standardized 0-3 scorecard, explicit red-flag review, weighted ranking, historical-integrity classification, reproducibility classification, and source-gate acceptance class. Comparisons should remain category/source-evaluation artifacts only until a separate task authorizes formal candidate evaluation.

What constitutes a strong candidate?

A strong candidate provides point-in-time or reproducible dated-snapshot identity and ticker lineage, stable security identifiers, explicit ticker windows, corporate-action continuity, broad measurable coverage, retained source lineage, deterministic reproducibility, manageable implementation complexity, and clear licensing for research audit retention.

What should block a candidate?

Static snapshots, missing effective/as-of dates, ticker-only identity, unresolved ticker reuse, missing inactive/delisted securities, unreproducible source history, unclear licensing, unmeasurable coverage, high leakage risk, or any score of 0 in PIT integrity, identifier quality, effective-date support, auditability, or reproducibility should block a candidate from lineage evaluation.

What should the next Codex task be?

The next Codex task should be **Project Underdog - Security Master and Ticker Lineage Source Candidate Evaluation Rubric Scaffold v1**. It should create source-candidate comparison templates and placeholder scoring artifacts aligned to this framework. It should not identify vendors, evaluate real sources, ingest data, load source files, accept or reject sources, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run validation, mutate governance, register production outputs, or implement ML.
