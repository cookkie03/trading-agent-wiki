<!-- source: https://silviobaratto.github.io/optimizer/guide/optimization/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/optimization/#optimization)
# Optimization[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#optimization "Permanent link")
Comprehensive guide to the portfolio optimization module. This module provides 10+ optimizer models spanning convex programming, hierarchical clustering, ensemble methods, robust formulations, and naive baselines. Every model follows the same pattern: **frozen`@dataclass` config** + **factory function** + **`str, Enum`types**.
* * *
## Architecture[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#architecture "Permanent link")
All optimizers produce sklearn-compatible estimators that expose `fit(X)` / `predict(X)` and compose into `sklearn.pipeline.Pipeline`. The config/factory split enforces a strict boundary:
  * **Config** (`@dataclass(frozen=True)`) -- holds only primitives, enums, and nested frozen dataclasses (serializable, hashable).
  * **Factory function** -- accepts the config plus any non-serializable objects (prior estimators, numpy arrays, constraint matrices) as keyword arguments.



```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-3)# Config: serializable, hashable, suitable for storage/logging
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-4)config = MeanRiskConfig.for_max_sharpe()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-5)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-6)# Factory: builds the skfolio estimator, accepts non-serializable kwargs
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-7)model = build_mean_risk(config, prior_estimator=my_prior)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-8)model.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-0-9)portfolio = model.predict(X)

```

* * *
## Model Overview[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#model-overview "Permanent link")  
| Model  | Config  | Factory  | Category  |  
| --- | --- | --- | --- |  
| Mean-Risk  | `MeanRiskConfig`  | `build_mean_risk()`  | Convex  |  
| Risk Budgeting  | `RiskBudgetingConfig`  | `build_risk_budgeting()`  | Convex  |  
| Max Diversification  | `MaxDiversificationConfig`  | `build_max_diversification()`  | Convex  |  
| HRP  | `HRPConfig`  | `build_hrp()`  | Hierarchical  |  
| HERC  | `HERCConfig`  | `build_herc()`  | Hierarchical  |  
| NCO  | `NCOConfig`  | `build_nco()`  | Hierarchical  |  
| Benchmark Tracker  | `BenchmarkTrackerConfig`  | `build_benchmark_tracker()`  | Convex  |  
| Equal Weighted  | `EqualWeightedConfig`  | `build_equal_weighted()`  | Naive  |  
| Inverse Volatility  | `InverseVolatilityConfig`  | `build_inverse_volatility()`  | Naive  |  
| Stacking  | `StackingConfig`  | `build_stacking()`  | Ensemble  |  
| Robust Mean-Risk  | `RobustConfig`  | `build_robust_mean_risk()`  | Robust  |  
| DR-CVaR  | `DRCVaRConfig`  | `build_dr_cvar()`  | Robust  |  
| Regime-Blended  | `RegimeRiskConfig`  | `build_regime_blended_optimizer()`  | Regime  |  
* * *
## Enums[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#enums "Permanent link")
### ObjectiveFunctionType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#objectivefunctiontype "Permanent link")
Controls what the convex optimizer maximizes or minimizes.  
| Value  | Description  |  
| --- | --- |  
| `MINIMIZE_RISK`  | Minimize the chosen risk measure subject to constraints  |  
| `MAXIMIZE_RETURN`  | Maximize expected return subject to a risk budget  |  
| `MAXIMIZE_UTILITY`  | Maximize `risk_aversion`  |  
| `MAXIMIZE_RATIO`  | Maximize the return/risk ratio (e.g. Sharpe ratio)  |  
### RiskMeasureType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#riskmeasuretype "Permanent link")
Fifteen convex risk measures available for `MeanRisk`, `RiskBudgeting`, `BenchmarkTracker`, and other convex optimizers.  
| Value  | Mathematical Definition  |  
| --- | --- |  
| `VARIANCE`  |   |  
| `SEMI_VARIANCE`  | Variance computed only on below-mean returns  |  
| `STANDARD_DEVIATION`  |   |  
| `SEMI_DEVIATION`  | Standard deviation of below-mean returns  |  
| `MEAN_ABSOLUTE_DEVIATION`  |   |  
| `FIRST_LOWER_PARTIAL_MOMENT`  |   |  
| `CVAR`  |   |  
| `EVAR`  | Entropic Value at Risk (tightest upper bound on CVaR from Chernoff inequality)  |  
| `WORST_REALIZATION`  |   |  
| `CDAR`  | Conditional Drawdown at Risk (CVaR applied to the drawdown distribution)  |  
| `MAX_DRAWDOWN`  | Maximum peak-to-trough decline  |  
| `AVERAGE_DRAWDOWN`  | Mean of the drawdown series  |  
| `EDAR`  | Entropic Drawdown at Risk  |  
| `ULCER_INDEX`  |   |  
| `GINI_MEAN_DIFFERENCE`  |   |  
### ExtraRiskMeasureType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#extrariskmeasuretype "Permanent link")
Seven non-convex risk measures available exclusively for hierarchical methods (HRP, HERC) which do not require convexity.  
| Value  | Description  |  
| --- | --- |  
| `VALUE_AT_RISK`  |   |  
| `DRAWDOWN_AT_RISK`  | VaR applied to the drawdown distribution  |  
| `ENTROPIC_RISK_MEASURE`  | Entropic risk measure  |  
| `FOURTH_CENTRAL_MOMENT`  |   |  
| `FOURTH_LOWER_PARTIAL_MOMENT`  | Fourth moment of below-mean returns  |  
| `SKEW`  | Third standardized central moment  |  
| `KURTOSIS`  | Fourth standardized central moment  |  
### DistanceType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#distancetype "Permanent link")
Distance metrics for hierarchical clustering in HRP, HERC, and NCO.  
| Value  | Description  |  
| --- | --- |  
| `PEARSON`  |   |  
| `KENDALL`  | Kendall rank correlation distance  |  
| `SPEARMAN`  | Spearman rank correlation distance  |  
| `COVARIANCE`  | Covariance-based distance (requires a covariance estimator)  |  
| `DISTANCE_CORRELATION`  | Non-linear distance correlation (captures non-linear dependencies)  |  
| `MUTUAL_INFORMATION`  | Information-theoretic distance  |  
### LinkageMethodType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#linkagemethodtype "Permanent link")
Linkage methods for agglomerative hierarchical clustering.  
| Value  | Description  |  
| --- | --- |  
| `WARD`  | Minimize within-cluster variance (default, requires Euclidean distance)  |  
| `SINGLE`  | Nearest-neighbor linkage  |  
| `COMPLETE`  | Farthest-neighbor linkage  |  
| `AVERAGE`  | Average linkage (UPGMA)  |  
| `WEIGHTED`  | Weighted average linkage (WPGMA)  |  
| `CENTROID`  | Centroid linkage  |  
| `MEDIAN`  | Median linkage  |  
### RatioMeasureType[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#ratiomeasuretype "Permanent link")
Ratio measures for scoring and ensemble quantile selection. Includes 18 standard skfolio ratio measures plus a custom `INFORMATION_RATIO` (active return / tracking error).
* * *
## Sub-Configs[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#sub-configs "Permanent link")
### DistanceConfig[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#distanceconfig "Permanent link")
Configures the distance estimator used by hierarchical methods.  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `distance_type`  | `DistanceType`  | `PEARSON`  | Distance metric  |  
| `absolute`  | `bool`  | `False`  | Apply absolute transformation to correlation matrix  |  
| `power`  | `float`  | `1.0`  | Power transformation exponent  |  
| `threshold`  | `float`  | `0.5`  | Distance correlation threshold (only for `DISTANCE_CORRELATION`)  |  

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-1)from optimizer.optimization import DistanceConfig, DistanceType
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-3)# Spearman distance (robust to outliers)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-4)dist_cfg = DistanceConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-5)    distance_type=DistanceType.SPEARMAN,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-6)    absolute=True,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-1-7))

