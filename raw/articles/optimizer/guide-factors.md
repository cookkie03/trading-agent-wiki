<!-- source: https://silviobaratto.github.io/optimizer/guide/factors/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/factors/#factor-research)
# Factor Research[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-research "Permanent link")
Comprehensive guide to the factors module. This module provides a complete factor research pipeline from raw fundamentals to optimization-ready inputs, covering 17 individual factors across 9 factor groups. Every component follows the same pattern: **frozen`@dataclass` config** + **factory function** + **`str, Enum`types**.
* * *
## Pipeline Overview[¶](https://silviobaratto.github.io/optimizer/guide/factors/#pipeline-overview "Permanent link")
The factor pipeline is a sequential workflow where each stage transforms the output of the previous one:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-0-1)fundamentals --> construction --> standardization --> scoring -->
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-0-2)selection --> regime tilts --> validation --> integration

```
  
| Stage  | Input  | Output  | Key Function  |  
| --- | --- | --- | --- |  
| Construction  | Fundamentals, prices, volume  | Raw factor scores (`pd.DataFrame`)  | `compute_all_factors()`  |  
| Standardization  | Raw scores, sector labels  | Standardized scores + coverage  | `standardize_all_factors()`  |  
| Scoring  | Standardized scores, IC history  | Composite score per ticker (`pd.Series`)  | `compute_composite_score()`  |  
| Selection  | Composite scores  | Selected tickers (`pd.Index`)  | `select_stocks()`  |  
| Regime Tilts  | Group weights, macro data  | Tilted group weights  | `apply_regime_tilts()`  |  
| Validation  | Score history, return history  | `FactorValidationReport`  | `run_factor_validation()`  |  
| Integration  | Scores, premia, weights  | Constraints, views, net alpha  | `build_factor_exposure_constraints()`  |  
* * *
## Factor Taxonomy[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-taxonomy "Permanent link")
### FactorType (17 factors)[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factortype-17-factors "Permanent link")
Each factor is computed from one of four data sources: fundamental data, price history, volume history, or alternative data (analyst/insider).  
| Factor  | Enum Value  | Group  | Data Source  | Formula  |  
| --- | --- | --- | --- | --- |  
| Book-to-Price  | `BOOK_TO_PRICE`  | Value  | Fundamentals  | book_value / market_cap  |  
| Earnings Yield  | `EARNINGS_YIELD`  | Value  | Fundamentals  | net_income / market_cap  |  
| Cash Flow Yield  | `CASH_FLOW_YIELD`  | Value  | Fundamentals  | operating_cashflow / market_cap  |  
| Sales-to-Price  | `SALES_TO_PRICE`  | Value  | Fundamentals  | total_revenue / market_cap  |  
| EBITDA-to-EV  | `EBITDA_TO_EV`  | Value  | Fundamentals  | ebitda / enterprise_value  |  
| Gross Profitability  | `GROSS_PROFITABILITY`  | Profitability  | Fundamentals  | gross_profit / total_assets (Novy-Marx)  |  
| ROE  | `ROE`  | Profitability  | Fundamentals  | net_income / total_equity  |  
| Operating Margin  | `OPERATING_MARGIN`  | Profitability  | Fundamentals  | operating_income / total_revenue  |  
| Profit Margin  | `PROFIT_MARGIN`  | Profitability  | Fundamentals  | net_income / total_revenue  |  
| Asset Growth  | `ASSET_GROWTH`  | Investment  | Fundamentals  | -YoY total asset growth (sign-flipped)  |  
| Momentum (12-1)  | `MOMENTUM_12_1`  | Momentum  | Prices  | 12-month return skipping most recent month  |  
| Volatility  | `VOLATILITY`  | Low Risk  | Prices  | -annualized std (sign-flipped, lower = better)  |  
| Beta  | `BETA`  | Low Risk  | Prices  | -market beta (sign-flipped, lower = better)  |  
| Amihud Illiquidity  | `AMIHUD_ILLIQUIDITY`  | Liquidity  | Prices + Volume  | avg(|return| / dollar_volume)  |  
| Dividend Yield  | `DIVIDEND_YIELD`  | Dividend  | Fundamentals  | trailing annual dividend yield  |  
| Recommendation Change  | `RECOMMENDATION_CHANGE`  | Sentiment  | Analyst data  | net upgrades - downgrades  |  
| Net Insider Buying  | `NET_INSIDER_BUYING`  | Ownership  | Insider data  | purchases - sales (shares)  |  
Sign Conventions
Volatility, beta, and asset growth are **sign-flipped** so that higher values always indicate a more favorable factor exposure. For volatility and beta, lower raw values are better (less risk), so the sign is negated. For asset growth, conservative investment (lower growth) is favorable per the Hou-Xue-Zhang investment factor, so the sign is negated.
### FactorGroupType (9 groups)[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factorgrouptype-9-groups "Permanent link")
Factors are organized into groups for hierarchical aggregation during composite scoring.  
| Group  | Enum Value  | Weight Tier  | Member Factors  |  
| --- | --- | --- | --- |  
| Value  | `VALUE`  | CORE  | BOOK_TO_PRICE, EARNINGS_YIELD, CASH_FLOW_YIELD, SALES_TO_PRICE, EBITDA_TO_EV  |  
| Profitability  | `PROFITABILITY`  | CORE  | GROSS_PROFITABILITY, ROE, OPERATING_MARGIN, PROFIT_MARGIN  |  
| Momentum  | `MOMENTUM`  | CORE  | MOMENTUM_12_1  |  
| Low Risk  | `LOW_RISK`  | CORE  | VOLATILITY, BETA  |  
| Investment  | `INVESTMENT`  | SUPPLEMENTARY  | ASSET_GROWTH  |  
| Liquidity  | `LIQUIDITY`  | SUPPLEMENTARY  | AMIHUD_ILLIQUIDITY  |  
| Dividend  | `DIVIDEND`  | SUPPLEMENTARY  | DIVIDEND_YIELD  |  
| Sentiment  | `SENTIMENT`  | SUPPLEMENTARY  | RECOMMENDATION_CHANGE  |  
| Ownership  | `OWNERSHIP`  | SUPPLEMENTARY  | NET_INSIDER_BUYING  |  
The `GROUP_WEIGHT_TIER` mapping assigns each group to either `CORE` or `SUPPLEMENTARY`. Core groups receive `core_weight` (default 1.0) and supplementary groups receive `supplementary_weight` (default 0.5) during composite scoring, reflecting the stronger empirical evidence behind core factors.
* * *
## 1. Construction[¶](https://silviobaratto.github.io/optimizer/guide/factors/#1-construction "Permanent link")
Factor construction computes raw factor scores from fundamentals, prices, volume, analyst data, and insider data. All construction respects point-in-time alignment to prevent look-ahead bias.
### FactorConstructionConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factorconstructionconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `factors`  | `tuple[FactorType, ...]`  | 8 core factors  | Which factors to compute  |  
| `momentum_lookback`  | `int`  | `252`  | Lookback window for momentum (trading days)  |  
| `momentum_skip`  | `int`  | `21`  | Recent days to skip for momentum (reversal avoidance)  |  
| `volatility_lookback`  | `int`  | `252`  | Lookback window for volatility (trading days)  |  
| `beta_lookback`  | `int`  | `252`  | Lookback window for beta estimation (trading days)  |  
| `amihud_lookback`  | `int`  | `252`  | Lookback window for Amihud illiquidity (trading days)  |  
| `publication_lag`  | `PublicationLagConfig`  | Default lags  | Per-source publication lags for PIT correctness  |  
The default `factors` tuple includes: BOOK_TO_PRICE, EARNINGS_YIELD, GROSS_PROFITABILITY, ROE, ASSET_GROWTH, MOMENTUM_12_1, VOLATILITY, DIVIDEND_YIELD.
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-1)from optimizer.factors import FactorConstructionConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-3)# Core factors with strongest empirical support (8 factors, default)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-4)config = FactorConstructionConfig.for_core_factors()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-6)# All 17 factors
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-1-7)config = FactorConstructionConfig.for_all_factors()

```

### PublicationLagConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#publicationlagconfig "Permanent link")
Differentiated publication lags prevent look-ahead bias by ensuring that data is only used after it would realistically have been available.  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `annual_days`  | `int`  | `90`  | Lag for annual financial statements (10-K filing)  |  
| `quarterly_days`  | `int`  | `45`  | Lag for quarterly financial statements (10-Q filing)  |  
| `analyst_days`  | `int`  | `5`  | Lag for analyst estimates and recommendations  |  
| `macro_days`  | `int`  | `63`  | Lag for macroeconomic indicators (release + revision lag)  |  

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-1)from optimizer.factors import PublicationLagConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-3)# Uniform lag across all sources
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-4)lag = PublicationLagConfig.uniform(days=60)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-6)# Custom per-source lags
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-7)lag = PublicationLagConfig(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-8)    annual_days=120,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-9)    quarterly_days=60,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-10)    analyst_days=2,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-11)    macro_days=45,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-2-12))

```

Backward Compatibility
`FactorConstructionConfig` accepts a plain `int` for `publication_lag`, which is automatically converted to `PublicationLagConfig.uniform(int_value)`.
### Point-in-Time Alignment[¶](https://silviobaratto.github.io/optimizer/guide/factors/#point-in-time-alignment "Permanent link")
The `align_to_pit()` function filters time-series data to records that would have been published on or before a given computation date. For each ticker, it returns the most recent available record.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-1)from optimizer.factors import align_to_pit
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-3)# Get the most recent fundamentals available as of 2024-06-30,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-4)# accounting for a 90-day publication lag
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-5)pit_data = align_to_pit(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-6)    data=fundamentals_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-7)    period_date_col="fiscal_period_end",
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-8)    as_of_date="2024-06-30",
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-9)    lag_days=90,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-10)    ticker_col="ticker",
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-3-11))

```

A record with period end date `D` is considered published `lag_days` calendar days after `D`. The function returns a cross-sectional view (one row per ticker) containing only the latest record for which `D + lag_days <= as_of_date`.
### Computing Factors[¶](https://silviobaratto.github.io/optimizer/guide/factors/#computing-factors "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-1)from optimizer.factors import compute_all_factors, compute_factor, FactorConstructionConfig, FactorType
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-3)# Compute all configured factors at once
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-4)config = FactorConstructionConfig.for_all_factors()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-5)raw_factors = compute_all_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-6)    fundamentals=fundamentals_df,      # Cross-sectional, indexed by ticker
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-7)    price_history=price_df,            # Dates x tickers matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-8)    volume_history=volume_df,          # Dates x tickers matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-9)    analyst_data=analyst_df,           # Optional
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-10)    insider_data=insider_df,           # Optional
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-11)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-12))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-13)# raw_factors: pd.DataFrame with tickers as rows, factor names as columns
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-14)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-15)# Compute a single factor
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-16)momentum = compute_factor(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-17)    factor_type=FactorType.MOMENTUM_12_1,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-18)    fundamentals=fundamentals_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-19)    price_history=price_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-20)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-4-21))

```

Data Requirements
  * `fundamentals` must be a cross-sectional DataFrame indexed by ticker with columns matching the factor formulas (e.g., `market_cap`, `book_value`, `net_income`).
  * `price_history` must be a dates x tickers DataFrame. Momentum requires at least `momentum_lookback` rows of data.
  * `volume_history` is only required for `AMIHUD_ILLIQUIDITY`. If `None`, that factor returns an empty Series.
  * `analyst_data` is only required for `RECOMMENDATION_CHANGE`. It must contain either a `recommendation_change` column or `strong_buy`/`buy`/`sell`/`strong_sell` counts.
  * `insider_data` is only required for `NET_INSIDER_BUYING`. It must contain `shares`, `ticker`, and optionally `transaction_type` columns.


* * *
## 2. Standardization[¶](https://silviobaratto.github.io/optimizer/guide/factors/#2-standardization "Permanent link")
Cross-sectional standardization transforms raw factor scores into comparable, well-behaved distributions suitable for aggregation. The pipeline is: **winsorize** --> **z-score or rank-normal** --> **sector neutralize** --> **optional re-standardization**.
### StandardizationConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#standardizationconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `method`  | `StandardizationMethod`  | `RANK_NORMAL`  | Z-score or rank-normal standardization  |  
| `winsorize_method`  | `WinsorizeMethod`  | `PERCENTILE`  | Outlier treatment method  |  
| `winsorize_lower`  | `float`  | `0.01`  | Lower percentile for winsorization (0-1, PERCENTILE only)  |  
| `winsorize_upper`  | `float`  | `0.99`  | Upper percentile for winsorization (0-1, PERCENTILE only)  |  
| `neutralize_sector`  | `bool`  | `True`  | Whether to sector-neutralize scores  |  
| `neutralize_country`  | `bool`  | `False`  | Whether to country-neutralize scores  |  
| `re_standardize_after_neutralization`  | `bool`  | `False`  | Re-apply z-score after neutralization  |  
| `factor_method_overrides`  | `tuple[tuple[str, str], ...]`  | `()`  | Per-factor method overrides as `(factor_name, method_value)` pairs  |  
> **Note** : The default method changed from `Z_SCORE` to `RANK_NORMAL` to align with MSCI Barra USE4 (Menchero et al. 2011) and Gu/Kelly/Xiu (2020) best practice for heavy-tailed financial factor distributions. Use `StandardizationConfig.for_z_score()` for backward compatibility.
### StandardizationMethod[¶](https://silviobaratto.github.io/optimizer/guide/factors/#standardizationmethod "Permanent link")  
| Value  | Description  | Best For  |  
| --- | --- | --- |  
| `Z_SCORE`  | `(x - mean) / std`  | Approximately normal factors (e.g., momentum)  |  
| `RANK_NORMAL`  |  `Phi^-1((rank - 0.5) / N)` inverse normal transform  | Heavy-tailed distributions (e.g., value ratios)  |  
### WinsorizeMethod[¶](https://silviobaratto.github.io/optimizer/guide/factors/#winsorizemethod "Permanent link")  
| Value  | Description  | Best For  |  
| --- | --- | --- |  
| `PERCENTILE`  | Clip at fixed quantiles (1st/99th percentile)  | General use  |  
| `MAD`  | Clip at median ± 3 × 1.4826 × MAD (MSCI Barra convention)  | Heavy-tailed distributions  |  
### HEAVY_TAILED_FACTORS[¶](https://silviobaratto.github.io/optimizer/guide/factors/#heavy_tailed_factors "Permanent link")
The canonical classification of heavy-tailed factors (value ratios, illiquidity, dividend yield, accruals, asset growth): `book_to_price`, `earnings_yield`, `cash_flow_yield`, `sales_to_price`, `ebitda_to_ev`, `asset_growth`, `dividend_yield`, `amihud_illiquidity`, `accruals`.
Approximately normal factors (z-score is appropriate): `momentum_12_1`, `volatility`, `beta`.
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-1)from optimizer.factors import StandardizationConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-3)# Rank-normal for heavy-tailed distributions (value ratios, illiquidity)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-4)config = StandardizationConfig.for_heavy_tailed()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-6)# Z-score for approximately normal factors (momentum, profitability)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-7)config = StandardizationConfig.for_normal()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-9)# Z-score standardization (backward-compatibility alias)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-10)config = StandardizationConfig.for_z_score()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-11)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-12)# Per-factor: RANK_NORMAL for heavy-tailed, Z_SCORE for near-normal
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-13)config = StandardizationConfig.for_per_factor()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-14)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-15)# MAD-based winsorization (MSCI Barra +/-3 MAD)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-5-16)config = StandardizationConfig.for_mad_winsorize()

```

### Standardization Pipeline Steps[¶](https://silviobaratto.github.io/optimizer/guide/factors/#standardization-pipeline-steps "Permanent link")
#### Step 1: Winsorize[¶](https://silviobaratto.github.io/optimizer/guide/factors/#step-1-winsorize "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-6-1)from optimizer.factors import winsorize_cross_section
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-6-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-6-3)# Clip extremes at the 1st and 99th percentiles
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-6-4)clipped = winsorize_cross_section(raw_scores, lower_pct=0.01, upper_pct=0.99)

