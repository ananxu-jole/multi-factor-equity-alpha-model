# Sector-Relative / Peer-Relative Residual Metadata Inspection

Date: 2026-05-23
Status: `INSPECTION_ONLY`

## Inspection Objective

This note inspects whether Project Underdog currently has enough metadata and utility support to safely design sector-relative or peer-relative residual alpha candidates. This is not an alpha implementation batch and does not create sector-relative signal runners.

## Files, Scripts, and Tables Inspected

Code and notebooks inspected:

- `src/universe.py`
- `src/db.py`
- `src/signals.py`
- `src/expanded_discovery.py`
- `src/scoring/signal_scoring.py`
- `pipelines/run_track_b_robustness_discovery_v4.py`
- `pipelines/run_structural_interaction_alpha_discovery_batch_v1.py`
- `pipelines/run_structural_interaction_alpha_expansion_v2.py`
- `notebooks/2-Phase 2_Signal Expansion/01_Data Foundation.ipynb`
- `sql/project_underdog.db`

SQLite tables inspected:

- `universe_metadata_current`
- `universe_metadata_history`
- `raw_ticker_pool_current`
- `raw_ticker_pool_history`
- `universe_membership_dynamic_top300_current`
- `universe_membership_dynamic_top300_history`
- `universe_diagnostics_dynamic_top300_current`
- `universe_diagnostics_dynamic_top300_history`
- metadata table names containing `sector`, `industry`, `gics`, `sic`, `security`, `peer`, `class`, and `group`

## Available Metadata Summary

The project has a usable current universe and dynamic liquidity membership layer.

- Default SQLite database: `sql/project_underdog.db`
- `universe_metadata_current`: 489 distinct tickers
- `raw_ticker_pool_current`: 488 distinct stock tickers
- `universe_membership_dynamic_top300_current`: 624,900 selected membership rows, 461 distinct selected tickers, 2,083 selected dates from 2018-01-24 through 2026-05-07
- `universe_diagnostics_dynamic_top300_current`: 2,098 dates from 2018-01-02 through 2026-05-07
- Dynamic membership is shifted in the universe builder to avoid same-day liquidity membership look-ahead.

Available ticker-level metadata fields are limited to universe membership and source information:

- `ticker`
- `source`
- `universe_name`
- `universe_version`
- `active`
- `notes`
- `run_id`
- `timestamp_frozen`

Available dynamic membership fields include:

- `Date`
- `ticker`
- `in_universe`
- `adv20`
- `close`
- `volume`
- `universe_rank`
- `universe_mode`
- `universe_version`

## Missing Metadata Summary

No sector, industry, GICS, SIC, security-master, or peer-group classification table was found.

Searches for sector-like tables and columns found no usable classification metadata. The only `sic` matches were ticker columns such as `HSIC` in price tables, not SIC industry codes. The only `group` matches were signal diversity or alpha construction grouping fields, not issuer peer groups.

Missing fields for true sector-relative research:

- sector
- industry
- subindustry
- GICS or equivalent classification
- point-in-time classification effective dates
- peer group identifier
- classification source and version
- stale/reclassification handling

## Sector-Relative Research Feasibility

Sector-relative research is not currently feasible as a clean implementation using only existing metadata.

The repo can support cross-sectional and market-relative residual signals, but not true sector-relative ranking, sector-relative z-scores, or sector-neutral residualization without adding a sector/industry metadata layer first.

## Peer-Relative Research Feasibility

Peer-relative research is partially feasible only through non-fundamental proxy peer groups.

Feasible without external data:

- universe-relative residuals
- benchmark-relative residuals
- beta-adjusted market residuals
- liquidity-rank bucket relative residuals
- volatility-bucket relative residuals
- dynamic top-300 liquidity membership conditioning

Not feasible yet:

- sector peer residuals
- industry peer residuals
- business-comparable peer residuals
- point-in-time peer-group neutralization

Proxy peer groups could be useful for research, but they should not be described as sector-relative.

