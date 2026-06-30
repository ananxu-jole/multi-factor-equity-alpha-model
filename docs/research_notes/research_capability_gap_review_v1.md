# Research Capability Gap Review v1

Date: 2026-05-24

Status: `REVIEW_ROADMAP_ONLY`

## Purpose

This review targets the main weakness identified by the recent alpha research meta-review: recent OHLCV-only research branches were clean, diagnosable, and well-governed, but mostly underpowered.

The current bottleneck appears less likely to be research discipline or validation infrastructure. The more likely bottleneck is information content, metadata richness, and target definition.

Core question:

What specific capability gaps are preventing stronger alpha discovery?

This note does not implement alphas, create runners, fetch data, change schemas, modify governance, alter validation logic, change production registration, mutate survivor/watchlist state, touch detector files, or route anything into portfolio, ML, blending, or optimization.

## Recent Evidence Base

Recent parked or closed weak branches:

- Transition-State Alpha Discovery Batch
- `structural_interaction_alpha_expansion_v2`
- `proxy_relative_residual_alpha_batch_v1`
- `event_defined_liquidity_turnover_exhaustion_alpha_v1`
- exact `volatility_participation_asymmetry_20` formulation

Useful but non-deployed context infrastructure:

- Transition-State Composite Detector: `RESEARCH_CONTEXT_LAYER_OBSERVE`
- Transition-State Conditional Attribution
- Transition-State Detector Monitoring Framework

Current healthiest research evidence remains the Conditional Alpha Inventory:

- `participation_breadth_repair_under_hostile_trend`: `HEALTHY_ACTIVE_RESEARCH`
- `participation_liquidity_state_shift_20_60`: `WATCH_MONITOR`
- `volatility_compression_after_stress_stabilization`: `WATCH_MONITOR`

## Ranked Capability Gaps

### 1. Missing True Peer / Sector / Industry Metadata

Severity: `HIGH`

The project cannot currently run true sector-relative, industry-relative, or business-peer residual research. The metadata inspection found no usable sector, industry, GICS, SIC, security-master, or issuer peer-group classification layer.

Impact:

- relative-value and residual designs must use behavioral proxy buckets instead of true peers
- proxy-relative research can be structurally clean but economically blurry
- broad market, volatility, and liquidity effects are hard to separate from company-specific behavior
- peer-relative resilience, dislocation, and repair concepts cannot be tested cleanly

This is the highest-value capability gap because many recent weak branches were trying to approximate relative behavior without real peer structure.

### 2. Missing Market-Cap / Size Metadata

Severity: `HIGH`

The current framework has liquidity ranks and dynamic top-300 membership, but not a robust point-in-time market-cap or size layer.

Impact:

- liquidity effects can be mistaken for size effects
- large/liquid names may dominate residual and turnover behavior
- low-volatility and liquidity-quality candidates may hide size exposure
- true size-bucket residual research is unavailable

Liquidity buckets are not a clean substitute for market cap. A size layer would improve both alpha design and anti-failure diagnostics.

### 3. OHLCV-Only Feature Limits

Severity: `HIGH`

Recent OHLCV-only branches repeatedly produced interpretable but weak signals. The common pattern was not implementation failure; it was weak separation between economic mechanisms.

OHLCV alone struggles to distinguish:

- forced selling versus ordinary high volume
- informed participation versus noisy turnover
- sector dislocation versus broad market drawdown
- quality resilience versus low-volatility exposure
- true liquidity demand versus mechanical liquidity availability
- event-driven behavior versus routine volatility/range behavior

Impact:

- event-defined liquidity/turnover candidates fired too broadly or became sparse and unstable
- proxy-relative designs were feasible but underpowered
- structural interactions were clean but lacked standalone predictive strength

### 4. Missing Earnings / Calendar / Event Metadata

Severity: `MEDIUM_HIGH`

The project lacks a trusted event-calendar layer for earnings, corporate events, rebalances, or major scheduled information releases.

Impact:

- abnormal volume or volatility cannot be separated into scheduled versus unscheduled events
- event-defined turnover exhaustion may mix earnings-day noise with liquidity stress
- post-event repair, continuation, or normalization cannot be conditioned on event type
- sparse event concepts lack economic labels

This gap matters especially because recent event-defined work showed that "event-ness" was diagnosable but not economically sharp.

### 5. Missing Fundamental / Quality / Value / Profitability Inputs

Severity: `MEDIUM_HIGH`

Current research cannot directly test whether repair/stabilization is stronger for names with better quality, profitability, value, balance sheet, or earnings characteristics.

Impact:

- low-volatility and stability signals may accidentally proxy for quality without proving it
- "quality recovery" concepts are limited to OHLCV proxies
- current repair candidates cannot be stratified by company quality
- relative-value redesigns are incomplete

