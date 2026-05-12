<!-- source: https://silviobaratto.github.io/optimizer/guide/universe/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/universe/#universe-screening)
# Universe Screening[¶](https://silviobaratto.github.io/optimizer/guide/universe/#universe-screening "Permanent link")
The universe module implements investability screening with hysteresis-based entry/exit thresholds. It filters a raw stock universe down to securities that meet minimum standards of market capitalization, liquidity, price level, listing history, and data availability — the foundation for any systematic investment strategy.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/universe/#overview "Permanent link")
Before constructing a portfolio, you need a clean investable universe. Stocks that are too small, too illiquid, or too newly listed create problems: they may be impossible to trade at the quantities needed, they generate excessive transaction costs, or they lack sufficient history for reliable estimation.
The universe module enforces investability standards through 8 screens, each with separate entry and exit thresholds (hysteresis) to reduce turnover at screen boundaries.
### Why Hysteresis?[¶](https://silviobaratto.github.io/optimizer/guide/universe/#why-hysteresis "Permanent link")
Without hysteresis, a stock hovering near a threshold (e.g., market cap of $199M vs $201M) would oscillate in and out of the universe each month. Hysteresis sets a lower exit threshold than the entry threshold — once a stock enters the universe, it stays until it drops below a more lenient exit level.

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-0-1)Entry threshold:  $200M ─────────────────
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-0-2)                                          │ Stock enters here
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-0-3)Exit threshold:   $150M ─────────────────
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-0-4)                          │ Stock exits here

```

## HysteresisConfig[¶](https://silviobaratto.github.io/optimizer/guide/universe/#hysteresisconfig "Permanent link")
Each screen uses a `HysteresisConfig` with entry and exit thresholds:

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-1)from optimizer.universe import HysteresisConfig
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-3)config = HysteresisConfig(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-4)    entry=200_000_000,  # must exceed to enter
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-5)    exit_=150_000_000,  # must drop below to exit
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-1-6))

```
  
| Field  | Type  | Description  |  
| --- | --- | --- |  
| `entry`  | `float`  | Threshold a stock must exceed to enter the universe  |  
| `exit_`  | `float`  | Threshold below which a current member is removed  |  
exit_ must be <= entry
The exit threshold must be less than or equal to the entry threshold. This is enforced at construction time.
## InvestabilityScreenConfig[¶](https://silviobaratto.github.io/optimizer/guide/universe/#investabilityscreenconfig "Permanent link")
The main configuration holds all 8 screen thresholds plus listing requirements:

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-1)from optimizer.universe import InvestabilityScreenConfig
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-3)config = InvestabilityScreenConfig(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-4)    market_cap=HysteresisConfig(entry=200_000_000, exit_=150_000_000),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-5)    addv_12m=HysteresisConfig(entry=750_000, exit_=500_000),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-6)    addv_3m=HysteresisConfig(entry=500_000, exit_=350_000),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-7)    trading_frequency=HysteresisConfig(entry=0.95, exit_=0.90),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-8)    price_us=HysteresisConfig(entry=3.0, exit_=2.0),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-9)    price_europe=HysteresisConfig(entry=2.0, exit_=1.5),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-10)    min_trading_history=252,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-11)    min_ipo_seasoning=60,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-12)    min_annual_reports=3,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-13)    min_quarterly_reports=8,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-14)    exchange_region=ExchangeRegion.US,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-15)    mcap_percentile_entry=0.10,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-16)    mcap_percentile_exit=0.075,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-2-17))

