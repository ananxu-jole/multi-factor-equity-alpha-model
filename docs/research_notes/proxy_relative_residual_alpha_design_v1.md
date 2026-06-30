# Proxy-Relative Residual Alpha Design v1

Date: 2026-05-23
Status: `DESIGN_ONLY`

## Design Objective

Design a research-only framework for proxy-relative residual alpha candidates using only Project Underdog's existing internal data. The goal is to test whether internally defined peer proxies can capture relative structural behavior without requiring sector, industry, GICS, or external peer metadata.

This is proxy-relative research, not sector-relative research.

## Why Proxy-Relative Instead of Sector-Relative

The metadata inspection found no usable sector, industry, GICS, security-master, or issuer peer-group classification layer. True sector-relative ranking or neutralization would require adding a classification layer with coverage, lineage, effective dates, and stale-classification controls.

The repo does have enough internal data for safer proxy-relative research:

- dynamic top-300 liquidity membership
- `adv20` and liquidity rank fields
- OHLCV panels
- benchmark-relative residual patterns
- cross-sectional ranks and z-scores
- simple one-factor neutralization helpers
- existing Track B diagnostics for similarity, fragility, WFV-style stability, and inventory overlap

The design should therefore compare each stock to internally defined behavioral buckets, while clearly labeling those buckets as proxies rather than economic sectors.

## Available Internal Proxy Dimensions

Candidate peer proxies should be built only from data available before or at the signal date, ideally with shifted or trailing values.

Recommended proxy dimensions:

- Liquidity buckets: trailing dollar-volume rank or dynamic universe liquidity rank.
- Volatility buckets: trailing realized volatility rank.
- Beta buckets: trailing benchmark beta or benchmark-correlation/beta proxies.
- Residual-volatility buckets: trailing volatility of benchmark-relative residual returns.
- Turnover buckets: trailing share/dollar-volume churn or volume acceleration rank.
- Stability buckets: trailing rank churn, path orderliness, or residual volatility stability.
- Market-relative behavior buckets: trailing residual return, residual drawdown, residual momentum, or residual reversal exposure.

Avoid treating these as company peers. They are behavioral comparison cohorts.

## Bucket Construction Framework

Bucket construction should be simple, interpretable, and resistant to look-ahead.

Recommended default:

1. Compute trailing proxy exposure using only historical information.
2. Shift bucket assignment by one trading day when the exposure uses same-date close/volume.
3. Assign date-wise quantile buckets within the active universe.
4. Require a minimum bucket size before computing bucket-relative residuals.
5. Treat missing or thin buckets as inactive rather than forcing imputation.
6. Track bucket turnover and bucket drift as first-class diagnostics.

Suggested default bucket count:

- 3 buckets for early research when coverage is thin.
- 5 buckets only if sample-size diagnostics are healthy.

Minimum guardrails for later implementation:

- minimum 25 valid names per bucket/date for residualization-style operations
- minimum 10 valid names per bucket/date for simple bucket-relative demeaning
- explicit thin-bucket warnings
- no same-day bucket assignment from unshifted liquidity or volatility inputs

## Residualization Methods

Three residualization methods should be evaluated, from simplest to more controlled:

1. Bucket demeaned residual:
   - candidate input minus same-date bucket mean
   - easiest to inspect and explain
   - risk: unstable when bucket membership is thin

2. Bucket-relative rank or z-score:
   - rank or z-score candidate input within proxy bucket by date
   - useful for relative resilience and relative exhaustion
   - risk: may amplify noisy small buckets

3. Cross-sectional neutralized residual:
   - use simple exposure neutralization against benchmark-relative momentum, reversal, volatility, or liquidity exposures
   - useful as a diagnostic or final exposure-control layer
   - risk: can remove the intended mechanism if overused

The first implementation should prefer bucket-demeaned and bucket-ranked designs, then use neutralization only as a diagnostic/control comparison.

## Proposed Candidate Families

These are design concepts only. No candidates are implemented by this note.

### 1. Liquidity-Bucket Residual Resilience

Compare a stock's residual return or drawdown behavior against names with similar liquidity rank.

Thesis:

Names that hold up better than similarly liquid peers may reflect cleaner sponsorship or lower forced-selling pressure.

Primary risks:

- hidden momentum
- mega-cap liquidity dominance
- one-bucket concentration

### 2. Volatility-Bucket Residual Exhaustion

Compare downside residual pressure against names with similar trailing volatility.

Thesis:

Within a volatility cohort, unusually exhausted but stabilizing residual behavior may carry more information than raw reversal.

Primary risks:

- hidden reversal
- crisis-only dependence
- volatility carry duplication

### 3. Residual-Volatility Relative Stability

