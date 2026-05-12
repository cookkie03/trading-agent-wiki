<!-- source: https://silviobaratto.github.io/optimizer/api/universe/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/universe/#universe)
# universe[¶](https://silviobaratto.github.io/optimizer/api/universe/#universe "Permanent link")
###  `optimizer.universe` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe "Permanent link")
Investability screening for stock universe construction.
####  `ExchangeRegion` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.ExchangeRegion "Permanent link")
Bases: `str`, `Enum`
Exchange region for region-specific screening thresholds.
####  `HysteresisConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.HysteresisConfig "Permanent link")
Entry/exit thresholds with hysteresis to reduce turnover.
Setting exit below entry prevents marginal stocks from oscillating in and out of the universe with small fluctuations.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.HysteresisConfig--parameters "Permanent link")
entry : float Threshold a stock must exceed to enter the universe. exit_ : float Threshold below which a current member is removed. Must be <= `entry`.
####  `InvestabilityScreenConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig "Permanent link")
Immutable configuration for investability screening.
Enforces minimum standards of market capitalization, liquidity, price level, listing history, and data availability. All hysteresis thresholds use separate entry/exit values to reduce turnover at screen boundaries.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig--parameters "Permanent link")
market_cap : HysteresisConfig Free-float market capitalization thresholds (USD). addv_12m : HysteresisConfig 12-month average daily dollar volume thresholds (USD). addv_3m : HysteresisConfig 3-month average daily dollar volume thresholds (USD). trading_frequency : HysteresisConfig Fraction of trading days with nonzero volume (0-1). price_us : HysteresisConfig Minimum price for US-listed equities (USD). price_europe : HysteresisConfig Minimum price for European-listed equities (local currency). min_trading_history : int Minimum trading days of price history required. min_ipo_seasoning : int Minimum trading days since first price observation. min_annual_reports : int Minimum annual financial statements required. min_quarterly_reports : int Minimum quarterly financial statements required. exchange_region : ExchangeRegion Region for price threshold selection. mcap_percentile_entry : float Minimum exchange-percentile rank (0-1) for entry. A stock must exceed BOTH the absolute `market_cap.entry` floor AND this percentile within its exchange to enter the universe. Defaults to the 10th percentile (0.10). Requires an `exchange` column in the `fundamentals` DataFrame passed to `apply_investability_screens`. mcap_percentile_exit : float Minimum exchange-percentile rank (0-1) for existing members to avoid removal. Must be <= `mcap_percentile_entry`. Defaults to the 7.5th percentile (0.075).
#####  `for_developed_markets()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig.for_developed_markets "Permanent link")
Strict thresholds for developed-market institutional universes.
#####  `for_large_cap()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig.for_large_cap "Permanent link")
Large-cap universe (~S&P 500 comparable).
$2B market-cap entry, $5M daily volume, 252 trading days history.
#####  `for_broad_universe()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig.for_broad_universe "Permanent link")
Relaxed thresholds for broader coverage.
#####  `for_small_cap()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.InvestabilityScreenConfig.for_small_cap "Permanent link")
Thresholds appropriate for small-cap universes.
####  `screen_universe(fundamentals, price_history, volume_history, financial_statements=None, config=None, current_members=None)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.screen_universe "Permanent link")
Screen a stock universe for investability.
Convenience wrapper around :func:`apply_investability_screens` that applies default configuration when none is provided.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.screen_universe--parameters "Permanent link")
fundamentals : pd.DataFrame Cross-sectional data with one row per ticker. price_history : pd.DataFrame Price matrix (dates x tickers). volume_history : pd.DataFrame Volume matrix (dates x tickers). financial_statements : pd.DataFrame or None Statement-level data. config : InvestabilityScreenConfig or None Screening configuration. current_members : pd.Index or None Tickers currently in the universe for hysteresis.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.screen_universe--returns "Permanent link")
pd.Index Tickers passing all investability screens.
####  `apply_investability_screens(fundamentals, price_history, volume_history, financial_statements=None, config=None, current_members=None)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_investability_screens "Permanent link")
Apply all investability screens to produce a universe.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_investability_screens--parameters "Permanent link")
fundamentals : pd.DataFrame Cross-sectional data with one row per ticker. Required columns: `market_cap`, `current_price`. Index is ticker. All monetary columns (`market_cap`, `current_price`, etc.) must be denominated in major currency units (e.g. GBP, not GBX). Minor-unit normalisation must be applied upstream via `cli._currency.normalize_fundamentals()` before this function is called. price_history : pd.DataFrame Price matrix (dates x tickers). volume_history : pd.DataFrame Volume matrix (dates x tickers). financial_statements : pd.DataFrame or None Statement-level data with `ticker`, `period_type`, and optionally `period_date` columns. config : InvestabilityScreenConfig or None Screening configuration. Defaults to developed-market thresholds. current_members : pd.Index or None Tickers currently in the universe for hysteresis.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_investability_screens--returns "Permanent link")
pd.Index Tickers passing all investability screens.
####  `apply_screen(values, hysteresis, current_members=None)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_screen "Permanent link")
Apply a single screen with hysteresis.
New stocks must exceed `hysteresis.entry`; existing members are retained until they fall below `hysteresis.exit_`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_screen--parameters "Permanent link")
values : pd.Series Metric values indexed by ticker. hysteresis : HysteresisConfig Entry/exit thresholds. current_members : pd.Index or None Tickers currently in the universe. If `None`, entry thresholds are applied to all stocks.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.apply_screen--returns "Permanent link")
pd.Index Tickers passing the screen.
####  `compute_addv(price_history, volume_history, window)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_addv "Permanent link")
Compute average daily dollar volume over a trailing window.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_addv--parameters "Permanent link")
price_history : pd.DataFrame Price matrix (dates x tickers). Must be denominated in major currency units (e.g. GBP, not GBX). Minor-unit normalisation must be applied upstream (see `cli.data_assembly.assemble_prices`). volume_history : pd.DataFrame Volume matrix (dates x tickers), aligned with price_history. window : int Number of trailing trading days.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_addv--returns "Permanent link")
pd.Series Average daily dollar volume per ticker.
####  `compute_exchange_mcap_percentile_thresholds(market_caps, exchange_mapping, percentile, min_exchange_size=10)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_exchange_mcap_percentile_thresholds "Permanent link")
Compute per-exchange market-cap percentile threshold for each ticker.
For each exchange, the Nth percentile of all member market caps is computed and assigned as the threshold for every stock on that exchange. Exchanges with fewer than `min_exchange_size` stocks receive a threshold of 0 (no filter applied).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_exchange_mcap_percentile_thresholds--parameters "Permanent link")
market_caps : pd.Series Free-float market caps indexed by ticker. exchange_mapping : pd.Series Exchange labels indexed by ticker. percentile : float Percentile to compute on a 0-1 scale (e.g. 0.10 for the 10th percentile). min_exchange_size : int Minimum number of stocks an exchange must have before the percentile threshold is applied. Smaller exchanges default to a threshold of 0.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_exchange_mcap_percentile_thresholds--returns "Permanent link")
pd.Series Per-ticker threshold values (same index as `market_caps`).
####  `compute_listing_age(price_history)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_listing_age "Permanent link")
Compute listing age in trading days for each ticker.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_listing_age--parameters "Permanent link")
price_history : pd.DataFrame Price matrix (dates x tickers).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_listing_age--returns "Permanent link")
pd.Series Number of non-NaN trading days per ticker.
####  `compute_trading_frequency(volume_history, window)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_trading_frequency "Permanent link")
Compute fraction of trading days with nonzero volume.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_trading_frequency--parameters "Permanent link")
volume_history : pd.DataFrame Volume matrix (dates x tickers). window : int Number of trailing trading days.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.compute_trading_frequency--returns "Permanent link")
pd.Series Trading frequency per ticker (0 to 1).
####  `count_financial_statements(statements, period_type, min_lookback_days=None)` [¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.count_financial_statements "Permanent link")
Count financial statements per ticker.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.count_financial_statements--parameters "Permanent link")
statements : pd.DataFrame Must contain columns `ticker`, `period_type`, and optionally `period_date`. period_type : str Filter to this period type (e.g. `"annual"` or `"quarterly"`). min_lookback_days : int or None If provided, only count statements with `period_date` within this many calendar days from the latest date.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/universe/#optimizer.universe.count_financial_statements--returns "Permanent link")
pd.Series Statement count indexed by ticker.
