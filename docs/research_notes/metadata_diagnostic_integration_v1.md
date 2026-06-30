# Metadata Diagnostic Integration v1

Date: 2026-05-24

Status: `STATIC_SNAPSHOT_RESEARCH_ONLY_DIAGNOSTIC_INTEGRATION`

## Objective

Integrate the 150-row metadata seed into research-only diagnostics and inventory monitoring context.

This is not alpha research, not sector-relative validation, not point-in-time metadata, and not a production metadata layer.

## Guardrail

All outputs are labeled `STATIC_SNAPSHOT_RESEARCH_ONLY`. The metadata cannot be used for historical sector-relative validation claims, alpha candidate creation, production registration, portfolio routing, ML, blending, or optimization.

## Coverage

- Metadata rows: `360`
- Universe tickers: `489`
- Matched universe tickers: `360`
- Coverage ratio: `0.736196`
- Extra seed tickers: `0`

## Sector Distribution

| sector                 | ticker_count   | seed_share          | universe_coverage_share   | sector_size_ready_for_diagnostics   | snapshot_warning              |
|:-----------------------|:---------------|:--------------------|:--------------------------|:------------------------------------|:------------------------------|
| Financials             | 54             | 0.15                | 0.11042944785276074       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Information Technology | 47             | 0.13055555555555556 | 0.09611451942740286       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Health Care            | 46             | 0.12777777777777777 | 0.09406952965235174       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Industrials            | 43             | 0.11944444444444445 | 0.08793456032719836       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Consumer Discretionary | 33             | 0.09166666666666666 | 0.06748466257668712       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Consumer Staples       | 27             | 0.075               | 0.05521472392638037       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Utilities              | 27             | 0.075               | 0.05521472392638037       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Real Estate            | 26             | 0.07222222222222222 | 0.053169734151329244      | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Materials              | 23             | 0.06388888888888888 | 0.04703476482617587       | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Communication Services | 17             | 0.04722222222222222 | 0.034764826175869123      | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |
| Energy                 | 17             | 0.04722222222222222 | 0.034764826175869123      | True                                | STATIC_SNAPSHOT_RESEARCH_ONLY |

## Peer Readiness

| group_field      | group_label                                     | ticker_count   | thin_group   | min_size   | snapshot_warning              |
|:-----------------|:------------------------------------------------|:---------------|:-------------|:-----------|:------------------------------|
| peer_group_label | industry:Electric Utilities                     | 16             | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Health Care Equipment                  | 12             | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Semiconductors                         | 11             | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Application Software                   | 9              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Oil and Gas Exploration and Production | 9              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Aerospace and Defense                  | 8              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Asset Management and Custody Banks     | 8              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Multi Utilities                        | 8              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |
| peer_group_label | industry:Specialty Chemicals                    | 8              | False        | 8          | STATIC_SNAPSHOT_RESEARCH_ONLY |

Most industry and peer groups remain thin. This blocks peer-relative transforms and limits sector-conditioned interpretation to descriptive diagnostics.

## Inventory Metadata Coverage

| signal_name                                       | panel_tickers   | metadata_covered_tickers   | metadata_missing_panel_tickers   | metadata_coverage_ratio   | snapshot_warning              | descriptive_only   |
|:--------------------------------------------------|:----------------|:---------------------------|:---------------------------------|:--------------------------|:------------------------------|:-------------------|
| participation_liquidity_state_shift_20_60         | 478             | 351                        | 127                              | 0.7343096234309623        | STATIC_SNAPSHOT_RESEARCH_ONLY | True               |
| participation_breadth_repair_under_hostile_trend  | 478             | 351                        | 127                              | 0.7343096234309623        | STATIC_SNAPSHOT_RESEARCH_ONLY | True               |
| volatility_compression_after_stress_stabilization | 478             | 351                        | 127                              | 0.7343096234309623        | STATIC_SNAPSHOT_RESEARCH_ONLY | True               |

## Descriptive Inventory Sector Exposure

