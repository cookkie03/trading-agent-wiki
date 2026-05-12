<!-- source: https://silviobaratto.github.io/optimizer/api/factors/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/factors/#factors)
# factors[¶](https://silviobaratto.github.io/optimizer/api/factors/#factors "Permanent link")
###  `optimizer.factors` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors "Permanent link")
Factor construction, scoring, and selection for stock pre-selection.
####  `CompositeMethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeMethod "Permanent link")
Bases: `str`, `Enum`
Composite scoring method.
####  `CompositeScoringConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig "Permanent link")
Configuration for composite score construction.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig--parameters "Permanent link")
method : CompositeMethod Equal-weight, IC-weighted, ICIR-weighted, ridge, or GBT composite. ic_lookback : int Number of periods for IC estimation when using IC weighting. core_weight : float Relative weight for core factor groups. supplementary_weight : float Relative weight for supplementary factor groups. ridge_alpha : float L2 regularisation strength for `RIDGE_WEIGHTED`. Passed as the single candidate to `RidgeCV`; increase for more shrinkage. gbt_max_depth : int Maximum tree depth for `GBT_WEIGHTED`. gbt_n_estimators : int Number of boosting rounds for `GBT_WEIGHTED`. gbt_random_state : int Random state for `GBT_WEIGHTED` `GradientBoostingRegressor`. Change for sensitivity analysis or ensemble diversity. min_coverage_groups : int Minimum number of non-NaN group scores required. Tickers with fewer available groups receive NaN composite and are excluded from selection. 0 disables the threshold (default). return_coverage : bool When True, `compute_composite_score` returns a DataFrame with columns `["composite", "coverage_ratio"]` instead of a Series. ic_fallback_strategy : ICFallbackStrategy Strategy when all IC/ICIR weights resolve to zero (all groups have non-positive IC or ICIR). `EQUAL_WEIGHT` preserves the current behavior. `NAN` returns all-NaN scores to suppress trading. `RAISE` raises `ConfigurationError`. Default is `EQUAL_WEIGHT`.
#####  `for_equal_weight()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_equal_weight "Permanent link")
Equal-weight composite scoring.
#####  `for_ic_weighted()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_ic_weighted "Permanent link")
IC-weighted composite scoring (raw IC magnitude).
#####  `for_icir_weighted()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_icir_weighted "Permanent link")
ICIR-weighted composite scoring (mean IC / std IC).
Penalises inconsistent predictors by dividing mean IC by IC volatility before normalising weights.
#####  `for_ridge_weighted()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_ridge_weighted "Permanent link")
Ridge regression composite scoring.
Learns optimal linear factor weights from historical data with L2 regularisation, avoiding the need for IC proxies.
#####  `for_gbt_weighted()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_gbt_weighted "Permanent link")
Gradient-boosted tree composite scoring.
Captures non-linear factor interactions (e.g. high value + improving momentum = stronger combined signal).
#####  `for_ic_weighted_robust()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_ic_weighted_robust "Permanent link")
IC-weighted scoring with minimum coverage of 3 groups.
#####  `for_sparse_universe()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_sparse_universe "Permanent link")
Equal-weight scoring with minimum coverage of 2 groups.
#####  `for_coverage_diagnostics()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_coverage_diagnostics "Permanent link")
Equal-weight scoring returning coverage_ratio alongside composite.
#####  `for_ic_weighted_raise_on_fallback()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeScoringConfig.for_ic_weighted_raise_on_fallback "Permanent link")
IC-weighted scoring that raises if all groups have negative IC.
####  `FactorBuildHealth` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorBuildHealth "Permanent link")
Diagnostic report from build_factor_scores_history().
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorBuildHealth--parameters "Permanent link")
total_dates : int Number of rebalancing dates attempted. succeeded_dates : int Number of dates for which factor computation succeeded. failed_dates : int Number of dates skipped due to errors. failures : dict[str, str] Mapping of ISO-date string to exception message for each failure. min_success_fraction : float Minimum fraction of succeeded/total required before FactorCoverageError is raised.
#####  `success_fraction` `property` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorBuildHealth.success_fraction "Permanent link")
Fraction of dates that succeeded (1.0 if total_dates == 0).
#####  `is_healthy` `property` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorBuildHealth.is_healthy "Permanent link")
True when success_fraction >= min_success_fraction.
####  `FactorConstructionConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorConstructionConfig "Permanent link")
Configuration for factor computation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorConstructionConfig--parameters "Permanent link")
factors : tuple[FactorType, ...] Which factors to compute. momentum_lookback : int Lookback window for momentum in trading days. momentum_skip : int Recent days to skip for momentum (reversal avoidance). volatility_lookback : int Lookback window for volatility in trading days. beta_lookback : int Lookback window for beta estimation in trading days. amihud_lookback : int Lookback window for Amihud illiquidity in trading days. publication_lag : PublicationLagConfig Per-source publication lags for point-in-time correctness. Pass a plain `int` for a uniform lag across all sources (backward-compatible; converted to :class:`PublicationLagConfig` automatically).
#####  `for_core_factors()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorConstructionConfig.for_core_factors "Permanent link")
Core factors with strongest empirical support.
#####  `for_all_factors()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorConstructionConfig.for_all_factors "Permanent link")
All 17 factors.
####  `FactorGroupType` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorGroupType "Permanent link")
Bases: `str`, `Enum`
Factor group taxonomy.
####  `FactorIntegrationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorIntegrationConfig "Permanent link")
Configuration for bridging factor scores to optimization.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorIntegrationConfig--parameters "Permanent link")
risk_free_rate : float Annual risk-free rate for expected return mapping. market_risk_premium : float Annual equity risk premium. score_premium : float Annualized premium per unit of composite z-score. use_black_litterman : bool Whether to generate Black-Litterman views from factor scores. view_confidence_cap : float Maximum Idzorek confidence for BL views (0–1). At 1.0 the posterior equals the view exactly, causing extreme concentration. Values 0.25–0.50 blend the view with the equilibrium prior. max_weight : float Maximum per-asset weight enforced on the optimizer when the integration injects a BL prior. 0.0 disables the constraint. exposure_lower_bound : float Lower bound for factor exposure constraints. exposure_upper_bound : float Upper bound for factor exposure constraints.
#####  `for_linear_mapping()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorIntegrationConfig.for_linear_mapping "Permanent link")
Direct factor score to expected return mapping.
#####  `for_black_litterman()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorIntegrationConfig.for_black_litterman "Permanent link")
Factor-based Black-Litterman views.
####  `FactorType` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorType "Permanent link")
Bases: `str`, `Enum`
Individual factor identifiers.
####  `FactorValidationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorValidationConfig "Permanent link")
Configuration for factor validation and statistical testing.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorValidationConfig--parameters "Permanent link")
newey_west_lags : int Number of lags for Newey-West t-statistic. t_stat_threshold : float Minimum absolute t-statistic for significance. fdr_alpha : float False discovery rate alpha level. n_quantiles : int Number of quantiles for spread analysis. fmp_top_pct : float Top percentile for factor-mimicking portfolios. fmp_bottom_pct : float Bottom percentile for factor-mimicking portfolios. composite_min_observations : int Minimum non-NaN observations per cross-section for composite IC. Default: 24. Newey-West with 6 lags requires at least 13 observations (2*lags+1); 24 provides two years of monthly IC for reliable Spearman rank correlations. min_ic_observations : int Minimum non-NaN observations per cross-section date for per-factor IC computation in `run_factor_validation`. Default: 24, matching `composite_min_observations` so both paths apply consistent minimum-data guards.
#####  `for_strict()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorValidationConfig.for_strict "Permanent link")
Strict validation thresholds.
#####  `for_standard()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorValidationConfig.for_standard "Permanent link")
Standard validation thresholds.
####  `GroupICAggregationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig "Permanent link")
Configuration for group-level IC aggregation.
Controls how per-factor ICs are combined within each factor group.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig--parameters "Permanent link")
weighting : ICWeightingMethod Method for weighting per-factor ICs within a group. negative_filter : ICNegativeFilterPolicy Policy for handling factors with consistently negative IC. min_observations_tstat : int Minimum IC observations to compute a valid t-stat. Factors below this threshold fall back to equal weight when `weighting=TSTAT_WEIGHTED`. Default: 24. newey_west_lags : int Number of lags for Newey-West HAC standard errors when computing t-stat weights.
#####  `for_simple_mean()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig.for_simple_mean "Permanent link")
Default: simple arithmetic mean, no filtering.
#####  `for_tstat_weighted()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig.for_tstat_weighted "Permanent link")
Weight factor ICs by absolute Newey-West t-stat.
#####  `for_excluding_negative()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig.for_excluding_negative "Permanent link")
Exclude factors with consistently negative IC.
#####  `for_robust()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICAggregationConfig.for_robust "Permanent link")
T-stat weighted with negative IC exclusion.
####  `GroupWeight` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupWeight "Permanent link")
Bases: `str`, `Enum`
Weight tier for factor groups.
####  `ICFallbackStrategy` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICFallbackStrategy "Permanent link")
Bases: `str`, `Enum`
Strategy when all IC/ICIR weights are zero or negative.
Applied by IC-weighted and ICIR-weighted composite scoring when every factor group has non-positive IC or ICIR and the total weight sums to zero.
####  `ICNegativeFilterPolicy` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICNegativeFilterPolicy "Permanent link")
Bases: `str`, `Enum`
Policy for handling factors with consistently negative IC.
INCLUDE keeps all factors regardless of IC sign (current default). EXCLUDE removes negative-IC factors before computing the group average (denominator shrinks). SOFT zeros the contribution of negative-IC factors but keeps them in the denominator (dampening).
####  `ICWeightingMethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICWeightingMethod "Permanent link")
Bases: `str`, `Enum`
Method for aggregating per-factor ICs within a group.
SIMPLE_MEAN averages ICs equally (current default behaviour). TSTAT_WEIGHTED uses absolute Newey-West t-stat as weight so that factors with more statistically significant ICs dominate the group average.
####  `MacroRegime` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.MacroRegime "Permanent link")
Bases: `str`, `Enum`
Macro-economic regime classification.
####  `PublicationLagConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.PublicationLagConfig "Permanent link")
Differentiated publication lags by data source type.
Each source has an independent delay between the period end date and the date the data is reliably available for use in factor construction. Using source-specific lags avoids look-ahead bias when aligning fundamental data to price dates.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.PublicationLagConfig--parameters "Permanent link")
annual_days : int Lag for annual financial statements (days after fiscal year end). Default: 90 days (~3 months for 10-K filing). quarterly_days : int Lag for quarterly financial statements (days after quarter end). Default: 45 days (~6 weeks for 10-Q filing). analyst_days : int Lag for analyst estimates and recommendations. Default: 5 days (short dissemination buffer). macro_days : int Lag for macroeconomic indicators (release lag + revision lag). Default: 63 days (~2 months).
#####  `uniform(days)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.PublicationLagConfig.uniform "Permanent link")
Create a config with the same lag applied to all sources.
####  `RegimeThresholdConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeThresholdConfig "Permanent link")
Classification thresholds for the composite macro regime scorer.
All eight thresholds drive the {-1, 0, +1} component scores used by :func:`~optimizer.factors._regime.classify_regime_composite` and the research-layer scoring functions in `research/_macro.py`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeThresholdConfig--parameters "Permanent link")
hy_oas_risk_on : float HY OAS level (bps) below which credit conditions are benign (+1). Empirical basis: ~40th pctl of ICE BofA HY OAS 1997-2023. hy_oas_risk_off : float HY OAS level (bps) above which credit stress is elevated (-1). Empirical basis: ~75th pctl of ICE BofA HY OAS historically. pmi_expansion : float ISM Manufacturing PMI above which growth is accelerating (+1). 2-point buffer above the 50 neutral line (Koenig 2002). pmi_contraction : float ISM Manufacturing PMI below which growth is contracting (-1). Symmetric 2-point band around 50. spread_2s10s_steep : float 10Y-2Y spread (percentage points) above which the curve is steep (+1). 100 bps historically associated with early-cycle acceleration. spread_2s10s_inversion : float 10Y-2Y spread (percentage points) at/below which the curve is inverted (-1). Conventional inversion definition (Estrella & Mishkin 1998). sentiment_positive : float Normalized NLP sentiment score above which sentiment is positive (+1). sentiment_negative : float Normalized NLP sentiment score below which sentiment is negative (-1).
#####  `for_empirical()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeThresholdConfig.for_empirical "Permanent link")
Canonical empirical thresholds (Chapter 7 calibration).
#####  `for_rolling_percentile(hy_series=None, spread_series=None, pmi_series=None, sentiment_series=None, hy_risk_on_pct=0.4, hy_risk_off_pct=0.75, pmi_expansion_pct=0.6, pmi_contraction_pct=0.4, spread_steep_pct=0.65, sentiment_positive_pct=0.7)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeThresholdConfig.for_rolling_percentile "Permanent link")
Compute thresholds from trailing empirical distributions.
Pass historical Series for each indicator; thresholds are set at the specified percentiles. Any `None` series falls back to the hard-coded empirical default for that indicator.
####  `RegimeTiltConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeTiltConfig "Permanent link")
Configuration for macro regime factor tilts.
Per-regime multiplicative tilts stored as tuples of `(group_name, tilt_factor)` for frozen-dataclass compatibility.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeTiltConfig--parameters "Permanent link")
enable : bool Whether to apply regime tilts. expansion_tilts : tuple[tuple[str, float], ...] Group tilts during expansion. slowdown_tilts : tuple[tuple[str, float], ...] Group tilts during slowdown. recession_tilts : tuple[tuple[str, float], ...] Group tilts during recession. recovery_tilts : tuple[tuple[str, float], ...] Group tilts during recovery. unknown_tilts : tuple[tuple[str, float], ...] Group tilts when regime is unknown (neutral — all multipliers default to 1.0 via empty tuple). max_tilt_multiplier : float Upper bound on any single raw tilt multiplier (default 2.0). Multipliers exceeding this value are clamped before application. Must be >= 1.0. min_post_tilt_weight : float Minimum weight any group may hold after tilting, expressed as a fraction of the original total weight (default 0.05). Groups suppressed below this floor are raised to it before renormalization. Must be in [0.0, 1.0).
#####  `for_moderate_tilts()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeTiltConfig.for_moderate_tilts "Permanent link")
Enable moderate regime-conditional tilts.
#####  `for_no_tilts()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeTiltConfig.for_no_tilts "Permanent link")
Disable regime tilts (default).
#####  `for_strict_bounds()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.RegimeTiltConfig.for_strict_bounds "Permanent link")
Enable tilts with tight multiplier cap and weight floor.
Caps each raw tilt multiplier at 1.5x and prevents any group from falling below 10% of the total weight. Suitable for mandates requiring diversification guarantees.
####  `SelectionConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig "Permanent link")
Configuration for stock selection from scored universe.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig--parameters "Permanent link")
method : SelectionMethod Fixed-count or quantile-based selection. target_count : int Number of stocks to select (for FIXED_COUNT). target_quantile : float Quantile threshold for selection (for QUANTILE, 0-1). exit_quantile : float Exit quantile for hysteresis (for QUANTILE). buffer_fraction : float Buffer zone fraction around selection boundary. sector_balance : bool Whether to enforce sector-proportional representation. sector_tolerance : float Maximum deviation from parent universe sector weights (fraction, 0–1). Default 0.05 (5 pp) matches MSCI, S&P DJI, and FTSE Russell factor-index methodology. Use `for_low_tracking_error()` for a tighter 3% band suited to institutional low-active-risk mandates.
#####  `for_top_100()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig.for_top_100 "Permanent link")
Select top 100 stocks by composite score.
#####  `for_top_quintile()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig.for_top_quintile "Permanent link")
Select top quintile by composite score.
#####  `for_top_20()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig.for_top_20 "Permanent link")
Select top 20 stocks — concentrated diversified portfolio.
Uses relaxed sector tolerance (10%) because at 20 stocks each addition/removal changes sector weight by ~5%. Buffer of 3 stocks (15%) reduces unnecessary turnover.
#####  `for_concentrated()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig.for_concentrated "Permanent link")
Concentrated portfolio of top 30 stocks.
#####  `for_low_tracking_error()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionConfig.for_low_tracking_error "Permanent link")
Top 100 stocks with tighter sector tolerance for low tracking error.
Uses a 3% sector deviation cap (vs. the standard 5%) to more closely replicate the sector composition of the parent benchmark, matching the tighter band used by institutional index providers (e.g., MSCI Minimum Volatility) when minimising active sector bets is a mandate.
####  `SelectionMethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.SelectionMethod "Permanent link")
Bases: `str`, `Enum`
Stock selection method.
####  `StandardizationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig "Permanent link")
Configuration for cross-sectional factor standardization.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig--parameters "Permanent link")
method : StandardizationMethod Z-score or rank-normal standardization. Default is `RANK_NORMAL` following MSCI Barra USE4 and Gu/Kelly/Xiu (2020) best practice for heavy-tailed financial factor distributions. winsorize_method : WinsorizeMethod Outlier treatment method. `PERCENTILE` clips at fixed quantiles; `MAD` clips at median +/- k * 1.4826 * MAD. winsorize_lower : float Lower percentile for winsorization (0-1, used with PERCENTILE). winsorize_upper : float Upper percentile for winsorization (0-1, used with PERCENTILE). neutralize_sector : bool Whether to sector-neutralize scores. neutralize_country : bool Whether to country-neutralize scores. factor_method_overrides : tuple[tuple[str, str], ...] Per-factor standardization method overrides as `(factor_name, method_value)` pairs. When non-empty, each factor is standardized with its assigned method; factors not in the map fall back to `method`.
#####  `for_heavy_tailed()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig.for_heavy_tailed "Permanent link")
Rank-normal for heavy-tailed distributions (e.g. value ratios).
#####  `for_normal()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig.for_normal "Permanent link")
Z-score for approximately normal factors (e.g. momentum).
#####  `for_z_score()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig.for_z_score "Permanent link")
Z-score standardization (backward-compatibility alias).
#####  `for_per_factor()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig.for_per_factor "Permanent link")
Per-factor method: RANK_NORMAL for heavy-tailed, Z_SCORE for normal.
Based on MSCI Barra USE4 and Gu/Kelly/Xiu (2020) classification. Heavy-tailed: value ratios, illiquidity, dividend yield, accruals, asset growth. Approximately normal: momentum, volatility, beta.
#####  `for_mad_winsorize()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationConfig.for_mad_winsorize "Permanent link")
MAD-based winsorization (MSCI Barra +/-3 MAD convention).
####  `StandardizationMethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.StandardizationMethod "Permanent link")
Bases: `str`, `Enum`
Cross-sectional standardization method.
####  `WinsorizeMethod` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.WinsorizeMethod "Permanent link")
Bases: `str`, `Enum`
Winsorization method for outlier treatment.
####  `FactorPCAResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorPCAResult "Permanent link")
Principal component analysis result for a factor score matrix.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorPCAResult--attributes "Permanent link")
explained_variance_ratio : ndarray, shape (n_components,) Fraction of variance explained by each principal component, sorted in descending order. loadings : pd.DataFrame, shape (n_factors, n_components) PCA loading matrix. Rows are factor names; columns are `PC1`, `PC2`, ... . Each column is a unit eigenvector of the correlation matrix of the factor scores. n_components_95pct : int Smallest number of components whose cumulative explained variance ratio is ≥ 0.95.
####  `FactorExposureConstraints` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorExposureConstraints "Permanent link")
Enforceable linear constraints on portfolio factor exposure.
Encodes the set of per-factor inequalities::