```

### ClusteringConfig[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#clusteringconfig "Permanent link")
Configures hierarchical clustering used by HRP, HERC, and NCO.  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `max_clusters`  | `int or None`  | `None`  | Maximum number of flat clusters. `None` uses the Two-Order Difference Gap Statistic heuristic  |  
| `linkage_method`  | `LinkageMethodType`  | `WARD`  | Linkage method for the dendrogram  |  

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-1)from optimizer.optimization import ClusteringConfig, LinkageMethodType
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-3)cluster_cfg = ClusteringConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-4)    max_clusters=5,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-5)    linkage_method=LinkageMethodType.COMPLETE,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-2-6))

```

* * *
## 1. Mean-Risk Optimization (MeanRiskConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#1-mean-risk-optimization-meanriskconfig "Permanent link")
The workhorse of the module. Solves the general convex mean-risk program:
where `RiskMeasureType`.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `objective`  | `ObjectiveFunctionType`  | `MINIMIZE_RISK`  | Objective function  |  
| `risk_measure`  | `RiskMeasureType`  | `VARIANCE`  | Risk measure  |  
| `risk_aversion`  | `float`  | `1.0`  | Risk-aversion coefficient for `MAXIMIZE_UTILITY`  |  
| `efficient_frontier_size`  | `int or None`  | `None`  | Number of points on the efficient frontier (`None` = single portfolio)  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound on asset weights  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound on asset weights  |  
| `budget`  | `float or None`  | `1.0`  | Portfolio budget (sum of weights)  |  
| `max_short`  | `float or None`  | `None`  | Maximum short position  |  
| `max_long`  | `float or None`  | `None`  | Maximum long position  |  
| `cardinality`  | `int or None`  | `None`  | Maximum number of assets  |  
| `transaction_costs`  | `float`  | `0.0`  | Linear transaction costs  |  
| `management_fees`  | `float`  | `0.0`  | Linear management fees  |  
| `max_tracking_error`  | `float or None`  | `None`  | Maximum tracking error vs benchmark  |  
| `l1_coef`  | `float`  | `0.0`  | L1 regularization coefficient (promotes sparsity)  |  
| `l2_coef`  | `float`  | `0.0`  | L2 regularization coefficient (shrinks weights toward zero)  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate for ratio objectives  |  
| `cvar_beta`  | `float`  | `0.95`  | CVaR confidence level  |  
| `evar_beta`  | `float`  | `0.95`  | EVaR confidence level  |  
| `cdar_beta`  | `float`  | `0.95`  | CDaR confidence level  |  
| `edar_beta`  | `float`  | `0.95`  | EDaR confidence level  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver name  |  
| `solver_params`  | `dict or None`  | `None`  | Additional solver parameters  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Inner prior configuration  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-1)from optimizer.optimization import MeanRiskConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-3)# Minimum-variance portfolio
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-4)config = MeanRiskConfig.for_min_variance()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-5)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-6)# Maximum Sharpe ratio
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-7)config = MeanRiskConfig.for_max_sharpe()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-8)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-9)# Maximum utility with custom risk aversion
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-10)config = MeanRiskConfig.for_max_utility(risk_aversion=2.0)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-11)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-12)# Minimum CVaR at 99% confidence
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-13)config = MeanRiskConfig.for_min_cvar(beta=0.99)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-14)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-15)# Efficient frontier with 30 points
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-3-16)config = MeanRiskConfig.for_efficient_frontier(size=30)