Rank stability and path orderliness within residual-volatility buckets.

Thesis:

Relative stability among similarly noisy names may identify cleaner structural quality than absolute low-volatility screens.

Primary risks:

- hidden low-vol factor
- broad weak activation
- h20-only behavior

### 4. Beta-Bucket Relative Recovery Efficiency

Compare repair or recovery behavior among names with similar benchmark beta exposure.

Thesis:

Within beta peers, efficient recovery after residual drawdown may separate idiosyncratic repair from broad market rebound.

Primary risks:

- beta-estimation noise
- hidden market rebound/reversal
- unstable bucket membership

### 5. Turnover-Bucket Participation Quality

Compare participation quality among names with similar turnover or volume acceleration profiles.

Thesis:

Participation quality is more meaningful when normalized against names experiencing similar turnover intensity.

Primary risks:

- duplication of existing participation/liquidity repair
- event-volume contamination
- bucket drift during stress

### 6. Market-Relative Drawdown Containment

Compare residual drawdown containment within liquidity or volatility peers.

Thesis:

Names with contained residual drawdowns relative to comparable behavioral cohorts may reflect durable demand or less fragile ownership.

Primary risks:

- hidden defensive/low-vol exposure
- weak IC due to broad activation
- crisis-window concentration

### 7. Residual Strength With Anti-Momentum Controls

Identify relative residual strength within proxy buckets while explicitly controlling price-rank momentum and raw continuation.

Thesis:

Residual strength that survives peer normalization and anti-momentum diagnostics may be structurally cleaner than raw relative strength.

Primary risks:

- still becomes momentum
- h20 concentration
- poor behavior during sharp reversals

## Required Anti-Failure Diagnostics

Any future implementation must include diagnostics designed to reject fake alpha quickly.

Required diagnostics:

- hidden momentum overlap
- hidden reversal overlap
- hidden low-volatility or volatility-carry overlap
- bucket instability and bucket turnover
- one-bucket dominance
- crisis-only dependence
- peer-group drift
- broad activation with weak IC
- one-window dominance
- sample-size sanity
- inventory similarity
- WFV-style persistence/sign consistency
- active coverage
- turnover proxy
- h5/h10/h15/h20 IC, with h10/h20 primary
- bucket-conditioned IC and positive-rate summary
- comparison against universe-relative and benchmark-relative residual baselines

Interpretation rule:

A candidate should not advance if it only beats baselines inside one thin bucket, one crisis window, or one unstable peer proxy.

## Implementation Risks

Main risks:

- Proxy buckets are not economic sectors and should not be interpreted as fundamental peer groups.
- Bucket assignment can become unstable during stress, especially for volatility and turnover proxies.
- Liquidity buckets may overfit market-cap/liquidity structure.
- Volatility and residual-volatility buckets may collapse into low-volatility or volatility-carry effects.
- Residual behavior can quietly become momentum or reversal unless controls are explicit.
- Dynamic universe membership reduces some same-day membership issues but does not eliminate survivorship risk from the current large/liquid raw pool.
- Small buckets can create noisy ICs and misleading positive-rate estimates.

## Recommended First Implementation Batch

Recommended future batch:

`proxy_relative_residual_alpha_batch_v1`

Scope:

- 5 to 7 candidates maximum
- research-only runner
- no production registration
- no survivor/watchlist mutation
- no validation routing

Recommended first candidates:

1. `liquidity_bucket_residual_resilience_20`
2. `volatility_bucket_residual_exhaustion_20`
3. `residual_vol_bucket_relative_stability_20`
4. `beta_bucket_recovery_efficiency_20`
5. `turnover_bucket_participation_quality_20`
6. `liquidity_volatility_bucket_drawdown_containment_20`

Primary horizon focus:

- h10/h20 primary
- h5 diagnostic only
- avoid h5-led approval logic

Recommended artifact outputs for a future implementation:

- `candidate_score_summary.csv`
- `bucket_coverage_summary.csv`
- `bucket_stability_summary.csv`
- `bucket_conditioned_ic_summary.csv`
- `baseline_similarity_summary.csv`
- `inventory_similarity_summary.csv`
- `fragility_concentration_summary.csv`
- `candidate_decision_summary.csv`
- `manifest.json`

## Explicit Guardrails

- Do not implement candidates from this design note.
- Do not create signal runners from this design note.
- Do not fetch external metadata.
- Do not describe proxy-relative outputs as sector-relative outputs.
- Do not modify universe definitions.
- Do not change schemas, gates, validation logic, governance, production registration, survivor/watchlist state, detector files, portfolio logic, ML routing, blending, or optimization paths.
- Future candidates from this framework must remain research-only until they pass the existing strict research and validation process.