```
lb_g <= sum_i w_i * z_{i,g} <= ub_g

```

as a pair of matrices ready to be passed directly to :class:`skfolio.optimization.MeanRisk` (or any optimizer that accepts `left_inequality` / `right_inequality`).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorExposureConstraints--parameters "Permanent link")
left_inequality : np.ndarray of shape (2 * n_factors, n_assets) Inequality matrix `A` in the constraint `A @ w <= b`. Two rows per factor: `-z` (lower bound) and `+z` (upper bound). right_inequality : np.ndarray of shape (2 * n_factors,) Bound vector `b` in the constraint `A @ w <= b`. factor_names : list[str] Names of the constrained factors (in the same order as the row pairs in `left_inequality`). lower_bounds : np.ndarray of shape (n_factors,) Lower exposure bound per factor. upper_bounds : np.ndarray of shape (n_factors,) Upper exposure bound per factor.
####  `NetAlphaResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.NetAlphaResult "Permanent link")
Result of net alpha calculation after transaction cost deduction.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.NetAlphaResult--attributes "Permanent link")
gross_alpha : float Annualised IC-based alpha proxy: `mean(IC) * sqrt(annualisation)`. avg_turnover : float Mean one-way turnover across consecutive rebalancing dates, computed via :func:`~optimizer.rebalancing._rebalancer.compute_turnover`. total_cost : float Cost deduction: `avg_turnover * cost_bps / 10_000`. net_alpha : float Net annualised alpha after cost deduction: `gross_alpha - total_cost`. net_icir : float Net information coefficient information ratio: `net_alpha / (std(IC) * sqrt(annualisation))`. `0.0` when the IC series has zero variance.
####  `QuintileSpreadResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.QuintileSpreadResult "Permanent link")
Quintile spread analysis result for a single factor.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.QuintileSpreadResult--attributes "Permanent link")
quintile_returns : pd.DataFrame Dates × Q1..Qn equal-weight portfolio returns per quantile bucket. Q1 = bottom (lowest scores), Qn = top (highest scores). spread_returns : pd.Series Qn − Q1 long-short spread return series indexed by date. Equals `quintile_returns.iloc[:, -1] - quintile_returns.iloc[:, 0]` element-wise. annualised_mean : float `spread_returns.mean() * 252`. t_stat : float Two-tailed t-statistic: `mean / (std / sqrt(T))`. sharpe : float Annualised Sharpe ratio: `mean * sqrt(252) / std`.
####  `FactorOOSConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorOOSConfig "Permanent link")
Configuration for rolling block OOS validation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorOOSConfig--parameters "Permanent link")
train_periods : int Length of the training window in index periods. Default: 36. val_periods : int Length of the validation window in index periods. Default: 12. step_periods : int Number of index periods to roll forward between folds. Default: 6.
####  `FactorOOSResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorOOSResult "Permanent link")
Results from rolling block OOS factor validation.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorOOSResult--attributes "Permanent link")
per_fold_ic : pd.DataFrame `n_folds × factors` matrix of mean IC per fold per factor. per_fold_spread : pd.DataFrame `n_folds × factors` matrix of mean quintile spread per fold. mean_oos_ic : pd.Series Mean OOS IC aggregated across folds (one value per factor). mean_oos_icir : pd.Series OOS ICIR (mean IC / std IC across folds) per factor. n_folds : int Number of folds generated.
####  `CompositeICResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeICResult "Permanent link")
IC analysis results for the composite score signal.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CompositeICResult--attributes "Permanent link")
mean_ic : float Mean IC of the composite score over the evaluation period. ic_std : float Standard deviation of the IC series. t_stat : float Newey-West adjusted t-statistic. p_value : float Two-tailed p-value from the Newey-West t-statistic. icir : float IC Information Ratio: `mean(IC) / std(IC)`. significant : bool True when `abs(t_stat) >= t_stat_threshold`. best_individual_ic : float Highest mean IC among individual factors. `NaN` when no individual factors were validated alongside. outperforms_best_individual : bool True when `mean_ic > best_individual_ic`.
####  `CorrectedPValues` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CorrectedPValues "Permanent link")
Multiple-testing corrected p-values.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.CorrectedPValues--attributes "Permanent link")
holm : ndarray Holm-Bonferroni adjusted p-values (controls FWER). bh : ndarray Benjamini-Hochberg adjusted p-values (controls FDR).
####  `FactorValidationReport` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.FactorValidationReport "Permanent link")
Complete validation report for all factors.
####  `GroupICResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICResult "Permanent link")
Result of group-level IC aggregation with per-factor breakdown.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.GroupICResult--attributes "Permanent link")
group_ic : pd.DataFrame (dates x groups) group-level IC history. Identical in shape to the legacy `build_group_ic_history` return value. factor_ic : pd.DataFrame (dates x factors) per-factor IC time series. excluded_factors : dict[str, list[str]] Group name → list of factor names excluded by the negative-IC filter policy. Empty when `ICNegativeFilterPolicy.INCLUDE`.
####  `ICResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICResult "Permanent link")
Information coefficient analysis results for a single factor.
####  `ICStats` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICStats "Permanent link")
Full IC statistics for a single factor including Newey-West inference.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.ICStats--attributes "Permanent link")
mean : float Mean IC over the evaluation period. variance_nw : float Newey-West HAC variance of the IC series. t_stat_nw : float Newey-West adjusted t-statistic: `IC_mean / sqrt(Var_NW / T)`. p_value : float Two-tailed p-value derived from the Newey-West t-statistic. icir : float Information Coefficient Information Ratio: `mean(IC) / std(IC)`.
####  `QuantileSpreadResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.QuantileSpreadResult "Permanent link")
Quantile spread analysis results for a single factor.
####  `compute_gross_alpha(net_alpha, avg_turnover, cost_bps=10.0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_gross_alpha "Permanent link")
Compute gross alpha by adding back estimated transaction costs.
Formula::