```

### Screen Details[¶](https://silviobaratto.github.io/optimizer/guide/universe/#screen-details "Permanent link")  
| Screen  | Default Entry  | Default Exit  | Description  |  
| --- | --- | --- | --- |  
| `market_cap`  | $200M  | $150M  | Free-float market capitalization (USD)  |  
| `addv_12m`  | $750K  | $500K  | 12-month average daily dollar volume  |  
| `addv_3m`  | $500K  | $350K  | 3-month average daily dollar volume  |  
| `trading_frequency`  | 95%  | 90%  | Fraction of trading days with nonzero volume  |  
| `price_us`  | $3.00  | $2.00  | Minimum price for US equities  |  
| `price_europe`  | $2.00  | $1.50  | Minimum price for European equities  |  
| `mcap_percentile_entry`  | 10th  | 7.5th  | Exchange-relative market cap percentile  |  
### Non-Hysteresis Requirements[¶](https://silviobaratto.github.io/optimizer/guide/universe/#non-hysteresis-requirements "Permanent link")  
| Requirement  | Default  | Description  |  
| --- | --- | --- |  
| `min_trading_history`  | 252 days  | Minimum trading days of price history  |  
| `min_ipo_seasoning`  | 60 days  | Minimum days since first price observation  |  
| `min_annual_reports`  | 3  | Minimum annual financial statements  |  
| `min_quarterly_reports`  | 8  | Minimum quarterly financial statements  |  
| `exchange_region`  | `US`  | Region for price threshold selection  |  
### Exchange Percentile Screen[¶](https://silviobaratto.github.io/optimizer/guide/universe/#exchange-percentile-screen "Permanent link")
The exchange percentile screen adds a relative dimension to the absolute market cap floor. A stock must exceed **both** the absolute market cap threshold **and** the percentile rank within its exchange to enter the universe. This prevents very small stocks from entering when listed on exchanges with low median capitalizations.
## Presets[¶](https://silviobaratto.github.io/optimizer/guide/universe/#presets "Permanent link")  
| Preset  | Market Cap Entry  | ADDV 12m Entry  | Use Case  |  
| --- | --- | --- | --- |  
| `for_developed_markets()`  | $200M  | $750K  | Institutional-grade, strict liquidity  |  
| `for_broad_universe()`  | $100M  | $500K  | Broader coverage, relaxed thresholds  |  
| `for_small_cap()`  | $50M  | $250K  | Small-cap research, minimal screens  |  
### Preset Details[¶](https://silviobaratto.github.io/optimizer/guide/universe/#preset-details "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-1)# Strict institutional universe
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-2)config = InvestabilityScreenConfig.for_developed_markets()
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-3)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-4)# Broader coverage
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-5)config = InvestabilityScreenConfig.for_broad_universe()
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-6)# Relaxes: mcap to $100M, ADDV to $500K, history to 126 days, etc.
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-7)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-8)# Small-cap
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-9)config = InvestabilityScreenConfig.for_small_cap()
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-3-10)# Relaxes: mcap to $50M, ADDV to $250K, price to $1.00, etc.

```

## Screening Functions[¶](https://silviobaratto.github.io/optimizer/guide/universe/#screening-functions "Permanent link")
### screen_universe (main entry point)[¶](https://silviobaratto.github.io/optimizer/guide/universe/#screen_universe-main-entry-point "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-1)from optimizer.universe import screen_universe, InvestabilityScreenConfig
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-3)investable = screen_universe(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-4)    fundamentals=fundamentals_df,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-5)    price_history=price_df,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-6)    volume_history=volume_df,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-7)    financial_statements=statements_df,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-8)    config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-9)    current_members=None,  # pd.Index for hysteresis
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-10))
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-11)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-12)print(f"Investable universe: {len(investable)} stocks")
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-4-13)print(investable)  # pd.Index of passing tickers

