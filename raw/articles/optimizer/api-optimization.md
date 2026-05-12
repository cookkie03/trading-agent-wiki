<!-- source: https://silviobaratto.github.io/optimizer/api/optimization/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/optimization/#optimization)
# optimization[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimization "Permanent link")
###  `optimizer.optimization` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization "Permanent link")
Portfolio optimization models.
Includes Mean-Risk, Risk Budgeting, Maximum Diversification, HRP, HERC, NCO, Benchmark Tracking, naive baselines (Equal Weighted, Inverse Volatility), ensemble (Stacking) optimisation, robust mean-risk with ellipsoidal uncertainty sets, bootstrap covariance uncertainty, and distributionally robust CVaR over a Wasserstein ball.
####  `BenchmarkTrackerConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.BenchmarkTrackerConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.BenchmarkTracker`.
Minimises tracking error against benchmark returns (passed as `y` in `fit(X, y)`). Non-serialisable objects (`prior_estimator`, `previous_weights`, `groups`, `linear_constraints`) are passed as keyword arguments to the factory function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.BenchmarkTrackerConfig--parameters "Permanent link")
risk_measure : RiskMeasureType Risk measure for tracking error (default: standard deviation). min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. max_short : float or None Maximum short position. max_long : float or None Maximum long position. cardinality : int or None Maximum number of assets. transaction_costs : float Linear transaction costs. management_fees : float Linear management fees. l1_coef : float L1 regularisation coefficient. l2_coef : float L2 regularisation coefficient. risk_free_rate : float Risk-free rate. solver : str CVXPY solver name. solver_params : dict or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration.
####  `ClusteringConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.ClusteringConfig "Permanent link")
Immutable configuration for hierarchical clustering.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.ClusteringConfig--parameters "Permanent link")
max_clusters : int or None Maximum number of flat clusters. `None` uses the Two-Order Difference to Gap Statistic heuristic. linkage_method : LinkageMethodType Linkage method for building the dendrogram.
####  `DistanceConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DistanceConfig "Permanent link")
Immutable configuration for a distance estimator.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DistanceConfig--parameters "Permanent link")
distance_type : DistanceType Which distance estimator to build. absolute : bool Whether to apply absolute transformation to the correlation matrix (Pearson, Kendall, Spearman, Covariance distances). power : float Exponent of the power transformation applied to the correlation matrix. threshold : float Distance correlation threshold (only for `DISTANCE_CORRELATION`).
####  `DistanceType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DistanceType "Permanent link")
Bases: `str`, `Enum`
Distance estimator selection.
Maps to the distance classes in :mod:`skfolio.distance`.
####  `EqualWeightedConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.EqualWeightedConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.EqualWeighted`.
The equal-weighted portfolio assigns identical weight to each asset (1/N). No estimation is required.
####  `ExtraRiskMeasureType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.ExtraRiskMeasureType "Permanent link")
Bases: `str`, `Enum`
Non-convex risk measure selection (for HRP/HERC).
Maps to :class:`skfolio.measures.ExtraRiskMeasure`.
####  `HERCConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HERCConfig "Permanent link")
Immutable config for HERC optimisation.
Wraps :class:`skfolio.optimization.HierarchicalEqualRiskContribution`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HERCConfig--parameters "Permanent link")
risk_measure : RiskMeasureType Convex risk measure. extra_risk_measure : ExtraRiskMeasureType or None Non-convex risk measure (overrides `risk_measure` when set). min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. solver : str CVXPY solver name. solver_params : dict or None Additional solver parameters. distance_config : DistanceConfig or None Distance estimator configuration. clustering_config : ClusteringConfig or None Hierarchical clustering configuration. prior_config : MomentEstimationConfig or None Inner prior configuration.
#####  `for_variance()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HERCConfig.for_variance "Permanent link")
HERC with variance risk measure.
#####  `for_cvar()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HERCConfig.for_cvar "Permanent link")
HERC with CVaR risk measure.
####  `HRPConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HRPConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.HierarchicalRiskParity`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HRPConfig--parameters "Permanent link")
risk_measure : RiskMeasureType Convex risk measure. extra_risk_measure : ExtraRiskMeasureType or None Non-convex risk measure (overrides `risk_measure` when set). min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. distance_config : DistanceConfig or None Distance estimator configuration. clustering_config : ClusteringConfig or None Hierarchical clustering configuration. prior_config : MomentEstimationConfig or None Inner prior configuration.
#####  `for_variance()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HRPConfig.for_variance "Permanent link")
HRP with variance risk measure.
#####  `for_cvar()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.HRPConfig.for_cvar "Permanent link")
HRP with CVaR risk measure.
####  `InverseVolatilityConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.InverseVolatilityConfig "Permanent link")
Immutable config for :class:`skfolio.optimization.InverseVolatility`.
Scales each position inversely to its estimated volatility.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.InverseVolatilityConfig--parameters "Permanent link")
prior_config : MomentEstimationConfig or None Inner prior configuration (covariance estimator determines volatility estimates).
####  `LinkageMethodType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.LinkageMethodType "Permanent link")
Bases: `str`, `Enum`
Linkage method selection for hierarchical clustering.
Maps to :class:`skfolio.cluster.LinkageMethod`.
####  `MaxDiversificationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MaxDiversificationConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.MaximumDiversification`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MaxDiversificationConfig--parameters "Permanent link")
min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. budget : float or None Portfolio budget (sum of weights). max_short : float or None Maximum short position. max_long : float or None Maximum long position. cardinality : int or None Maximum number of assets. l1_coef : float L1 regularisation coefficient. l2_coef : float L2 regularisation coefficient. risk_free_rate : float Risk-free rate. solver : str CVXPY solver name. solver_params : dict or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration.
####  `MeanRiskConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.MeanRisk`.
Serialisable parameters only. Non-serialisable objects (`prior_estimator`, `previous_weights`, `groups`, `linear_constraints`, etc.) are passed as keyword arguments to the factory function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig--parameters "Permanent link")
objective : ObjectiveFunctionType Objective function. risk_measure : RiskMeasureType Convex risk measure. risk_aversion : float Risk-aversion coefficient (`MAXIMIZE_UTILITY`). efficient_frontier_size : int or None Number of points on the efficient frontier (`None` = single portfolio). min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. budget : float or None Portfolio budget (sum of weights). max_short : float or None Maximum short position. max_long : float or None Maximum long position. cardinality : int or None Maximum number of assets. transaction_costs : float Linear transaction costs penalising turnover relative to `previous_weights`. management_fees : float Linear management fees proportional to position size. max_tracking_error : float or None Maximum tracking error relative to benchmark returns (passed as `y` in `fit(X, y)`). l1_coef : float L1 regularisation coefficient. l2_coef : float L2 regularisation coefficient. risk_free_rate : float Risk-free rate for ratio objectives. cvar_beta : float CVaR confidence level. evar_beta : float EVaR confidence level. cdar_beta : float CDaR confidence level. edar_beta : float EDaR confidence level. solver : str CVXPY solver name. solver_params : dict or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration. max_sector_weight : float or None Maximum total weight allocated to any single sector. When set, `build_mean_risk()` requires a `sector_mapping` kwarg to resolve sector membership. `None` disables sector constraints (default).
#####  `for_min_variance()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_min_variance "Permanent link")
Minimum-variance portfolio.
#####  `for_max_sharpe()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_max_sharpe "Permanent link")
Maximum Sharpe-ratio portfolio.
#####  `for_max_sharpe_diversified()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_max_sharpe_diversified "Permanent link")
Maximum Sharpe with diversification constraints.
Targets the Sharpe ratio while using L2 regularisation and a per-asset weight cap to enforce diversification and keep volatility stable. Uses ShrunkMu + DenoiseCovariance for robust moment estimates.
#####  `for_concentrated_sharpe()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_concentrated_sharpe "Permanent link")
Max Sharpe for concentrated portfolios (15-30 stocks).
Uses `min_weights=0.01` to ensure all selected stocks get a meaningful allocation and `max_weights=0.10` to cap individual positions. L2 regularisation pushes toward equal-weight.
#####  `for_max_sharpe_sector_constrained(max_sector_weight=0.25)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_max_sharpe_sector_constrained "Permanent link")
Max Sharpe with per-asset and per-sector diversification constraints.
Combines L2 regularisation, a 10% per-asset cap, and a uniform per-sector cap to prevent sector concentration.
Uses ShrunkMu + DenoiseCovariance for robust moment estimates.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_max_sharpe_sector_constrained--parameters "Permanent link")
max_sector_weight : float Maximum total weight for any single sector. Default 0.25.
#####  `for_max_utility(risk_aversion=1.0)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_max_utility "Permanent link")
Maximum utility portfolio.
#####  `for_min_cvar(beta=0.95)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_min_cvar "Permanent link")
Minimum-CVaR portfolio.
#####  `for_efficient_frontier(size=20, risk_measure=RiskMeasureType.VARIANCE)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.MeanRiskConfig.for_efficient_frontier "Permanent link")
Efficient frontier with _size_ portfolios.
####  `NCOConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.NCOConfig "Permanent link")
Immutable config for NCO optimisation.
Wraps :class:`skfolio.optimization.NestedClustersOptimization`.
The `inner_estimator` and `outer_estimator` are passed as factory arguments (not stored here) because they are not serialisable.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.NCOConfig--parameters "Permanent link")
quantile : float Quantile for portfolio selection across cross-validation folds. n_jobs : int or None Number of parallel jobs for cross-validation. distance_config : DistanceConfig or None Distance estimator configuration. clustering_config : ClusteringConfig or None Hierarchical clustering configuration.
####  `ObjectiveFunctionType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.ObjectiveFunctionType "Permanent link")
Bases: `str`, `Enum`
Objective function selection.
Maps to :class:`skfolio.optimization.convex._base.ObjectiveFunction`.
####  `RatioMeasureType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RatioMeasureType "Permanent link")
Bases: `str`, `Enum`
Ratio measure selection for scoring (e.g. stacking meta-optimiser).
Most members map directly to :class:`skfolio.measures.RatioMeasure`. `INFORMATION_RATIO` is implemented as a custom scorer (active return divided by tracking error) because skfolio does not expose it natively; use :func:`~optimizer.scoring.build_scorer` with a `benchmark_returns` argument to build the corresponding callable.
####  `RiskBudgetingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig "Permanent link")
Immutable configuration for :class:`skfolio.optimization.RiskBudgeting`.
The `risk_budget` array is passed as a factory argument (not stored here) because `numpy` arrays are not hashable in frozen dataclasses.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig--parameters "Permanent link")
risk_measure : RiskMeasureType Convex risk measure. min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. risk_free_rate : float Risk-free rate. cvar_beta : float CVaR confidence level. evar_beta : float EVaR confidence level. cdar_beta : float CDaR confidence level. edar_beta : float EDaR confidence level. solver : str CVXPY solver name. solver_params : dict or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration.
#####  `for_risk_parity()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig.for_risk_parity "Permanent link")
Equal risk-budget (risk parity) with variance.
#####  `for_cvar_parity(beta=0.95)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig.for_cvar_parity "Permanent link")
Equal risk-budget with CVaR.
#####  `for_cdar_parity(beta=0.95)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig.for_cdar_parity "Permanent link")
Equal risk-budget with CDaR.
####  `RiskMeasureType` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskMeasureType "Permanent link")
Bases: `str`, `Enum`
Convex risk measure selection.
Maps to :class:`skfolio.measures.RiskMeasure`.
####  `StackingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.StackingConfig "Permanent link")
Immutable config for :class:`skfolio.optimization.StackingOptimization`.
Combines multiple optimisers into an ensemble via a meta-optimiser. The `estimators` list and `final_estimator` are passed as factory arguments (not stored here) because they are not serialisable.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.StackingConfig--parameters "Permanent link")
quantile : float Quantile for portfolio selection across cross-validation folds. quantile_measure : RatioMeasureType Ratio measure used when selecting the quantile portfolio. n_jobs : int or None Number of parallel jobs for cross-validation. cv : int or None Number of cross-validation folds (`None` = no cross-validation).
####  `DRCVaRConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DRCVaRConfig "Permanent link")
Immutable configuration for distributionally robust CVaR optimization.
Finds the allocation that minimises the worst-case CVaR over all probability distributions within a Wasserstein ball of radius `epsilon` centred at the empirical distribution::