```
gross = net_alpha + avg_turnover * cost_bps / 10_000

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_gross_alpha--parameters "Permanent link")
net_alpha : float Net alpha after transaction costs (annualised). avg_turnover : float Average one-way turnover (e.g. 0.5 means 50% of portfolio traded per period). cost_bps : float One-way transaction cost in basis points.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_gross_alpha--returns "Permanent link")
float Gross alpha before transaction costs.
####  `factor_scores_to_expected_returns(scores, betas, factor_premiums, risk_free_rate=0.0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.factor_scores_to_expected_returns "Permanent link")
Convert factor Z-scores to expected returns via linear model.
Implements the formula::

```
E[r_i] = r_f + λ_mkt · β_i + Σ_g λ_g · z_{i,g}

```

where `λ_mkt` is read from `factor_premiums["market"]` and each `λ_g` is read from `factor_premiums[g]` for factor group `g`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.factor_scores_to_expected_returns--parameters "Permanent link")
scores : pd.DataFrame Assets × factor-groups matrix of standardised Z-scores. Rows are ticker symbols; columns are factor group names (e.g. `"value"`, `"momentum"`). betas : pd.Series Market (CAPM) beta per asset, indexed by ticker. Assets missing from this Series are treated as having a beta of `1.0` (market neutral assumption). factor_premiums : dict[str, float] Mapping of premium label → annualised premium (e.g. `{"market": 0.05, "value": 0.03, "momentum": 0.04}`). The reserved `"market"` key provides `λ_mkt`; all other keys are matched against columns in _scores_. risk_free_rate : float, default 0.0 Annualised risk-free rate `r_f`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.factor_scores_to_expected_returns--returns "Permanent link")
pd.Series Annualised expected return per ticker, indexed by `scores.index`.
###### Examples[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.factor_scores_to_expected_returns--examples "Permanent link")
> > > import pandas as pd scores = pd.DataFrame( ... {"value": [1.0, -1.0], "momentum": [0.5, 0.0]}, ... index=["AAPL", "MSFT"], ... ) betas = pd.Series({"AAPL": 1.2, "MSFT": 0.8}) factor_premiums = {"market": 0.05, "value": 0.03, "momentum": 0.04} factor_scores_to_expected_returns(scores, betas, factor_premiums, 0.02) AAPL 0.132 MSFT 0.018 dtype: float64
####  `align_to_pit(data, period_date_col, as_of_date, lag_days, ticker_col='ticker')` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.align_to_pit "Permanent link")
Filter time-series data to records published before `as_of_date`.
A record with period end date `D` is considered published `lag_days` calendar days after `D`. A record is available as of `as_of_date` only when `D + lag_days <= as_of_date`, equivalently when `D <= as_of_date - lag_days`.
For each ticker, the most recent record satisfying the availability constraint is returned so that callers receive a cross-sectional view as of `as_of_date`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.align_to_pit--parameters "Permanent link")
data : pd.DataFrame Time-series data containing `period_date_col` and optionally `ticker_col`. period_date_col : str Name of the column holding the period end date. as_of_date : pd.Timestamp or str The computation date. Only records available on or before this date (after the lag has elapsed) are returned. lag_days : int Calendar days between period end and data availability. ticker_col : str Column holding the ticker identifier. Defaults to `"ticker"`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.align_to_pit--returns "Permanent link")
pd.DataFrame Cross-sectional view: one row per ticker (the most recent available record), indexed by `ticker_col` when present. Returns an empty DataFrame with the same columns if no records pass the cutoff.
####  `compute_all_factors(fundamentals, price_history, volume_history=None, analyst_data=None, insider_data=None, config=None, market_returns=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_all_factors "Permanent link")
Compute all configured factors.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_all_factors--parameters "Permanent link")
fundamentals : pd.DataFrame Cross-sectional data indexed by ticker. price_history : pd.DataFrame Price matrix (dates x tickers). volume_history : pd.DataFrame or None Volume matrix. analyst_data : pd.DataFrame or None Analyst recommendation data. insider_data : pd.DataFrame or None Insider transaction data. config : FactorConstructionConfig or None Construction parameters. market_returns : pd.Series or None Pre-computed market return series for beta estimation. See :func:`compute_factor` for details.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_all_factors--returns "Permanent link")
pd.DataFrame Tickers x factors matrix.
####  `compute_factor(factor_type, fundamentals, price_history, volume_history=None, analyst_data=None, insider_data=None, config=None, market_returns=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor "Permanent link")
Compute a single factor.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor--parameters "Permanent link")
factor_type : FactorType Which factor to compute. fundamentals : pd.DataFrame Cross-sectional data indexed by ticker. price_history : pd.DataFrame Price matrix (dates x tickers). volume_history : pd.DataFrame or None Volume matrix (dates x tickers). analyst_data : pd.DataFrame or None Analyst recommendation data. insider_data : pd.DataFrame or None Insider transaction data. config : FactorConstructionConfig or None Construction parameters. market_returns : pd.Series or None Pre-computed market return series for beta estimation. When provided, used as the benchmark instead of the equal-weight cross-sectional mean. Pass a currency- consistent broad index (e.g. SPY daily returns) when `price_history` spans multiple currency zones.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor--returns "Permanent link")
pd.Series Factor values indexed by ticker.
####  `check_survivorship_bias(returns, final_periods=12, zero_threshold=1e-10)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_survivorship_bias "Permanent link")
Check for potential survivorship bias in a return panel.
Survivorship bias occurs when delisted or failed assets are excluded from the sample. A simple heuristic: if **no** asset has near-zero returns in the final `final_periods` rows (i.e., no asset appears to have stopped trading), the panel may suffer from survivorship bias.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_survivorship_bias--parameters "Permanent link")
returns : pd.DataFrame Dates × assets return matrix. final_periods : int Number of trailing periods to inspect. zero_threshold : float Absolute threshold below which a return is considered "zero".
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_survivorship_bias--returns "Permanent link")
bool `True` if survivorship bias is suspected, `False` otherwise.
####  `compute_factor_pca(scores, n_components=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor_pca "Permanent link")
Compute PCA on a cross-sectional factor score matrix.
Rows with any NaN are dropped before fitting. Scores are standardised (zero mean, unit variance per factor) so that PCA operates on the correlation structure rather than the covariance structure.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor_pca--parameters "Permanent link")
scores : pd.DataFrame Tickers × factors matrix of factor scores. Columns are factor names; rows are asset observations. n_components : int or None, default None Number of principal components to retain. `None` keeps all components (min(n_samples, n_features)).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor_pca--returns "Permanent link")
FactorPCAResult See :class:`FactorPCAResult` for field descriptions.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_factor_pca--raises "Permanent link")
ValueError If fewer than 2 factors or fewer than 2 observations are available after dropping NaN rows.
####  `flag_redundant_factors(scores, vif_threshold=10.0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.flag_redundant_factors "Permanent link")
Return factor names whose VIF exceeds _vif_threshold_.
A VIF above the threshold indicates that the factor's variance is largely explained by the remaining factors, making it a candidate for merging or removal from the composite score.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.flag_redundant_factors--parameters "Permanent link")
scores : pd.DataFrame Tickers × factors matrix of factor scores. Must contain at least 2 factor columns. vif_threshold : float, default 10.0 VIF cutoff above which a factor is considered redundant. Commonly used values: 5 (conservative) or 10 (standard).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.flag_redundant_factors--returns "Permanent link")
list[str] Factor names with `VIF > vif_threshold`, in the order they appear in `scores.columns`. Empty list if none exceed the threshold.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.flag_redundant_factors--raises "Permanent link")
ValueError Propagated from :func:`compute_vif` if fewer than 2 factors are provided.
####  `build_factor_bl_views(composite_scores, selected_tickers, config)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_bl_views "Permanent link")
Generate Black-Litterman absolute views from composite factor scores.
For each selected ticker with composite score `z_i`, generates a view::