```

#### Step 2: Z-Score or Rank-Normal[¶](https://silviobaratto.github.io/optimizer/guide/factors/#step-2-z-score-or-rank-normal "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-1)from optimizer.factors import z_score_standardize, rank_normal_standardize
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-3)# Z-score: mean 0, std 1
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-4)z_scored = z_score_standardize(clipped)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-6)# Rank-normal: maps ranks to normal distribution, robust to outliers
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-7-7)rank_normed = rank_normal_standardize(clipped)

```

#### Step 3: Sector Neutralize[¶](https://silviobaratto.github.io/optimizer/guide/factors/#step-3-sector-neutralize "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-1)from optimizer.factors import neutralize_sector
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-3)# Demean scores within each sector
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-4)neutral = neutralize_sector(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-5)    scores=z_scored,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-6)    sector_labels=sector_series,          # pd.Series: ticker -> sector
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-7)    country_labels=country_series,        # Optional: ticker -> country
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-8-8))

```

Sector neutralization removes sector-level biases so that the factor captures stock-level characteristics rather than sector membership. When both `neutralize_sector` and `neutralize_country` are enabled, the function creates sector-country interaction groups (e.g., `"Technology_US"`) and demeans within each.
### Full Standardization[¶](https://silviobaratto.github.io/optimizer/guide/factors/#full-standardization "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-1)from optimizer.factors import standardize_all_factors, StandardizationConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-3)config = StandardizationConfig(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-4)    method=StandardizationMethod.RANK_NORMAL,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-5)    neutralize_sector=True,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-6))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-7)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-8)standardized, coverage = standardize_all_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-9)    raw_factors=raw_factors,          # Tickers x factors DataFrame
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-10)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-11)    sector_labels=sector_series,      # pd.Series: ticker -> sector
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-12))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-13)# standardized: pd.DataFrame of standardized scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-9-14)# coverage: pd.DataFrame (boolean) indicating non-NaN values

```

### PCA Orthogonalization[¶](https://silviobaratto.github.io/optimizer/guide/factors/#pca-orthogonalization "Permanent link")
For eliminating multicollinearity among factor scores, `orthogonalize_factors()` projects the scores onto principal components:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-1)from optimizer.factors import orthogonalize_factors
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-3)# Retain components explaining >= 95% of variance
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-4)orthogonal = orthogonalize_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-5)    factor_scores=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-6)    method="pca",
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-7)    min_variance_explained=0.95,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-10-9)# orthogonal: pd.DataFrame with columns PC1, PC2, ...

```

Orthogonalization Limitations
  * Only `"pca"` is supported as the method. Other values raise `ConfigurationError`.
  * Requires at least 2 factors and 2 non-NaN observations.
  * Rows with NaN in the input produce NaN in the output but preserve the index.
  * After orthogonalization, factor scores lose their economic interpretation (they become statistical principal components).


* * *
## 3. Composite Scoring[¶](https://silviobaratto.github.io/optimizer/guide/factors/#3-composite-scoring "Permanent link")
Composite scoring aggregates standardized factor scores into a single composite score per ticker. The process is hierarchical: factors are first averaged within their group, then group scores are combined using configurable weighting schemes.
### CompositeScoringConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#compositescoringconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `method`  | `CompositeMethod`  | `EQUAL_WEIGHT`  | Scoring method  |  
| `ic_lookback`  | `int`  | `36`  | Number of periods for IC estimation (IC/ICIR methods)  |  
| `core_weight`  | `float`  | `1.0`  | Relative weight for CORE factor groups  |  
| `supplementary_weight`  | `float`  | `0.5`  | Relative weight for SUPPLEMENTARY factor groups  |  
| `ridge_alpha`  | `float`  | `1.0`  | L2 regularization strength for RIDGE_WEIGHTED  |  
| `gbt_max_depth`  | `int`  | `3`  | Maximum tree depth for GBT_WEIGHTED  |  
| `gbt_n_estimators`  | `int`  | `50`  | Number of boosting rounds for GBT_WEIGHTED  |  
| `min_coverage_groups`  | `int`  | `0`  | Minimum non-NaN group scores required; tickers below this receive NaN composite. 0 disables  |  
| `return_coverage`  | `bool`  | `False`  | When True, returns DataFrame with `composite` and `coverage_ratio` columns  |  
### Sparse-Coverage Handling[¶](https://silviobaratto.github.io/optimizer/guide/factors/#sparse-coverage-handling "Permanent link")
When a ticker is missing all factors in a group (e.g., no analyst estimates for the Sentiment group), the group score is NaN. The composite scoring functions compute a **renormalized weighted average** using only available (non-NaN) groups per ticker, rather than filling missing groups with zero. This prevents systematic dilution of the signal for sparse-coverage tickers.
  * **`min_coverage_groups`**: Set a minimum threshold for data quality. Tickers with fewer than this many non-NaN group scores receive NaN composite and are automatically excluded by`select_stocks()`.
  * **`coverage_ratio`**: When`return_coverage=True` , a `coverage_ratio` column (0.0–1.0) is returned alongside the composite, enabling downstream diagnostics.


### CompositeMethod[¶](https://silviobaratto.github.io/optimizer/guide/factors/#compositemethod "Permanent link")  
| Method  | Description  | Requirements  | Strengths  |  
| --- | --- | --- | --- |  
| `EQUAL_WEIGHT`  | Core/supplementary tiered equal weighting  | None  | Robust, no estimation error  |  
| `IC_WEIGHTED`  | Trailing IC magnitude as weights  | `ic_history`  | Adapts to recent predictive power  |  
| `ICIR_WEIGHTED`  |  `max(mean(IC) / std(IC), 0)` as weights  | `ic_history`  | Penalizes inconsistent predictors  |  
| `RIDGE_WEIGHTED`  | Ridge regression on historical returns  |  `training_scores`, `training_returns`  | Captures linear factor interactions  |  
| `GBT_WEIGHTED`  | Gradient-boosted trees on historical returns  |  `training_scores`, `training_returns`  | Captures non-linear interactions  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_2 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-1)from optimizer.factors import CompositeScoringConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-3)config = CompositeScoringConfig.for_equal_weight()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-4)config = CompositeScoringConfig.for_ic_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-5)config = CompositeScoringConfig.for_icir_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-6)config = CompositeScoringConfig.for_ridge_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-7)config = CompositeScoringConfig.for_gbt_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-8)config = CompositeScoringConfig.for_sparse_universe()        # min_coverage_groups=2
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-11-9)config = CompositeScoringConfig.for_coverage_diagnostics()   # return_coverage=True

```

### Scoring Workflow[¶](https://silviobaratto.github.io/optimizer/guide/factors/#scoring-workflow "Permanent link")
#### Step 1: Compute Group Scores[¶](https://silviobaratto.github.io/optimizer/guide/factors/#step-1-compute-group-scores "Permanent link")
Group scores are the coverage-weighted mean of factor scores within each group:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-12-1)from optimizer.factors import compute_group_scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-12-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-12-3)group_scores = compute_group_scores(standardized, coverage)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-12-4)# group_scores: pd.DataFrame with tickers as rows, group names as columns

```

#### Step 2: Compute Composite Score[¶](https://silviobaratto.github.io/optimizer/guide/factors/#step-2-compute-composite-score "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-1)from optimizer.factors import compute_composite_score, CompositeScoringConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-3)# Equal-weight composite (simplest)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-4)composite = compute_composite_score(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-5)    standardized_factors=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-6)    coverage=coverage,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-9)# IC-weighted composite (requires IC history)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-10)config = CompositeScoringConfig.for_ic_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-11)composite = compute_composite_score(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-12)    standardized_factors=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-13)    coverage=coverage,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-14)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-15)    ic_history=ic_df,             # Periods x groups DataFrame of IC values
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-16))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-17)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-18)# ML composite (requires training data)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-19)config = CompositeScoringConfig.for_ridge_weighted()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-20)composite = compute_composite_score(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-21)    standardized_factors=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-22)    coverage=coverage,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-23)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-24)    training_scores=historical_scores,      # Historical tickers x factors
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-25)    training_returns=forward_returns,       # Forward return per ticker
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-13-26))

```