```
min_w  sup_{P ∈ B_ε(P̂)} CVaR_α^P(w)

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DRCVaRConfig--parameters "Permanent link")
epsilon : float Wasserstein ball radius ε ≥ 0. Larger values produce more conservative, diversified portfolios. `epsilon=0` recovers standard empirical CVaR minimisation exactly. alpha : float CVaR confidence level α ∈ (0, 1). Passed as `cvar_beta` to skfolio. risk_aversion : float Risk-aversion coefficient λ for the utility formulation when `epsilon > 0`::

```
    max_w  μ̂ᵀw − λ · worst-case-CVaR_α(w)

``lambda=1`` (default) balances expected return and CVaR.
Ignored when ``epsilon=0``.

```

norm : int Wasserstein norm order. Only `norm=2` (L2) is supported by the current skfolio backend. Any other value raises `ValueError` at construction time. min_weights : float or None Lower bound on asset weights. max_weights : float or None Upper bound on asset weights. budget : float or None Portfolio budget (sum of weights). max_short : float or None Maximum short position. max_long : float or None Maximum long position. risk_free_rate : float Risk-free rate. solver : str CVXPY solver name. `MOSEK` is preferred for large instances; `CLARABEL` is the open-source default. solver_params : dict or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration. `None` uses skfolio's default empirical prior.
#####  `for_conservative()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DRCVaRConfig.for_conservative "Permanent link")
Conservative DRO-CVaR portfolio (ε=0.01).
Suitable for markets where the empirical distribution may substantially underestimate tail risk.
#####  `for_standard()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.DRCVaRConfig.for_standard "Permanent link")
Standard DRO-CVaR portfolio (ε=0.001).
Moderate hedge against distribution misspecification.
####  `RegimeRiskConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig "Permanent link")
Configuration for Markov-driven blended risk measure optimisation.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig--attributes "Permanent link")
regime_measures : tuple[RiskMeasureType, ...] One :class:`RiskMeasureType` per HMM state (index = state label). States are sorted by ascending mean return after HMM fitting, so state 0 is always the lowest-mean regime (bear/stress). E.g. `(CVAR, VARIANCE)` means bear → CVaR, bull → variance. Must match `HMMResult.n_states`. hmm_config : HMMConfig HMM hyper-parameters used when fitting inside the pipeline. cvar_beta : float Confidence level for CVaR / ES computation (default 0.95 = 95th percentile).
#####  `for_calm_stress(**kwargs)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig.for_calm_stress "Permanent link")
Two-regime preset: bear/stress → CVaR, calm/bull → variance.
States are sorted by ascending mean return after HMM fitting, so state 0 is always the lowest-mean regime (bear/stress).
#####  `for_calm_stress_drawdown(**kwargs)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig.for_calm_stress_drawdown "Permanent link")
Two-regime preset: bear/stress → CDaR, calm/bull → variance.
States are sorted by ascending mean return after HMM fitting, so state 0 is always the lowest-mean regime (bear/stress).
#####  `for_three_regimes(**kwargs)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig.for_three_regimes "Permanent link")
Three-regime: bear → CVaR, normal → MAD, bull → variance.
States are sorted by ascending mean return after HMM fitting, so state 0 is always the lowest-mean regime (bear/stress).
####  `CovarianceUncertaintyResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.CovarianceUncertaintyResult "Permanent link")
Result of bootstrap covariance uncertainty estimation.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.CovarianceUncertaintyResult--attributes "Permanent link")
cov_hat : np.ndarray, shape (n_assets, n_assets) Sample covariance matrix estimated from the full return series. delta : float Frobenius-norm confidence radius: the `(1-alpha)` quantile of `‖Σ_b - Σ̂‖_F` across B stationary bootstrap samples. cov_samples : np.ndarray, shape (B, n_assets, n_assets) Bootstrap covariance estimates, one per bootstrap resample.
####  `RobustConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig "Permanent link")
Immutable configuration for robust mean-risk optimization.
Implements ellipsoidal uncertainty sets for μ (and optionally Σ) to hedge against estimation error in the input parameters.
The robust objective modifies the standard mean-risk problem by assuming the true mean lies within the ellipsoid U_μ and optimising for the worst-case expected return::