```
E[r_i] = (rf + market_premium + z_i * score_premium) / 252

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_bl_views--parameters "Permanent link")
composite_scores : pd.Series Composite factor scores indexed by ticker. selected_tickers : pd.Index Tickers in the portfolio. config : FactorIntegrationConfig Integration configuration with rf, market premium, and score premium.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_bl_views--returns "Permanent link")
tuple[tuple[str, ...], tuple[float, ...]] `(views, confidences)` where views are BL-compatible strings like `"AAPL == 0.00045"` and confidences are in [0, 1].
####  `build_factor_exposure_constraints(factor_scores, bounds)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_exposure_constraints "Permanent link")
Build enforceable linear factor exposure constraints.
For each factor `g`, the constraint enforces::

```
lb_g <= sum_i w_i * z_{i,g} <= ub_g

```

The result is expressed as `left_inequality @ w <= right_inequality` (two rows per factor) and can be passed directly to :class:`skfolio.optimization.MeanRisk` via its `left_inequality` / `right_inequality` constructor arguments.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_exposure_constraints--parameters "Permanent link")
factor_scores : pd.DataFrame Tickers x factors matrix of standardised factor scores. The tickers must match the assets used in the optimizer `fit`. bounds : tuple[float, float] or dict[str, tuple[float, float]] Exposure bounds applied to every factor (uniform) when given as a single `(lower, upper)` tuple, or per-factor bounds when given as a dict mapping factor name → `(lower, upper)`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_exposure_constraints--returns "Permanent link")
FactorExposureConstraints Dataclass holding `left_inequality`, `right_inequality`, and metadata. Pass `left_inequality` and `right_inequality` as keyword arguments to the optimizer.
###### Warns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_exposure_constraints--warns "Permanent link")
UserWarning If the equal-weight portfolio exposure lies outside `[lb, ub]` for any factor (i.e. the constraint may be infeasible or very tight under a balanced allocation).
####  `build_factor_integration(config, composite_scores, standardized_factors, selected_tickers)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_integration "Permanent link")
Build factor-to-optimizer integration objects.
Depending on `config.use_black_litterman`, either creates a Black-Litterman prior from composite scores or builds linear factor exposure constraints.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_integration--parameters "Permanent link")
config : FactorIntegrationConfig Integration configuration. composite_scores : pd.Series Composite factor scores indexed by ticker. standardized_factors : pd.DataFrame Standardized factor scores (tickers x factors). selected_tickers : pd.Index Tickers selected for the portfolio.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_integration--returns "Permanent link")
tuple[BasePrior | None, FactorExposureConstraints | None] `(prior, constraints)` — one of the two will be set, the other `None`.
####  `compute_net_alpha(ic_series, weights_history, cost_bps=10.0, annualisation=252)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_net_alpha "Permanent link")
Compute factor net alpha after deducting turnover-based transaction costs.
Combines IC-based gross alpha with the turnover cost from a weights history to produce a single net performance metric::

