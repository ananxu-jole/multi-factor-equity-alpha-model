from __future__ import annotations

import numpy as np
import pandas as pd


PHASE2_TEST_UNIVERSE = [
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOGL",
    "META",
    "NVDA",
    "BRK-B",
    "JPM",
    "V",
    "MA",
    "UNH",
    "HD",
    "PG",
    "XOM",
    "CVX",
    "LLY",
    "ABBV",
    "PEP",
    "KO",
    "COST",
    "MRK",
    "AVGO",
    "WMT",
    "BAC",
    "ADBE",
    "CRM",
    "NFLX",
    "MCD",
    "TMO",
    "ACN",
]

PHASE2_FULL_UNIVERSE = [
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOGL",
    "META",
    "NVDA",
    "BRK-B",
    "JPM",
    "V",
    "MA",
    "UNH",
    "HD",
    "PG",
    "XOM",
    "CVX",
    "LLY",
    "ABBV",
    "PEP",
    "KO",
    "COST",
    "MRK",
    "AVGO",
    "WMT",
    "BAC",
    "ADBE",
    "CRM",
    "NFLX",
    "MCD",
    "TMO",
    "ACN",
    "AMD",
    "ABT",
    "ORCL",
    "CSCO",
    "QCOM",
    "INTU",
    "TXN",
    "IBM",
    "CAT",
    "DHR",
    "GE",
    "AMGN",
    "ISRG",
    "BKNG",
    "NOW",
    "GS",
    "MS",
    "BLK",
    "AXP",
    "SCHW",
    "PGR",
    "SPGI",
    "MMC",
    "TJX",
    "LOW",
    "CMCSA",
    "TMUS",
    "DIS",
    "UBER",
    "LIN",
    "NEE",
    "DUK",
    "SO",
    "HON",
    "UNP",
    "RTX",
    "LMT",
    "BA",
    "DE",
    "ETN",
    "COP",
    "SLB",
    "EOG",
    "VRTX",
    "ADP",
    "PANW",
    "CRWD",
    "PLTR",
    "SNOW",
    "ANET",
    "MU",
    "KLAC",
    "LRCX",
    "AMAT",
    "ADI",
    "MDT",
    "BSX",
    "SYK",
    "CI",
    "ELV",
    "C",
    "WFC",
    "CB",
    "ICE",
    "MO",
    "PM",
    "MDLZ",
    "SBUX",
    "GILD",
    "REGN",
    "PFE",
]

CURRENT_LARGE_LIQUID_POOL_TICKERS_TEXT = """
A AAPL ABBV ABNB ABT ACGL ACN ADBE ADI ADM ADP ADSK AEE AEP AES AFL AIG AIZ AJG AKAM ALB ALGN
ALL ALLE AMAT AMCR AMD AME AMGN AMP AMT AMZN ANET ANSS AON AOS APA APD APH APO APTV ARE ATO AVB
AVGO AVY AWK AXON AXP AZO BA BAC BALL BAX BBY BDx? BDX BEN BG BIIB BK BKNG BKR BLK BMY BR BRK-B BRO BSX
BWA BX BXP C CAG CAH CARR CAT CB CBOE CBRE CCI CCL CDNS CDW CE CEG CF CFG CHD CHRW CHTR CI CINF CL
CLX CMCSA CME CMG CMI CMS CNC CNP COF COO COP COR COST CPAY CPRT CPT CRL CRM CRWD CSCO CSGP CSX CTAS
CTLT CTRA CTSH CTVA CVS CVX CZR D DAL DAY DD DE DECK DELL DFS DG DGX DHI DHR DIS DLR DLTR DOC DOV
DOW DPZ DRI DTE DUK DVA DVN DXCM EA EBAY ECL ED EFX EG EIX EL ELV EMN EMR ENPH EOG EPAM EQIX EQR
EQT ES ESS ETN ETR EVRG EW EXC EXPD EXPE F FANG FAST FCX FDS FDX FE FFIV FI FICO FIS FITB FOX FOXA
FRT FSLR FTNT FTV GD GE GEV GILD GIS GL GLW GM GNRC GOOG GOOGL GPC GPN GRMN GS GWW HAL HAS HBAN
HCA HD HES HIG HII HLT HOLX HON HPE HPQ HRL HSIC HST HSY HUBB HUM HWM IBM ICE IDXX IEX IFF INCY
INTC INTU INVH IP IPG IQV IR IRM ISRG IT ITW IVZ J JBHT JBL JCI JKHY JNJ JNPR JPM K KDP KEY KEYS
KHC KIM KKR KLAC KMB KMI KMX KO KR KVUE L LDOS LEN LH LHX LIN LKQ LLY LMT LNT LOW LRCX LULU LUV
LVS LW LYB LYV MA MAA MAR MAS MCD MCHP MCK MCO MDLZ MDT MET META MGM MHK MKC MKTX MLM MMC MMM
MNST MO MOH MOS MPC MPWR MRK MRNA MS MSCI MSFT MSI MTB MTCH MTD MU NCLH NDAQ NDSN NEE NEM NFLX NI
NKE NOC NOW NRG NSC NTAP NTRS NUE NVDA NVR NWS NWSA NXPI O ODFL OKE OMC ON ORCL ORLY OTIS OXY
PANW PAYC PAYX PCAR PCG PEG PEP PFE PFG PG PGR PH PHM PKG PLD PLTR PM PNC PNR PNW PODD POOL PPG
PPL PRU PSA PSX PTC PYPL QCOM QRVO RCL REG REGN RF RMD ROK ROL ROP ROST RSG RTX RVTY SBAC SBUX
SCHW SHW SJM SLB SMCI SNA SNPS SO SOLV SPG SPGI SRE STE STLD STT STX STZ SWK SWKS SYF SYK SYY
T TAP TDG TDY TECH TEL TER TFC TFX TGT TJX TMO TMUS TPR TRGP TRMB TROW TRV TSCO TSLA TSN TT TTWO
TXN TXT TYL UAL UBER UDR UHS ULTA UNH UNP UPS URI USB V VICI VLO VLTO VMC VRSK VRSN VRTX VST VTR
VTRS VZ WAB WAT WBA WBD WDC WEC WELL WFC WM WMB WMT WRB WST WTW WY WYNN XEL XOM XYL YUM ZBH ZBRA
ZTS
""".replace("BDx?", "BDX")