```
min_w  ρ(w)       subject to  min_{μ ∈ U_μ} μᵀw ≥ target

```

The worst-case mean within U_μ is::

```
min_{μ ∈ U_μ} μᵀw  =  μ̂ᵀw − κ · ‖S_μ^(1/2) · w‖₂

```

so the penalty grows with κ and with the portfolio's exposure to estimation uncertainty.
When `cov_uncertainty=True` and `cov_uncertainty_method="bootstrap"` a stationary block bootstrap is used (via `arch`) to construct a skfolio `BootstrapCovarianceUncertaintySet`. The `"empirical"` method falls back to `EmpiricalCovarianceUncertaintySet`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig--parameters "Permanent link")
kappa : float Ellipsoidal uncertainty radius for μ. Larger κ produces more conservative (diversified) portfolios. `kappa=0` recovers the standard (non-robust) MeanRisk exactly. cov_uncertainty : bool If True, also apply a covariance uncertainty set to hedge against covariance estimation error. The method is controlled by `cov_uncertainty_method`. cov_uncertainty_method : str Method for covariance uncertainty set construction. `"bootstrap"` (default) uses stationary block bootstrap via `BootstrapCovarianceUncertaintySet`; `"empirical"` uses the formula-based `EmpiricalCovarianceUncertaintySet`. B : int Number of bootstrap resamples for the stationary block bootstrap (only used when `cov_uncertainty_method="bootstrap"`). block_size : int Expected block length for the stationary bootstrap (≈ 1 trading month). Only used when `cov_uncertainty_method="bootstrap"`. bootstrap_alpha : float Significance level for the covariance uncertainty ellipsoid; the `BootstrapCovarianceUncertaintySet` confidence level is set to `1 - bootstrap_alpha`. Only used when `cov_uncertainty_method="bootstrap"`. mean_risk_config : MeanRiskConfig or None Embedded mean-risk configuration (objective, risk measure, weight bounds, …). `None` uses `MeanRiskConfig()` defaults (minimum-variance, long-only, fully invested).
#####  `for_conservative()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig.for_conservative "Permanent link")
Conservative robust portfolio (κ=2.0).
Suitable when estimation uncertainty is high (short history, non-stationary markets).
#####  `for_moderate()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig.for_moderate "Permanent link")
Moderate robust portfolio (κ=1.0).
Balanced trade-off between estimation uncertainty and expected return.
#####  `for_aggressive()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig.for_aggressive "Permanent link")
Mildly robust portfolio (κ=0.5).
Closer to the standard mean-risk solution; retains most of the in-sample expected return while still penalising extreme concentration.
#####  `for_bootstrap_covariance()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RobustConfig.for_bootstrap_covariance "Permanent link")
Robust portfolio with bootstrap covariance uncertainty (κ=1.0).
Combines mean-vector robustness (κ=1.0) with stationary block bootstrap covariance uncertainty to hedge against both sources of estimation error.
####  `build_dr_cvar(config=None, *, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_dr_cvar "Permanent link")
Build a distributionally robust CVaR optimiser from _config_.
Dispatches to:
  * **ε=0** — :class:`skfolio.optimization.MeanRisk` with `MINIMIZE_RISK` and `CVAR`. Identical to standard CVaR minimisation on the empirical distribution.
  * **ε >0** — :class:`skfolio.optimization.DistributionallyRobustCVaR` with `wasserstein_ball_radius=epsilon`. Solves the Wasserstein DRO reformulation via the built-in SOCP.