```
gross_alpha  = mean(IC) * sqrt(annualisation)
avg_turnover = mean one-way turnover across rebalancing dates
total_cost   = avg_turnover * cost_bps / 10_000
net_alpha    = gross_alpha - total_cost
net_icir     = net_alpha / (std(IC) * sqrt(annualisation))

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_net_alpha--parameters "Permanent link")
ic_series : pd.Series Time series of period information coefficients (Spearman or Pearson rank correlation between factor scores and forward returns), one value per rebalancing period. weights_history : pd.DataFrame Portfolio weights at each rebalancing date: rows = dates, columns = assets. Turnover is computed between every pair of consecutive rows. cost_bps : float, default=10.0 Round-trip transaction cost in basis points. annualisation : int, default=252 Number of periods per year (252 for daily, 12 for monthly).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_net_alpha--returns "Permanent link")
NetAlphaResult Dataclass with `gross_alpha`, `avg_turnover`, `total_cost`, `net_alpha`, and `net_icir`.
####  `estimate_factor_premia(factor_mimicking_returns)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.estimate_factor_premia "Permanent link")
Estimate annualized factor premia from long-short returns.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.estimate_factor_premia--parameters "Permanent link")
factor_mimicking_returns : pd.DataFrame Dates x factors matrix of factor-mimicking portfolio returns.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.estimate_factor_premia--returns "Permanent link")
dict[str, float] Annualized premium per factor.
####  `build_factor_mimicking_portfolios(scores, returns, quantile=0.3, weighting='equal', beta_neutral=False, market_returns=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_mimicking_portfolios "Permanent link")
Build long-short factor-mimicking portfolio return time series.
For each date the top _quantile_ fraction of assets (by factor score) are held long and the bottom _quantile_ fraction are held short. The long-short return is the equal- or value-weighted long leg minus the corresponding short leg.
The function handles **one factor at a time** : _scores_ is a dates × assets DataFrame encoding cross-sectional scores for a single factor. For multiple factors, call once per factor and concatenate the results::

