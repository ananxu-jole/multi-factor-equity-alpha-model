# Multi-Factor Equity Alpha Model

Project Underdog is my modular quantitative equity research platform for developing, validating, and assembling alpha signals into portfolio-ready research outputs. The project began as a simple multi-factor model, but has evolved into a staged research system covering signal discovery, multi-horizon signal scoring, walk-forward validation, alpha construction, stress testing, survivor selection, and portfolio construction.

The goal is not to present a finished trading strategy. The goal is to build a reproducible research pipeline that can reject weak ideas, preserve useful evidence, and make each alpha candidate explainable before it reaches portfolio construction.

## Research Philosophy

I prioritize robustness over backtest perfection. A strong-looking backtest is not useful if the signal is unstable, unreproducible, overfit to a narrow window, or dependent on assumptions that would be difficult to defend.

The project is built around a few principles:

- Reject unstable signals early, even when they look attractive in isolated tests.
- Preserve reproducibility through explicit pipeline stages, versioned outputs, and validation checks.
- Keep alpha behavior explainable across horizons, regimes, stress scenarios, and portfolio use.
- Use realistic constraints such as execution lag, turnover awareness, benchmark comparison, and out-of-sample validation.
- Treat signal decay as a first-class research problem rather than an afterthought.

## Current Pipeline Architecture

The current research flow is:

```text
Signal Discovery
-> Signal Quality Gate
-> Multi-Horizon Scoring
-> Signal Health / Reproducibility / Diversity
-> Alpha Construction
-> Alpha Walk-Forward Validation
-> Alpha Stress Testing
-> Survivor Freeze
-> Portfolio Construction
-> Dashboard
```

Earlier stages focus on discovering, scoring, and filtering raw signal families. Later stages construct alpha candidates, validate them through walk-forward testing, stress test survivorship, freeze the pre-ML alpha registry, and build portfolio views for evaluation.

## Extracted Engine Pipeline

The downstream notebook logic has been extracted into callable engines and CLI-backed runners for the current reusable research path:

```text
04A -> 04B -> 07 -> 08 -> 09 -> 09B
```

Those stages correspond to:

- `04A`: alpha construction
- `04B`: alpha walk-forward validation
- `07`: alpha stress testing
- `08`: survivor freeze
- `09`: portfolio construction
- `09B`: dashboard assembly

The extracted pipeline supports dry runs, parity checks, validation scripts, and combined pipeline runners. Notebook outputs are being separated from reusable engine logic so the notebooks can remain useful for research review while the core execution path becomes callable, testable, and easier to reproduce.

## Repository Structure

```text
multi-factor-equity-alpha-model/
├── src/
│   ├── core/          # shared project utilities and database helpers
│   ├── data/          # data access and preparation helpers
│   ├── signals/       # signal discovery and signal engineering modules
│   ├── scoring/       # signal scoring, health, reproducibility, and diversity logic
│   ├── alpha/         # alpha construction, WFV, stress, and survivor engines
│   ├── portfolio/     # portfolio construction and dashboard engines
│   └── pipeline/      # pipeline metadata and orchestration helpers
├── pipelines/         # runnable CLI pipeline scripts
├── pipelines/checks/  # parity and smoke validation scripts
├── notebooks/         # research notebooks and historical notebook outputs
├── configs/           # committed configuration files
├── sql/               # SQL definitions and migration/reference files
├── artifacts/         # local checkpoints, logs, and large generated artifacts
└── outputs/           # generated tables, reports, and figures
```

## Current Baseline Result

The current frozen pre-ML core alpha is:

```text
alpha_regime_blend_dynamic_v4_smooth
```

This baseline produced a long-only portfolio with positive return and a moderate Sharpe ratio in the current research sample. It did not outperform SPY over the full sample. I treat it as a valid baseline alpha for continuing research, not as a final trading strategy or evidence of market-beating performance.

## How To Run

Recommended fast full-platform dry run using local reproducible caches:

```bash
python pipelines/run_full_research_platform.py --dry-run --quiet --use-panel-cache --use-daily-ic-cache
```

Safe non-cached fallback:

```bash
python pipelines/run_full_research_platform.py --dry-run --quiet
```

Refresh local panel and daily-IC caches when inputs change:

```bash
python pipelines/run_full_research_platform.py --dry-run --quiet --use-panel-cache --use-daily-ic-cache --rebuild-panel-cache --rebuild-daily-ic-cache
```

Run the full extracted alpha-to-portfolio path without writing SQLite outputs:

```bash
python pipelines/run_alpha_to_portfolio_full.py --dry-run --quiet
```

Run the combined smoke/parity check:

```bash
python pipelines/checks/check_alpha_to_portfolio_full_pipeline.py
```

Most stage runners also support `--describe`, `--dry-run`, `--run`, and `--quiet`. Dry-run mode is the preferred first check because it exercises the extracted logic without mutating database tables.

## What Is Intentionally Excluded From Git

The repository is designed to keep source code, configuration, SQL references, and lightweight documentation under version control while excluding generated or heavy research artifacts.

Intentionally excluded items include:

- SQLite database files.
- Generated outputs under `outputs/`.
- Large artifacts, checkpoints, and logs under `artifacts/`.
- Local signal panel caches under `artifacts/panels/`.
- Local daily IC caches under `artifacts/ic/`.
- Notebook-heavy outputs and other large execution products.

Directory README files document the intended commit behavior for `sql/`, `artifacts/`, `outputs/`, and `configs/`.

## Roadmap

Near-term work:

- Profile and optimize the `03G` diversity engine.
- Add caching and checkpointing for expensive research stages.
- Expand signal families while preserving strict validation gates.
- Expand the stock universe beyond the current baseline.
- Add an ML layer only after a robust alpha library exists.

## Disclaimer

This is a research and educational project. It is not financial advice, not an investment recommendation, and not a production or live-trading system.
