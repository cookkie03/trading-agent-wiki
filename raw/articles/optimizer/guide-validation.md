<!-- source: https://silviobaratto.github.io/optimizer/guide/validation/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/validation/#validation)
# Validation[¶](https://silviobaratto.github.io/optimizer/guide/validation/#validation "Permanent link")
The validation module provides cross-validation strategies designed specifically for financial time series. Unlike standard k-fold CV which randomly shuffles data, these methods respect the temporal ordering of observations to prevent look-ahead bias — a critical requirement when backtesting portfolio strategies.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/validation/#overview "Permanent link")
Standard cross-validation assumes observations are i.i.d., which is violated by financial returns that exhibit autocorrelation, volatility clustering, and regime changes. The three validation strategies in this module address this by enforcing temporal ordering:
  * **Walk-Forward** — rolling or expanding window that mimics real-time portfolio management
  * **Combinatorial Purged CV (CPCV)** — generates a population of backtest paths with purging and embargoing
  * **Multiple Randomized CV** — dual randomization across time and assets for robustness testing


All validators follow the frozen-config + factory pattern: a `@dataclass(frozen=True)` config holds serializable parameters, and a factory function builds the skfolio cross-validator.
## Walk-Forward[¶](https://silviobaratto.github.io/optimizer/guide/validation/#walk-forward "Permanent link")
Walk-Forward validation partitions the time series into successive train/test windows that move forward in time. This is the most common and intuitive method — it directly simulates how a portfolio manager would use the model in practice.

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-0-1)|-------- train --------|-- test --|
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-0-2)                    |-------- train --------|-- test --|
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-0-3)                                        |-------- train --------|-- test --|

```

### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/validation/#configuration "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-1)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-3)config = WalkForwardConfig(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-4)    test_size=63,       # ~1 quarter of trading days
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-5)    train_size=252,     # ~1 year of trading days
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-6)    purged_size=5,      # observations purged between train/test (default: 5 = one trading week)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-7)    expend_train=False, # False = rolling, True = expanding
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-8)    reduce_test=False,  # allow shorter final test window
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-1-9))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `test_size`  | `int`  | 63  | Trading days per test window  |  
| `train_size`  | `int`  | 252  | Trading days per training window (initial size when expanding)  |  
| `purged_size`  | `int`  | 5  | Observations excised between train and test (one trading week)  |  
| `expend_train`  | `bool`  | `False`  |  `True` = expanding window, `False` = rolling window  |  
| `reduce_test`  | `bool`  | `False`  | Allow shorter final test window to avoid data waste  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/validation/#presets "Permanent link")  
| Preset  | test_size  | train_size  | purged_size  | Window Type  |  
| --- | --- | --- | --- | --- |  
| `for_monthly_rolling()`  | 21  | 252  | 21  | Rolling  |  
| `for_quarterly_rolling()`  | 63  | 252  | 21  | Rolling  |  
| `for_quarterly_expanding()`  | 63  | 252  | 21  | Expanding  |  
### Rolling vs Expanding[¶](https://silviobaratto.github.io/optimizer/guide/validation/#rolling-vs-expanding "Permanent link")
  * **Rolling window** (`expend_train=False`): Training window has fixed size and slides forward. Better when the market regime changes over time — older data may not be representative.
  * **Expanding window** (`expend_train=True`): Training window grows as data accumulates. Better when more data always improves estimation — the estimator benefits from a longer history.


## Combinatorial Purged Cross-Validation (CPCV)[¶](https://silviobaratto.github.io/optimizer/guide/validation/#combinatorial-purged-cross-validation-cpcv "Permanent link")
CPCV generates a combinatorial population of backtest paths from all possible selections of test folds, with purging and embargoing to prevent information leakage. Developed by Marcos Lopez de Prado, it provides a distribution of backtest performance rather than a single path.

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-1)from optimizer.validation import CPCVConfig
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-3)config = CPCVConfig(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-4)    n_folds=10,       # non-overlapping temporal blocks
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-5)    n_test_folds=8,   # blocks per test set in each combination
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-6)    purged_size=0,    # observations purged at train/test boundary
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-7)    embargo_size=0,   # observations embargoed after each test block
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-2-8))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `n_folds`  | `int`  | 10  | Number of non-overlapping temporal blocks  |  
| `n_test_folds`  | `int`  | 8  | Blocks assigned to test set per combination  |  
| `purged_size`  | `int`  | 0  | Observations purged at each train-test boundary  |  
| `embargo_size`  | `int`  | 0  | Observations embargoed after each test block  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/validation/#presets_1 "Permanent link")  
| Preset  | n_folds  | n_test_folds  | Paths  | Use Case  |  
| --- | --- | --- | --- | --- |  
| `for_statistical_testing()`  | 12  | 2  | C(12,2) = 66  | Significance testing with high statistical power  |  
| `for_small_sample()`  | 6  | 2  | C(6,2) = 15  | Shorter time series  |  
### Purging and Embargoing[¶](https://silviobaratto.github.io/optimizer/guide/validation/#purging-and-embargoing "Permanent link")
  * **Purging** : Removes observations immediately adjacent to the train-test boundary to prevent information leakage from autocorrelated returns.
  * **Embargoing** : Removes observations immediately following each test block to prevent the model from learning patterns that persist into the test period.


## Multiple Randomized CV[¶](https://silviobaratto.github.io/optimizer/guide/validation/#multiple-randomized-cv "Permanent link")
Dual randomization across both temporal windows and asset subsets to test strategy robustness along both dimensions. Each trial randomly selects a time window and a subset of assets, then runs walk-forward validation within that subsample.

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-1)from optimizer.validation import MultipleRandomizedCVConfig
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-3)config = MultipleRandomizedCVConfig(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-4)    walk_forward_config=WalkForwardConfig(),
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-5)    n_subsamples=10,       # number of random trials
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-6)    asset_subset_size=10,  # assets drawn per trial
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-7)    window_size=None,      # None = full sample
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-8)    random_state=42,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-3-9))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `walk_forward_config`  | `WalkForwardConfig`  | default  | Inner walk-forward configuration  |  
| `n_subsamples`  | `int`  | 10  | Number of random trials  |  
| `asset_subset_size`  | `int`  | 10  | Assets drawn per trial  |  
| `window_size`  |  `int` or `None`  | `None`  | Temporal window length; `None` = full sample  |  
| `random_state`  |  `int` or `None`  | `None`  | Seed for reproducibility  |  
### Preset[¶](https://silviobaratto.github.io/optimizer/guide/validation/#preset "Permanent link")  
| Preset  | n_subsamples  | asset_subset_size  | Use Case  |  
| --- | --- | --- | --- |  
| `for_robustness_check(20, 10)`  | 20  | 10  | Standard robustness testing  |  
## Running Cross-Validation[¶](https://silviobaratto.github.io/optimizer/guide/validation/#running-cross-validation "Permanent link")
The `run_cross_val` function is the main entry point for executing cross-validation:

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-4-1)from optimizer.validation import WalkForwardConfig, run_cross_val
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-4-3)cv_config = WalkForwardConfig.for_quarterly_rolling()
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-4-4)cv_result = run_cross_val(pipeline, X, cv=cv_config, y=None, n_jobs=None)

```