```
factor_returns = pd.concat(
    [
        build_factor_mimicking_portfolios(scores_value, returns)
            .rename(columns={"factor_return": "value"}),
        build_factor_mimicking_portfolios(scores_mom, returns)
            .rename(columns={"factor_return": "momentum"}),
    ],
    axis=1,
)

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_mimicking_portfolios--parameters "Permanent link")
scores : pd.DataFrame Dates × assets matrix of cross-sectional factor scores. Index = dates; columns = asset tickers. returns : pd.DataFrame Dates × assets matrix of asset returns, aligned with _scores_ on the date index. Columns may be a superset or subset of _scores_ columns; the intersection is used. quantile : float, default 0.30 Fraction of the asset universe assigned to each leg. Must be in `(0, 0.5]`. weighting : {"equal", "value"}, default "equal" Weighting scheme within each leg. `"equal"` — every asset in the leg receives the same weight. `"value"` — assets are weighted by the absolute value of their factor score. beta_neutral : bool, default False When `True`, hedge the long-short portfolio against market beta exposure. The hedge ratio adjusts the short-leg weight so that the portfolio beta is approximately zero. market_returns : pd.Series or None Market return series, required when `beta_neutral=True`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_mimicking_portfolios--returns "Permanent link")
pd.DataFrame Dates × 1 DataFrame of long-short portfolio returns. Column name is `"factor_return"`. Index is the intersection of _scores_ and _returns_ dates. Missing periods (fewer than `2 * k` valid observations) are filled with NaN.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.build_factor_mimicking_portfolios--raises "Permanent link")
ValueError If _quantile_ is outside `(0, 0.5]` or _weighting_ is unknown.
####  `compute_cross_factor_correlation(factor_returns)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_cross_factor_correlation "Permanent link")
Compute the Pearson correlation matrix across factor-mimicking portfolios.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_cross_factor_correlation--parameters "Permanent link")
factor_returns : pd.DataFrame Dates × factors DataFrame of long-short factor returns, as returned by `build_factor_mimicking_portfolios` (possibly concatenated across multiple factors).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_cross_factor_correlation--returns "Permanent link")
pd.DataFrame Factors × factors symmetric correlation matrix. Diagonal entries are exactly 1.0. Computed on the rows where all factors have non-NaN returns (pairwise-complete otherwise).
####  `compute_quintile_spread(scores, returns, n_quantiles=5)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quintile_spread "Permanent link")
Compute quintile portfolio returns and spread for a single factor.
At each date assets are ranked by factor score and split into _n_quantiles_ equal-count buckets (Q1 = lowest scores, Qn = highest). Each bucket return is the equal-weight average of its members. The long-short spread is Qn − Q1.
Ties in scores are broken by rank order (`method="first"`), ensuring every bucket is populated at every date.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quintile_spread--parameters "Permanent link")
scores : pd.DataFrame Dates × assets matrix of cross-sectional factor scores. returns : pd.DataFrame Dates × assets matrix of asset returns, aligned with _scores_. n_quantiles : int, default 5 Number of equal-count buckets. 5 = quintiles, 10 = deciles. Must be ≥ 2.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quintile_spread--returns "Permanent link")
QuintileSpreadResult See :class:`QuintileSpreadResult` for field descriptions.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quintile_spread--raises "Permanent link")
ValueError If _n_quantiles_ < 2.
####  `fit_gbt_composite(scores, forward_returns, max_depth=3, n_estimators=50, random_state=0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_gbt_composite "Permanent link")
Fit a gradient-boosted tree model mapping factor scores to forward returns.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_gbt_composite--parameters "Permanent link")
scores : pd.DataFrame Historical tickers x factors matrix (training observations). forward_returns : pd.Series Forward return per ticker for the training period. max_depth : int Maximum depth of individual regression trees (3-5 recommended to limit extrapolation and retain interpretability). n_estimators : int Number of boosting rounds. random_state : int Random state for reproducibility.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_gbt_composite--returns "Permanent link")
GradientBoostingRegressor Fitted GBT model.
####  `fit_ridge_composite(scores, forward_returns, alpha=1.0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_ridge_composite "Permanent link")
Fit a ridge regression model mapping factor scores to forward returns.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_ridge_composite--parameters "Permanent link")
scores : pd.DataFrame Historical tickers x factors matrix (training observations). Must be aligned with `forward_returns` on the index. forward_returns : pd.Series Forward return per ticker for the training period. alpha : float L2 regularisation strength. A single-element array is passed to `RidgeCV` so cross-validation still runs internally if multiple alphas are desired; here we keep one alpha for determinism.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.fit_ridge_composite--returns "Permanent link")
RidgeCV Fitted ridge model. Call `predict(scores)` for new data.
####  `predict_composite_scores(model, scores)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.predict_composite_scores "Permanent link")
Apply a fitted ridge or GBT model to produce normalised composite scores.
The raw predictions are standardised to zero mean and unit variance so the output is on the same scale as z-score factor inputs.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.predict_composite_scores--parameters "Permanent link")
model : RidgeCV or GradientBoostingRegressor A model returned by :func:`fit_ridge_composite` or :func:`fit_gbt_composite`. scores : pd.DataFrame Current-period tickers x factors matrix.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.predict_composite_scores--returns "Permanent link")
pd.Series Normalised composite score per ticker (zero mean, unit variance). Tickers with all-NaN factor rows receive `NaN`.
####  `run_factor_oos_validation(scores, returns, config=None, cpcv_config=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_oos_validation "Permanent link")
Rolling block or CPCV out-of-sample validation of factor IC and spreads.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_oos_validation--parameters "Permanent link")
scores : pd.DataFrame Panel of standardised factor scores with a two-level row MultiIndex `(date, ticker)` and one column per factor. returns : pd.DataFrame Forward returns panel with the same `(date, ticker)` MultiIndex and a single return column. config : FactorOOSConfig or None Rolling window parameters. Defaults to `FactorOOSConfig()`. Ignored when `cpcv_config` is provided. cpcv_config : CPCVConfig or None When provided, uses combinatorial purged cross-validation instead of rolling blocks. Overrides `config`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_oos_validation--returns "Permanent link")
FactorOOSResult Per-fold and aggregate IC and quintile spread statistics.
###### Notes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_oos_validation--notes "Permanent link")
The validation window computation uses **only val-window dates** ; no training-window data is used. Fold count equals `floor((total_periods - train_periods) / step_periods)` for rolling, or `C(n_folds, n_test_folds)` for CPCV.
####  `apply_regime_tilts(group_weights, regime, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_regime_tilts "Permanent link")
Apply regime-conditional multiplicative tilts to group weights.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_regime_tilts--parameters "Permanent link")
group_weights : dict[FactorGroupType, float] Base group weights. regime : MacroRegime Current macro regime. config : RegimeTiltConfig or None Tilt configuration.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_regime_tilts--returns "Permanent link")
dict[FactorGroupType, float] Tilted group weights (re-normalized to sum to original total).
###### Notes[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_regime_tilts--notes "Permanent link")
The bounding sequence is:
  1. Look up raw tilts from `get_regime_tilts`.
  2. Clamp each multiplier to `[0, config.max_tilt_multiplier]`.
  3. Apply clamped multiplier to each group weight.
  4. Floor each result to `config.min_post_tilt_weight * total` so no group is compressed to near-zero.
  5. Re-normalize to preserve the original total weight.