Look-Ahead Bias in ML Scoring
For `RIDGE_WEIGHTED` and `GBT_WEIGHTED`, the training window must end **strictly before** the prediction date. The caller is responsible for ensuring temporal separation between `training_scores` and the current-period `standardized_factors`.
### IC-Weighted Scoring Details[¶](https://silviobaratto.github.io/optimizer/guide/factors/#ic-weighted-scoring-details "Permanent link")
The IC-weighted method uses trailing Information Coefficient (Spearman rank correlation between factor scores and forward returns) to dynamically weight factor groups:
  1. Compute the mean IC over the trailing `ic_lookback` periods for each group
  2. Clamp negative ICs to zero (negative-IC groups should not contribute positively)
  3. Multiply by the core/supplementary tier weight
  4. Normalize to sum to 1


If all groups have negative or zero IC, the method falls back to equal-weight scoring.
### ICIR-Weighted Scoring Details[¶](https://silviobaratto.github.io/optimizer/guide/factors/#icir-weighted-scoring-details "Permanent link")
ICIR (Information Coefficient Information Ratio) penalizes factors that are inconsistent predictors:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-14-1)ICIR = max(mean(IC) / std(IC), 0)

```

A factor with high mean IC but also high IC volatility receives a lower weight than a factor with moderate but stable IC. Groups with negative ICIR (consistently wrong-direction predictions) receive zero weight rather than being included with flipped sign. Falls back to equal-weight when all groups have ICIR <= 0.
### ML Scoring Details[¶](https://silviobaratto.github.io/optimizer/guide/factors/#ml-scoring-details "Permanent link")
Both ML methods train a model on historical `(factor_scores, forward_returns)` pairs and predict on the current period. The raw predictions are standardized to zero mean and unit variance.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-1)from optimizer.factors import fit_ridge_composite, fit_gbt_composite, predict_composite_scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-3)# Fit ridge regression
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-4)model = fit_ridge_composite(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-5)    scores=historical_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-6)    forward_returns=forward_returns,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-7)    alpha=1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-9)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-10)# Or fit gradient-boosted trees
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-11)model = fit_gbt_composite(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-12)    scores=historical_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-13)    forward_returns=forward_returns,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-14)    max_depth=3,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-15)    n_estimators=50,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-16))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-17)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-18)# Predict on current-period scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-15-19)composite = predict_composite_scores(model, current_scores)

```

The `FittedMLModel` type alias covers both `RidgeCV` and `GradientBoostingRegressor`.
### Regime-Tilted Scoring[¶](https://silviobaratto.github.io/optimizer/guide/factors/#regime-tilted-scoring "Permanent link")
When regime tilts are applied, group weights can be passed through to the scoring functions:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-1)from optimizer.factors import (
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-2)    classify_regime,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-3)    apply_regime_tilts,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-4)    compute_composite_score,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-5)    RegimeTiltConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-6)    FactorGroupType,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-9)# Classify regime
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-10)regime = classify_regime(macro_data)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-11)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-12)# Compute tilted weights
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-13)base_weights = {
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-14)    FactorGroupType.VALUE: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-15)    FactorGroupType.MOMENTUM: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-16)    FactorGroupType.LOW_RISK: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-17)    FactorGroupType.PROFITABILITY: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-18)}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-19)tilted = apply_regime_tilts(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-20)    base_weights, regime, RegimeTiltConfig.for_moderate_tilts()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-21))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-22)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-23)# Convert to string keys for compute_composite_score
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-24)group_weights = {g.value: w for g, w in tilted.items()}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-25)composite = compute_composite_score(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-26)    standardized, coverage, group_weights=group_weights,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-16-27))

```

* * *
## 4. Stock Selection[¶](https://silviobaratto.github.io/optimizer/guide/factors/#4-stock-selection "Permanent link")
Stock selection filters the scored universe down to a target number of stocks, with mechanisms to reduce unnecessary turnover.
### SelectionConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#selectionconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `method`  | `SelectionMethod`  | `FIXED_COUNT`  | Fixed-count or quantile-based selection  |  
| `target_count`  | `int`  | `100`  | Number of stocks to select (for FIXED_COUNT)  |  
| `target_quantile`  | `float`  | `0.8`  | Quantile threshold for entry (for QUANTILE, 0-1)  |  
| `exit_quantile`  | `float`  | `0.7`  | Exit quantile for hysteresis (for QUANTILE)  |  
| `buffer_fraction`  | `float`  | `0.1`  | Buffer zone fraction around selection boundary  |  
| `sector_balance`  | `bool`  | `True`  | Whether to enforce sector-proportional representation  |  
| `sector_tolerance`  | `float`  | `0.05`  | Maximum deviation from parent universe sector weights  |  
### SelectionMethod[¶](https://silviobaratto.github.io/optimizer/guide/factors/#selectionmethod "Permanent link")  
| Method  | Description  |  
| --- | --- |  
| `FIXED_COUNT`  | Select top N stocks by composite score  |  
| `QUANTILE`  | Select all stocks above a quantile threshold  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_3 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-1)from optimizer.factors import SelectionConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-3)# Top 100 stocks (default)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-4)config = SelectionConfig.for_top_100()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-6)# Top quintile (top 20%)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-7)config = SelectionConfig.for_top_quintile()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-9)# Concentrated portfolio of top 30
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-10)config = SelectionConfig.for_concentrated()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-11)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-12)# Tight 3% sector cap for low tracking error (institutional use)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-17-13)config = SelectionConfig.for_low_tracking_error()

```

### Buffer-Zone Hysteresis[¶](https://silviobaratto.github.io/optimizer/guide/factors/#buffer-zone-hysteresis "Permanent link")
Hysteresis prevents excessive turnover by creating a buffer zone around the selection boundary. Current members within the buffer are retained even if they would not qualify as new entrants.
**Fixed-Count hysteresis** : The top `target_count` stocks are always included. Current members ranking between `target_count` and `target_count + buffer_fraction * target_count` are retained.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-1)from optimizer.factors import select_fixed_count
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-3)selected = select_fixed_count(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-4)    scores=composite_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-5)    target_count=100,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-6)    buffer_fraction=0.1,                 # Buffer of 10 stocks
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-7)    current_members=previous_selection,   # pd.Index of previously selected tickers
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-18-8))

```

**Quantile hysteresis** : New stocks must score above `target_quantile` (e.g., 80th percentile). Existing members survive as long as they stay above `exit_quantile` (e.g., 70th percentile).

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-1)from optimizer.factors import select_quantile
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-3)selected = select_quantile(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-4)    scores=composite_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-5)    target_quantile=0.8,                 # Entry threshold
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-6)    exit_quantile=0.7,                   # Exit threshold (lower = more sticky)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-7)    current_members=previous_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-19-8))

```

### Sector Balancing[¶](https://silviobaratto.github.io/optimizer/guide/factors/#sector-balancing "Permanent link")
When `sector_balance=True`, the selection is adjusted so that no sector is over- or under-represented relative to the parent universe by more than `sector_tolerance`:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-1)from optimizer.factors import apply_sector_balance
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-3)balanced = apply_sector_balance(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-4)    selected=initial_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-5)    scores=composite_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-6)    sector_labels=sector_series,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-7)    parent_universe=full_universe,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-8)    tolerance=0.05,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-20-9))

```

Under-represented sectors gain their highest-scoring non-selected stocks. Over-represented sectors lose their lowest-scoring selected stocks.
### Full Selection Pipeline[¶](https://silviobaratto.github.io/optimizer/guide/factors/#full-selection-pipeline "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-1)from optimizer.factors import select_stocks, SelectionConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-3)config = SelectionConfig(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-4)    method=SelectionMethod.FIXED_COUNT,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-5)    target_count=100,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-6)    buffer_fraction=0.1,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-7)    sector_balance=True,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-8)    sector_tolerance=0.05,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-9))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-10)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-11)# Without turnover tracking
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-12)selected = select_stocks(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-13)    scores=composite_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-14)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-15)    current_members=previous_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-16)    sector_labels=sector_series,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-17)    parent_universe=full_universe,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-18))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-19)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-20)# With turnover tracking
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-21)selected, turnover = select_stocks(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-22)    scores=composite_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-23)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-24)    current_members=previous_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-25)    sector_labels=sector_series,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-26)    parent_universe=full_universe,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-27)    return_turnover=True,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-21-28))

```