BENCHMARK_TICKERS = ["SPY"]
PHASE2_TEST_UNIVERSE_NAME = "phase2_test_equity_universe"
PHASE2_FULL_UNIVERSE_NAME = "phase2_full_equity_universe"
PHASE2_TEST_UNIVERSE_VERSION = "phase2_test_v1_30"
PHASE2_FULL_UNIVERSE_VERSION = "phase2_full_v1_101_largecap"
RAW_TICKER_POOL_MODE = "current_large_liquid_pool_v1"
RAW_TICKER_POOL_VERSION = "current_large_liquid_pool_v1"
DYNAMIC_TOP300_LIQUIDITY_MODE = "dynamic_top300_liquidity"
DYNAMIC_TOP300_AVAILABLE_POOL_MODE = "dynamic_top300_from_current_large_liquid_pool"
DYNAMIC_TOP300_LIQUIDITY_VERSION = "dynamic_top300_from_current_large_liquid_pool_v1"
UNIVERSE_LIMITATION_NOTE = (
    "Dynamic top-300 liquidity selection is applied to a current large/liquid ticker pool. "
    "This is useful for engineering robustness testing, but not fully survivorship-free. "
    "A fully survivorship-free test requires historical constituent membership or a point-in-time security master."
)
VALID_PHASE2_UNIVERSE_MODES = {"test", "full", DYNAMIC_TOP300_LIQUIDITY_MODE}


def get_benchmark_tickers() -> list[str]:
    return BENCHMARK_TICKERS.copy()


def _validate_phase2_universe_mode(mode: str) -> str:
    normalized_mode = mode.strip().lower()
    if normalized_mode not in VALID_PHASE2_UNIVERSE_MODES:
        valid_modes = ", ".join(sorted(VALID_PHASE2_UNIVERSE_MODES))
        raise ValueError(f"Unsupported Phase 2 universe mode '{mode}'. Expected one of: {valid_modes}.")
    return normalized_mode


def get_phase2_test_universe() -> list[str]:
    return PHASE2_TEST_UNIVERSE.copy()


def get_phase2_full_universe() -> list[str]:
    return PHASE2_FULL_UNIVERSE.copy()


def get_current_large_liquid_pool_tickers() -> list[str]:
    """Return a de-duplicated current large/liquid US equity raw ticker pool."""
    tickers = CURRENT_LARGE_LIQUID_POOL_TICKERS_TEXT.split()
    return list(dict.fromkeys(tickers))


def get_phase2_stock_universe(mode: str = "test") -> list[str]:
    normalized_mode = _validate_phase2_universe_mode(mode)
    if normalized_mode == "test":
        return get_phase2_test_universe()
    if normalized_mode == DYNAMIC_TOP300_LIQUIDITY_MODE:
        return get_current_large_liquid_pool_tickers()
    return get_phase2_full_universe()


def get_phase2_all_tickers(mode: str = "test", include_benchmarks: bool = True) -> list[str]:
    tickers = get_phase2_stock_universe(mode=mode)
    if include_benchmarks:
        tickers.extend(get_benchmark_tickers())
    return tickers


