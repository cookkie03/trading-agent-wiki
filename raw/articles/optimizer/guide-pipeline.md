<!-- source: https://silviobaratto.github.io/optimizer/guide/pipeline/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/pipeline/#pipeline-overview)
# Pipeline Overview[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#pipeline-overview "Permanent link")
The pipeline module orchestrates the full portfolio construction workflow — from raw price data through preprocessing, optimization, validation, and rebalancing into a single function call. It composes sklearn-compatible transformers and skfolio optimizers into a unified `Pipeline` object that can be cross-validated, tuned, and serialized.
## Architecture[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#architecture "Permanent link")
The optimizer library follows a linear data-flow architecture:

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-0-1)prices → returns → [preprocess → pre-select → optimize] → backtest → weights

```

The conversion from prices to returns happens **outside** the sklearn pipeline (it changes data semantics from levels to differences), while everything inside the brackets is a single `sklearn.pipeline.Pipeline` object.

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-1)┌─────────────────────────────────────────────────────────────┐
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-2)│                     run_full_pipeline()                      │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-3)│                                                              │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-4)│  prices ──→ prices_to_returns() ──→ returns DataFrame        │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-5)│                                         │                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-6)│           ┌─────────────────────────────┤                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-7)│           │  build_portfolio_pipeline() │                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-8)│           │                             │                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-9)│           │  validate ──→ outliers ──→ impute                │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-10)│           │      ──→ SelectComplete ──→ DropZeroVariance     │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-11)│           │      ──→ DropCorrelated ──→ [SelectKExtremes]    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-12)│           │      ──→ optimizer (skfolio)                     │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-13)│           └─────────────────────────────┘                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-14)│                                         │                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-15)│  backtest (walk-forward CV) ←───────────┘                    │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-16)│  fit full data → final weights                               │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-17)│  rebalancing check (if previous_weights)                     │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-18)│                                                              │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-19)│  → PortfolioResult                                           │
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-1-20)└──────────────────────────────────────────────────────────────┘

```

### Why prices_to_returns() runs outside[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#why-prices_to_returns-runs-outside "Permanent link")
The sklearn pipeline convention requires that `fit(X)` and `transform(X)` operate on the same kind of data. Price-to-return conversion changes the data semantics (levels become differences, one row is consumed), so it runs before pipeline construction. Inside the pipeline, every transformer receives and returns a return DataFrame.
### Flattened pipeline for parameter access[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#flattened-pipeline-for-parameter-access "Permanent link")
`build_portfolio_pipeline()` flattens the pre-selection sub-pipeline steps into the top-level pipeline so that `get_params()` exposes all nested parameters for hyperparameter tuning:

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-1)from optimizer.pipeline import build_portfolio_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-4)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-5)pipeline = build_portfolio_pipeline(optimizer)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-6)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-7)# All pre-selection + optimizer params are accessible
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-8)print(pipeline.get_params().keys())
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-9)# dict_keys(['validate__max_abs_return', 'outliers__winsorize_threshold',
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-2-10)#             'drop_correlated__threshold', 'optimizer__risk_measure', ...])

```

## Core Functions[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#core-functions "Permanent link")
### run_full_pipeline[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#run_full_pipeline "Permanent link")
The primary entry point. Converts prices to returns, builds the pipeline, optionally backtests, fits on the full dataset, and checks rebalancing thresholds:

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-2)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-3)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-4)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-5)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-6)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-7)    prices=price_df,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-8)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-9)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-10))
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-11)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-12)print(result.weights)              # pd.Series: ticker → weight
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-13)print(result.summary)              # dict: sharpe_ratio, max_drawdown, ...
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-3-14)print(result.backtest.sharpe_ratio) # out-of-sample Sharpe

```