Wasserstein norm note ~~~~~~~~~~~~~~~~~~~~~ Only `norm=2` (L2-Wasserstein) is supported. The config enforces this via `__post_init__` validation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_dr_cvar--parameters "Permanent link")
config : DRCVaRConfig or None DRO-CVaR configuration. Defaults to `DRCVaRConfig()` (ε=0.001, α=0.95, long-only, fully invested). prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.prior_config` (or skfolio's empirical default). **kwargs Additional keyword arguments forwarded to the underlying skfolio constructor (e.g. `groups`, `linear_constraints`, `previous_weights`).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_dr_cvar--returns "Permanent link")
MeanRisk When `epsilon=0`: standard CVaR-minimising :class:`MeanRisk`. DistributionallyRobustCVaR When `epsilon>0`: Wasserstein DRO-CVaR optimiser.
####  `build_benchmark_tracker(config=None, *, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_benchmark_tracker "Permanent link")
Build a skfolio :class:`BenchmarkTracker` optimiser from _config_.
The resulting model minimises tracking error against benchmark returns. Pass benchmark returns as `y` in `model.fit(X, y)`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_benchmark_tracker--parameters "Permanent link")
config : BenchmarkTrackerConfig or None Benchmark tracker configuration. Defaults to `BenchmarkTrackerConfig()`. prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.prior_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`BenchmarkTracker` constructor (for non-serialisable parameters such as `previous_weights`, `groups`, `linear_constraints`).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_benchmark_tracker--returns "Permanent link")
BenchmarkTracker A fitted-ready skfolio optimiser.
####  `build_clustering_estimator(config=None)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_clustering_estimator "Permanent link")
Build a skfolio hierarchical clustering estimator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_clustering_estimator--parameters "Permanent link")
config : ClusteringConfig or None Clustering configuration. Defaults to `ClusteringConfig()` (Ward linkage, auto max_clusters).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_clustering_estimator--returns "Permanent link")
HierarchicalClustering A fitted-ready skfolio clustering estimator.
####  `build_distance_estimator(config=None, *, covariance_estimator=None)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_distance_estimator "Permanent link")
Build a skfolio distance estimator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_distance_estimator--parameters "Permanent link")
config : DistanceConfig or None Distance configuration. Defaults to `DistanceConfig()` (Pearson distance). covariance_estimator : BaseCovariance or None Covariance estimator for `CovarianceDistance`. Ignored for other distance types.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_distance_estimator--returns "Permanent link")
BaseDistance A fitted-ready skfolio distance estimator.
####  `build_equal_weighted(config=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_equal_weighted "Permanent link")
Build a skfolio :class:`EqualWeighted` (1/N) optimiser.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_equal_weighted--parameters "Permanent link")
config : EqualWeightedConfig or None Configuration (currently has no parameters). **kwargs Additional keyword arguments forwarded to the :class:`EqualWeighted` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_equal_weighted--returns "Permanent link")
EqualWeighted A fitted-ready skfolio optimiser.
####  `build_herc(config=None, *, prior_estimator=None, distance_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_herc "Permanent link")
Build a skfolio HERC optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_herc--parameters "Permanent link")
config : HERCConfig or None HERC configuration. Defaults to `HERCConfig()` (variance). prior_estimator : BasePrior or None Prior estimator. distance_estimator : BaseDistance or None Distance estimator. When `None`, one is built from `config.distance_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`HierarchicalEqualRiskContribution` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_herc--returns "Permanent link")
HierarchicalEqualRiskContribution A fitted-ready skfolio optimiser.
####  `build_hrp(config=None, *, prior_estimator=None, distance_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_hrp "Permanent link")
Build a skfolio :class:`HierarchicalRiskParity` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_hrp--parameters "Permanent link")
config : HRPConfig or None HRP configuration. Defaults to `HRPConfig()` (variance). prior_estimator : BasePrior or None Prior estimator. distance_estimator : BaseDistance or None Distance estimator. When `None`, one is built from `config.distance_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`HierarchicalRiskParity` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_hrp--returns "Permanent link")
HierarchicalRiskParity A fitted-ready skfolio optimiser.
####  `build_inverse_volatility(config=None, *, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_inverse_volatility "Permanent link")
Build a skfolio :class:`InverseVolatility` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_inverse_volatility--parameters "Permanent link")
config : InverseVolatilityConfig or None Configuration. Defaults to `InverseVolatilityConfig()`. prior_estimator : BasePrior or None Prior estimator (covariance estimator determines volatility). When `None`, one is built from `config.prior_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`InverseVolatility` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_inverse_volatility--returns "Permanent link")
InverseVolatility A fitted-ready skfolio optimiser.
####  `build_max_diversification(config=None, *, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_max_diversification "Permanent link")
Build a skfolio :class:`MaximumDiversification` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_max_diversification--parameters "Permanent link")
config : MaxDiversificationConfig or None Configuration. Defaults to `MaxDiversificationConfig()`. prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.prior_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`MaximumDiversification` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_max_diversification--returns "Permanent link")
MaximumDiversification A fitted-ready skfolio optimiser.
####  `build_mean_risk(config=None, *, prior_estimator=None, factor_exposure_constraints=None, sector_mapping=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_mean_risk "Permanent link")
Build a skfolio :class:`MeanRisk` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_mean_risk--parameters "Permanent link")
config : MeanRiskConfig or None Mean-risk configuration. Defaults to `MeanRiskConfig()` (minimum-variance). prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.prior_config` (or skfolio default). factor_exposure_constraints : FactorExposureConstraints or None Enforceable factor exposure constraints produced by :func:`~optimizer.factors.build_factor_exposure_constraints`. When provided, `left_inequality` and `right_inequality` are injected into the :class:`MeanRisk` constructor. Any explicit `left_inequality` / `right_inequality` entries in `kwargs` take precedence. sector_mapping : dict[str, str] or None Ticker -> sector name mapping. Used to build `groups` and `linear_constraints` when `config.max_sector_weight` is set. Ignored when `config.max_sector_weight is None`. Any explicit `groups` or `linear_constraints` in `kwargs` take precedence. **kwargs Additional keyword arguments forwarded to the :class:`MeanRisk` constructor (for non-serialisable parameters such as `previous_weights`, `groups`, `linear_constraints`, etc.).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_mean_risk--returns "Permanent link")
MeanRisk A fitted-ready skfolio optimiser.
####  `build_nco(config=None, *, inner_estimator=None, outer_estimator=None, distance_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_nco "Permanent link")
Build a skfolio :class:`NestedClustersOptimization` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_nco--parameters "Permanent link")
config : NCOConfig or None NCO configuration. Defaults to `NCOConfig()`. inner_estimator : BaseOptimization or None Inner cluster optimiser. outer_estimator : BaseOptimization or None Outer (inter-cluster) optimiser. distance_estimator : BaseDistance or None Distance estimator. When `None`, one is built from `config.distance_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`NestedClustersOptimization` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_nco--returns "Permanent link")
NestedClustersOptimization A fitted-ready skfolio optimiser.
####  `build_risk_budgeting(config=None, *, risk_budget=None, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_risk_budgeting "Permanent link")
Build a skfolio :class:`RiskBudgeting` optimiser from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_risk_budgeting--parameters "Permanent link")
config : RiskBudgetingConfig or None Risk-budgeting configuration. Defaults to `RiskBudgetingConfig()` (variance risk parity). risk_budget : ndarray or None Per-asset risk budget. `None` gives equal budgets. prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.prior_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`RiskBudgeting` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_risk_budgeting--returns "Permanent link")
RiskBudgeting A fitted-ready skfolio optimiser.
####  `build_sector_constraints(sector_mapping, max_sector_weight)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_sector_constraints "Permanent link")
Build skfolio `groups` and `linear_constraints` from a sector mapping.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_sector_constraints--parameters "Permanent link")
sector_mapping : dict[str, str] Mapping from asset ticker to sector name (e.g. `{"AAPL": "Technology", "JPM": "Financials"}`). max_sector_weight : float Maximum total weight for any single sector (e.g. 0.25 = 25%).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_sector_constraints--returns "Permanent link")
groups : dict[str, str] Ticker -> sector label, as required by :class:`skfolio.optimization.MeanRisk` (converted to a 2-D group array at fit-time via `input_to_array`). linear_constraints : list[str] One constraint string per sector (`"SectorName <= cap"`).
####  `build_stacking(config=None, *, estimators=None, final_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_stacking "Permanent link")
Build a skfolio :class:`StackingOptimization` ensemble from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_stacking--parameters "Permanent link")
config : StackingConfig or None Stacking configuration. Defaults to `StackingConfig()`. estimators : list of (name, estimator) tuples or None Sub-optimisers whose outputs are combined. Required by skfolio but passed here (not in config) because estimator objects are not serialisable. final_estimator : BaseOptimization or None Meta-optimiser that allocates across sub-portfolios. **kwargs Additional keyword arguments forwarded to the :class:`StackingOptimization` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_stacking--returns "Permanent link")
StackingOptimization A fitted-ready skfolio ensemble optimiser.
####  `build_regime_blended_optimizer(config, hmm_result, **mean_risk_kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_regime_blended_optimizer "Permanent link")
Return a MeanRisk optimizer configured for the dominant regime.
Because skfolio's `MeanRisk` requires a single convex risk measure, this function selects the risk measure of the **dominant regime** — the state s* = argmax_s γ_T(s) — and builds a standard :class:`skfolio.optimization.MeanRisk` with that measure.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `RegimeRiskConfig[](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RegimeRiskConfig "RegimeRiskConfig


  
      dataclass
   \(optimizer.optimization._regime_risk.RegimeRiskConfig\)")`  |  Regime risk configuration.  |  _required_  |  