def get_raw_ticker_pool_metadata(
    mode: str = RAW_TICKER_POOL_MODE,
    limitation_note: str = UNIVERSE_LIMITATION_NOTE,
) -> pd.DataFrame:
    if mode != RAW_TICKER_POOL_MODE:
        raise ValueError(f"Unsupported raw ticker pool mode '{mode}'.")
    records = [
        {
            "ticker": ticker,
            "source_pool": RAW_TICKER_POOL_MODE,
            "inclusion_reason": "Current large/liquid US equity common-stock engineering pool.",
            "raw_pool_version": RAW_TICKER_POOL_VERSION,
            "limitation_note": limitation_note,
        }
        for ticker in get_current_large_liquid_pool_tickers()
    ]
    return pd.DataFrame.from_records(records).sort_values("ticker").reset_index(drop=True)


def get_phase2_universe_metadata(mode: str = "test", include_benchmarks: bool = True) -> pd.DataFrame:
    normalized_mode = _validate_phase2_universe_mode(mode)
    records: list[dict[str, object]] = []
    if normalized_mode == "test":
        universe_name = PHASE2_TEST_UNIVERSE_NAME
        universe_version = PHASE2_TEST_UNIVERSE_VERSION
        universe_note = "30-stock smoke-test universe carried forward from Phase 1."
    elif normalized_mode == DYNAMIC_TOP300_LIQUIDITY_MODE:
        universe_name = DYNAMIC_TOP300_AVAILABLE_POOL_MODE
        universe_version = DYNAMIC_TOP300_LIQUIDITY_VERSION
        universe_note = UNIVERSE_LIMITATION_NOTE
    else:
        universe_name = PHASE2_FULL_UNIVERSE_NAME
        universe_version = PHASE2_FULL_UNIVERSE_VERSION
        universe_note = "Expanded Phase 2 research universe for full-run coverage."

    for ticker in get_phase2_stock_universe(mode=normalized_mode):
        records.append(
            {
                "ticker": ticker,
                "source": f"phase2_universe_module_{normalized_mode}",
                "universe_name": universe_name,
                "universe_version": universe_version,
                "active": True,
                "notes": universe_note,
            }
        )

    if include_benchmarks:
        for ticker in get_benchmark_tickers():
            records.append(
                {
                    "ticker": ticker,
                    "source": "benchmark_default",
                    "universe_name": "phase2_benchmark",
                    "universe_version": universe_version,
                    "active": True,
                    "notes": "Benchmark ticker for market reference.",
                }
            )

    universe_df = pd.DataFrame.from_records(records)
    universe_df = universe_df.sort_values(["universe_name", "ticker"]).reset_index(drop=True)

    return universe_df