####  `check_regime_disagreement(regime_a, regime_b, label_a='composite', label_b='hmm')` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_regime_disagreement "Permanent link")
Check whether two regime classifications disagree.
When the macro-indicator and HMM-based (or any two) regime systems produce different classifications, this function logs a `WARNING` and returns `True`. Returns `False` when they agree.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_regime_disagreement--parameters "Permanent link")
regime_a, regime_b : MacroRegime Regime classifications from two different subsystems. label_a, label_b : str Human-readable labels for the two sources (used in the log message).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.check_regime_disagreement--returns "Permanent link")
bool `True` if the regimes disagree, `False` otherwise.
####  `classify_regime(macro_data, thresholds=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime "Permanent link")
Classify the current macro-economic regime.
Uses a simple heuristic based on GDP growth and leading indicators. The regime is determined by the latest observation's position relative to trend.
When richer indicators (`pmi`, `spread_2s10s`, `hy_oas`) are present, delegates to :func:`classify_regime_composite`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime--parameters "Permanent link")
macro_data : pd.DataFrame Macro indicators with columns that may include `gdp_growth`, `leading_indicator`, `yield_spread`, `unemployment_rate`. Index is date. thresholds : RegimeThresholdConfig or None Scoring thresholds forwarded to the composite classifier.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime--returns "Permanent link")
MacroRegime Current regime classification.
####  `classify_regime_composite(macro_data, thresholds=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime_composite "Permanent link")
Classify macro regime using the multi-indicator composite score.
Uses ISM PMI, 2s10s yield curve spread, and HY credit spread to compute a composite score S_t as defined in the macroeconomic analysis framework (Chapter 7).
The input DataFrame should contain any of these columns: `pmi` (Manufacturing PMI), `spread_2s10s` (10Y-2Y spread in %), `hy_oas` (HY OAS in basis points), `sentiment` (news score).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime_composite--parameters "Permanent link")
macro_data : pd.DataFrame Macro indicators indexed by date. thresholds : RegimeThresholdConfig or None Scoring thresholds. Defaults to the empirical calibration.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.classify_regime_composite--returns "Permanent link")
MacroRegime Regime classification based on composite score.
####  `get_regime_tilts(regime, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.get_regime_tilts "Permanent link")
Get multiplicative tilts for a given regime.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.get_regime_tilts--parameters "Permanent link")
regime : MacroRegime Current macro regime. config : RegimeTiltConfig or None Tilt configuration.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.get_regime_tilts--returns "Permanent link")
dict[FactorGroupType, float] Multiplicative tilt per group. Groups not listed get a tilt of 1.0.
####  `compute_composite_score(standardized_factors, coverage, config=None, ic_history=None, training_scores=None, training_returns=None, group_weights=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_score "Permanent link")
Compute composite score from standardized factors.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_score--parameters "Permanent link")
standardized_factors : pd.DataFrame Tickers x factors matrix. coverage : pd.DataFrame Boolean coverage matrix. config : CompositeScoringConfig or None Scoring configuration. ic_history : pd.DataFrame or None Required when `config.method` is `IC_WEIGHTED` or `ICIR_WEIGHTED`. Columns must match group names; each column is treated as the IC time series for that group. training_scores : pd.DataFrame or None Required when `config.method` is `RIDGE_WEIGHTED` or `GBT_WEIGHTED`. Historical tickers x factors matrix used to train the ML model (must not overlap with current-period data). training_returns : pd.Series or None Required when `config.method` is `RIDGE_WEIGHTED` or `GBT_WEIGHTED`. Forward returns aligned with `training_scores`. group_weights : dict[str, float] or None Pre-computed group weights (e.g. from regime tilts). Threaded through to the inner scoring functions.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_score--returns "Permanent link")
pd.Series or pd.DataFrame Composite score per ticker. When `config.return_coverage` is True, returns a DataFrame with `composite` and `coverage_ratio` columns.
####  `compute_equal_weight_composite(group_scores, config=None, group_weights=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_equal_weight_composite "Permanent link")
Equal-weight composite with core/supplementary tiering.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_equal_weight_composite--parameters "Permanent link")
group_scores : pd.DataFrame Tickers x groups matrix. config : CompositeScoringConfig or None Scoring configuration. group_weights : dict[str, float] or None Pre-computed group weights (e.g. from regime tilts). When provided, skip tier-based derivation and use these weights directly.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_equal_weight_composite--returns "Permanent link")
pd.Series Composite score per ticker.
####  `compute_group_scores(standardized_factors, coverage)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_group_scores "Permanent link")
Average factor scores within each group.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_group_scores--parameters "Permanent link")
standardized_factors : pd.DataFrame Tickers x factors matrix of standardized scores. coverage : pd.DataFrame Boolean matrix of non-NaN coverage.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_group_scores--returns "Permanent link")
pd.DataFrame Tickers x groups matrix of group-level scores.
####  `compute_ic_weighted_composite(group_scores, ic_history, config=None, group_weights=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_weighted_composite "Permanent link")
IC-weighted composite score.
Uses trailing information coefficient history to weight groups.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_weighted_composite--parameters "Permanent link")
group_scores : pd.DataFrame Tickers x groups matrix. ic_history : pd.DataFrame Periods x groups matrix of IC values. config : CompositeScoringConfig or None Scoring configuration. group_weights : dict[str, float] or None Pre-computed group weights (e.g. from regime tilts). When provided, use as tier multipliers instead of config core/supplementary weights.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_weighted_composite--returns "Permanent link")
pd.Series Composite score per ticker.
####  `compute_icir_weighted_composite(group_scores, ic_series_per_group, config=None, group_weights=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir_weighted_composite "Permanent link")
ICIR-weighted composite score.
Weights each group by `max(ICIR, 0) = max(mean(IC) / std(IC), 0)`, normalised to sum to 1. Groups with zero, negative, or undefined ICIR receive zero weight. Falls back to equal-weight when all groups have ICIR <= 0.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir_weighted_composite--parameters "Permanent link")
group_scores : pd.DataFrame Tickers x groups matrix. ic_series_per_group : dict[str, pd.Series] Per-group IC time series. Keys must match `group_scores` columns. config : CompositeScoringConfig or None Scoring configuration. group_weights : dict[str, float] or None Pre-computed group weights (e.g. from regime tilts). When provided, use as tier multipliers instead of config core/supplementary weights.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir_weighted_composite--returns "Permanent link")
pd.Series Composite score per ticker.
####  `compute_ml_composite(standardized_factors, training_scores, training_returns, config)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ml_composite "Permanent link")
ML composite score using ridge regression or gradient-boosted trees.
Trains the model on historical `(training_scores, training_returns)` and predicts on the current-period `standardized_factors`. The prediction is normalised to zero mean and unit variance.
The training window must end strictly before the prediction date to avoid look-ahead bias; callers are responsible for this temporal split.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ml_composite--parameters "Permanent link")
standardized_factors : pd.DataFrame Current-period tickers x factors matrix (prediction target). training_scores : pd.DataFrame Historical tickers x factors matrix aligned with `training_returns`. training_returns : pd.Series Forward return per ticker for the training period. config : CompositeScoringConfig Must have `method` set to `RIDGE_WEIGHTED` or `GBT_WEIGHTED`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ml_composite--returns "Permanent link")
pd.Series Normalised composite score per ticker (zero mean, unit variance).
####  `apply_sector_balance(selected, scores, sector_labels, parent_universe, tolerance=0.05)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_sector_balance "Permanent link")
Adjust selection for sector-proportional representation.
Iterates the balance pass until convergence (no further adds or removes are needed) or until `_MAX_BALANCE_ITERATIONS` is reached. A warning is logged if the cap is hit before convergence.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_sector_balance--parameters "Permanent link")
selected : pd.Index Initially selected tickers. scores : pd.Series Composite scores for all candidates. sector_labels : pd.Series Sector label per ticker. parent_universe : pd.Index Full universe for computing target sector weights. tolerance : float Maximum deviation from parent sector weights.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.apply_sector_balance--returns "Permanent link")
pd.Index Sector-balanced selection.
####  `compute_selection_turnover(current, new, universe)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_selection_turnover "Permanent link")
Compute selection turnover as fraction of universe changed.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_selection_turnover--parameters "Permanent link")
current : pd.Index Currently selected tickers. new : pd.Index Newly selected tickers. universe : pd.Index Full investable universe.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_selection_turnover--returns "Permanent link")
float `len(added | removed) / len(universe)`, or 0.0 if universe is empty.
####  `select_fixed_count(scores, target_count, buffer_fraction=0.1, current_members=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_fixed_count "Permanent link")
Select top N stocks by composite score with buffer.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_fixed_count--parameters "Permanent link")
scores : pd.Series Composite scores indexed by ticker. target_count : int Target number of stocks. buffer_fraction : float Buffer as a fraction of target_count. Current members within the buffer zone are retained in preference to the lowest-ranked direct entrants, but the returned index always contains exactly `min(len(valid_scores), target_count)` tickers. current_members : pd.Index or None Tickers currently selected.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_fixed_count--returns "Permanent link")
pd.Index Selected tickers. Length is always `min(len(scores.dropna()), target_count)`.
####  `select_quantile(scores, target_quantile=0.8, exit_quantile=None, current_members=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_quantile "Permanent link")
Select stocks above a quantile threshold.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_quantile--parameters "Permanent link")
scores : pd.Series Composite scores indexed by ticker. target_quantile : float Quantile threshold for entry (0-1). exit_quantile : float or None Quantile threshold for exit (hysteresis). If `None`, uses `target_quantile`. current_members : pd.Index or None Currently selected tickers.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_quantile--returns "Permanent link")
pd.Index Selected tickers.
####  `select_stocks(scores, config=None, current_members=None, sector_labels=None, parent_universe=None, return_turnover=False)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_stocks "Permanent link")
Select stocks from scored universe.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_stocks--parameters "Permanent link")
scores : pd.Series Composite scores indexed by ticker. config : SelectionConfig or None Selection configuration. current_members : pd.Index or None Currently selected tickers for buffer/hysteresis. sector_labels : pd.Series or None Sector labels for sector balancing. parent_universe : pd.Index or None Full universe for sector weight targets. return_turnover : bool When `True`, return `(selected, turnover)` tuple.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.select_stocks--returns "Permanent link")
pd.Index or tuple[pd.Index, float] Selected tickers, optionally with turnover.
####  `neutralize_sector(scores, sector_labels, country_labels=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.neutralize_sector "Permanent link")
Demean scores within each sector (and optionally country).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.neutralize_sector--parameters "Permanent link")
scores : pd.Series Standardized factor scores. sector_labels : pd.Series Sector label per ticker. country_labels : pd.Series or None Country label per ticker for country neutralization.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.neutralize_sector--returns "Permanent link")
pd.Series Sector-neutralized scores.
####  `orthogonalize_factors(factor_scores, method='pca', min_variance_explained=0.95)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.orthogonalize_factors "Permanent link")
Project factor scores onto orthogonal principal components.
Eliminates multicollinearity among factor scores by projecting them into a lower-dimensional PCA space. Retains the minimum number of components that explain at least `min_variance_explained` of the total variance.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.orthogonalize_factors--parameters "Permanent link")
factor_scores : pd.DataFrame Tickers × factors matrix of factor scores. method : str Projection method. Only `"pca"` is supported. min_variance_explained : float Minimum cumulative explained variance ratio for retained components. Must be in `(0, 1]`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.orthogonalize_factors--returns "Permanent link")
pd.DataFrame Tickers × PCs matrix with columns named `PC1`, `PC2`, .... Rows with NaN in the input are filled with NaN in the output but otherwise preserve the original index.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.orthogonalize_factors--raises "Permanent link")
ConfigurationError If _method_ is not `"pca"`. DataError If fewer than 2 factors or fewer than 2 non-NaN observations.
####  `rank_normal_standardize(scores)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.rank_normal_standardize "Permanent link")
Rank-normal (inverse normal) standardization.
Uses `Phi^-1((rank - 0.5) / N)` to map ranks to a normal distribution, robust to heavy-tailed distributions.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.rank_normal_standardize--parameters "Permanent link")
scores : pd.Series Factor scores (may contain NaN).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.rank_normal_standardize--returns "Permanent link")
pd.Series Rank-normalized scores.
####  `standardize_all_factors(raw_factors, config=None, sector_labels=None, country_labels=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_all_factors "Permanent link")
Standardize all factors and compute coverage.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_all_factors--parameters "Permanent link")
raw_factors : pd.DataFrame Tickers x factors matrix of raw values. config : StandardizationConfig or None Standardization parameters. sector_labels : pd.Series or None Sector labels for neutralization. country_labels : pd.Series or None Country labels for neutralization.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_all_factors--returns "Permanent link")
tuple[pd.DataFrame, pd.DataFrame] (standardized_scores, coverage) where coverage is a boolean DataFrame indicating non-NaN values.
####  `standardize_factor(raw_scores, config=None, sector_labels=None, country_labels=None, *, factor_name='')` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_factor "Permanent link")
Full standardization pipeline for a single factor.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_factor--parameters "Permanent link")
raw_scores : pd.Series Raw factor values. config : StandardizationConfig or None Standardization parameters. sector_labels : pd.Series or None Sector labels for neutralization. country_labels : pd.Series or None Country labels for neutralization. factor_name : str Column name of the factor, used to look up per-factor method overrides in `config.factor_method_overrides` and the `FACTOR_DIRECTION` sign convention.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.standardize_factor--returns "Permanent link")
pd.Series Standardized factor scores.
####  `winsorize_cross_section(scores, lower_pct=0.01, upper_pct=0.99)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section "Permanent link")
Clip scores at percentile boundaries.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section--parameters "Permanent link")
scores : pd.Series Raw factor scores. lower_pct : float Lower percentile (0-1). upper_pct : float Upper percentile (0-1).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section--returns "Permanent link")
pd.Series Winsorized scores.
####  `winsorize_cross_section_mad(scores, mad_multiplier=3.0)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section_mad "Permanent link")
Clip scores using Median Absolute Deviation (MAD).
Uses the normal-consistent scale factor `1.4826 * MAD` to set clip boundaries at `median +/- mad_multiplier * scale`, following the MSCI Barra USE4 convention (+/-3 MAD).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section_mad--parameters "Permanent link")
scores : pd.Series Raw factor scores (may contain NaN). mad_multiplier : float Number of scaled-MAD units for clip boundaries.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.winsorize_cross_section_mad--returns "Permanent link")
pd.Series Winsorized scores.
####  `z_score_standardize(scores)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.z_score_standardize "Permanent link")
Z-score standardization: (x - mean) / std.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.z_score_standardize--parameters "Permanent link")
scores : pd.Series Factor scores (may contain NaN).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.z_score_standardize--returns "Permanent link")
pd.Series Standardized scores with mean 0 and std 1.
####  `benjamini_hochberg(p_values, alpha=0.05)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.benjamini_hochberg "Permanent link")
Benjamini-Hochberg FDR correction.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.benjamini_hochberg--parameters "Permanent link")
p_values : pd.Series Raw p-values indexed by factor name. alpha : float FDR significance level.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.benjamini_hochberg--returns "Permanent link")
pd.Series Boolean series indicating significant factors.
####  `compute_composite_ic(composite_scores_history, returns_history, newey_west_lags=6, t_stat_threshold=2.0, min_observations=3)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_ic "Permanent link")
Compute IC statistics for the composite score signal.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_ic--parameters "Permanent link")
composite_scores_history : pd.DataFrame Dates x tickers matrix of composite scores. returns_history : pd.DataFrame Dates x tickers matrix of forward returns. newey_west_lags : int, default 6 Number of lags for HAC standard errors. t_stat_threshold : float, default 2.0 Threshold for significance decision. min_observations : int, default 3 Minimum non-NaN observations per cross-section date.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_composite_ic--returns "Permanent link")
CompositeICResult IC statistics for the composite score. The `best_individual_ic` and `outperforms_best_individual` fields are populated by `run_factor_validation` when individual factor results are available.
####  `compute_ic_series(factor_scores_history, returns_history, factor_name, min_observations=3)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_series "Permanent link")
Compute IC time series for a factor.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_series--parameters "Permanent link")
factor_scores_history : pd.DataFrame Dates x tickers matrix of factor scores. returns_history : pd.DataFrame Dates x tickers matrix of forward returns. factor_name : str Used only for labeling. min_observations : int, default 3 Minimum number of common non-NaN observations per date. Passed through to `compute_monthly_ic`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_series--returns "Permanent link")
pd.Series IC values indexed by date.
####  `compute_ic_stats(ic_series, lags=5)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_stats "Permanent link")
Compute full IC statistics including Newey-West t-stat and ICIR.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_stats--parameters "Permanent link")
ic_series : pd.Series Time series of IC values (one per cross-section date). lags : int Number of lags for Newey-West HAC standard errors.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_ic_stats--returns "Permanent link")
ICStats Dataclass containing `mean`, `variance_nw`, `t_stat_nw`, `p_value`, and `icir`.
####  `compute_icir(ic_series)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir "Permanent link")
Compute the IC Information Ratio (mean IC / std IC).
ICIR penalises factors with high average IC but also high IC volatility (inconsistent predictors). Use this as the weighting signal in ICIR-weighted composite scoring.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir--parameters "Permanent link")
ic_series : pd.Series Time series of IC values (one per cross-section date).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_icir--returns "Permanent link")
float ICIR value, or 0.0 if `std(IC) == 0` or fewer than 2 non-NaN observations.
####  `compute_monthly_ic(factor_scores, forward_returns, min_observations=3)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_monthly_ic "Permanent link")
Compute rank information coefficient (Spearman correlation).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_monthly_ic--parameters "Permanent link")
factor_scores : pd.Series Cross-sectional factor scores. forward_returns : pd.Series Forward returns for the same tickers. min_observations : int, default 3 Minimum number of common non-NaN observations required. Returns NaN if fewer are available.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_monthly_ic--returns "Permanent link")
float Rank IC (Spearman correlation).
####  `compute_newey_west_tstat(ic_series, n_lags=6)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_newey_west_tstat "Permanent link")
Compute Newey-West t-statistic for IC significance.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_newey_west_tstat--parameters "Permanent link")
ic_series : pd.Series Time series of IC values. n_lags : int Number of lags for HAC standard errors.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_newey_west_tstat--returns "Permanent link")
tuple[float, float] (t_statistic, p_value).
####  `compute_quantile_spread(factor_scores, forward_returns, n_quantiles=5)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quantile_spread "Permanent link")
Compute long-short quantile spread return.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quantile_spread--parameters "Permanent link")
factor_scores : pd.Series Cross-sectional factor scores. forward_returns : pd.Series Forward returns. n_quantiles : int Number of quantile buckets.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_quantile_spread--returns "Permanent link")
float Top quantile return minus bottom quantile return.
####  `compute_vif(factor_matrix)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_vif "Permanent link")
Compute variance inflation factors for multicollinearity.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_vif--parameters "Permanent link")
factor_matrix : pd.DataFrame Tickers x factors matrix (no NaN). Must contain at least 2 factors.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_vif--returns "Permanent link")
pd.Series VIF per factor. Values are ≥ 1.0 by construction.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.compute_vif--raises "Permanent link")
ValueError If fewer than 2 factor columns are provided.
####  `correct_pvalues(p_values, alpha=0.05)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.correct_pvalues "Permanent link")
Apply Holm-Bonferroni and Benjamini-Hochberg multiple testing corrections.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.correct_pvalues--parameters "Permanent link")
p_values : ndarray, shape (m,) Raw p-values in any order. alpha : float Significance level used to compute the adjustments (does not filter here; callers compare adjusted p-values against `alpha`).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.correct_pvalues--returns "Permanent link")
CorrectedPValues `holm` — FWER-controlling Holm-Bonferroni adjusted p-values. `bh` — FDR-controlling Benjamini-Hochberg adjusted p-values. Both arrays are returned in the **same order** as the input.
####  `run_factor_validation(factor_scores_history, returns_history, config=None, composite_scores_history=None)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_validation "Permanent link")
Run complete factor validation suite.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_validation--parameters "Permanent link")
factor_scores_history : dict[str, pd.DataFrame] Factor name -> (dates x tickers) score history. returns_history : pd.DataFrame Dates x tickers forward return matrix. config : FactorValidationConfig or None Validation parameters. composite_scores_history : pd.DataFrame or None Dates x tickers matrix of composite scores. When provided, IC analysis is run on the composite signal and compared against the best individual factor IC.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.run_factor_validation--returns "Permanent link")
FactorValidationReport Complete validation results.
####  `validate_factor_universe(ic_matrix, lags=5, alpha=0.05)` [¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.validate_factor_universe "Permanent link")
Validate all factors simultaneously with multiple testing correction.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.validate_factor_universe--parameters "Permanent link")
ic_matrix : pd.DataFrame Dates × factors matrix of IC values (one IC per period per factor). lags : int Number of Newey-West HAC lags. alpha : float Significance level for both FWER and FDR rejection decisions.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/factors/#optimizer.factors.validate_factor_universe--returns "Permanent link")
pd.DataFrame Factor × statistic summary with columns: `ic_mean`, `icir`, `t_stat_nw`, `p_value_raw`, `p_value_holm`, `p_value_bh`, `significant_holm`, `significant_bh`.
