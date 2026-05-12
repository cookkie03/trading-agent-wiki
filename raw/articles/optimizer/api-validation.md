<!-- source: https://silviobaratto.github.io/optimizer/api/validation/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/validation/#validation)
# validation[¶](https://silviobaratto.github.io/optimizer/api/validation/#validation "Permanent link")
###  `optimizer.validation` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation "Permanent link")
Model selection and cross-validation for portfolio backtesting.
Includes Walk-Forward backtesting, Combinatorial Purged Cross-Validation (CPCV), and Multiple Randomized Cross-Validation.
####  `CPCVConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.CPCVConfig "Permanent link")
Configuration for :class:`skfolio.model_selection.CombinatorialPurgedCV`.
Generates a population of backtest paths from all combinatorial selections of test folds, with purging and embargoing to prevent information leakage.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.CPCVConfig--parameters "Permanent link")
n_folds : int Number of non-overlapping temporal blocks. n_test_folds : int Number of blocks assigned to the test set in each combination. purged_size : int Number of observations excised on each side of the train-test boundary. embargo_size : int Number of observations embargoed immediately following each test block to avoid autocorrelation contamination.
#####  `for_statistical_testing()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.CPCVConfig.for_statistical_testing "Permanent link")
High-path-count configuration for significance testing.
Uses C(12, 2) = 66 paths with 10 training folds per split, providing high statistical power for backtest overfitting tests.
#####  `for_small_sample()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.CPCVConfig.for_small_sample "Permanent link")
Fewer folds for shorter time series.
####  `MultipleRandomizedCVConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.MultipleRandomizedCVConfig "Permanent link")
Configuration for :class:`skfolio.model_selection.MultipleRandomizedCV`.
Dual randomisation across temporal windows and asset subsets to test robustness of the strategy to both dimensions.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.MultipleRandomizedCVConfig--parameters "Permanent link")
walk_forward_config : WalkForwardConfig Inner walk-forward configuration for temporal splitting. n_subsamples : int Number of random trials. asset_subset_size : int Number of assets drawn per trial. window_size : int or None Length of the random temporal window drawn per trial. `None` uses the full sample. random_state : int or None Seed for reproducibility.
#####  `for_robustness_check(n_subsamples=20, asset_subset_size=10)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.MultipleRandomizedCVConfig.for_robustness_check "Permanent link")
Standard robustness check with 20 trials.
####  `WalkForwardConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.WalkForwardConfig "Permanent link")
Immutable configuration for :class:`skfolio.model_selection.WalkForward`.
Walk-forward backtesting partitions time series into successive train/test windows that respect the causal arrow of time.
**Purging** : A `purged_size` gap is excised between the end of the training window and the start of the test window. Without this buffer, autocorrelated returns (volatility clustering, momentum) can leak information from training observations into the first test observations, inflating out-of-sample scores. For daily equity returns a purge of 21 observations (one trading month) is the standard minimum; increase it to match the longest look-back window used by any feature in the estimator pipeline.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.WalkForwardConfig--parameters "Permanent link")
test_size : int Number of observations in each test window. train_size : int Number of observations in each training window. When `expend_train` is `True`, this is the _initial_ training window size. purged_size : int Number of observations purged between the end of the training window and the start of the test window to prevent look-ahead bias from autocorrelated returns. Defaults to 5 (one trading week). Presets use 21 (one trading month). expend_train : bool When `True`, the training window expands as new data arrives (expanding window). When `False`, the training window rolls forward (rolling window). reduce_test : bool When `True`, the last test window may be shorter than `test_size` to avoid discarding data.
#####  `for_monthly_rolling()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.WalkForwardConfig.for_monthly_rolling "Permanent link")
Monthly test windows with one-year rolling training.
Uses `purged_size=21` (one trading month) to eliminate autocorrelation leakage at the train/test boundary.
#####  `for_quarterly_rolling()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.WalkForwardConfig.for_quarterly_rolling "Permanent link")
Quarterly test windows with one-year rolling training.
Uses `purged_size=21` (one trading month) to eliminate autocorrelation leakage at the train/test boundary.
#####  `for_quarterly_expanding()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.WalkForwardConfig.for_quarterly_expanding "Permanent link")
Quarterly test windows with expanding training.
Uses `purged_size=21` (one trading month) to eliminate autocorrelation leakage at the train/test boundary.
####  `RegimeValidationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationConfig "Permanent link")
Immutable configuration for regime-conditional Sharpe analysis.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationConfig--parameters "Permanent link")
min_regime_obs : int Minimum trading days required to compute meaningful statistics for a subperiod or regime aggregate. Subperiods shorter than this produce `NaN` metrics. single_regime_alpha_threshold : float Fraction of total positive alpha above which a single regime is flagged as concentrated (acceptance criterion 4). trading_days_per_year : int Annualization constant for Sharpe, return, and volatility. risk_free_rate : float Annual risk-free rate for Sharpe ratio computation. include_unknown_regime : bool Whether to include `MacroRegime.UNKNOWN` periods in the per-regime breakdown. Default `False` since UNKNOWN days are typically data gaps.
#####  `for_standard()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationConfig.for_standard "Permanent link")
Standard defaults.
#####  `for_strict()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationConfig.for_strict "Permanent link")
Tighter thresholds for production use.
#####  `for_research()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationConfig.for_research "Permanent link")
Include unknown regime periods for diagnostics.
####  `RegimeValidationResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationResult "Permanent link")
Result of regime-conditional subperiod Sharpe analysis.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationResult--attributes "Permanent link")
per_regime_metrics : pd.DataFrame Index is regime name strings. Columns: `obs`, `coverage_pct`, `ann_return`, `ann_vol`, `sharpe`, `max_drawdown`, `obs_sufficient`. per_subperiod_metrics : pd.DataFrame One row per contiguous regime block. Columns: `start`, `end`, `regime`, `obs`, `ann_return`, `ann_vol`, `sharpe`, `max_drawdown`. regime_alpha_concentration : pd.Series Fraction of total positive alpha attributable to each regime. concentrated_regimes : list[str] Regimes exceeding `single_regime_alpha_threshold`. regime_timeline : pd.Series DatetimeIndex → regime name string for every OOS observation. total_obs : int Total number of OOS observations. n_regimes_observed : int Distinct regimes with at least one observation.
#####  `to_attribution_dict()` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.RegimeValidationResult.to_attribution_dict "Permanent link")
Serialize performance attribution across regimes.
Returns a dict suitable for frontend charting (ECharts) or CLI reporting. Structure::