**Parameters:**  
| Parameter  | Type  | Description  |  
| --- | --- | --- |  
| `prices`  | `pd.DataFrame`  | Price matrix (dates x tickers)  |  
| `optimizer`  | skfolio optimizer  | From any `build_*()` factory  |  
| `pre_selection_config`  |  `PreSelectionConfig` or `None`  | Data cleaning config  |  
| `sector_mapping`  |  `dict[str, str]` or `None`  | Ticker → sector for imputation  |  
| `cv_config`  |  `WalkForwardConfig` or `None`  |  `None` skips backtesting  |  
| `previous_weights`  |  `ndarray` or `None`  | For rebalancing analysis  |  
| `rebalancing_config`  |  `ThresholdRebalancingConfig` / `HybridRebalancingConfig` or `None`  | Rebalancing strategy  |  
| `current_date`  |  `pd.Timestamp` or `None`  | For hybrid rebalancing  |  
| `last_review_date`  |  `pd.Timestamp` or `None`  | For hybrid rebalancing  |  
| `y_prices`  |  `pd.DataFrame` or `None`  | Benchmark/factor prices  |  
| `n_jobs`  |  `int` or `None`  | Parallel jobs for backtesting  |  
### run_full_pipeline_with_selection[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#run_full_pipeline_with_selection "Permanent link")
Extends `run_full_pipeline` with upstream stock selection. When `fundamentals` is provided, the function:
  1. Screens the universe for investability
  2. Computes and standardizes factor scores
  3. Applies macro regime tilts (optional)
  4. Computes composite score and selects stocks
  5. Delegates to `run_full_pipeline()` on the selected tickers



```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-1)from optimizer.pipeline import run_full_pipeline_with_selection
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-2)from optimizer.factors import SelectionConfig, CompositeScoringConfig
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-4)result = run_full_pipeline_with_selection(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-5)    prices=price_df,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-6)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-7)    fundamentals=fundamentals_df,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-8)    volume_history=volume_df,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-9)    scoring_config=CompositeScoringConfig(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-10)    selection_config=SelectionConfig(n_stocks=50),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-11)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-4-12))

```

When `fundamentals=None`, all selection steps are skipped and the function delegates directly to `run_full_pipeline()`.
### Lower-level composable functions[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#lower-level-composable-functions "Permanent link")
For more control, use the individual building blocks:

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-1)from optimizer.pipeline import optimize, backtest, tune_and_optimize, build_portfolio_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-2)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-4)# Manual pipeline composition
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-5)X = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-6)pipeline = build_portfolio_pipeline(optimizer)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-7)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-8)# Option 1: Just optimize (no backtest)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-9)result = optimize(pipeline, X)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-10)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-11)# Option 2: Backtest first, then optimize
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-12)bt = backtest(pipeline, X, cv_config=WalkForwardConfig.for_quarterly_rolling())
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-13)result = optimize(pipeline, X)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-14)result.backtest = bt
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-15)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-16)# Option 3: Tune hyperparameters then optimize
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-17)result = tune_and_optimize(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-18)    pipeline, X,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-19)    param_grid={"optimizer__l2_coef": [0.0, 0.01, 0.1]},
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-5-20))

```

## PortfolioResult[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#portfolioresult "Permanent link")
All pipeline functions return a `PortfolioResult` dataclass:  
| Field  | Type  | Description  |  
| --- | --- | --- |  
| `weights`  | `pd.Series`  | Final asset weights (ticker → weight)  |  
| `portfolio`  | skfolio `Portfolio`  | In-sample portfolio with `.sharpe_ratio`, `.max_drawdown`, `.composition`  |  
| `backtest`  |  `MultiPeriodPortfolio` / `Population` / `None`  | Out-of-sample results; `None` when backtesting was skipped  |  
| `pipeline`  | sklearn `Pipeline`  | The fitted pipeline, reusable for `predict()` on new data  |  
| `summary`  | `dict[str, float]`  | Key metrics: `mean`, `annualized_mean`, `variance`, `standard_deviation`, `sharpe_ratio`, `sortino_ratio`, `max_drawdown`, `cvar`  |  
| `rebalance_needed`  |  `bool` or `None`  | Whether drift exceeds thresholds; `None` when no previous weights  |  
| `turnover`  |  `float` or `None`  | One-way turnover vs previous weights  |  
## Transaction Cost Deduction[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#transaction-cost-deduction "Permanent link")
For net-of-cost backtest analysis, use `compute_net_backtest_returns`:

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-1)from optimizer.pipeline import compute_net_backtest_returns
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-2)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-3)net_returns = compute_net_backtest_returns(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-4)    gross_returns=backtest_returns,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-5)    weight_changes=weight_change_df,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-6)    cost_bps=10.0,  # 10 basis points per unit of turnover
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-6-7))

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#code-examples "Permanent link")
### Minimal pipeline[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#minimal-pipeline "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-2)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-4)optimizer = build_mean_risk(MeanRiskConfig.for_min_variance())
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-5)result = run_full_pipeline(prices=prices, optimizer=optimizer)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-7-6)print(result.weights)

```