```

### Factory: build_mean_risk()[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#factory-build_mean_risk "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-3)# Basic usage
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-4)model = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-5)model.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-6)portfolio = model.predict(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-7)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-8)# With prior estimator and factor constraints
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-9)from optimizer.moments import build_prior, MomentEstimationConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-10)from optimizer.factors import build_factor_exposure_constraints
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-11)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-12)prior = build_prior(MomentEstimationConfig.for_shrunk_denoised())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-13)constraints = build_factor_exposure_constraints(...)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-14)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-15)model = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-16)    config,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-17)    prior_estimator=prior,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-18)    factor_exposure_constraints=constraints,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-19)    previous_weights=old_weights,  # for transaction cost optimization
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-4-20))

```

**Factory kwargs** (non-serializable, not stored in config): - `prior_estimator` -- skfolio `BasePrior` instance - `factor_exposure_constraints` -- `FactorExposureConstraints` (injects `left_inequality` / `right_inequality`) - `previous_weights` -- numpy array for turnover-aware optimization - `groups` -- asset group labels - `linear_constraints` -- additional linear constraints
### Short-Selling Example[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#short-selling-example "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-1)config = MeanRiskConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-2)    objective=ObjectiveFunctionType.MAXIMIZE_RATIO,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-3)    risk_measure=RiskMeasureType.VARIANCE,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-4)    min_weights=-0.3,    # allow up to 30% short per asset
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-5)    max_weights=0.5,     # max 50% long per asset
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-6)    max_short=0.5,       # total short exposure <= 50%
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-7)    max_long=1.5,        # total long exposure <= 150%
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-8)    budget=1.0,          # net exposure = 100%
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-5-9))

```

### Cardinality-Constrained Example[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#cardinality-constrained-example "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-1)config = MeanRiskConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-2)    objective=ObjectiveFunctionType.MINIMIZE_RISK,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-3)    risk_measure=RiskMeasureType.VARIANCE,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-4)    cardinality=15,      # at most 15 assets
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-5)    l1_coef=0.001,       # L1 regularization for sparsity
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-6-6))

```

* * *
## 2. Risk Budgeting (RiskBudgetingConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#2-risk-budgeting-riskbudgetingconfig "Permanent link")
Risk parity and generalized risk budgeting. Each asset contributes a pre-specified share of total portfolio risk:
where **risk parity**.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_1 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `risk_measure`  | `RiskMeasureType`  | `VARIANCE`  | Risk measure  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound on asset weights  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound on asset weights  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate  |  
| `cvar_beta`  | `float`  | `0.95`  | CVaR confidence level  |  
| `evar_beta`  | `float`  | `0.95`  | EVaR confidence level  |  
| `cdar_beta`  | `float`  | `0.95`  | CDaR confidence level  |  
| `edar_beta`  | `float`  | `0.95`  | EDaR confidence level  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver name  |  
| `solver_params`  | `dict or None`  | `None`  | Additional solver parameters  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Inner prior configuration  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-1)from optimizer.optimization import RiskBudgetingConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-3)# Equal risk contribution (risk parity) with variance
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-4)config = RiskBudgetingConfig.for_risk_parity()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-5)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-6)# Risk parity with CVaR
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-7)config = RiskBudgetingConfig.for_cvar_parity(beta=0.95)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-8)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-9)# Risk parity with CDaR
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-7-10)config = RiskBudgetingConfig.for_cdar_parity(beta=0.95)

```

### Factory: build_risk_budgeting()[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#factory-build_risk_budgeting "Permanent link")
The `risk_budget` array is passed as a factory kwarg because numpy arrays are not hashable in frozen dataclasses.

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-1)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-2)from optimizer.optimization import RiskBudgetingConfig, build_risk_budgeting
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-4)# Equal risk parity (default when risk_budget=None)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-5)model = build_risk_budgeting(RiskBudgetingConfig.for_risk_parity())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-6)model.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-7)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-8)# Custom risk budgets: 60% risk to equities, 40% to bonds
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-9)budgets = np.array([0.15, 0.15, 0.15, 0.15, 0.20, 0.20])
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-10)model = build_risk_budgeting(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-11)    RiskBudgetingConfig.for_cvar_parity(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-12)    risk_budget=budgets,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-8-13))

```