```
{
  "regimes": [
    {
      "regime": "expansion",
      "obs": 120,
      "coverage_pct": 0.667,
      "ann_return": 0.52,
      "ann_vol": 0.16,
      "sharpe": 3.2,
      "max_drawdown": -0.03,
      "alpha_concentration": 0.95,
      "is_concentrated": True,
    },
    ...
  ],
  "subperiods": [
    {
      "start": "2024-01-02",
      "end": "2024-03-28",
      "regime": "expansion",
      "obs": 60,
      "ann_return": 0.50,
      "ann_vol": 0.16,
      "sharpe": 3.1,
      "max_drawdown": -0.02,
    },
    ...
  ],
  "summary": {
    "total_obs": 180,
    "n_regimes_observed": 2,
    "concentrated_regimes": ["expansion"],
    "has_concentration_warning": True,
  },
}

```

####  `build_cpcv(config=None)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_cpcv "Permanent link")
Build a skfolio :class:`CombinatorialPurgedCV` cross-validator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_cpcv--parameters "Permanent link")
config : CPCVConfig or None CPCV configuration. Defaults to `CPCVConfig()` (10 folds, 8 test folds).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_cpcv--returns "Permanent link")
CombinatorialPurgedCV A skfolio combinatorial purged cross-validator.
####  `build_multiple_randomized_cv(config=None)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_multiple_randomized_cv "Permanent link")
Build a :class:`MultipleRandomizedCV` cross-validator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_multiple_randomized_cv--parameters "Permanent link")
config : MultipleRandomizedCVConfig or None Multiple randomised CV configuration. Defaults to `MultipleRandomizedCVConfig()`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_multiple_randomized_cv--returns "Permanent link")
MultipleRandomizedCV A skfolio multi-randomised cross-validator.
####  `build_walk_forward(config=None)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_walk_forward "Permanent link")
Build a skfolio :class:`WalkForward` cross-validator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_walk_forward--parameters "Permanent link")
config : WalkForwardConfig or None Walk-forward configuration. Defaults to `WalkForwardConfig()` (quarterly rolling with one-year training window).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.build_walk_forward--returns "Permanent link")
WalkForward A skfolio temporal cross-validator.
####  `compute_optimal_folds(n_observations, target_train_size, target_n_test_paths, weight_train_size=1.0, weight_n_test_paths=1.0)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.compute_optimal_folds "Permanent link")
Compute optimal fold counts for CPCV.
Wraps :func:`skfolio.model_selection.optimal_folds_number`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.compute_optimal_folds--parameters "Permanent link")
n_observations : int Total number of observations. target_train_size : int Desired training window size. target_n_test_paths : int Desired number of backtest paths. weight_train_size : float Relative importance of matching train size. weight_n_test_paths : float Relative importance of matching path count.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.compute_optimal_folds--returns "Permanent link")
tuple[int, int] `(n_folds, n_test_folds)` optimal parameters.
####  `run_cross_val(estimator, X, *, cv=None, y=None, params=None, n_jobs=None, portfolio_params=None)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_cross_val "Permanent link")
Run cross-validated prediction with a temporal cross-validator.
Thin wrapper around :func:`skfolio.model_selection.cross_val_predict` that enforces temporal splitting (no random shuffle).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_cross_val--parameters "Permanent link")
estimator : BaseEstimator A fitted-ready skfolio optimisation estimator or pipeline. X : array-like Return matrix (observations x assets). cv : temporal cross-validator or None Cross-validator. Defaults to `WalkForward` with quarterly test windows. y : array-like or None Benchmark returns or factor returns (for models that require `fit(X, y)`). params : dict or None Auxiliary metadata forwarded to nested estimators via sklearn metadata routing (e.g. `{"implied_vol": implied_vol_df}`). Requires `sklearn.set_config(enable_metadata_routing=True)` and the relevant `set_fit_request` calls on sub-estimators. n_jobs : int or None Number of parallel jobs. portfolio_params : dict or None Additional parameters forwarded to the portfolio constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_cross_val--returns "Permanent link")
MultiPeriodPortfolio or Population Out-of-sample portfolio predictions. `WalkForward` returns a `MultiPeriodPortfolio`; `CombinatorialPurgedCV` and `MultipleRandomizedCV` return a `Population`.
####  `run_regime_validation(oos_returns, macro_data, config=None, thresholds=None)` [¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_regime_validation "Permanent link")
Run regime-conditional subperiod Sharpe analysis.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_regime_validation--parameters "Permanent link")
oos_returns : pd.Series Daily portfolio returns indexed by `DatetimeIndex`. macro_data : pd.DataFrame Macro indicators indexed by date, compatible with :func:`~optimizer.factors._regime.classify_regime_composite`. config : RegimeValidationConfig or None Validation configuration. Defaults to standard. thresholds : RegimeThresholdConfig or None Regime classification thresholds.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_regime_validation--returns "Permanent link")
RegimeValidationResult Per-regime and per-subperiod statistics with alpha concentration flags.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/validation/#optimizer.validation.run_regime_validation--raises "Permanent link")
DataError If `oos_returns` is empty.
