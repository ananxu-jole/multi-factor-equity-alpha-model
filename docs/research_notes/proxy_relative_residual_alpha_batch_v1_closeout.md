# Proxy-Relative Residual Alpha Batch v1 Closeout

Date: 2026-05-23

Run id: `proxy_relative_residual_alpha_batch_v1`

Final status: `CLOSED_WEAK_RESEARCH`

## Objective

This research-only batch tested whether internally defined proxy-relative residual structures could improve medium-horizon cross-sectional alpha quality without requiring true sector, industry, GICS, or external peer metadata.

The batch was explicitly proxy-relative, not sector-relative.

## Proxy Dimensions Used

The batch used only internal behavioral proxy groupings:

- liquidity buckets
- volatility buckets
- residual-volatility buckets
- turnover buckets
- beta-like / market-relative behavior buckets
- market-relative residual behavior
- liquidity x volatility proxy buckets

No external sector metadata was fetched or introduced.

## Candidate Outcomes

Candidates classified as `CONDITIONAL_ONLY_RESEARCH`:

- `liquidity_volatility_peer_residual_quality_20`
- `volatility_bucket_residual_stability_20`

Candidates classified as `REJECT_RESEARCH`:

- `proxy_relative_resilience_20`
- `liquidity_bucket_relative_repair_20`
- `turnover_bucket_exhaustion_residual_10_20`
- `residual_vol_bucket_quality_recovery_20`

No candidate reached `CONDITIONAL_REFINEMENT_CANDIDATE` or `CANDIDATE_FOR_CONDITIONAL_VALIDATION`.

## Strongest Weak Clue

The strongest weak clue was `liquidity_volatility_peer_residual_quality_20`.

Observed behavior:

- h20 IC around `0.00542`
- WFV-style persistence / sign consistency: `0.75 / 0.75`
- low inventory overlap
- low reversal and momentum overlap
- no obvious crisis-only dependency

However, the signal remained too weak and too broadly active. The evidence is useful as a research clue, not as a refinement or validation candidate.

## Why Nothing Advanced

The proxy-relative framework improved structural cleanliness, but it did not produce enough standalone predictive strength.

Main limitations:

- h10 behavior was weak across the batch
- h20 behavior was only modestly positive for the two live-looking candidates
- active coverage remained broad, suggesting proxy normalization did not solve activation quality by itself
- several candidates had negative or directionally weak IC profiles
- one candidate showed one-bucket dominance
- no candidate combined meaningful h10/h20 IC, strong positive IC rate, clean persistence, controlled activation, and low redundancy strongly enough to justify refinement

## Key Lesson

Proxy-relative normalization was feasible and cleaner than broad absolute-state interaction designs, but internal proxy buckets alone did not create strong standalone medium-horizon alpha.

The likely missing ingredient is not another proxy bucket or harder residualization threshold. The next useful step should be more event-defined behavior: clearer liquidity/turnover exhaustion events, sharper repair timing, and explicit normalization after an identifiable stress or participation episode.

## Decision

Preserve this batch as research evidence only.

Do not refine `proxy_relative_residual_alpha_batch_v1` immediately. Do not promote any candidate. Do not convert the conditional-only candidates into validation targets without a redesigned event-defined mechanism.

Recommended next direction: move toward `event_defined_liquidity_turnover_exhaustion_alpha_v1`, focused on discrete stress/exhaustion behavior rather than broad continuous proxy-relative residual structures.

## Intentional Non-Changes

This closeout did not introduce:

- external metadata
- sector-relative implementation
- detector changes
- production registration
- survivor/watchlist mutation
- validation, gate, schema, or governance changes
- portfolio, ML, blending, or optimization routing