**Gotcha** : When `risk_budget=None`, skfolio assigns equal budgets (1/n per asset). You do not need to manually construct the equal-weight array.
* * *
## 3. Maximum Diversification (MaxDiversificationConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#3-maximum-diversification-maxdiversificationconfig "Permanent link")
Maximizes the diversification ratio:
where 
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_2 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound on asset weights  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound on asset weights  |  
| `budget`  | `float or None`  | `1.0`  | Portfolio budget  |  
| `max_short`  | `float or None`  | `None`  | Maximum short position  |  
| `max_long`  | `float or None`  | `None`  | Maximum long position  |  
| `cardinality`  | `int or None`  | `None`  | Maximum number of assets  |  
| `l1_coef`  | `float`  | `0.0`  | L1 regularization  |  
| `l2_coef`  | `float`  | `0.0`  | L2 regularization  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver  |  
| `solver_params`  | `dict or None`  | `None`  | Solver parameters  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-9-1)from optimizer.optimization import MaxDiversificationConfig, build_max_diversification
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-9-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-9-3)config = MaxDiversificationConfig(l2_coef=0.01)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-9-4)model = build_max_diversification(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-9-5)model.fit(X)

```

* * *
## 4. Hierarchical Risk Parity -- HRP (HRPConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#4-hierarchical-risk-parity-hrp-hrpconfig "Permanent link")
Hierarchical Risk Parity (Lopez de Prado, 2016) avoids matrix inversion entirely. It builds a hierarchical clustering dendrogram from asset distances, then allocates risk by recursively bisecting the dendrogram and inverse-variance weighting each split.
### Algorithm Steps[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#algorithm-steps "Permanent link")
  1. Compute a distance matrix from asset returns (e.g. Pearson correlation distance)
  2. Build a hierarchical clustering dendrogram using a linkage method
  3. Quasi-diagonalize the covariance matrix according to the dendrogram ordering
  4. Recursively bisect the dendrogram, allocating weights inversely proportional to cluster risk at each split


### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_3 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `risk_measure`  | `RiskMeasureType`  | `VARIANCE`  | Convex risk measure  |  
| `extra_risk_measure`  | `ExtraRiskMeasureType or None`  | `None`  | Non-convex risk measure (overrides `risk_measure` when set)  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound on asset weights  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound on asset weights  |  
| `distance_config`  | `DistanceConfig or None`  | `None`  | Distance estimator configuration  |  
| `clustering_config`  | `ClusteringConfig or None`  | `None`  | Clustering configuration  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_2 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-10-1)from optimizer.optimization import HRPConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-10-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-10-3)config = HRPConfig.for_variance()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-10-4)config = HRPConfig.for_cvar()

```

### Usage with Custom Distance and Clustering[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage-with-custom-distance-and-clustering "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-1)from optimizer.optimization import (
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-2)    HRPConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-3)    build_hrp,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-4)    DistanceConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-5)    DistanceType,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-6)    ClusteringConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-7)    LinkageMethodType,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-8)    ExtraRiskMeasureType,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-9))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-10)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-11)config = HRPConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-12)    risk_measure=RiskMeasureType.CVAR,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-13)    distance_config=DistanceConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-14)        distance_type=DistanceType.SPEARMAN,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-15)        absolute=True,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-16)    ),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-17)    clustering_config=ClusteringConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-18)        max_clusters=5,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-19)        linkage_method=LinkageMethodType.COMPLETE,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-20)    ),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-21))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-22)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-23)model = build_hrp(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-11-24)model.fit(X)

```

### Using Non-Convex Risk Measures[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#using-non-convex-risk-measures "Permanent link")
HRP and HERC support non-convex risk measures via `extra_risk_measure`. When set, it overrides `risk_measure`:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-12-1)config = HRPConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-12-2)    extra_risk_measure=ExtraRiskMeasureType.VALUE_AT_RISK,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-12-3))

```

* * *
## 5. Hierarchical Equal Risk Contribution -- HERC (HERCConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#5-hierarchical-equal-risk-contribution-herc-hercconfig "Permanent link")
HERC (Thomas et al., 2018) extends HRP by equalizing risk contributions within each cluster, similar to risk budgeting but applied to the hierarchical tree structure. Unlike HRP, HERC can use a solver for the intra-cluster allocation step.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_4 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `risk_measure`  | `RiskMeasureType`  | `VARIANCE`  | Convex risk measure  |  
| `extra_risk_measure`  | `ExtraRiskMeasureType or None`  | `None`  | Non-convex risk measure (overrides `risk_measure`)  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver  |  
| `solver_params`  | `dict or None`  | `None`  | Solver parameters  |  
| `distance_config`  | `DistanceConfig or None`  | `None`  | Distance configuration  |  
| `clustering_config`  | `ClusteringConfig or None`  | `None`  | Clustering configuration  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_3 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-13-1)from optimizer.optimization import HERCConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-13-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-13-3)config = HERCConfig.for_variance()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-13-4)config = HERCConfig.for_cvar()

```

### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-1)from optimizer.optimization import HERCConfig, build_herc
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-3)config = HERCConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-4)    risk_measure=RiskMeasureType.CVAR,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-5)    clustering_config=ClusteringConfig(max_clusters=4),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-6))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-7)model = build_herc(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-14-8)model.fit(X)

```

* * *
## 6. Nested Clusters Optimization -- NCO (NCOConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#6-nested-clusters-optimization-nco-ncoconfig "Permanent link")
NCO (Lopez de Prado, 2019) addresses the instability of mean-variance by decomposing the optimization into intra-cluster and inter-cluster stages:
  1. Cluster assets using hierarchical clustering
  2. Run an **inner optimizer** within each cluster
  3. Run an **outer optimizer** across the cluster-level portfolios


### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_5 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `quantile`  | `float`  | `0.5`  | Quantile for portfolio selection across CV folds  |  
| `n_jobs`  | `int or None`  | `None`  | Number of parallel jobs  |  
| `distance_config`  | `DistanceConfig or None`  | `None`  | Distance configuration  |  
| `clustering_config`  | `ClusteringConfig or None`  | `None`  | Clustering configuration  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_2 "Permanent link")
The inner and outer estimators are passed as factory kwargs because they are not serializable:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-1)from optimizer.optimization import (
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-2)    NCOConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-3)    build_nco,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-4)    build_mean_risk,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-5)    MeanRiskConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-6))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-7)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-8)inner = build_mean_risk(MeanRiskConfig.for_min_variance())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-9)outer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-10)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-11)config = NCOConfig(quantile=0.5)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-12)model = build_nco(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-13)    config,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-14)    inner_estimator=inner,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-15)    outer_estimator=outer,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-16))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-15-17)model.fit(X)

```

* * *
## 7. Benchmark Tracker (BenchmarkTrackerConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#7-benchmark-tracker-benchmarktrackerconfig "Permanent link")
Minimizes tracking error against a benchmark index. The benchmark returns are passed as `y` in `fit(X, y)`.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_6 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `risk_measure`  | `RiskMeasureType`  | `STANDARD_DEVIATION`  | Risk measure for tracking error  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound  |  
| `max_short`  | `float or None`  | `None`  | Maximum short  |  
| `max_long`  | `float or None`  | `None`  | Maximum long  |  
| `cardinality`  | `int or None`  | `None`  | Maximum assets  |  
| `transaction_costs`  | `float`  | `0.0`  | Transaction costs  |  
| `management_fees`  | `float`  | `0.0`  | Management fees  |  
| `l1_coef`  | `float`  | `0.0`  | L1 regularization  |  
| `l2_coef`  | `float`  | `0.0`  | L2 regularization  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver  |  
| `solver_params`  | `dict or None`  | `None`  | Solver parameters  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_3 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-1)from optimizer.optimization import BenchmarkTrackerConfig, build_benchmark_tracker
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-3)config = BenchmarkTrackerConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-4)    cardinality=50,       # replicate benchmark with at most 50 stocks
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-5)    l1_coef=0.001,        # sparse tracking
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-6))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-7)model = build_benchmark_tracker(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-8)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-9)# benchmark_returns is a 1-D array/Series aligned with X
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-10)model.fit(X, y=benchmark_returns)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-16-11)portfolio = model.predict(X)

```

**Gotcha** : Benchmark returns must be passed as `y` in `fit(X, y)`, not as part of the config or factory kwargs.
* * *
## 8. Equal Weighted (EqualWeightedConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#8-equal-weighted-equalweightedconfig "Permanent link")
The naive 1/N allocation. Assigns identical weight 
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_4 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-17-1)from optimizer.optimization import EqualWeightedConfig, build_equal_weighted
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-17-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-17-3)model = build_equal_weighted(EqualWeightedConfig())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-17-4)model.fit(X)

```

`EqualWeightedConfig` has no parameters.
* * *
## 9. Inverse Volatility (InverseVolatilityConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#9-inverse-volatility-inversevolatilityconfig "Permanent link")
Weights each asset inversely proportional to its estimated volatility:
The volatility estimates come from the diagonal of the covariance matrix provided by the prior estimator.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_7 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration (covariance estimator determines volatility)  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_5 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-1)from optimizer.optimization import InverseVolatilityConfig, build_inverse_volatility
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-2)from optimizer.moments import MomentEstimationConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-4)config = InverseVolatilityConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-5)    prior_config=MomentEstimationConfig.for_shrunk_denoised(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-6))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-7)model = build_inverse_volatility(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-18-8)model.fit(X)

```

* * *
## 10. Stacking Optimization (StackingConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#10-stacking-optimization-stackingconfig "Permanent link")
Ensemble method that combines multiple sub-optimizers via a meta-optimizer. Each sub-optimizer produces a portfolio, and the meta-optimizer allocates across those portfolios.
### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_8 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `quantile`  | `float`  | `0.5`  | Quantile for portfolio selection across CV folds  |  
| `quantile_measure`  | `RatioMeasureType`  | `SHARPE_RATIO`  | Ratio measure for quantile selection  |  
| `n_jobs`  | `int or None`  | `None`  | Number of parallel jobs  |  
| `cv`  | `int or None`  | `None`  | Cross-validation folds (`None` = no CV)  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_6 "Permanent link")
The `estimators` list and `final_estimator` are passed as factory kwargs:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-1)from optimizer.optimization import (
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-2)    StackingConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-3)    build_stacking,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-4)    build_mean_risk,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-5)    build_hrp,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-6)    MeanRiskConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-7)    HRPConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-8)    RatioMeasureType,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-9))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-10)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-11)sub_optimizers = [
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-12)    ("min_var", build_mean_risk(MeanRiskConfig.for_min_variance())),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-13)    ("max_sharpe", build_mean_risk(MeanRiskConfig.for_max_sharpe())),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-14)    ("hrp", build_hrp(HRPConfig.for_variance())),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-15)]
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-16)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-17)meta = build_mean_risk(MeanRiskConfig.for_min_variance())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-18)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-19)config = StackingConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-20)    quantile=0.5,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-21)    quantile_measure=RatioMeasureType.SHARPE_RATIO,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-22)    cv=5,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-23))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-24)model = build_stacking(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-25)    config,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-26)    estimators=sub_optimizers,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-27)    final_estimator=meta,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-28))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-19-29)model.fit(X)