### With rebalancing[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#with-rebalancing "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-1)from optimizer.rebalancing import ThresholdRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-4)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-5)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-6)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-7)    previous_weights=np.array([0.25, 0.25, 0.25, 0.25]),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-8)    rebalancing_config=ThresholdRebalancingConfig(threshold=0.05),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-9))
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-10)print(f"Rebalance needed: {result.rebalance_needed}")
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-8-11)print(f"Turnover: {result.turnover:.4f}")

```

### With stock selection[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#with-stock-selection "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-1)from optimizer.factors import SelectionConfig, CompositeScoringConfig
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-2)from optimizer.universe import InvestabilityScreenConfig
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-4)result = run_full_pipeline_with_selection(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-5)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-6)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-7)    fundamentals=fundamentals,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-8)    volume_history=volume,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-9)    investability_config=InvestabilityScreenConfig.for_developed_markets(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-10)    scoring_config=CompositeScoringConfig(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-11)    selection_config=SelectionConfig(n_stocks=50),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-12)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-9-13))

```

### Hyperparameter tuning[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#hyperparameter-tuning "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-1)from optimizer.pipeline import tune_and_optimize, build_portfolio_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-2)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-3)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-4)X = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-5)pipeline = build_portfolio_pipeline(optimizer)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-6)
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-7)result = tune_and_optimize(
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-8)    pipeline, X,
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-9)    param_grid={
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-10)        "optimizer__l2_coef": [0.0, 0.01, 0.1],
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-11)        "drop_correlated__threshold": [0.90, 0.95],
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-12)    },
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-13))
[](https://silviobaratto.github.io/optimizer/guide/pipeline/#__codelineno-10-14)print(f"Best params: {result.pipeline.get_params()}")

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#gotchas-and-tips "Permanent link")
prices_to_returns() is not in the pipeline
The price-to-return conversion runs **outside** the sklearn pipeline. Do not add it as a pipeline step — it changes data dimensionality (drops one row) which breaks cross-validation fold alignment.
previous_weights alignment
When `previous_weights` is passed to `run_full_pipeline()`, the function auto-aligns them on the post-pre-selection universe and re-normalizes. If pre-selection drops assets, their previous weights are set to zero and the remainder is rescaled to sum to 1.
Benchmark returns via y_prices
For `BenchmarkTracker` or any model that requires `fit(X, y)`, pass benchmark prices via `y_prices`. They are converted to returns alongside asset prices.
Sector mapping
Sector mapping is injected as a plain `dict[str, str]` (ticker → sector label), not queried from a database. Assets not in the mapping are assigned to an `"__unmapped__"` sector.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/pipeline/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Basic optimization  | `run_full_pipeline(prices, optimizer)`  |  
| With backtest  | `run_full_pipeline(prices, optimizer, cv_config=WalkForwardConfig())`  |  
| With rebalancing  | `run_full_pipeline(prices, optimizer, previous_weights=w, rebalancing_config=cfg)`  |  
| With stock selection  | `run_full_pipeline_with_selection(prices, optimizer, fundamentals=df)`  |  
| Manual pipeline  |  `build_portfolio_pipeline(optimizer)` then `optimize(pipeline, X)`  |  
| Tune + optimize  | `tune_and_optimize(pipeline, X, param_grid={...})`  |  
| Net-of-cost returns  | `compute_net_backtest_returns(gross, changes, cost_bps=10)`  |