### Selection Turnover[¶](https://silviobaratto.github.io/optimizer/guide/factors/#selection-turnover "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-1)from optimizer.factors import compute_selection_turnover
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-3)turnover = compute_selection_turnover(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-4)    current=previous_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-5)    new=new_selection,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-6)    universe=full_universe,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-22-8)# turnover = len(added | removed) / len(universe)

```

* * *
## 5. Regime Tilts[¶](https://silviobaratto.github.io/optimizer/guide/factors/#5-regime-tilts "Permanent link")
Regime tilts apply macro-economic regime-conditional adjustments to factor group weights. The system classifies the current macro environment and applies multiplicative tilts to emphasize factors with stronger expected performance in that regime.
### MacroRegime[¶](https://silviobaratto.github.io/optimizer/guide/factors/#macroregime "Permanent link")  
| Regime  | Description  | Factor Emphasis  |  
| --- | --- | --- |  
| `EXPANSION`  | GDP above trend, accelerating  | Momentum (1.2x), reduce Value/Low Risk  |  
| `SLOWDOWN`  | GDP above trend, decelerating  | Low Risk (1.3x), Dividend (1.2x), reduce Momentum  |  
| `RECESSION`  | GDP below trend, decelerating  | Low Risk (1.5x), Profitability (1.3x), Value (1.2x), reduce Momentum  |  
| `RECOVERY`  | GDP below trend, accelerating  | Value (1.3x), Momentum (1.2x), reduce Low Risk  |  
### RegimeTiltConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#regimetiltconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `enable`  | `bool`  | `False`  | Whether to apply regime tilts  |  
| `expansion_tilts`  | `tuple[tuple[str, float], ...]`  | See defaults  | Group tilts during expansion  |  
| `slowdown_tilts`  | `tuple[tuple[str, float], ...]`  | See defaults  | Group tilts during slowdown  |  
| `recession_tilts`  | `tuple[tuple[str, float], ...]`  | See defaults  | Group tilts during recession  |  
| `recovery_tilts`  | `tuple[tuple[str, float], ...]`  | See defaults  | Group tilts during recovery  |  
Tilts are stored as tuples of `(group_name, tilt_factor)` for frozen-dataclass compatibility.
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_4 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-1)from optimizer.factors import RegimeTiltConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-3)# Enable moderate tilts (uses the built-in tilt tables)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-4)config = RegimeTiltConfig.for_moderate_tilts()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-6)# Disable tilts (default)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-23-7)config = RegimeTiltConfig.for_no_tilts()

```

### Regime Classification[¶](https://silviobaratto.github.io/optimizer/guide/factors/#regime-classification "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-24-1)from optimizer.factors import classify_regime
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-24-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-24-3)regime = classify_regime(macro_data)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-24-4)# macro_data: pd.DataFrame with date index and columns like
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-24-5)# 'gdp_growth', 'yield_spread', 'unemployment_rate'

```

The classification heuristic uses GDP growth as the primary signal:
  1. If `gdp_growth` is available with 2+ observations:
     * Rising unemployment with positive GDP overrides to `SLOWDOWN`
     * Current > trend and current > previous --> `EXPANSION`
     * Current > trend and current <= previous --> `SLOWDOWN`
     * Current <= trend and current <= previous --> `RECESSION`
     * Current <= trend and current > previous --> `RECOVERY`
  2. Fallback: `yield_spread` (10Y-2Y Treasury spread):
     * > 1.0 --> `EXPANSION`
     * > 0.0 --> `SLOWDOWN`
     * > -0.5 --> `RECOVERY`
     * <= -0.5 --> `RECESSION`
  3. Default: `EXPANSION`


### Applying Tilts[¶](https://silviobaratto.github.io/optimizer/guide/factors/#applying-tilts "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-1)from optimizer.factors import apply_regime_tilts, get_regime_tilts, FactorGroupType, MacroRegime
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-3)# Get the raw tilt dictionary for a regime
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-4)tilts = get_regime_tilts(MacroRegime.RECESSION)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-5)# {FactorGroupType.LOW_RISK: 1.5, FactorGroupType.PROFITABILITY: 1.3, ...}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-6)# Groups not listed receive a default tilt of 1.0
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-7)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-8)# Apply tilts to base group weights (with re-normalization)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-9)base_weights = {
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-10)    FactorGroupType.VALUE: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-11)    FactorGroupType.PROFITABILITY: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-12)    FactorGroupType.MOMENTUM: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-13)    FactorGroupType.LOW_RISK: 1.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-14)}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-15)tilted = apply_regime_tilts(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-16)    group_weights=base_weights,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-17)    regime=MacroRegime.RECESSION,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-18)    config=RegimeTiltConfig.for_moderate_tilts(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-25-19))

```

Re-Normalization
After applying multiplicative tilts, the total weight is re-normalized to preserve the original total. This ensures that tilts only change the relative allocation between groups, not the overall magnitude.
Disabled by Default
`RegimeTiltConfig.enable` defaults to `False`. When `enable=False`, `apply_regime_tilts()` returns a copy of the original weights unchanged. You must explicitly use `RegimeTiltConfig.for_moderate_tilts()` or set `enable=True`.
* * *
## 6. Validation[¶](https://silviobaratto.github.io/optimizer/guide/factors/#6-validation "Permanent link")
Factor validation assesses the statistical significance and economic value of factors before deploying them in production.
### FactorValidationConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factorvalidationconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `newey_west_lags`  | `int`  | `6`  | Number of lags for Newey-West HAC standard errors  |  
| `t_stat_threshold`  | `float`  | `2.0`  | Minimum absolute t-statistic for significance  |  
| `fdr_alpha`  | `float`  | `0.05`  | False discovery rate alpha level  |  
| `n_quantiles`  | `int`  | `5`  | Number of quantiles for spread analysis  |  
| `fmp_top_pct`  | `float`  | `0.2`  | Top percentile for factor-mimicking portfolios  |  
| `fmp_bottom_pct`  | `float`  | `0.2`  | Bottom percentile for factor-mimicking portfolios  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_5 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-1)from optimizer.factors import FactorValidationConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-3)# Standard validation
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-4)config = FactorValidationConfig.for_standard()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-6)# Strict validation (t > 3.0, FDR alpha = 1%)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-26-7)config = FactorValidationConfig.for_strict()

```

### Information Coefficient (IC) Analysis[¶](https://silviobaratto.github.io/optimizer/guide/factors/#information-coefficient-ic-analysis "Permanent link")
The Information Coefficient is the Spearman rank correlation between factor scores and subsequent forward returns. A positive IC indicates that higher factor scores predict higher returns.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-1)from optimizer.factors import compute_monthly_ic, compute_ic_series, compute_icir, compute_ic_stats
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-3)# Single-period IC
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-4)ic = compute_monthly_ic(factor_scores, forward_returns)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-6)# IC time series (one IC per date)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-7)ic_series = compute_ic_series(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-8)    factor_scores_history=scores_df,    # Dates x tickers matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-9)    returns_history=returns_df,         # Dates x tickers matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-10)    factor_name="book_to_price",
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-11))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-12)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-13)# ICIR: mean(IC) / std(IC)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-14)icir = compute_icir(ic_series)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-15)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-16)# Full IC statistics with Newey-West inference
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-17)stats = compute_ic_stats(ic_series, lags=5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-27-18)# stats.mean, stats.variance_nw, stats.t_stat_nw, stats.p_value, stats.icir

```