```

**Default estimators** : When `estimators=None`, the factory defaults to `[("mean_risk", MeanRisk()), ("hrp", HierarchicalRiskParity())]`.
* * *
## Robust Variants[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#robust-variants "Permanent link")
### 11. Robust Mean-Risk (RobustConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#11-robust-mean-risk-robustconfig "Permanent link")
Hedges against estimation error in the expected return vector by constructing an ellipsoidal uncertainty set around the sample mean and optimizing for the worst-case expected return within that set.
#### Uncertainty Set for Expected Returns[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#uncertainty-set-for-expected-returns "Permanent link")
The ellipsoidal uncertainty set is:
where: - 
The worst-case expected return within 
The penalty term 
#### Kappa-Confidence Level Mapping[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#kappa-confidence-level-mapping "Permanent link")
The parameter 
where `confidence_level` is deferred to the `fit()` call.
#### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_9 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `kappa`  | `float`  | `1.0`  | Ellipsoidal uncertainty radius for `kappa=0` recovers standard MeanRisk exactly  |  
| `cov_uncertainty`  | `bool`  | `False`  | Also apply covariance uncertainty set  |  
| `cov_uncertainty_method`  | `str`  | `"bootstrap"`  |  `"bootstrap"` (stationary block bootstrap) or `"empirical"` (formula-based)  |  
| `B`  | `int`  | `500`  | Number of bootstrap resamples (only for `"bootstrap"` method)  |  
| `block_size`  | `int`  | `21`  | Expected block length for stationary bootstrap (~1 trading month)  |  
| `bootstrap_alpha`  | `float`  | `0.05`  | Significance level for covariance uncertainty ellipsoid  |  
| `mean_risk_config`  | `MeanRiskConfig or None`  | `None`  | Embedded mean-risk configuration  |  
#### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_4 "Permanent link")  
| Preset  | kappa  | cov_uncertainty  | Use Case  |  
| --- | --- | --- | --- |  
| `for_conservative()`  | 2.0  | `False`  | High estimation uncertainty (short history, non-stationary)  |  
| `for_moderate()`  | 1.0  | `False`  | Balanced trade-off  |  
| `for_aggressive()`  | 0.5  | `False`  | Closer to standard MeanRisk  |  
| `for_bootstrap_covariance()`  | 1.0  | `True`  | Hedges against both mean and covariance estimation error  |  
#### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_7 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-1)from optimizer.optimization import RobustConfig, build_robust_mean_risk, MeanRiskConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-3)# Conservative: strong robustness
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-4)model = build_robust_mean_risk(RobustConfig.for_conservative())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-5)model.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-6)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-7)# kappa=0: identical to standard MeanRisk (no penalty)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-8)baseline = build_robust_mean_risk(RobustConfig(kappa=0.0))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-9)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-10)# Robust max-Sharpe with bootstrap covariance uncertainty
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-11)config = RobustConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-12)    kappa=1.5,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-13)    cov_uncertainty=True,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-14)    cov_uncertainty_method="bootstrap",
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-15)    B=1000,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-16)    block_size=21,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-17)    mean_risk_config=MeanRiskConfig.for_max_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-18))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-19)model = build_robust_mean_risk(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-20-20)model.fit(X)

```

#### Standalone Bootstrap Covariance Utility[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#standalone-bootstrap-covariance-utility "Permanent link")
The module also exposes `bootstrap_covariance_uncertainty()` for standalone analysis of covariance estimation uncertainty:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-1)from optimizer.optimization import bootstrap_covariance_uncertainty
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-3)result = bootstrap_covariance_uncertainty(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-4)    returns,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-5)    B=500,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-6)    block_size=21,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-7)    alpha=0.05,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-8)    seed=42,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-9))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-10)print(f"Frobenius-norm confidence radius: {result.delta:.4f}")
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-11)print(f"Sample covariance shape: {result.cov_hat.shape}")
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-21-12)print(f"Bootstrap samples shape: {result.cov_samples.shape}")  # (500, n, n)