| signal_name                                       | sector                 | covered_tickers   | active_ticker_date_count   | covered_ticker_date_count   | active_share_within_sector   | share_of_candidate_active_exposure   | mean_signal_descriptive   | mean_abs_signal_descriptive   | descriptive_only   | snapshot_warning              |
|:--------------------------------------------------|:-----------------------|:------------------|:---------------------------|:----------------------------|:-----------------------------|:-------------------------------------|:--------------------------|:------------------------------|:-------------------|:------------------------------|
| participation_breadth_repair_under_hostile_trend  | Financials             | 52                | 19300                      | 107536                      | 0.17947478053861032          | 0.14917528482431325                  | 0.014733966200693421      | 0.09547488891380154           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_breadth_repair_under_hostile_trend  | Health Care            | 45                | 16728                      | 92830                       | 0.18020036626090705          | 0.129295552566897                    | -0.0013711307414033833    | 0.09594893716032118           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_breadth_repair_under_hostile_trend  | Information Technology | 45                | 16600                      | 92010                       | 0.18041517226388437          | 0.12830620352764766                  | -0.00535818113497731      | 0.0922316882737982            | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_breadth_repair_under_hostile_trend  | Industrials            | 42                | 15140                      | 84746                       | 0.17865149977580064          | 0.11702144104870998                  | 0.007280847142094751      | 0.09447440768879797           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_breadth_repair_under_hostile_trend  | Consumer Discretionary | 33                | 12180                      | 67504                       | 0.18043375207395118          | 0.09414274451606919                  | -0.0031511083913082195    | 0.09005442988698197           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60         | Financials             | 52                | 104728                     | 107068                      | 0.9781447304516756           | 0.1495904859034021                   | 0.003114613638035057      | 0.4809108826346               | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60         | Health Care            | 45                | 90613                      | 92398                       | 0.9806814000303037           | 0.12942902279395171                  | 0.004990808398981504      | 0.504268160430066             | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60         | Information Technology | 45                | 89943                      | 91602                       | 0.9818890417239798           | 0.12847201391805146                  | -0.03210668044273923      | 0.5382838825852707            | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60         | Industrials            | 42                | 82566                      | 84354                       | 0.9788036133437655           | 0.11793491768295296                  | -0.010222532863453345     | 0.48176474867954494           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60         | Consumer Discretionary | 33                | 65915                      | 67206                       | 0.9807904056185459           | 0.09415110455964737                  | -0.015368576444635759     | 0.5132998371666089            | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| volatility_compression_after_stress_stabilization | Financials             | 52                | 20057                      | 106912                      | 0.1876028883567794           | 0.1497148572793503                   | 0.013533028256092457      | 0.09557599033728627           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| volatility_compression_after_stress_stabilization | Health Care            | 45                | 17287                      | 92263                       | 0.18736654997127777          | 0.12903827779768304                  | -0.0014488804164340945    | 0.09990978185134153           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| volatility_compression_after_stress_stabilization | Information Technology | 45                | 17190                      | 91467                       | 0.18793663288399096          | 0.12831422429236833                  | -0.005084737427402568     | 0.09844940439899894           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| volatility_compression_after_stress_stabilization | Industrials            | 42                | 15837                      | 84228                       | 0.1880253597378544           | 0.11821479756359728                  | 0.014819943854228726      | 0.0969580999314329            | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |
| volatility_compression_after_stress_stabilization | Consumer Discretionary | 33                | 12566                      | 67107                       | 0.18725319266246443          | 0.09379851904932521                  | -0.003184355988917571     | 0.09507826500505331           | True               | STATIC_SNAPSHOT_RESEARCH_ONLY |

These are descriptive signal-exposure summaries only. They are not sector-conditioned IC, not return attribution, and not validation evidence.

## Readiness Dashboard

| readiness_item                  | status   | value    | interpretation                                                                                    |
|:--------------------------------|:---------|:---------|:--------------------------------------------------------------------------------------------------|
| static_snapshot_warning_present | PASS     | True     | All rows must remain STATIC_SNAPSHOT_RESEARCH_ONLY.                                               |
| overall_metadata_coverage       | PASS     | 0.736196 | At or above 50% universe coverage; still diagnostic overlay only.                                 |
| sector_distribution_diagnostics | PARTIAL  | 11       | Number of sectors with at least 10 covered names.                                                 |
| peer_group_diagnostics          | PARTIAL  | 9        | Several peer groups are diagnostically usable, but broad peer-relative transforms remain blocked. |
| inventory_metadata_coverage     | PASS     | 0.734310 | Inventory panel metadata coverage is above 50%, but descriptive-only.                             |
| key_field_missingness           | PASS     | 0        | Key seed fields are populated for all covered rows.                                               |
| point_in_time_validity          | BLOCK    | False    | No point-in-time validity; no historical validation claims.                                       |

## Artifacts

- `industry_distribution.csv`
- `inventory_candidate_peer_group_coverage.csv`
- `inventory_candidate_sector_exposure_summary.csv`
- `inventory_metadata_coverage.csv`
- `inventory_panel_status.csv`
- `inventory_regime_metadata_context.csv`
- `lineage_source_audit.csv`
- `manifest.json`
- `market_cap_bucket_distribution.csv`
- `metadata_coverage_summary.csv`
- `metadata_missingness_lineage_warnings.csv`
- `metadata_readiness_dashboard.csv`
- `peer_group_thinness.csv`
- `sector_conditioned_descriptive_signal_summary.csv`
- `sector_distribution.csv`
- `size_bucket_distribution.csv`
- `static_snapshot_warnings.csv`

## Decision

The metadata seed is now integrated into research-only diagnostics. It is useful for coverage, sector distribution, inventory metadata coverage, and thin-group warnings, but it is not ready for sector-relative alpha research or validation.

## Recommended Next Step

Expand the seed toward at least 50% universe coverage, prioritizing underrepresented sectors and thin non-semiconductor peer groups. Rerun this diagnostic integration after each controlled expansion.

## Intentional Non-Changes

- no alpha candidates created
- no sector-relative signals created
- no validation claims made
- no point-in-time correctness claimed
- no SQLite tables written
- no universe definitions modified
- no gates, schemas, validation logic, or governance changed
- no production registration or survivor/watchlist state changed
- no detector, portfolio, ML, blending, or optimization routing changed