### Newey-West t-Statistic[¶](https://silviobaratto.github.io/optimizer/guide/factors/#newey-west-t-statistic "Permanent link")
The Newey-West HAC (heteroscedasticity and autocorrelation consistent) estimator provides robust standard errors for IC significance testing, accounting for the serial correlation inherent in overlapping IC measurements.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-28-1)from optimizer.factors import compute_newey_west_tstat
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-28-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-28-3)t_stat, p_value = compute_newey_west_tstat(ic_series, n_lags=6)

```

The variance estimator uses Bartlett kernel weights:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-29-1)Var_NW = gamma_0 + 2 * sum_{j=1}^{L} (1 - j/(L+1)) * gamma_j

```

where `gamma_j = E[(IC_t - mean)(IC_{t-j} - mean)]`.
### Multiple Testing Correction[¶](https://silviobaratto.github.io/optimizer/guide/factors/#multiple-testing-correction "Permanent link")
When testing multiple factors simultaneously, p-values must be corrected for multiple comparisons.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-1)from optimizer.factors import correct_pvalues, benjamini_hochberg
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-3)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-4)# Holm-Bonferroni (FWER) + Benjamini-Hochberg (FDR)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-5)raw_pvalues = np.array([0.01, 0.04, 0.03, 0.15, 0.02])
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-6)corrected = correct_pvalues(raw_pvalues, alpha=0.05)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-7)# corrected.holm: Holm-Bonferroni adjusted p-values (controls family-wise error rate)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-8)# corrected.bh: Benjamini-Hochberg adjusted p-values (controls false discovery rate)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-9)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-10)# Standalone BH correction (returns boolean series)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-30-11)significant = benjamini_hochberg(p_values_series, alpha=0.05)

```

### Variance Inflation Factor (VIF)[¶](https://silviobaratto.github.io/optimizer/guide/factors/#variance-inflation-factor-vif "Permanent link")
VIF detects multicollinearity among factors. A VIF above 10 indicates that the factor's variance is largely explained by other factors.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-31-1)from optimizer.factors import compute_vif
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-31-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-31-3)vif = compute_vif(standardized_factors)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-31-4)# pd.Series: VIF per factor (>= 1.0 by construction)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-31-5)high_vif = vif[vif > 10]  # Candidates for removal or merging

```

### Quantile Spread Analysis[¶](https://silviobaratto.github.io/optimizer/guide/factors/#quantile-spread-analysis "Permanent link")
Quantile spreads measure the economic value of a factor by comparing returns across factor-sorted portfolios.

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-1)from optimizer.factors import compute_quantile_spread
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-3)# Single-period spread: top quantile return - bottom quantile return
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-4)spread = compute_quantile_spread(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-5)    factor_scores=scores_series,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-6)    forward_returns=returns_series,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-7)    n_quantiles=5,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-32-8))

```

### Factor Spread Benchmarks[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-spread-benchmarks "Permanent link")
The module includes annualized long-short quintile spread benchmarks derived from academic literature (Fama-French, AQR, Novy-Marx):  
| Group  | Low  | High  |  
| --- | --- | --- |  
| value  | 2%  | 6%  |  
| profitability  | 2%  | 5%  |  
| investment  | 1%  | 4%  |  
| momentum  | 4%  | 10%  |  
| low_risk  | 1%  | 4%  |  
| liquidity  | 1%  | 3%  |  
| dividend  | 1%  | 3%  |  
| sentiment  | 0.5%  | 2%  |  
| ownership  | 0.5%  | 2%  |  
### Universe-Level Validation[¶](https://silviobaratto.github.io/optimizer/guide/factors/#universe-level-validation "Permanent link")
`validate_factor_universe()` validates all factors simultaneously with Newey-West inference and multiple testing correction:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-1)from optimizer.factors import validate_factor_universe
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-3)summary = validate_factor_universe(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-4)    ic_matrix=ic_matrix,     # Dates x factors matrix of IC values
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-5)    lags=5,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-6)    alpha=0.05,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-8)# Returns pd.DataFrame with columns:
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-9)# ic_mean, icir, t_stat_nw, p_value_raw, p_value_holm, p_value_bh,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-33-10)# significant_holm, significant_bh

```

### Full Validation Report[¶](https://silviobaratto.github.io/optimizer/guide/factors/#full-validation-report "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-1)from optimizer.factors import run_factor_validation, FactorValidationConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-3)report = run_factor_validation(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-4)    factor_scores_history={
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-5)        "book_to_price": scores_bp_df,    # Dates x tickers per factor
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-6)        "momentum_12_1": scores_mom_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-7)    },
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-8)    returns_history=returns_df,            # Dates x tickers forward returns
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-9)    config=FactorValidationConfig.for_standard(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-10))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-11)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-12)# report.ic_results: list[ICResult] with per-factor IC, t-stat, p-value
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-13)# report.quantile_spreads: list[QuantileSpreadResult] with per-factor spreads
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-14)# report.significant_factors: list[str] (BH FDR-significant factors)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-34-15)# report.significant_factors_holm: list[str] (Holm FWER-significant factors)

```

### Out-of-Sample Validation[¶](https://silviobaratto.github.io/optimizer/guide/factors/#out-of-sample-validation "Permanent link")
Rolling block or combinatorial purged cross-validation (CPCV) for out-of-sample factor assessment:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-1)from optimizer.factors import run_factor_oos_validation, FactorOOSConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-3)# Rolling block OOS
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-4)config = FactorOOSConfig(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-5)    train_periods=36,     # 36-period training window
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-6)    val_periods=12,       # 12-period validation window
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-7)    step_periods=6,       # Roll forward 6 periods per fold
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-9)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-10)result = run_factor_oos_validation(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-11)    scores=panel_scores,     # MultiIndex (date, ticker) x factors
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-12)    returns=panel_returns,   # MultiIndex (date, ticker) x return column
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-13)    config=config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-14))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-15)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-16)# result.per_fold_ic: n_folds x factors DataFrame of mean IC per fold
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-17)# result.per_fold_spread: n_folds x factors DataFrame of mean spread per fold
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-18)# result.mean_oos_ic: pd.Series of mean OOS IC per factor
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-19)# result.mean_oos_icir: pd.Series of OOS ICIR per factor
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-35-20)# result.n_folds: int

```

#### FactorOOSConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factoroosconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `train_periods`  | `int`  | `36`  | Length of the training window in index periods  |  
| `val_periods`  | `int`  | `12`  | Length of the validation window in index periods  |  
| `step_periods`  | `int`  | `6`  | Number of index periods to roll forward between folds  |  
#### CPCV Mode[¶](https://silviobaratto.github.io/optimizer/guide/factors/#cpcv-mode "Permanent link")
When a `CPCVConfig` is provided, CPCV is used instead of rolling blocks. CPCV generates all `C(n_folds, n_test_folds)` combinations with purging and embargo at train-test boundaries:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-1)from optimizer.validation import CPCVConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-3)cpcv = CPCVConfig(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-4)    n_folds=10,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-5)    n_test_folds=2,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-6)    purged_size=3,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-7)    embargo_size=5,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-9)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-10)result = run_factor_oos_validation(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-11)    scores=panel_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-12)    returns=panel_returns,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-13)    cpcv_config=cpcv,    # Overrides config when provided
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-36-14))

```

Input Format for OOS Validation
`scores` must have a two-level row MultiIndex `(date, ticker)` with one column per factor. `returns` must have the same MultiIndex with a single return column.
* * *
## 7. Diagnostics[¶](https://silviobaratto.github.io/optimizer/guide/factors/#7-diagnostics "Permanent link")
Diagnostic tools for assessing factor quality, redundancy, and data integrity.
### PCA Analysis[¶](https://silviobaratto.github.io/optimizer/guide/factors/#pca-analysis "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-1)from optimizer.factors import compute_factor_pca
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-3)pca_result = compute_factor_pca(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-4)    scores=standardized_factors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-5)    n_components=None,               # Keep all components
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-6))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-7)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-8)# pca_result.explained_variance_ratio: ndarray of variance per component
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-9)# pca_result.loadings: pd.DataFrame (factors x PCs) -- PCA loading matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-37-10)# pca_result.n_components_95pct: smallest n components for >= 95% variance

```

