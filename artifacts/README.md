# Artifacts

This directory is for generated run artifacts such as checkpoints, logs, diagnostic files, and local caches.

Local cache directories:

- `artifacts/panels/` contains reproducible signal panel Parquet caches used by cache-enabled scoring and diagnostics.
- `artifacts/ic/` contains reproducible daily IC Parquet caches used by cache-enabled signal scoring, decay, and regime IC stages.

These caches are local acceleration artifacts. They can be rebuilt from the SQLite inputs and should not be committed.

Refresh cache artifacts with:

```bash
python pipelines/run_full_research_platform.py --dry-run --quiet --use-panel-cache --use-daily-ic-cache --rebuild-panel-cache --rebuild-daily-ic-cache
```

Individual stage runners also support `--rebuild-panel-cache` and `--rebuild-daily-ic-cache` where applicable.

Commit:
- Directory placeholders such as `.gitkeep`.
- Small documentation files that describe artifact conventions.

Do not commit:
- Generated checkpoints, model artifacts, logs, cache files, or large binary outputs.
- Signal panel caches under `artifacts/panels/`.
- Daily IC caches under `artifacts/ic/`.
- Machine-specific files from local experiments.