|  `hmm_result`  |  `HMMResult[](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMResult "HMMResult


  
      dataclass
   \(optimizer.moments._hmm.HMMResult\)")`  |  Fitted HMM providing current regime probabilities.  |  _required_  |  
|  `**mean_risk_kwargs`  |  `object`  |  Additional keyword arguments forwarded to :class:`skfolio.optimization.MeanRisk` (e.g. `min_weights`, `max_weights`, `prior_estimator`).  |  `{}`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `MeanRisk`  |  class:`skfolio.optimization.MeanRisk` instance ready for  |  
|  `MeanRisk`  |  `fit(X)` calls.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If `len(config.regime_measures) != hmm_result.n_states`.  |  
####  `build_regime_risk_budgeting(config, hmm_result, regime_budgets, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_regime_risk_budgeting "Permanent link")
Return a RiskBudgeting optimizer with a regime-blended budget vector.
Computes `b_t = Σ_s γ_T(s) · b_s` from the current HMM state probabilities and injects the result as `risk_budget` into :func:`build_risk_budgeting`.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `config`  |  `RiskBudgetingConfig[](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskBudgetingConfig "RiskBudgetingConfig


  
      dataclass
   \(optimizer.optimization._config.RiskBudgetingConfig\)")`  |  Risk-budgeting configuration (risk measure, constraints, …).  |  _required_  |  