### Redundant Factor Detection[¶](https://silviobaratto.github.io/optimizer/guide/factors/#redundant-factor-detection "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-1)from optimizer.factors import flag_redundant_factors
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-3)redundant = flag_redundant_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-4)    scores=standardized_factors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-5)    vif_threshold=10.0,              # VIF cutoff (5 = conservative, 10 = standard)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-6))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-38-7)# redundant: list[str] of factor names with VIF > threshold

```

### Survivorship Bias Check[¶](https://silviobaratto.github.io/optimizer/guide/factors/#survivorship-bias-check "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-1)from optimizer.factors import check_survivorship_bias
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-3)has_bias = check_survivorship_bias(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-4)    returns=returns_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-5)    final_periods=12,                # Inspect last 12 periods
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-6)    zero_threshold=1e-10,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-39-8)# True if no assets have near-zero returns in the tail (potential survivorship bias)

```

The heuristic is simple: if **no** asset appears to have stopped trading (near-zero returns in the final periods), the dataset may exclude delisted or failed companies. A `UserWarning` is emitted when survivorship bias is suspected.
* * *
## 8. Mimicking Portfolios[¶](https://silviobaratto.github.io/optimizer/guide/factors/#8-mimicking-portfolios "Permanent link")
Factor-mimicking portfolios are long-short portfolios designed to isolate pure factor exposure. They are used for factor premium estimation, validation, and cross-factor correlation analysis.
### Building Mimicking Portfolios[¶](https://silviobaratto.github.io/optimizer/guide/factors/#building-mimicking-portfolios "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-1)from optimizer.factors import build_factor_mimicking_portfolios
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-3)fmp_returns = build_factor_mimicking_portfolios(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-4)    scores=scores_df,           # Dates x assets matrix for one factor
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-5)    returns=returns_df,         # Dates x assets return matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-6)    quantile=0.30,              # 30% in each leg
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-7)    weighting="equal",          # "equal" or "value"
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-40-9)# fmp_returns: pd.DataFrame with column "factor_return"

```

For each date, the top `quantile` fraction of assets (by factor score) are held long and the bottom `quantile` fraction are held short. The function processes **one factor at a time**. For multiple factors, call once per factor and concatenate:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-2)from optimizer.factors import build_factor_mimicking_portfolios
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-3)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-4)factor_returns = pd.concat([
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-5)    build_factor_mimicking_portfolios(scores_value, returns)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-6)        .rename(columns={"factor_return": "value"}),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-7)    build_factor_mimicking_portfolios(scores_mom, returns)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-8)        .rename(columns={"factor_return": "momentum"}),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-41-9)], axis=1)

```

### Beta-Neutral Mimicking Portfolios[¶](https://silviobaratto.github.io/optimizer/guide/factors/#beta-neutral-mimicking-portfolios "Permanent link")
When `beta_neutral=True`, the hedge ratio adjusts the short-leg weight to approximate zero market beta exposure:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-1)fmp_returns = build_factor_mimicking_portfolios(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-2)    scores=scores_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-3)    returns=returns_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-4)    quantile=0.30,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-5)    beta_neutral=True,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-6)    market_returns=market_series,    # Required when beta_neutral=True
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-42-7))

```

The hedge ratio is computed as `beta_long / beta_short`, where each beta is the OLS regression coefficient of the leg returns against market returns.
### Quintile Spread Analysis[¶](https://silviobaratto.github.io/optimizer/guide/factors/#quintile-spread-analysis "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-1)from optimizer.factors import compute_quintile_spread
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-3)result = compute_quintile_spread(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-4)    scores=scores_df,           # Dates x assets factor scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-5)    returns=returns_df,         # Dates x assets returns
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-6)    n_quantiles=5,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-9)# result.quintile_returns: pd.DataFrame (Dates x Q1..Q5) -- per-bucket returns
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-10)# result.spread_returns: pd.Series (Q5 - Q1) -- long-short spread
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-11)# result.annualised_mean: mean daily spread * 252
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-12)# result.t_stat: mean / (std / sqrt(T))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-43-13)# result.sharpe: mean * sqrt(252) / std

```

Assets are ranked by factor score at each date and split into `n_quantiles` equal-count buckets. Q1 = lowest scores (short), Qn = highest scores (long).
### Cross-Factor Correlation[¶](https://silviobaratto.github.io/optimizer/guide/factors/#cross-factor-correlation "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-44-1)from optimizer.factors import compute_cross_factor_correlation
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-44-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-44-3)corr_matrix = compute_cross_factor_correlation(factor_returns)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-44-4)# pd.DataFrame: factors x factors Pearson correlation matrix

```

* * *
## 9. Integration with Optimization[¶](https://silviobaratto.github.io/optimizer/guide/factors/#9-integration-with-optimization "Permanent link")
The integration layer bridges factor scores and analytics to portfolio optimization inputs: expected returns, exposure constraints, Black-Litterman views, and net alpha.
### FactorIntegrationConfig[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factorintegrationconfig "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `risk_free_rate`  | `float`  | `0.04`  | Annual risk-free rate  |  
| `market_risk_premium`  | `float`  | `0.05`  | Annual equity risk premium  |  
| `use_black_litterman`  | `bool`  | `False`  | Whether to generate BL views from factor scores  |  
| `exposure_lower_bound`  | `float`  | `-0.5`  | Lower bound for factor exposure constraints  |  
| `exposure_upper_bound`  | `float`  | `0.5`  | Upper bound for factor exposure constraints  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/factors/#presets_6 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-1)from optimizer.factors import FactorIntegrationConfig
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-3)# Direct factor score to expected return mapping
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-4)config = FactorIntegrationConfig.for_linear_mapping()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-5)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-6)# Factor-based Black-Litterman views
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-45-7)config = FactorIntegrationConfig.for_black_litterman()

```

### Factor Scores to Expected Returns[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-scores-to-expected-returns "Permanent link")
Convert factor Z-scores to expected returns via a linear model:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-46-1)E[r_i] = r_f + lambda_mkt * beta_i + sum_g lambda_g * z_{i,g}

```


```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-1)from optimizer.factors import factor_scores_to_expected_returns
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-3)expected_returns = factor_scores_to_expected_returns(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-4)    scores=group_scores,           # Assets x factor-groups DataFrame
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-5)    betas=market_betas,            # pd.Series of CAPM beta per asset
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-6)    factor_premiums={
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-7)        "market": 0.05,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-8)        "value": 0.03,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-9)        "momentum": 0.04,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-10)        "profitability": 0.02,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-11)    },
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-12)    risk_free_rate=0.02,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-47-13))

```

Assets missing from `betas` are treated as having a beta of 1.0. The `"market"` key provides the market premium; all other keys are matched against columns in `scores`.
### Factor Exposure Constraints[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-exposure-constraints "Permanent link")
Build linear inequality constraints that limit portfolio factor exposure, ready for `MeanRisk`:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-1)from optimizer.factors import build_factor_exposure_constraints
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-3)# Uniform bounds: all factors constrained to [-0.5, 0.5]
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-4)constraints = build_factor_exposure_constraints(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-5)    factor_scores=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-6)    bounds=(-0.5, 0.5),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-8)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-9)# Per-factor bounds
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-10)constraints = build_factor_exposure_constraints(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-11)    factor_scores=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-12)    bounds={
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-13)        "book_to_price": (-0.3, 0.3),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-14)        "momentum_12_1": (-0.5, 0.5),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-15)        "volatility": (-0.2, 0.2),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-16)    },
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-17))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-18)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-19)# Use with MeanRisk optimizer
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-20)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-21)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-22)model = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-23)    MeanRiskConfig.for_max_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-24)    factor_exposure_constraints=constraints,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-48-25))

```