def build_dynamic_liquidity_universe_mask(
    close_prices: pd.DataFrame,
    volume: pd.DataFrame,
    top_n: int = 300,
    adv_window: int = 20,
    min_price: float = 5.0,
    min_valid_obs: int = 15,
    shift_membership: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build a trailing-liquidity universe mask with no same-day membership look-ahead.

    Membership is ranked from trailing 20-day average dollar volume, computed from
    close * volume. When shift_membership=True, the returned mask is shifted by one
    trading day so same-day close/volume cannot decide same-day eligibility.
    """
    if top_n <= 0:
        raise ValueError("top_n must be positive.")
    if adv_window <= 0:
        raise ValueError("adv_window must be positive.")
    if min_valid_obs <= 0:
        raise ValueError("min_valid_obs must be positive.")
    if not isinstance(close_prices.index, pd.DatetimeIndex):
        raise TypeError("close_prices must use a DatetimeIndex.")
    if not isinstance(volume.index, pd.DatetimeIndex):
        raise TypeError("volume must use a DatetimeIndex.")

    close_aligned, volume_aligned = close_prices.align(volume, join="inner", axis=0)
    close_aligned, volume_aligned = close_aligned.align(volume_aligned, join="inner", axis=1)
    close_aligned = close_aligned.sort_index().sort_index(axis=1)
    volume_aligned = volume_aligned.sort_index().sort_index(axis=1)

    dollar_volume = close_aligned * volume_aligned
    finite_inputs = close_aligned.notna() & volume_aligned.notna()
    adv20 = dollar_volume.where(finite_inputs).rolling(adv_window, min_periods=min_valid_obs).mean()
    valid_obs = finite_inputs.rolling(adv_window, min_periods=1).sum()
    liquid_eligible = (
        close_aligned.ge(min_price)
        & close_aligned.notna()
        & volume_aligned.notna()
        & adv20.gt(0)
        & valid_obs.ge(min_valid_obs)
    )
    ranks = adv20.where(liquid_eligible).rank(axis=1, method="first", ascending=False)
    raw_mask = ranks.le(top_n) & liquid_eligible
    trading_mask = raw_mask.shift(1, fill_value=False) if shift_membership else raw_mask
    selected_adv20 = adv20.shift(1) if shift_membership else adv20

    diagnostics = pd.DataFrame(
        {
            "Date": close_aligned.index,
            "n_available_tickers": finite_inputs.sum(axis=1).astype(int).values,
            "n_liquid_eligible_tickers": liquid_eligible.sum(axis=1).astype(int).values,
            "n_selected_tickers": trading_mask.sum(axis=1).astype(int).values,
            "median_adv20": adv20.median(axis=1, skipna=True).values,
            "min_selected_adv20": selected_adv20.where(trading_mask).min(axis=1, skipna=True).values,
            "max_selected_adv20": selected_adv20.where(trading_mask).max(axis=1, skipna=True).values,
            "pct_missing_close": close_aligned.isna().mean(axis=1).values,
            "pct_missing_volume": volume_aligned.isna().mean(axis=1).values,
            "shift_membership": bool(shift_membership),
            "adv_window": int(adv_window),
            "top_n": int(top_n),
            "min_price": float(min_price),
            "min_valid_obs": int(min_valid_obs),
            "universe_mode": DYNAMIC_TOP300_LIQUIDITY_MODE,
            "universe_version": DYNAMIC_TOP300_LIQUIDITY_VERSION,
            "limitation_note": UNIVERSE_LIMITATION_NOTE,
        }
    )

    return trading_mask.astype(bool), diagnostics


def build_dynamic_liquidity_membership_table(
    close_prices: pd.DataFrame,
    volume: pd.DataFrame,
    universe_mask: pd.DataFrame,
    top_n: int = 300,
    adv_window: int = 20,
    min_valid_obs: int = 15,
    shift_membership: bool = True,
    universe_mode: str = DYNAMIC_TOP300_LIQUIDITY_MODE,
    universe_version: str = DYNAMIC_TOP300_LIQUIDITY_VERSION,
) -> pd.DataFrame:
    """Build a storage-efficient selected-membership table for dynamic top-N liquidity."""
    close_aligned, volume_aligned = close_prices.align(volume, join="inner", axis=0)
    close_aligned, volume_aligned = close_aligned.align(volume_aligned, join="inner", axis=1)
    mask = universe_mask.reindex(index=close_aligned.index, columns=close_aligned.columns, fill_value=False)

    dollar_volume = close_aligned * volume_aligned
    adv20 = dollar_volume.where(close_aligned.notna() & volume_aligned.notna()).rolling(
        adv_window,
        min_periods=min_valid_obs,
    ).mean()
    ranks = adv20.where(adv20.gt(0)).rank(axis=1, method="first", ascending=False)
    selection_adv20 = adv20.shift(1) if shift_membership else adv20
    selection_ranks = ranks.shift(1) if shift_membership else ranks

    records = []
    selected_positions = np.where(mask.to_numpy(dtype=bool))
    dates = close_aligned.index.to_numpy()
    tickers = close_aligned.columns.to_numpy()
    for row_idx, col_idx in zip(*selected_positions):
        date = dates[row_idx]
        ticker = tickers[col_idx]
        records.append(
            {
                "Date": pd.Timestamp(date),
                "ticker": str(ticker),
                "in_universe": True,
                "adv20": selection_adv20.iat[row_idx, col_idx],
                "close": close_aligned.iat[row_idx, col_idx],
                "volume": volume_aligned.iat[row_idx, col_idx],
                "universe_rank": selection_ranks.iat[row_idx, col_idx],
                "universe_mode": universe_mode,
                "universe_version": universe_version,
            }
        )

    return pd.DataFrame.from_records(
        records,
        columns=[
            "Date",
            "ticker",
            "in_universe",
            "adv20",
            "close",
            "volume",
            "universe_rank",
            "universe_mode",
            "universe_version",
        ],
    )


def apply_universe_mask_to_panels(
    panels: dict[str, pd.DataFrame],
    universe_mask: pd.DataFrame,
    benchmark_tickers: list[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Apply a dynamic stock universe mask to OHLCV panels while preserving benchmarks."""
    benchmark_tickers = list(benchmark_tickers or [])
    masked: dict[str, pd.DataFrame] = {}
    for name, panel in panels.items():
        mask = universe_mask.reindex(index=panel.index, columns=panel.columns, fill_value=False)
        benchmark_columns = [ticker for ticker in benchmark_tickers if ticker in panel.columns]
        if benchmark_columns:
            mask.loc[:, benchmark_columns] = True
        masked[name] = panel.where(mask).copy()
    return masked