When no `cv` argument is provided, `run_cross_val` defaults to quarterly rolling walk-forward validation.
### Computing Optimal Folds[¶](https://silviobaratto.github.io/optimizer/guide/validation/#computing-optimal-folds "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-5-1)from optimizer.validation import compute_optimal_folds
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-5-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-5-3)n_folds = compute_optimal_folds(n_observations=1260, min_train=252, min_test=63)

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/validation/#code-examples "Permanent link")
### Walk-forward backtest[¶](https://silviobaratto.github.io/optimizer/guide/validation/#walk-forward-backtest "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-2)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-3)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-4)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-5)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-6)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-7)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-8)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-9)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-10))
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-11)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-12)# Out-of-sample performance
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-13)print(f"OOS Sharpe: {result.backtest.sharpe_ratio:.3f}")
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-6-14)print(f"OOS Max DD: {result.backtest.max_drawdown:.3f}")

```

### CPCV for backtest overfitting detection[¶](https://silviobaratto.github.io/optimizer/guide/validation/#cpcv-for-backtest-overfitting-detection "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-1)from optimizer.validation import CPCVConfig, build_cpcv, run_cross_val
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-3)cpcv = build_cpcv(CPCVConfig.for_statistical_testing())
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-4)population = run_cross_val(pipeline, X, cv=cpcv)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-5)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-6)# population is a Population object — analyze distribution of paths
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-7)for path in population:
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-7-8)    print(f"Path Sharpe: {path.sharpe_ratio:.3f}")

```