```

The Frobenius-norm confidence set is 
* * *
### 12. Distributionally Robust CVaR (DRCVaRConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#12-distributionally-robust-cvar-drcvarconfig "Permanent link")
Minimizes the worst-case CVaR over all probability distributions within a Wasserstein ball of radius 
The tractable SOCP reformulation (Esfahani and Kuhn, 2018) is solved via skfolio's `DistributionallyRobustCVaR`, which exposes this as a risk-aversion utility:
#### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_10 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `epsilon`  | `float`  | `0.001`  | Wasserstein ball radius. Larger values = more conservative. `epsilon=0` = standard CVaR  |  
| `alpha`  | `float`  | `0.95`  | CVaR confidence level  |  
| `risk_aversion`  | `float`  | `1.0`  | Risk-aversion coefficient `epsilon=0`)  |  
| `norm`  | `int`  | `2`  | Wasserstein norm order. **Only L2 is supported**  |  
| `min_weights`  | `float or None`  | `0.0`  | Lower bound  |  
| `max_weights`  | `float or None`  | `1.0`  | Upper bound  |  
| `budget`  | `float or None`  | `1.0`  | Portfolio budget  |  
| `max_short`  | `float or None`  | `None`  | Maximum short  |  
| `max_long`  | `float or None`  | `None`  | Maximum long  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate  |  
| `solver`  | `str`  | `"CLARABEL"`  | CVXPY solver. `MOSEK` preferred for large instances  |  
| `solver_params`  | `dict or None`  | `None`  | Solver parameters  |  
| `prior_config`  | `MomentEstimationConfig or None`  | `None`  | Prior configuration  |  
#### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_5 "Permanent link")  
| Preset  | epsilon  | Description  |  
| --- | --- | --- |  
| `for_conservative()`  | `0.01`  | Wider ball, more robust against tail risk misspecification  |  
| `for_standard()`  | `0.001`  | Moderate hedge against distribution misspecification  |  
#### Dispatch Behavior[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#dispatch-behavior "Permanent link")
The factory `build_dr_cvar()` dispatches to different skfolio classes based on epsilon:
  * **epsilon = 0** : Returns `MeanRisk(MINIMIZE_RISK, CVAR)` -- identical to standard empirical CVaR minimization.
  * **epsilon > 0**: Returns `DistributionallyRobustCVaR` -- solves the Wasserstein DRO reformulation.


#### Usage[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#usage_8 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-1)from optimizer.optimization import DRCVaRConfig, build_dr_cvar
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-3)# Conservative DRO-CVaR
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-4)model = build_dr_cvar(DRCVaRConfig.for_conservative())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-5)model.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-6)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-7)# epsilon=0 -> standard CVaR (exact equivalence)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-8)baseline = build_dr_cvar(DRCVaRConfig(epsilon=0.0))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-9)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-10)# Custom: 99% CVaR, wider Wasserstein ball
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-11)config = DRCVaRConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-12)    epsilon=0.05,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-13)    alpha=0.99,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-14)    risk_aversion=2.0,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-15))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-16)model = build_dr_cvar(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-22-17)model.fit(X)

```

**Gotcha** : Only `norm=2` (L2 Wasserstein) is supported. Setting any other value raises `ValueError` at config construction via `__post_init__` validation.
* * *
### 13. Regime-Blended Optimization (RegimeRiskConfig)[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#13-regime-blended-optimization-regimeriskconfig "Permanent link")
HMM-driven regime-conditional risk measure selection and risk budgeting. Uses a fitted Hidden Markov Model to select the risk measure based on the current market regime.
#### Blended Risk Measure[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#blended-risk-measure "Permanent link")
The probability-weighted blended risk is:
where 
#### Configuration Fields[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#configuration-fields_11 "Permanent link")  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `regime_measures`  | `tuple[RiskMeasureType, ...]`  | (required)  | One risk measure per HMM state. Must match `HMMResult.n_states`  |  
| `hmm_config`  | `HMMConfig`  | `HMMConfig()`  | HMM hyper-parameters  |  
| `cvar_beta`  | `float`  | `0.95`  | CVaR confidence level  |  
#### Presets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#presets_6 "Permanent link")  
| Preset  | States  | Risk Measures  | Description  |  
| --- | --- | --- | --- |  
| `for_calm_stress()`  | 2  | Variance, CVaR  | Low-vol regime uses variance; stress regime uses CVaR  |  
| `for_calm_stress_drawdown()`  | 2  | Variance, CDaR  | Low-vol regime uses variance; stress regime uses CDaR  |  
| `for_three_regimes()`  | 3  | Variance, MAD, CVaR  | Calm/normal/stress with increasing tail sensitivity  |  
#### Blended Optimizer[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#blended-optimizer "Permanent link")
Because skfolio's `MeanRisk` requires a single convex risk measure, `build_regime_blended_optimizer()` selects the risk measure of the **dominant regime** (the state with the highest current probability):

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-1)from optimizer.moments import HMMConfig, fit_hmm
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-2)from optimizer.optimization import RegimeRiskConfig, build_regime_blended_optimizer
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-4)# Fit HMM
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-5)hmm_result = fit_hmm(returns, HMMConfig(n_states=2))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-6)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-7)# Build optimizer using dominant regime's risk measure
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-8)config = RegimeRiskConfig.for_calm_stress()
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-9)model = build_regime_blended_optimizer(config, hmm_result)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-23-10)model.fit(X)

```

#### Blended Risk Computation[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#blended-risk-computation "Permanent link")
For analytics and monitoring, `compute_blended_risk_measure()` computes the full probability-weighted blended risk:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-1)from optimizer.optimization import compute_blended_risk_measure
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-2)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-3)risk = compute_blended_risk_measure(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-4)    returns,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-5)    weights,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-6)    hmm_result,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-7)    regime_measures=(RiskMeasureType.VARIANCE, RiskMeasureType.CVAR),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-8)    cvar_beta=0.95,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-24-9))

```

Regimes with fewer than 5 observations fall back to full-sample risk computation.
#### Regime-Conditional Risk Budgets[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#regime-conditional-risk-budgets "Permanent link")
`build_regime_risk_budgeting()` computes a probability-weighted blended budget vector and passes it to `build_risk_budgeting()`:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-1)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-2)from optimizer.optimization import (
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-3)    RiskBudgetingConfig,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-4)    build_regime_risk_budgeting,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-5))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-6)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-7)# Per-regime budget vectors
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-8)calm_budget = np.array([0.25, 0.25, 0.25, 0.25])     # equal in calm
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-9)stress_budget = np.array([0.10, 0.10, 0.40, 0.40])    # tilt to safe assets in stress
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-10)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-11)model = build_regime_risk_budgeting(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-12)    RiskBudgetingConfig.for_risk_parity(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-13)    hmm_result,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-14)    regime_budgets=[calm_budget, stress_budget],
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-15))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-25-16)model.fit(X)