```
  
| Parameter  | Type  | Description  |  
| --- | --- | --- |  
| `fundamentals`  | `pd.DataFrame`  | Cross-sectional data indexed by ticker  |  
| `price_history`  | `pd.DataFrame`  | Price matrix (dates x tickers)  |  
| `volume_history`  | `pd.DataFrame`  | Volume matrix (dates x tickers)  |  
| `financial_statements`  |  `pd.DataFrame` or `None`  | Statement-level data  |  
| `config`  |  `InvestabilityScreenConfig` or `None`  | Screening config  |  
| `current_members`  |  `pd.Index` or `None`  | Current universe for hysteresis  |  
### Lower-level functions[¶](https://silviobaratto.github.io/optimizer/guide/universe/#lower-level-functions "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-1)from optimizer.universe import (
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-2)    apply_investability_screens,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-3)    compute_addv,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-4)    compute_listing_age,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-5)    compute_trading_frequency,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-6)    count_financial_statements,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-7)    compute_exchange_mcap_percentile_thresholds,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-8))
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-9)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-10)# Compute individual metrics
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-11)addv = compute_addv(price_history, volume_history, window=252)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-12)listing_age = compute_listing_age(price_history)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-5-13)freq = compute_trading_frequency(volume_history, window=252)

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/universe/#code-examples "Permanent link")
### Basic universe screening[¶](https://silviobaratto.github.io/optimizer/guide/universe/#basic-universe-screening "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-1)from optimizer.universe import screen_universe, InvestabilityScreenConfig
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-2)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-3)investable = screen_universe(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-4)    fundamentals=fundamentals,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-5)    price_history=prices,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-6)    volume_history=volume,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-7)    config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-8))
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-9)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-10)# Use investable universe for optimization
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-6-11)selected_prices = prices[prices.columns.intersection(investable)]

```

### Screening with hysteresis[¶](https://silviobaratto.github.io/optimizer/guide/universe/#screening-with-hysteresis "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-3)# First month: no current members
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-4)month1_universe = screen_universe(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-5)    fundamentals=fundamentals_jan,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-6)    price_history=prices_jan,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-7)    volume_history=volume_jan,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-8)    config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-9)    current_members=None,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-10))
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-11)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-12)# Second month: pass previous universe for hysteresis
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-13)month2_universe = screen_universe(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-14)    fundamentals=fundamentals_feb,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-15)    price_history=prices_feb,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-16)    volume_history=volume_feb,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-17)    config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-18)    current_members=month1_universe,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-7-19))

```

### Full pipeline with universe screening[¶](https://silviobaratto.github.io/optimizer/guide/universe/#full-pipeline-with-universe-screening "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-1)from optimizer.pipeline import run_full_pipeline_with_selection
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-2)from optimizer.universe import InvestabilityScreenConfig
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-3)
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-4)result = run_full_pipeline_with_selection(
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-5)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-6)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-7)    fundamentals=fundamentals,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-8)    volume_history=volume,
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-9)    investability_config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-10)    scoring_config=CompositeScoringConfig(),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-11)    selection_config=SelectionConfig(n_stocks=100),
[](https://silviobaratto.github.io/optimizer/guide/universe/#__codelineno-8-12))

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/universe/#gotchas-and-tips "Permanent link")
fundamentals DataFrame must be indexed by ticker
The `fundamentals` DataFrame should have tickers as the index, with columns for `market_cap`, `price`, and optionally `exchange` (for percentile screening).
Pass current_members for turnover reduction
Without `current_members`, every screening round applies entry thresholds to all stocks. Passing the previous universe enables hysteresis — existing members use the more lenient exit thresholds, reducing unnecessary churn.
Exchange percentile requires 'exchange' column
The exchange percentile screen requires an `exchange` column in the `fundamentals` DataFrame. Without it, only the absolute market cap floor is applied.
Combine with factor selection
Universe screening and factor selection are complementary: screening ensures investability, while factor selection picks the best stocks from the investable universe. Use `run_full_pipeline_with_selection()` to chain both steps.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/universe/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Developed markets  | `InvestabilityScreenConfig.for_developed_markets()`  |  
| Broad universe  | `InvestabilityScreenConfig.for_broad_universe()`  |  
| Small-cap  | `InvestabilityScreenConfig.for_small_cap()`  |  
| Screen universe  | `screen_universe(fundamentals, prices, volume, config=cfg)`  |  
| With hysteresis  | `screen_universe(..., current_members=prev_universe)`  |  
| Compute ADDV  | `compute_addv(prices, volume, window=252)`  |  
| Listing age  | `compute_listing_age(prices)`  |  
| Trading frequency  | `compute_trading_frequency(volume, window=252)`  |
