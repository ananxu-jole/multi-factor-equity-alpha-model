# Alpha Family Diversification — Redundancy Screening Engine v1

Date: 2026-06-17

Purpose: Implement a research-only, metadata-driven redundancy screening engine to provide advisory classifications for candidate overlap before discovery execution.

Summary

- The engine is metadata-only and advisory: it does not score, promote, demote, register, or mutate candidate state.
- It inspects candidate registry metadata fields (`family`, `theme`, `feature_group`, `horizon`, `redundancy_risk`, `signal_name`, `candidate_id`) and applies lightweight rules to flag potential overlap or contamination.

Advisory classifications

- `LOW_METADATA_REDUNDANCY`: little or no overlap inferred from metadata
- `MODERATE_METADATA_REDUNDANCY`: multiple metadata overlaps detected
- `HIGH_METADATA_REDUNDANCY`: strong evidence of duplication or high overlap
- `REVIEW_REQUIRED`: immediate manual review recommended (e.g., stress/participation keywords detected)

Limitations

- This engine uses only metadata and must not be used as a final decision. It is a guardrail to direct analyst attention.
- It will not detect statistical redundancy (value/rank correlation) — a separate redundancy metric module is required before discovery execution.
- Results are advisory only and must be reviewed by research and governance before enabling `--run`.

Next steps

- Implement statistical redundancy checks (value and rank correlations) with provenance and lookback configuration.
- Integrate governance gating based on review checklist and approvals.
