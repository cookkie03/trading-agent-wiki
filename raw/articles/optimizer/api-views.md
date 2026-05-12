<!-- source: https://silviobaratto.github.io/optimizer/api/views/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/views/#views)
# views[¶](https://silviobaratto.github.io/optimizer/api/views/#views "Permanent link")
###  `optimizer.views` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views "Permanent link")
View integration frameworks (Black-Litterman, Entropy Pooling, Opinion Pooling).
####  `BlackLittermanConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.BlackLittermanConfig "Permanent link")
Immutable configuration for the Black-Litterman prior.
All parameters map 1:1 to :class:`skfolio.prior.BlackLitterman` constructor arguments, keeping the config serialisable and suitable for hyperparameter sweeps.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.BlackLittermanConfig--parameters "Permanent link")
views : tuple[str, ...] View expressions (absolute or relative). tau : float Uncertainty scaling parameter. risk_free_rate : float Risk-free rate added to posterior expected returns. uncertainty_method : ViewUncertaintyMethod How to calibrate view uncertainty (omega matrix). view_confidences : tuple[float, ...] or None Per-view confidence levels in [0, 1] for the Idzorek method. groups : dict[str, list[str]] or None Asset group mapping for group-relative views. prior_config : MomentEstimationConfig or None Inner prior configuration. Defaults to `MomentEstimationConfig.for_equilibrium_ledoitwolf()`. use_factor_model : bool If `True`, wrap the Black-Litterman prior in a :class:`skfolio.prior.FactorModel`. residual_variance : bool Whether to include residual variance in `FactorModel`.
#####  `for_equilibrium(views)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.BlackLittermanConfig.for_equilibrium "Permanent link")
Standard BL with EquilibriumMu prior, tau=0.05.
#####  `for_factor_model(views)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.BlackLittermanConfig.for_factor_model "Permanent link")
BL Factor Model variant.
#####  `for_idzorek(views, view_confidences)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.BlackLittermanConfig.for_idzorek "Permanent link")
Idzorek method with per-view confidence levels.
####  `EntropyPoolingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.EntropyPoolingConfig "Permanent link")
Immutable configuration for the Entropy Pooling prior.
All parameters map 1:1 to :class:`skfolio.prior.EntropyPooling` constructor arguments.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.EntropyPoolingConfig--parameters "Permanent link")
mean_views : tuple[str, ...] or None Mean view expressions. variance_views : tuple[str, ...] or None Variance view expressions. correlation_views : tuple[str, ...] or None Correlation view expressions. skew_views : tuple[str, ...] or None Skewness view expressions. kurtosis_views : tuple[str, ...] or None Kurtosis view expressions. cvar_views : tuple[str, ...] or None CVaR view expressions. cvar_beta : float Confidence level for CVaR views. groups : dict[str, list[str]] or None Asset group mapping for group-relative views. solver : str Scipy solver for the dual optimisation. solver_params : dict[str, object] or None Additional solver parameters. prior_config : MomentEstimationConfig or None Inner prior configuration. Defaults to `EmpiricalPrior()`.
#####  `for_mean_views(mean_views)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.EntropyPoolingConfig.for_mean_views "Permanent link")
Mean-only Entropy Pooling.
#####  `for_stress_test(variance_views, correlation_views)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.EntropyPoolingConfig.for_stress_test "Permanent link")
Stress-test Entropy Pooling with variance + correlation views.
#####  `for_group_views(mean_views, groups)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.EntropyPoolingConfig.for_group_views "Permanent link")
Entropy Pooling with group-relative mean views.
####  `OpinionPoolingConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.OpinionPoolingConfig "Permanent link")
Immutable configuration for the Opinion Pooling prior.
The `estimators` argument is passed directly to the factory function (not stored here) because estimator objects are not serialisable in a frozen dataclass.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.OpinionPoolingConfig--parameters "Permanent link")
opinion_probabilities : tuple[float, ...] or None Per-expert weight. is_linear_pooling : bool `True` for arithmetic (linear) pooling, `False` for geometric (logarithmic) pooling. divergence_penalty : float KL-divergence penalty for robust pooling. n_jobs : int or None Number of parallel jobs for expert fitting. prior_config : MomentEstimationConfig or None Common prior configuration.
####  `ViewUncertaintyMethod` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.ViewUncertaintyMethod "Permanent link")
Bases: `str`, `Enum`
View uncertainty calibration method for Black-Litterman.
Maps to the `view_confidences` parameter in :class:`skfolio.prior.BlackLitterman`.
####  `build_black_litterman(config, view_history=None, return_history=None, omega=None)` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_black_litterman "Permanent link")
Build a skfolio Black-Litterman prior from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_black_litterman--parameters "Permanent link")
config : BlackLittermanConfig Black-Litterman configuration. view_history : pd.DataFrame or None Historical forecasted Q values (dates × views). Required when `config.uncertainty_method` is `EMPIRICAL_TRACK_RECORD` and `omega` is not pre-supplied. return_history : pd.DataFrame or None Realised returns aligned to each view (dates × views). Required together with `view_history` for empirical omega calibration. omega : ndarray of shape (n_views, n_views) or None Pre-computed diagonal omega matrix. When provided and method is `EMPIRICAL_TRACK_RECORD`, used directly (skipping the history computation).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_black_litterman--returns "Permanent link")
BasePrior A fitted-ready :class:`skfolio.prior.BlackLitterman` (or :class:`_EmpiricalOmegaBlackLitterman` for the empirical method), optionally wrapped in a :class:`skfolio.prior.FactorModel`.
####  `build_entropy_pooling(config, prior_moments=None, asset_names=None)` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_entropy_pooling "Permanent link")
Build a skfolio Entropy Pooling prior from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_entropy_pooling--parameters "Permanent link")
config : EntropyPoolingConfig Entropy Pooling configuration. prior_moments : tuple[ndarray, ndarray] or None `(mu, cov)` arrays from a fitted prior. Required when `config.relative_mean_views` or `config.relative_variance_views` are set. asset_names : list[str] or None Asset names corresponding to rows/columns of _prior_moments_. Required together with _prior_moments_.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_entropy_pooling--returns "Permanent link")
EntropyPooling A fitted-ready :class:`skfolio.prior.EntropyPooling`.
####  `build_opinion_pooling(estimators, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_opinion_pooling "Permanent link")
Build a skfolio Opinion Pooling prior from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_opinion_pooling--parameters "Permanent link")
estimators : list[tuple[str, BasePrior]] Named expert prior estimators. Passed directly because estimator objects are not serialisable in a frozen dataclass. config : OpinionPoolingConfig or None Opinion Pooling configuration. Defaults to `OpinionPoolingConfig()`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.build_opinion_pooling--returns "Permanent link")
OpinionPooling A fitted-ready :class:`skfolio.prior.OpinionPooling`.
####  `calibrate_omega_from_track_record(view_history, return_history)` [¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.calibrate_omega_from_track_record "Permanent link")
Calibrate the Black-Litterman omega matrix from a forecast error track record.
Implements the empirical method described in the theory:

```
Ω_{kk} = Var(Q_{k,t} − r_{k,t})

```

where `Q_{k,t}` is the analyst's forecast for view `k` at time `t` and `r_{k,t}` is the realised return for that view. The diagonal entries are non-negative by construction (they are sample variances).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.calibrate_omega_from_track_record--parameters "Permanent link")
view_history : pd.DataFrame, shape (n_dates, n_views) Historical forecasted Q values, one column per view. return_history : pd.DataFrame, shape (n_dates, n_views) Realised returns aligned to each view, same shape as `view_history`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.calibrate_omega_from_track_record--returns "Permanent link")
ndarray, shape (n_views, n_views) Diagonal Ω matrix where `Ω_{kk} = Var(Q_k − r_k)`.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/views/#optimizer.views.calibrate_omega_from_track_record--raises "Permanent link")
ValueError If the two DataFrames have different shapes or column sets, or if fewer than 5 aligned observations are available per view.