This capability would be especially valuable if Project Underdog's durable identity remains active repair/stabilization.

### 6. Missing Borrow / Short Interest / Options / Implied Volatility Inputs

Severity: `MEDIUM`

The recent branches often tried to infer stress, crowding, shock absorption, or propagation from OHLCV alone. Borrow, short interest, options, and implied volatility could identify different forms of pressure.

Impact:

- short squeeze / crowded short behavior cannot be separated from ordinary rebound
- implied versus realized volatility normalization cannot be studied
- options-market stress cannot be used to identify panic or absorption
- borrow/short pressure cannot help distinguish forced covering from durable recovery

This is likely high value but may be harder to source and normalize reliably.

### 7. Missing ETF / Benchmark / Peer Mapping

Severity: `MEDIUM`

The project uses benchmark-relative residual patterns, but does not appear to have a broader mapping layer for sector ETFs, industry ETFs, factor ETFs, or custom peer benchmarks.

Impact:

- benchmark residuals are too broad
- sector/factor-relative behavior cannot be decomposed
- market beta, sector beta, and idiosyncratic behavior remain blurred
- ETF-flow or sector-stress effects cannot be separated from single-name behavior

### 8. Target Definition May Be Too Narrow

Severity: `HIGH`

Most recent discovery asked whether a signal can produce cross-sectional IC on raw forward returns at h10/h20. That is clean and disciplined, but may be too narrow for some evidence types.

Potential issue:

- transition-state detectors may explain when existing alphas work, not directly predict returns
- repair/stabilization candidates may reduce downside or improve recovery quality more than maximize raw average IC
- some mechanisms may be useful as context/risk layers, not standalone alphas

Target alternatives worth designing, not implementing yet:

- drawdown-adjusted forward return
- downside-tail avoidance
- recovery-quality target after stress
- conditional long-short hit rate by state
- alpha drawdown clustering reduction
- regime-conditioned IC target

This does not mean loosening validation. It means defining what the research question actually is before more batches.

## Metadata Limitations

True sector-relative research is currently not feasible. The project has dynamic liquidity membership, OHLCV panels, cross-sectional ranks, benchmark-relative residuals, and simple neutralization helpers, but no reliable economic peer classification.

Proxy-relative research showed the limitation clearly:

- liquidity, volatility, beta-like, residual-volatility, turnover, and market-relative buckets can be built
- bucket coverage and diagnostics can be healthy
- but proxy buckets do not supply enough economic identity
- proxy normalization improved cleanliness, not standalone predictive strength

Bucket drift was not the main observed blocker in the proxy-relative batch. The larger issue was weak economic specificity. The buckets were stable enough to diagnose, but not meaningful enough to create stronger alpha.

## Target-Definition Limitations

Raw h10/h20 forward-return IC should remain the primary test for standalone alpha, but not every useful research artifact should be forced into that role.

Current evidence suggests three different object types:

1. Standalone alphas
   - must pass h10/h20 IC, persistence, overlap, and fragility standards

2. Context layers
   - should explain when existing alphas work, fail, or draw down
   - Transition-State Composite Detector belongs here

3. Risk / recovery diagnostics
   - may be useful if they identify downside clustering, recovery quality, or state-dependent fragility
   - should not be promoted as alphas without a separate target design

The current research process is strongest at evaluating object type 1. It now needs a clearer design protocol for object types 2 and 3 so they are not overclaimed or discarded incorrectly.

## Feature-Library Limitations

Recent feature families are over-concentrated in OHLCV repair/stabilization:

- volatility compression
- liquidity repair
- turnover exhaustion
- participation quality
- breadth repair
- shock absorption
- range/volume stabilization
- residual volatility behavior

The diagnostics are strong enough to show repeated failure modes:

- broad activation with weak IC
- h5 hints that do not carry to h10/h20
- weak standalone behavior despite low overlap
- liquidity / low-volatility duplication
- true interaction behavior that becomes brittle under tighter filters

The issue is not that the feature library is poorly engineered. It is that the library is now repeatedly recombining the same information channels.

## Inventory Limitations

Current inventory remains the healthiest evidence base, but it has known concentration risks:

- all three inventory candidates remain h20-centered
- all three are hostile/stress or repair/stabilization dependent
- co-activation remains concentrated between participation/liquidity and breadth repair
- two candidates remain `WATCH_MONITOR`

The healthiest candidate is `participation_breadth_repair_under_hostile_trend`. The WATCH_MONITOR candidates should not be over-refined or used as justification for construction-layer work.

Before more discovery, the inventory needs:

- continued monitoring
- recent-window drift tracking
- active-window drift checks
- co-activation drift checks
- rebuild/equivalence checks
- explicit acceptance of WATCH_MONITOR risks