```

* * *
## Common Patterns[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#common-patterns "Permanent link")
### Passing Prior Estimators[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#passing-prior-estimators "Permanent link")
All convex optimizers accept a `prior_estimator` factory kwarg. When `None`, the factory checks `config.prior_config` and builds a prior from it. If both are `None`, skfolio's default empirical prior is used.

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-1)from optimizer.moments import MomentEstimationConfig, build_prior
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-4)# Option 1: via config (serializable)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-5)config = MeanRiskConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-6)    prior_config=MomentEstimationConfig.for_shrunk_denoised(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-7))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-8)model = build_mean_risk(config)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-9)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-10)# Option 2: via factory kwarg (non-serializable, takes precedence)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-11)prior = build_prior(MomentEstimationConfig.for_adaptive())
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-26-12)model = build_mean_risk(config, prior_estimator=prior)

```

### Factor Exposure Constraints[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#factor-exposure-constraints "Permanent link")
`build_mean_risk()` accepts a `factor_exposure_constraints` kwarg that injects `left_inequality` and `right_inequality` matrices:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-1)from optimizer.factors import build_factor_exposure_constraints
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-4)constraints = build_factor_exposure_constraints(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-5)    factor_scores=scores,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-6)    target_exposures=targets,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-7)    tolerance=0.1,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-8))
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-9)model = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-10)    MeanRiskConfig.for_min_variance(),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-11)    factor_exposure_constraints=constraints,
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-27-12))

```

Explicit `left_inequality` / `right_inequality` entries in kwargs take precedence over the constraints object.
### Pipeline Integration[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#pipeline-integration "Permanent link")
All optimizers are sklearn-compatible and compose into pipelines:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-1)from sklearn.pipeline import Pipeline
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-2)from optimizer.optimization import build_mean_risk, MeanRiskConfig
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-4)pipe = Pipeline([
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-5)    ("optimizer", build_mean_risk(MeanRiskConfig.for_max_sharpe())),
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-6)])
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-28-7)pipe.fit(X)

```

Nested parameter access uses sklearn's `__` notation:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-1)# Access nested parameters for tuning
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-2)pipe.get_params()["optimizer__l2_coef"]
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-3)
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-4)# Set parameters for grid search
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-5)param_grid = {
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-6)    "optimizer__l2_coef": [0.0, 0.001, 0.01],
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-7)    "optimizer__risk_aversion": [0.5, 1.0, 2.0],
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-29-8)}

```

* * *
## Solver Notes[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#solver-notes "Permanent link")
All convex optimizers default to `solver="CLARABEL"`, an open-source interior-point solver. For large instances or specific problem structures:  
| Solver  | License  | Best For  |  
| --- | --- | --- |  
| `CLARABEL`  | Open source (Apache 2.0)  | General-purpose default  |  
| `MOSEK`  | Commercial  | Large-scale SOCP/SDP, DR-CVaR  |  
| `SCS`  | Open source  | Large sparse problems  |  
| `ECOS`  | Open source  | Small to medium conic programs  |  
Pass solver parameters via `solver_params`:

```
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-30-1)config = MeanRiskConfig(
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-30-2)    solver="MOSEK",
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-30-3)    solver_params={"MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-10},
[](https://silviobaratto.github.io/optimizer/guide/optimization/#__codelineno-30-4))

```

* * *
## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/optimization/#gotchas-and-tips "Permanent link")
  1. **Non-serializable objects are factory kwargs, not config fields.** Prior estimators, risk budget arrays, inner/outer estimators (NCO), and estimator lists (Stacking) must be passed to the factory function, not stored in the config.
  2. **`kappa=0`and`epsilon=0` recover standard models exactly.** `RobustConfig(kappa=0.0)` produces the same result as `build_mean_risk()`. `DRCVaRConfig(epsilon=0.0)` produces the same result as `MeanRisk(MINIMIZE_RISK, CVAR)`.
  3. **HRP/HERC support non-convex risk measures; convex optimizers do not.** Use `ExtraRiskMeasureType` only with `HRPConfig` and `HERCConfig`. When `extra_risk_measure` is set, it overrides `risk_measure`.
  4. **Benchmark returns are`y` , not part of the config.** For `BenchmarkTracker`, always call `model.fit(X, y=benchmark_returns)`.
  5. **Regime measures must match HMM states.** `len(config.regime_measures)` must equal `hmm_result.n_states`, or a `ConfigurationError` is raised.
  6. **DR-CVaR only supports L2 norm.** Setting `norm` to anything other than `2` raises `ValueError` at construction time.
  7. **Stacking defaults.** When `estimators=None`, the factory defaults to `[("mean_risk", MeanRisk()), ("hrp", HierarchicalRiskParity())]` with skfolio defaults.
  8. **Cardinality constraints make the problem mixed-integer.** Using `cardinality` may significantly increase solve time. Consider L1 regularization (`l1_coef`) as a convex relaxation alternative.
  9. **Transaction costs require`previous_weights`.** The `transaction_costs` field in `MeanRiskConfig` penalizes turnover relative to `previous_weights`, which must be passed as a factory kwarg.
  10. **ClusteringConfig`max_clusters=None` uses automatic selection.** The Two-Order Difference Gap Statistic heuristic determines the optimal number of clusters automatically.