### Robustness testing with randomized CV[¶](https://silviobaratto.github.io/optimizer/guide/validation/#robustness-testing-with-randomized-cv "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-1)from optimizer.validation import MultipleRandomizedCVConfig, build_multiple_randomized_cv
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-2)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-3)config = MultipleRandomizedCVConfig.for_robustness_check(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-4)    n_subsamples=20,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-5)    asset_subset_size=15,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-6))
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-7)cv = build_multiple_randomized_cv(config)
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-8-8)population = run_cross_val(pipeline, X, cv=cv)

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/validation/#gotchas-and-tips "Permanent link")
Never use standard k-fold CV
Standard `KFold` or `StratifiedKFold` will randomly assign future data to the training set, creating look-ahead bias. Always use temporal validation methods for financial time series.
Default is quarterly rolling
`run_cross_val()` defaults to quarterly rolling walk-forward (`test_size=63`, `train_size=252`) when no `cv` is passed. This is a sensible default for daily equity returns.
CPCV returns Population, not MultiPeriodPortfolio
Walk-forward returns a `MultiPeriodPortfolio` (single path). CPCV returns a `Population` (collection of paths). Handle them differently when extracting metrics.
Purging prevents temporal leakage
For daily equity data, `purged_size=21` (one trading month) is recommended and enforced by all presets. Increase it further when using features with long look-back windows (e.g., 60-day rolling averages). For intraday data, scale proportionally.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/validation/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Quarterly rolling backtest  | `WalkForwardConfig.for_quarterly_rolling()`  |  
| Monthly rolling backtest  | `WalkForwardConfig.for_monthly_rolling()`  |  
| Expanding window  | `WalkForwardConfig.for_quarterly_expanding()`  |  
| CPCV statistical test  | `CPCVConfig.for_statistical_testing()`  |  
| Robustness check  | `MultipleRandomizedCVConfig.for_robustness_check()`  |  
| Run CV  | `run_cross_val(pipeline, X, cv=config)`  |  
| Default CV  |  `run_cross_val(pipeline, X)` → quarterly rolling  |  
## Point-in-Time Fundamental Correctness[¶](https://silviobaratto.github.io/optimizer/guide/validation/#point-in-time-fundamental-correctness "Permanent link")
### The Look-Ahead Bias Problem[¶](https://silviobaratto.github.io/optimizer/guide/validation/#the-look-ahead-bias-problem "Permanent link")
Factor scores that depend on financial statement data (book-to-price, earnings yield, ROE, asset growth, etc.) must use only the data that would have been available at each historical rebalancing date. Annual 10-K filings are published approximately 90 days after fiscal year end; quarterly 10-Q filings are published approximately 45 days after quarter end. Using the current snapshot of fundamentals at all historical dates introduces look-ahead bias: the model "sees" future earnings and balance sheet data when computing historical factor scores, overstating IC and all downstream metrics.
### The Fix (Issue #273)[¶](https://silviobaratto.github.io/optimizer/guide/validation/#the-fix-issue-273 "Permanent link")
`build_factor_scores_history()` in `research/_factors.py` accepts a `fundamental_history` parameter — a `pd.DataFrame` with `MultiIndex (period_date, ticker)` and a `period_type` column (`'annual'` | `'quarterly'`). When provided, the function calls `_slice_fundamentals_at()` at each rebalancing date, which applies differentiated publication lags via `align_to_pit()`:
  * Annual statements: 90-day lag (`PublicationLagConfig.annual_days`)
  * Quarterly statements: 45-day lag (`PublicationLagConfig.quarterly_days`)


The assembly layer (`cli/data_assembly.py`, `assemble_all()`) populates `assembly.fundamental_history` from the `financial_statements` table. The fix in `research/stock_selection_pipeline.py` passes this panel to `build_factor_scores_history()`:

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-9-1)factor_scores_history, returns_history, build_health = build_factor_scores_history(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-9-2)    ...
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-9-3)    fundamental_history=assembly.fundamental_history,   # eliminates look-ahead bias
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-9-4))

```

When `assembly.fundamental_history` is empty (DB has no financial statement history), the function falls back to snapshot mode and emits a `UserWarning`.
### Publication Lag Reference[¶](https://silviobaratto.github.io/optimizer/guide/validation/#publication-lag-reference "Permanent link")  
| Source  | Default lag  | Configurable via  |  
| --- | --- | --- |  
| Annual 10-K  | 90 days  | `PublicationLagConfig.annual_days`  |  
| Quarterly 10-Q  | 45 days  | `PublicationLagConfig.quarterly_days`  |  
| Analyst estimates  | 5 days  | `PublicationLagConfig.analyst_days`  |  
| Macro indicators  | 63 days  | `PublicationLagConfig.macro_days`  |  
## Survivorship Bias Correction[¶](https://silviobaratto.github.io/optimizer/guide/validation/#survivorship-bias-correction "Permanent link")
Delisted stocks are included in the research pipeline by default (`include_delisted=True` in `research/_data.py`). Two complementary mechanisms prevent survivorship bias:
  1. **Price-space correction** (`cli/data_assembly._apply_delisting_returns`) — appends a synthetic price row at the delisting date so `prices_to_returns()` produces the correct terminal return.
  2. **Returns-space correction** (`optimizer.preprocessing.apply_delisting_returns`) — replaces each delisted ticker's last valid return with its delisting return value. Wired into `run_full_pipeline()` via the `delisting_returns` parameter.


`DataAssembly.delisting_returns` is automatically populated by `assemble_all()` from the `instruments` table. When a ticker's `delisting_return` is NULL in the DB, a default of -30% is used.

```
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-10-1)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-10-2)    prices=assembly.prices,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-10-3)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-10-4)    delisting_returns=assembly.delisting_returns,
[](https://silviobaratto.github.io/optimizer/guide/validation/#__codelineno-10-5))

```

Tickers not present in the returns columns (e.g., filtered out by pre-selection) are silently ignored.