## Infrastructure Gaps

The project does not need more generic infrastructure before more alpha work. It already has strong research runners, diagnostics, manifests, guardrails, monitoring notes, governance notes, and closeout discipline.

Infrastructure gaps worth considering only because they support richer research:

1. Metadata ingestion and lineage layer
   - needed for sector/industry, market cap, and event calendars

2. Point-in-time metadata coverage diagnostics
   - needed to avoid look-ahead, stale classification, and survivorship artifacts

3. Target-definition evaluation utilities
   - needed only after target definitions are formally designed

Avoid building broad infrastructure for its own sake.

## Ranked Capability Upgrade Roadmap

### 1. Trustworthy Sector / Industry / Peer Metadata Layer

Expected research value: `VERY_HIGH`

Purpose:

- enable true sector-relative and industry-relative residual research
- reduce reliance on proxy buckets
- separate broad market effects from comparable-company behavior

Minimum requirements:

- ticker
- classification date or effective date
- sector
- industry or subindustry
- source
- source version
- coverage diagnostics
- stale/missing classification flags

This should be research-only first.

### 2. Market-Cap / Size Layer

Expected research value: `HIGH`

Purpose:

- separate liquidity from size
- improve peer grouping
- control hidden size exposure
- support size-relative repair and resilience diagnostics

Minimum requirements:

- point-in-time or date-stamped market cap
- split-adjustment consistency review
- dynamic universe coverage
- size-bucket diagnostics

### 3. Target-Definition Review

Expected research value: `HIGH`

Purpose:

- decide when raw h10/h20 IC is the right target
- define separate standards for context layers and risk/recovery diagnostics
- prevent useful context tools from being misclassified as failed alphas
- prevent weak alphas from being relabeled as context without evidence

This can be done before new external data, but should be informed by the current inventory and detector evidence.

### 4. Current Inventory Robustness Deep Dive

Expected research value: `MEDIUM_HIGH`

Purpose:

- determine whether the current inventory is robust enough to remain the anchor while capability upgrades are built
- review WATCH_MONITOR candidates more deeply
- check active-window drift, co-activation drift, recent-window fragility, and rebuild equivalence

This should not become a refinement pass unless monitoring identifies a concrete governance need.

### 5. Earnings / Calendar Event Layer

Expected research value: `MEDIUM_HIGH`

Purpose:

- separate scheduled information events from unscheduled stress
- improve interpretation of volume/turnover shocks
- enable event-conditioned repair/stabilization research

This is likely the best next enrichment after sector/size metadata if event-defined alpha research remains attractive.

### 6. Fundamentals / Quality / Value / Profitability Data Plan

Expected research value: `MEDIUM_HIGH`

Purpose:

- distinguish quality repair from low-volatility or liquidity effects
- build quality-conditioned repair/stabilization candidates
- test whether current repair edges are stronger in fundamentally resilient names

This may require more sourcing, normalization, and point-in-time discipline than sector or size metadata.

### 7. Borrow / Short Interest / Options / Implied Volatility Plan

Expected research value: `MEDIUM`

Purpose:

- distinguish crowding, squeeze, panic, and volatility-risk behavior

This should be considered later unless sourcing is already available.

## Immediate Next Action Recommendation

Do not launch another OHLCV-only alpha discovery batch immediately.

Recommended next step:

Create a research-only metadata enrichment plan focused first on sector/industry/peer metadata and market-cap/size metadata.

The plan should answer:

- what data source or existing internal file can provide classification and size data
- whether the data can be made point-in-time or only current snapshot
- what coverage exists for the current universe and dynamic top-300 membership
- what stale/missing classification risks exist
- what tables or artifacts would be needed
- what diagnostics would prevent look-ahead and survivorship misuse
- what first research batch would become possible after enrichment

Parallel but lower priority:

- perform a target-definition design review for standalone alpha versus context layer versus risk/recovery diagnostics
- continue regular Conditional Alpha Inventory monitoring

In plain terms: fix one information-content gap before asking the current OHLCV feature library to produce another round of standalone alphas.

## What Not To Do Next

Do not immediately run:

- another structural interaction batch
- another proxy-relative bucket batch
- another event-defined liquidity/turnover batch
- another h5/h10 transition-state micro-signal batch
- stricter threshold refinements of parked weak clues

Do not convert context evidence into alpha claims.

Do not lower standards to keep research momentum.

## Intentional Non-Changes

This review did not:

- implement new alpha candidates
- create signal runners
- fetch external data
- modify detector files
- change schemas, gates, thresholds, governance, or validation logic
- change production registration
- mutate survivor/watchlist state
- route anything into portfolio, ML, blending, or optimization