## Reusable Helpers Found

Reusable infrastructure exists for current-style residual and cross-sectional research:

- `src.db.load_universe_metadata()` loads current/history universe metadata.
- `src.db.load_ohlcv_panels()` loads canonical OHLCV panels.
- `src.universe.build_dynamic_liquidity_universe_mask()` builds shifted liquidity membership.
- `src.universe.build_dynamic_liquidity_membership_table()` stores dynamic membership with `adv20` and `universe_rank`.
- `src.signals._cross_sectional_zscore()` and `_cross_sectional_rank()` support date-level z-scores and percentile ranks.
- `src.expanded_discovery.cross_sectional_zscore()` supports clipped date-level z-scores.
- Track B runners reuse `_cs_neutralize()` from `run_track_b_robustness_discovery_v4.py` for simple one-factor cross-sectional residualization.
- Existing research runners already build benchmark-relative residuals using SPY or equal-weight universe returns.

Reusable pieces are sufficient for market-relative and bucket-relative research, but not group-relative sector operations.

## Data Risks and Caveats

- Current universe construction is explicitly not fully survivorship-free. The raw pool is a current large/liquid engineering pool, and the project notes that a fully survivorship-free test requires historical constituent membership or a point-in-time security master.
- Dynamic top-300 liquidity membership is shifted, which reduces same-day membership look-ahead, but it does not solve survivorship in the starting ticker pool.
- Static sector metadata, if added later from a current snapshot, would introduce classification survivorship/staleness risk.
- Point-in-time sector classifications would be preferable before treating sector-relative outputs as validation-quality.
- Sector group sizes may be thin in the 300-name dynamic universe, especially after missing data and active filters.
- Proxy peers based on liquidity or volatility buckets are safer with current data, but they answer a different question than sector-relative residual behavior.

## Recommended Implementation Path

Do not implement a sector-relative alpha batch until a minimal classification layer exists.

Cleanest path if sector metadata becomes available:

1. Add a research-only `ticker_classification_current` and `ticker_classification_history` layer, or equivalent artifact, with `ticker`, `classification_date`, `sector`, `industry`, `source`, `source_version`, `effective_start`, and optional `effective_end`.
2. Add an inspection diagnostic that reports coverage by universe, date, sector, and dynamic membership.
3. Add group-size guardrails before scoring any sector-relative signal.
4. Implement group-relative transforms as reusable research helpers:
   - sector-relative rank by date
   - sector-relative z-score by date
   - sector-demeaned residual
   - sector-neutral residualization with minimum group size
5. Keep all initial outputs under research artifacts only and compare against existing universe-relative residual baselines.

If no sector metadata is added, the safer near-term path is a proxy-relative residual batch using existing data:

- liquidity-bucket relative residuals
- volatility-bucket relative residuals
- beta/residual-volatility bucket relative behavior
- market-relative residual resilience/exhaustion with anti-momentum and anti-reversal diagnostics

## Recommended First Research Batch Design

Recommended next batch, after this inspection, should be design-only first:

`proxy_relative_residual_alpha_design_v1`

Purpose:

Test whether peer-like residual structures can be defined from existing internal data without pretending they are true sector-relative signals.

Candidate families to design:

- liquidity-bucket residual resilience
- volatility-bucket residual exhaustion
- residual relative-value stabilization
- beta-adjusted relative underperformance repair
- residual strength with anti-momentum controls
- residual drawdown containment within liquidity/volatility peers

Diagnostics to require later:

- comparison versus universe-relative residual baselines
- bucket-size and coverage checks
- look-ahead review for bucket assignment
- turnover and active coverage
- WFV-style persistence/sign consistency
- inventory similarity
- reversal/momentum similarity
- crisis/stress concentration

## Guardrail Statement

No alpha candidates were implemented. No sector-relative signal runners were created. No external data was fetched. No universe definitions, schemas, gates, validation logic, governance, production registration, survivor/watchlist state, detector files, portfolio logic, ML routing, blending, or optimization paths were changed.
