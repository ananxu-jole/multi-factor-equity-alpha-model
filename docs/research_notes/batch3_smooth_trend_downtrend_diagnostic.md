# Batch 3 Smooth Trend Downtrend WFV Diagnostic

## Objective

Diagnose why `smooth_trend_persistence_60_downtrend` at h20 showed strong effective mean test IC and perfect sign consistency in the controlled Batch 3 WFV bridge, but was still rejected for weak effective IC IR and low persistence.

This note is diagnostic only. No gates, schemas, promotion logic, official WFV logic, or 04A+ stages were changed.

## Official WFV Result

| Metric | Value |
|---|---:|
| Signal | `smooth_trend_persistence_60_downtrend` |
| Horizon | h20 |
| Direction | `NEGATIVE_EDGE_REVERSE_SIGNAL` |
| WFV status | `REJECTED_WFV` |
| Mean train IC | -0.201354 |
| Mean test IC | -0.292996 |
| Effective mean test IC | 0.292996 |
| Effective test IC IR | n/a |
| Persistence ratio | n/a |
| Sign consistency | 1.000000 |
| Rejection reason | weak effective IC IR; low persistence |

The effective mean test IC is strong, but it comes from only one valid test window. With one valid test IC, test IC standard deviation and IC IR are undefined. Persistence is also not measurable because no WFV window has both a valid train IC and a valid test IC for this conditional signal.

## WFV Window-Level Results

| Window | Train Range | Test Range | Train Active Dates | Test Active Dates | Train Valid IC Dates | Test Valid IC Dates | Train IC | Test IC | Effective Test IC | Test Positive IC Rate |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2018-01-02 to 2019-07-03 | 2019-08-02 to 2019-10-30 | 38 | 0 | 38 | 0 | -0.204751 | n/a | n/a | n/a |
| 2 | 2019-11-07 to 2021-05-10 | 2021-06-09 to 2021-09-07 | 38 | 0 | 38 | 0 | -0.307116 | n/a | n/a | n/a |
| 3 | 2021-09-15 to 2023-03-16 | 2023-04-17 to 2023-07-17 | 188 | 0 | 188 | 0 | -0.092195 | n/a | n/a | n/a |
| 4 | 2023-07-25 to 2025-01-24 | 2025-02-25 to 2025-05-23 | 0 | 17 | 0 | 17 | n/a | -0.292996 | 0.292996 | 0.000000 |

Window 4 contributes 100% of the valid official test IC average. Windows 1-3 have no active DOWNTREND test dates. Window 4 has active test dates but no active train dates, so it cannot support train/test persistence.

## Conditional Regime Coverage

The condition is `benchmark_trend_regime = DOWNTREND`, implemented with the same SPY 50-day / 200-day trend definition used in the Batch 3 conditional diagnostics.

Coverage is highly sparse inside the fixed WFV windows:

- Test windows 1-3: 0 active dates each.
- Test window 4: 17 active dates out of 63.
- Train windows 1-3: active dates exist, but their paired test windows do not.
- Train window 4: 0 active dates, while its test window has the only active test sample.

This means the official bridge is trying to judge a conditional edge with no overlapping train/test active regime samples across WFV windows.

## Daily IC Distribution

| Sample | N Valid Active Dates | Mean IC | Effective Mean IC | Median IC | Effective Median IC | Std | Skew | Min | Max | Winsorized Effective Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| All active valid dates | 281 | -0.148629 | 0.148629 | -0.136096 | 0.136096 | 0.201786 | -0.343871 | -0.733246 | 0.373442 | 0.144337 |
| WFV test active valid dates | 17 | -0.292996 | 0.292996 | -0.257109 | 0.257109 | 0.132852 | -0.512616 | -0.536661 | -0.076687 | 0.294294 |

The active-date distribution is not obviously weak. Across all active dates, the edge is directionally consistent with the expected negative raw IC orientation. In the WFV test sample, all 17 active daily IC values have the expected negative raw sign. However, the WFV test sample is too small and concentrated in one window to support an official persistence or IR claim.

## All-Date vs Active-Only WFV Diagnostic

Inactive dates were neutralized to zero in the implemented signal. For daily cross-sectional IC, those inactive dates are constant signal rows and therefore produce undefined daily IC. The official WFV daily IC calculation drops those undefined daily IC values.

As a result:

- The official all-date WFV IC and active-only diagnostic IC match on active dates.
- Neutral inactive dates do not appear to distort the IC value when the signal is active.
- The main issue is that inactive dates remove most WFV test windows from the valid IC sample.
- Official `test_n_obs` counts paired signal/return cells, including neutral inactive cells, so it can look well-populated even when valid daily IC dates are zero.

This is best described as conditional-regime sparsity, not an IC-value dilution problem.

## Failure Classification

Primary classification: `sparse conditional edge`.

Secondary classifications:

- `one-window dominated edge`: the full official effective test IC comes from window 4.
- `inactive-date dilution`: not dilution of IC magnitude, but dilution of usable WFV windows because inactive dates are constant and produce no valid daily IC.
- `high-variance edge`: possible, but not proven; the active sample has meaningful daily IC variance and only 17 WFV test active dates.
- `true instability`: not established. The bridge lacks enough active train/test overlap to distinguish instability from sparse regime sampling.

## Recommendation

Do not promote or run 04A+ from this evidence.

Recommended next action:

1. Keep `smooth_trend_persistence_60_downtrend` on a research watchlist only.
2. Create an active-only WFV diagnostic path for conditional signals, clearly separated from official WFV gates.
3. Defer implementation decisions to a later conditional-alpha framework that can evaluate conditional samples on regime-active windows rather than forcing sparse conditional signals through universal fixed windows.

Do not relax gates. The official bridge behaved conservatively and correctly rejected the signal because the apparent edge is not persistent across the existing fixed WFV windows.