|  `hmm_result`  |  `HMMResult[](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMResult "HMMResult


  
      dataclass
   \(optimizer.moments._hmm.HMMResult\)")`  |  Fitted HMM providing current filtered state probabilities.  |  _required_  |  
|  `regime_budgets`  |  `list[NDArray[float64]]`  |  One budget vector per HMM state, each shape `(n_assets,)`.  |  _required_  |  
|  `**kwargs`  |  `object`  |  Additional keyword arguments forwarded to :func:`build_risk_budgeting` (e.g. `prior_estimator`).  |  `{}`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `RiskBudgeting`  |  class:`skfolio.optimization.RiskBudgeting` instance ready for  |  
|  `RiskBudgeting`  |  `fit(X)` calls.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If `len(regime_budgets) != hmm_result.n_states`.  |  
####  `compute_blended_risk_measure(returns, weights, hmm_result, regime_measures, cvar_beta=0.95)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.compute_blended_risk_measure "Permanent link")
Compute ρ_t(w) = Σ_s γ_T(s) · ρ_s(w): probability-weighted blended risk.
Each regime's risk ρ_s(w) is computed on the historical portfolio returns from periods assigned to that regime (hard Viterbi-style assignment via argmax of filtered probabilities). Regimes with fewer than `_MIN_REGIME_SAMPLES` observations fall back to full-sample risk.
The blend weights γ_T(s) are the **last row** of `hmm_result.filtered_probs` — the most-recent filtered state probabilities, which sum to 1 by HMM construction.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `returns`  |  `DataFrame`  |  Dates × assets matrix of linear returns.  |  _required_  |  
|  `weights`  |  `NDArray[float64]`  |  1-D array of portfolio weights, shape `(n_assets,)`.  |  _required_  |  
|  `hmm_result`  |  `HMMResult[](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMResult "HMMResult


  
      dataclass
   \(optimizer.moments._hmm.HMMResult\)")`  |  Fitted HMM with `filtered_probs` aligned to _returns_.  |  _required_  |  