The constraint encodes `lb_g <= sum_i w_i * z_{i,g} <= ub_g` as the pair `left_inequality @ w <= right_inequality` (two rows per factor: one for the lower bound, one for the upper bound).
Feasibility Warning
`build_factor_exposure_constraints()` checks whether the equal-weight portfolio exposure falls within the bounds for each factor. If not, a `UserWarning` is emitted indicating the constraint may be infeasible. Tighten bounds carefully.
### Black-Litterman Views from Factors[¶](https://silviobaratto.github.io/optimizer/guide/factors/#black-litterman-views-from-factors "Permanent link")
Generate relative views for Black-Litterman based on factor scores and factor premia:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-1)from optimizer.factors import build_factor_bl_views
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-3)views, confidences = build_factor_bl_views(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-4)    factor_scores=standardized,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-5)    factor_premia={"book_to_price": 0.03, "momentum_12_1": 0.06},
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-6)    selected_tickers=selected,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-8)# views: list[tuple[str, ...]] -- top-quartile vs bottom-quartile tickers
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-49-9)# confidences: list[float] -- |premium| as confidence

```

For each factor, the function identifies top-quartile and bottom-quartile assets and generates a relative view that the top outperforms the bottom by the factor premium.
### Factor Premia Estimation[¶](https://silviobaratto.github.io/optimizer/guide/factors/#factor-premia-estimation "Permanent link")
Estimate annualized factor premia from long-short factor-mimicking portfolio returns:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-50-1)from optimizer.factors import estimate_factor_premia
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-50-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-50-3)premia = estimate_factor_premia(factor_mimicking_returns)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-50-4)# dict[str, float]: annualized premium per factor (mean_daily * 252)

```

### Net Alpha[¶](https://silviobaratto.github.io/optimizer/guide/factors/#net-alpha "Permanent link")
Compute factor alpha after deducting turnover-based transaction costs:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-1)from optimizer.factors import compute_net_alpha
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-3)result = compute_net_alpha(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-4)    ic_series=ic_series,              # Time series of IC values
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-5)    weights_history=weights_df,       # Dates x assets weight matrix
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-6)    cost_bps=10.0,                    # Round-trip cost in basis points
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-7)    annualisation=252,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-8))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-9)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-10)# result.gross_alpha: mean(IC) * sqrt(252)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-11)# result.avg_turnover: mean one-way turnover across rebalancing dates
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-12)# result.total_cost: avg_turnover * cost_bps / 10_000
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-13)# result.net_alpha: gross_alpha - total_cost
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-51-14)# result.net_icir: net_alpha / (std(IC) * sqrt(252))

```

Net ICIR
`net_icir` divides the net alpha by the annualized IC volatility. A net ICIR above 0.5 is generally considered attractive for a factor strategy; above 1.0 is exceptional.
### Gross Alpha Recovery[¶](https://silviobaratto.github.io/optimizer/guide/factors/#gross-alpha-recovery "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-1)from optimizer.factors import compute_gross_alpha
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-2)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-3)gross = compute_gross_alpha(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-4)    net_alpha=0.03,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-5)    avg_turnover=0.50,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-6)    cost_bps=10.0,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-7))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-52-8)# gross = net_alpha + avg_turnover * cost_bps / 10_000

```

* * *
## End-to-End Example[¶](https://silviobaratto.github.io/optimizer/guide/factors/#end-to-end-example "Permanent link")
A complete workflow from raw data to optimized portfolio:

```
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-2)from optimizer.factors import (
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-3)    FactorConstructionConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-4)    StandardizationConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-5)    CompositeScoringConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-6)    SelectionConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-7)    RegimeTiltConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-8)    FactorValidationConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-9)    FactorIntegrationConfig,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-10)    compute_all_factors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-11)    standardize_all_factors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-12)    compute_composite_score,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-13)    select_stocks,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-14)    classify_regime,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-15)    apply_regime_tilts,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-16)    run_factor_validation,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-17)    build_factor_exposure_constraints,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-18)    FactorGroupType,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-19))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-20)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-21)# 1. Construction: compute raw factor scores
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-22)construction_config = FactorConstructionConfig.for_all_factors()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-23)raw_factors = compute_all_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-24)    fundamentals=fundamentals_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-25)    price_history=price_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-26)    volume_history=volume_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-27)    analyst_data=analyst_df,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-28)    config=construction_config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-29))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-30)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-31)# 2. Standardization: winsorize, z-score, sector-neutralize
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-32)std_config = StandardizationConfig(neutralize_sector=True)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-33)standardized, coverage = standardize_all_factors(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-34)    raw_factors, config=std_config, sector_labels=sectors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-35))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-36)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-37)# 3. Regime tilts (optional)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-38)regime = classify_regime(macro_data)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-39)base_weights = {g: 1.0 for g in FactorGroupType}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-40)tilted = apply_regime_tilts(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-41)    base_weights, regime, RegimeTiltConfig.for_moderate_tilts(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-42))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-43)group_weights = {g.value: w for g, w in tilted.items()}
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-44)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-45)# 4. Composite scoring
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-46)scoring_config = CompositeScoringConfig.for_equal_weight()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-47)composite = compute_composite_score(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-48)    standardized, coverage, config=scoring_config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-49)    group_weights=group_weights,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-50))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-51)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-52)# 5. Stock selection
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-53)selection_config = SelectionConfig.for_top_100()
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-54)selected = select_stocks(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-55)    scores=composite,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-56)    config=selection_config,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-57)    sector_labels=sectors,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-58)    parent_universe=standardized.index,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-59))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-60)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-61)# 6. Validation (on historical data)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-62)report = run_factor_validation(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-63)    factor_scores_history=historical_scores,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-64)    returns_history=historical_returns,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-65)    config=FactorValidationConfig.for_standard(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-66))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-67)print(f"Significant factors (BH): {report.significant_factors}")
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-68)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-69)# 7. Integration: build constraints for optimizer
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-70)constraints = build_factor_exposure_constraints(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-71)    factor_scores=standardized.loc[selected],
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-72)    bounds=(-0.5, 0.5),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-73))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-74)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-75)# 8. Pass to optimizer
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-76)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-77)
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-78)model = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-79)    MeanRiskConfig.for_max_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-80)    factor_exposure_constraints=constraints,
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-81))
[](https://silviobaratto.github.io/optimizer/guide/factors/#__codelineno-53-82)# model.fit(returns_selected) ...

```

* * *
## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/factors/#gotchas-and-tips "Permanent link")
  1. **Sign conventions matter.** Volatility, beta, and asset growth are sign-flipped internally so that higher values always indicate a more favorable exposure. Do not negate these yourself before passing to the pipeline.
  2. **Point-in-time alignment is critical.** Always use `align_to_pit()` with appropriate publication lags when constructing factors from fundamental data. Using `PublicationLagConfig` with source-specific lags is more accurate than a single uniform lag.
  3. **Coverage-weighted group aggregation.** `compute_group_scores()` uses a coverage-weighted mean, not a simple mean. Factors with NaN scores do not drag down the group score for tickers where they are missing -- they are simply excluded from the average.
  4. **IC-weighted fallback.** When all factor groups have negative or zero IC, both `compute_ic_weighted_composite()` and `compute_icir_weighted_composite()` fall back to equal-weight scoring rather than producing degenerate weights.
  5. **ML scoring requires temporal separation.** The `training_scores` and `training_returns` for RIDGE_WEIGHTED and GBT_WEIGHTED must not overlap with the current prediction period. The caller is responsible for this split.
  6. **Hysteresis reduces turnover.** Both `select_fixed_count()` and `select_quantile()` accept `current_members` to implement buffer-zone hysteresis. Without passing previous members, every rebalancing produces a fresh selection from scratch, potentially causing excessive turnover.
  7. **Sector balance adjustments are post-hoc.** `apply_sector_balance()` runs after the initial selection and may add or remove stocks to meet tolerance constraints. The final count may differ slightly from `target_count`.
  8. **Regime tilts are disabled by default.** `RegimeTiltConfig.enable` is `False`. When disabled, `apply_regime_tilts()` returns the original weights unchanged, even if tilt tables are defined in the config.
  9. **OOS validation input format.** `run_factor_oos_validation()` expects a two-level MultiIndex `(date, ticker)` on both `scores` and `returns`. This is different from other functions that use separate dates-x-tickers DataFrames.
  10. **Factor exposure constraints require matching tickers.** The tickers in `factor_scores` passed to `build_factor_exposure_constraints()` must match the assets used in the optimizer `fit()` call. Mismatches produce incorrect constraint matrices.


