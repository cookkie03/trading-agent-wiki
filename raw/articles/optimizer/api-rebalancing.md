<!-- source: https://silviobaratto.github.io/optimizer/api/rebalancing/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/rebalancing/#rebalancing)
# rebalancing[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#rebalancing "Permanent link")
###  `optimizer.rebalancing` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing "Permanent link")
Rebalancing frameworks for portfolio management.
Includes calendar-based, threshold-based, and hybrid rebalancing logic, turnover computation, and transaction cost estimation.
####  `CalendarRebalancingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig "Permanent link")
Immutable configuration for calendar-based rebalancing.
Triggers portfolio reconstruction at fixed intervals regardless of portfolio drift.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig--parameters "Permanent link")
frequency : RebalancingFrequency Rebalancing frequency.
#####  `trading_days` `property` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig.trading_days "Permanent link")
Number of trading days between rebalances.
#####  `for_monthly()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig.for_monthly "Permanent link")
Monthly rebalancing (21 trading days).
#####  `for_quarterly()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig.for_quarterly "Permanent link")
Quarterly rebalancing (63 trading days).
#####  `for_semiannual()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig.for_semiannual "Permanent link")
Semiannual rebalancing (126 trading days).
#####  `for_annual()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.CalendarRebalancingConfig.for_annual "Permanent link")
Annual rebalancing (252 trading days).
####  `HybridRebalancingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.HybridRebalancingConfig "Permanent link")
Hybrid rebalancing: check threshold only at calendar review dates.
Combines calendar and threshold strategies: the portfolio is reviewed at regular calendar intervals, but trades are executed only when drift exceeds the threshold at that review date. Between review dates, `should_rebalance_hybrid` always returns `False` regardless of drift.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.HybridRebalancingConfig--parameters "Permanent link")
calendar : CalendarRebalancingConfig Calendar schedule that defines review dates. threshold : ThresholdRebalancingConfig Drift threshold evaluated at each review date.
#####  `for_monthly_with_5pct_threshold()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.HybridRebalancingConfig.for_monthly_with_5pct_threshold "Permanent link")
Monthly review with 5pp absolute drift threshold.
#####  `for_quarterly_with_10pct_threshold()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.HybridRebalancingConfig.for_quarterly_with_10pct_threshold "Permanent link")
Quarterly review with 10pp absolute drift threshold.
####  `RebalancingFrequency` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.RebalancingFrequency "Permanent link")
Bases: `str`, `Enum`
Calendar-based rebalancing frequency.
Each value corresponds to the approximate number of trading days in the rebalancing period.
####  `ThresholdRebalancingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.ThresholdRebalancingConfig "Permanent link")
Immutable configuration for threshold-based rebalancing.
Rebalances only when portfolio drift exceeds specified limits, avoiding unnecessary turnover during stable periods.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.ThresholdRebalancingConfig--parameters "Permanent link")
threshold_type : ThresholdType Whether to use absolute or relative drift thresholds. threshold : float Drift threshold. For absolute: percentage points of weight (e.g. 0.05 = 5pp). For relative: fraction of target weight (e.g. 0.25 = 25% deviation).
#####  `for_absolute(threshold=0.05)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.ThresholdRebalancingConfig.for_absolute "Permanent link")
Absolute drift threshold (default 5pp).
#####  `for_relative(threshold=0.25)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.ThresholdRebalancingConfig.for_relative "Permanent link")
Relative drift threshold (default 25%).
####  `ThresholdType` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.ThresholdType "Permanent link")
Bases: `str`, `Enum`
Threshold convention for drift-based rebalancing.
####  `compute_drifted_weights(weights, returns)` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_drifted_weights "Permanent link")
Compute portfolio weights after one period of returns.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_drifted_weights--parameters "Permanent link")
weights : ndarray, shape (n_assets,) Current portfolio weights (must sum to 1). returns : ndarray, shape (n_assets,) Single-period asset returns.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_drifted_weights--returns "Permanent link")
ndarray, shape (n_assets,) Drifted weights after applying returns.
####  `compute_rebalancing_cost(current_weights, target_weights, transaction_costs)` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_rebalancing_cost "Permanent link")
Compute the total transaction cost of rebalancing.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_rebalancing_cost--parameters "Permanent link")
current_weights : ndarray, shape (n_assets,) Current portfolio weights. target_weights : ndarray, shape (n_assets,) Target portfolio weights. transaction_costs : float or ndarray Per-unit transaction cost (scalar for uniform costs, array for asset-specific costs).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_rebalancing_cost--returns "Permanent link")
float Total rebalancing cost as a fraction of portfolio value.
####  `compute_turnover(current_weights, target_weights)` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_turnover "Permanent link")
Compute one-way turnover between current and target weights.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_turnover--parameters "Permanent link")
current_weights : ndarray, shape (n_assets,) Current portfolio weights. target_weights : ndarray, shape (n_assets,) Target portfolio weights.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.compute_turnover--returns "Permanent link")
float One-way turnover (sum of absolute weight changes / 2).
####  `should_rebalance(current_weights, target_weights, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance "Permanent link")
Determine whether any asset breaches the drift threshold.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance--parameters "Permanent link")
current_weights : ndarray, shape (n_assets,) Current (drifted) portfolio weights. target_weights : ndarray, shape (n_assets,) Target portfolio weights from the optimiser. config : ThresholdRebalancingConfig or None Threshold configuration. Defaults to absolute 5pp threshold.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance--returns "Permanent link")
bool `True` if at least one asset breaches the threshold.
####  `should_rebalance_hybrid(current_weights, target_weights, config, current_date, last_review_date)` [¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance_hybrid "Permanent link")
Determine whether to rebalance under a hybrid calendar+threshold policy.
Returns `True` only when **both** conditions are met:
  1. `current_date` is a calendar review date — at least `config.calendar.trading_days` business days have elapsed since `last_review_date`.
  2. At least one asset's drift exceeds the threshold defined in `config.threshold`.


Between calendar review dates the function always returns `False` regardless of how much drift has accumulated.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance_hybrid--parameters "Permanent link")
current_weights : ndarray, shape (n_assets,) Current (drifted) portfolio weights. target_weights : ndarray, shape (n_assets,) Target portfolio weights from the optimiser. config : HybridRebalancingConfig Hybrid configuration combining calendar and threshold rules. current_date : pd.Timestamp The date being evaluated. last_review_date : pd.Timestamp Date of the last calendar review.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/rebalancing/#optimizer.rebalancing.should_rebalance_hybrid--returns "Permanent link")
bool `True` only if it is a calendar review date AND drift exceeds the threshold.