|  `regime_measures`  |  `Sequence[RiskMeasureType[](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.RiskMeasureType "RiskMeasureType \(optimizer.optimization._config.RiskMeasureType\)")]`  |  One :class:`RiskMeasureType` per HMM state.  |  _required_  |  
|  `cvar_beta`  |  `float`  |  CVaR confidence level (used when a regime uses CVaR).  |  `0.95`  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `float`  |  Scalar non-negative blended risk value.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If `len(regime_measures) != hmm_result.n_states`.  |  
|  `ValueError`  |  If _weights_ length does not match _returns_ columns.  |  
####  `compute_regime_budget(regime_budgets, filtered_probs_last)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.compute_regime_budget "Permanent link")
Compute b_t = Σ_s γ_T(s) · b_s: probability-weighted blended budget.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `regime_budgets`  |  `list[NDArray[float64]]`  |  One budget vector per HMM state, each shape `(n_assets,)`. Values must be non-negative.  |  _required_  |  
|  `filtered_probs_last`  |  `NDArray[float64]`  |  Current state probabilities γ_T, shape `(n_states,)`. Typically the last row of `HMMResult.filtered_probs`.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `NDArray[float64]`  |  Blended budget vector of shape `(n_assets,)`, normalised to sum  |  
|  `NDArray[float64]`  |  to 1.  |  
Raises:  
| Type  | Description  |  
| --- | --- |  
|  `ValueError`  |  If `len(regime_budgets) != len(filtered_probs_last)`.  |  
####  `bootstrap_covariance_uncertainty(returns, B=500, block_size=21, alpha=0.05, seed=None)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.bootstrap_covariance_uncertainty "Permanent link")
Estimate covariance uncertainty via stationary block bootstrap.
Draws _B_ bootstrap resamples from _returns_ using a stationary block bootstrap (preserving autocorrelation structure), estimates the sample covariance for each resample, and reports the Frobenius-norm confidence radius as the `(1-alpha)` quantile of `‖Σ_b - Σ̂‖_F`.
The Frobenius-norm confidence set is::

```
{ Σ : ‖Σ - Σ̂‖_F ≤ δ }

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.bootstrap_covariance_uncertainty--parameters "Permanent link")
returns : pd.DataFrame, shape (T, n_assets) Linear asset returns (rows = observations, columns = assets). B : int, default=500 Number of bootstrap resamples. block_size : int, default=21 Expected block length for the stationary bootstrap (≈ 1 trading month). Larger values preserve more autocorrelation at the cost of bootstrap variance. alpha : float, default=0.05 Significance level; `delta` is the `(1-alpha)` quantile of Frobenius distances. seed : int or None, default=None Random seed for reproducibility.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.bootstrap_covariance_uncertainty--returns "Permanent link")
CovarianceUncertaintyResult Dataclass with `cov_hat`, `delta`, and `cov_samples`.
####  `build_robust_mean_risk(config=None, *, prior_estimator=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_robust_mean_risk "Permanent link")
Build a robust :class:`MeanRisk` optimiser with ellipsoidal uncertainty sets.
Injects skfolio's `mu_uncertainty_set_estimator` into a standard `MeanRisk` to hedge against estimation error in the expected return vector μ. Optionally adds covariance uncertainty via stationary block bootstrap (`cov_uncertainty_method="bootstrap"`, default) or the analytic formula (`cov_uncertainty_method="empirical"`).
Kappa-confidence_level mapping ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ At fit time, `n_assets` is known and the conversion is::

```
confidence_level = F_{χ²_{n_assets}}(κ²)

```

This ensures the ellipsoid half-width equals κ regardless of n_assets.
Special case `kappa=0` ~~~~~~~~~~~~~~~~~~~~~~~~ When `kappa=0`, no uncertainty set is injected, so the optimiser is identical to the output of :func:`build_mean_risk` with the same `mean_risk_config`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_robust_mean_risk--parameters "Permanent link")
config : RobustConfig or None Robust configuration. Defaults to `RobustConfig()` (κ=1.0, min-variance objective, no covariance uncertainty). prior_estimator : BasePrior or None Prior estimator. When `None`, one is built from `config.mean_risk_config.prior_config` (or skfolio default). **kwargs Additional keyword arguments forwarded to the :class:`MeanRisk` constructor (e.g. `previous_weights`, `groups`, `linear_constraints`).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/optimization/#optimizer.optimization.build_robust_mean_risk--returns "Permanent link")
MeanRisk A fitted-ready skfolio optimiser with ellipsoidal uncertainty sets.
