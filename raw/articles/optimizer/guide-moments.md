<!-- source: https://silviobaratto.github.io/optimizer/guide/moments/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/moments/#moment-estimation)
# Moment Estimation[¶](https://silviobaratto.github.io/optimizer/guide/moments/#moment-estimation "Permanent link")
The `optimizer.moments` module provides expected return estimation, covariance estimation, Hidden Markov Model regime blending, Deep Markov Models, and multi-period log-normal scaling. Every component follows the library-wide pattern of **frozen dataclass config + factory function** , and all estimators conform to the skfolio `BaseMu` / `BaseCovariance` API so they compose directly inside sklearn pipelines.
* * *
## Module Layout[¶](https://silviobaratto.github.io/optimizer/guide/moments/#module-layout "Permanent link")  
| File  | Contents  |  
| --- | --- |  
| `optimizer/moments/_config.py`  |  `MuEstimatorType`, `CovEstimatorType`, `ShrinkageMethod` enums; `MomentEstimationConfig` frozen dataclass  |  
| `optimizer/moments/_factory.py`  |  `build_mu_estimator()`, `build_cov_estimator()`, `build_prior()` factories  |  
| `optimizer/moments/_hmm.py`  |  `HMMConfig`, `HMMResult`, `fit_hmm()`, `select_hmm_n_states()`, `blend_moments_by_regime()`, `HMMBlendedMu`, `HMMBlendedCovariance`  |  
| `optimizer/moments/_dmm.py`  |  `DMMConfig`, `DMMResult`, `fit_dmm()`, `blend_moments_dmm()` (optional; requires `torch` + `pyro-ppl`)  |  
| `optimizer/moments/_scaling.py`  |  `apply_lognormal_correction()`, `scale_moments_to_horizon()`  |  
* * *
## Expected Return Estimators[¶](https://silviobaratto.github.io/optimizer/guide/moments/#expected-return-estimators "Permanent link")
The `MuEstimatorType` enum selects which skfolio `BaseMu` estimator `build_mu_estimator()` instantiates.  
| Enum value  | skfolio class  | Key parameter(s)  | Description  |  
| --- | --- | --- | --- |  
| `EMPIRICAL`  | `EmpiricalMu`  | --  | Sample mean of historical returns  |  
| `SHRUNK`  | `ShrunkMu`  | `shrinkage_method`  | Shrinkage toward a structured target (see table below)  |  
| `EW`  | `EWMu`  |  `ew_mu_alpha` (default 0.2)  | Exponentially weighted mean; higher alpha puts more weight on recent observations  |  
| `EQUILIBRIUM`  | `EquilibriumMu`  |  `risk_aversion` (default 1.0)  | Implied equilibrium returns from market-cap weights; Black-Litterman starting point  |  
| `HMM_BLENDED`  | `HMMBlendedMu`  | `hmm_config`  | Regime-probability-weighted blend of per-state means (see [HMM section](https://silviobaratto.github.io/optimizer/guide/moments/#hidden-markov-model-regime-blending))  |  
### Shrinkage methods[¶](https://silviobaratto.github.io/optimizer/guide/moments/#shrinkage-methods "Permanent link")
When `mu_estimator = MuEstimatorType.SHRUNK`, the `ShrinkageMethod` enum controls which shrinkage flavour is used:  
| Enum value  | skfolio method  | Reference  |  
| --- | --- | --- |  
| `JAMES_STEIN`  | `ShrunkMuMethods.JAMES_STEIN`  | James & Stein (1961)  |  
| `BAYES_STEIN`  | `ShrunkMuMethods.BAYES_STEIN`  | Jorion (1986)  |  
| `BODNAR_OKHRIN`  | `ShrunkMuMethods.BODNAR_OKHRIN`  | Bodnar & Okhrin (2011)  |  
* * *
## Covariance Estimators[¶](https://silviobaratto.github.io/optimizer/guide/moments/#covariance-estimators "Permanent link")
The `CovEstimatorType` enum selects which skfolio `BaseCovariance` estimator `build_cov_estimator()` instantiates.  
| Enum value  | skfolio class  | Key parameter(s)  | Description  |  
| --- | --- | --- | --- |  
| `EMPIRICAL`  | `EmpiricalCovariance`  | --  | Sample covariance matrix  |  
| `LEDOIT_WOLF`  | `LedoitWolf`  | --  | Analytical shrinkage (Ledoit & Wolf, 2004); optimal bias-variance trade-off without cross-validation  |  
| `OAS`  | `OAS`  | --  | Oracle Approximating Shrinkage (Chen et al., 2010); similar to Ledoit-Wolf but with a different analytical formula  |  
| `SHRUNK`  | `ShrunkCovariance`  |  `shrunk_cov_shrinkage` (default 0.1)  | Fixed shrinkage intensity toward a diagonal target  |  
| `EW`  | `EWCovariance`  |  `ew_cov_alpha` (default 0.2)  | Exponentially weighted covariance; recent observations receive higher weight  |  
| `GERBER`  | `GerberCovariance`  |  `gerber_threshold` (default 0.5)  | Gerber statistic-based covariance; only co-movements that exceed the threshold contribute  |  
| `GRAPHICAL_LASSO_CV`  | `GraphicalLassoCV`  | --  | Sparse inverse covariance via L1-penalised MLE with cross-validated penalty  |  
| `DENOISE`  | `DenoiseCovariance`  | inner: `EmpiricalCovariance`  | Random matrix theory denoising; filters eigenvalues below the Marchenko-Pastur threshold  |  
| `DETONE`  | `DetoneCovariance`  | inner: `EmpiricalCovariance`  | Market factor removal; strips the largest eigenvalue (market mode) from the covariance  |  
| `IMPLIED`  | `ImpliedCovariance`  | --  | Implied covariance from option-market data  |  
| `HMM_BLENDED`  | `HMMBlendedCovariance`  | `hmm_config`  | Full law-of-total-variance blend of regime covariances (see [HMM section](https://silviobaratto.github.io/optimizer/guide/moments/#hidden-markov-model-regime-blending))  |  
* * *
## MomentEstimationConfig[¶](https://silviobaratto.github.io/optimizer/guide/moments/#momentestimationconfig "Permanent link")
`MomentEstimationConfig` is a frozen dataclass that bundles all moment estimation parameters into a single serialisable object. Non-serialisable objects (estimator instances, numpy arrays) are never stored in the config; they are constructed by the factory functions.
### Fields[¶](https://silviobaratto.github.io/optimizer/guide/moments/#fields "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-1)@dataclass(frozen=True)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-2)class MomentEstimationConfig:
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-3)    # Expected return estimator
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-4)    mu_estimator: MuEstimatorType = MuEstimatorType.EMPIRICAL
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-5)    shrinkage_method: ShrinkageMethod = ShrinkageMethod.JAMES_STEIN
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-6)    ew_mu_alpha: float = 0.2
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-7)    risk_aversion: float = 1.0
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-8)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-9)    # Covariance estimator
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-10)    cov_estimator: CovEstimatorType = CovEstimatorType.LEDOIT_WOLF
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-11)    ew_cov_alpha: float = 0.2
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-12)    shrunk_cov_shrinkage: float = 0.1
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-13)    gerber_threshold: float = 0.5
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-14)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-15)    # Prior assembly
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-16)    is_log_normal: bool = False
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-17)    investment_horizon: float | None = None
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-18)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-19)    # HMM blended estimators
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-20)    hmm_config: HMMConfig = field(default_factory=HMMConfig)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-21)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-22)    # Factor model
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-23)    use_factor_model: bool = False
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-0-24)    residual_variance: bool = True

```

### Presets[¶](https://silviobaratto.github.io/optimizer/guide/moments/#presets "Permanent link")  
| Preset method  | mu estimator  | cov estimator  | Use case  |  
| --- | --- | --- | --- |  
| `for_equilibrium_ledoitwolf()`  | `EquilibriumMu`  | `LedoitWolf`  | Black-Litterman-ready prior; equilibrium returns serve as the neutral starting point  |  
| `for_shrunk_denoised()`  |  `ShrunkMu` (James-Stein)  | `DenoiseCovariance`  | Conservative prior; shrinks expected returns and removes noise from the covariance spectrum  |  
| `for_adaptive()`  | `EWMu`  | `EWCovariance`  | Responsive prior; exponentially weighted moments adapt quickly to regime changes  |  
| `for_hmm_blended(n_states=2)`  | `HMMBlendedMu`  | `HMMBlendedCovariance`  | Regime-aware prior; probability-weighted blend of per-regime moments  |  
### Usage[¶](https://silviobaratto.github.io/optimizer/guide/moments/#usage "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-1)from optimizer.moments import MomentEstimationConfig
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-3)# Use a preset
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-4)config = MomentEstimationConfig.for_equilibrium_ledoitwolf()
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-6)# Or build from scratch
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-7)config = MomentEstimationConfig(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-8)    mu_estimator=MuEstimatorType.SHRUNK,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-9)    shrinkage_method=ShrinkageMethod.BAYES_STEIN,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-10)    cov_estimator=CovEstimatorType.DENOISE,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-1-11))

```

* * *
## Factory Functions[¶](https://silviobaratto.github.io/optimizer/guide/moments/#factory-functions "Permanent link")
### build_mu_estimator[¶](https://silviobaratto.github.io/optimizer/guide/moments/#build_mu_estimator "Permanent link")
Maps the `mu_estimator` field of a `MomentEstimationConfig` to a concrete skfolio `BaseMu` instance.

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-2-1)from optimizer.moments import MomentEstimationConfig, build_mu_estimator
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-2-3)config = MomentEstimationConfig(mu_estimator=MuEstimatorType.EW, ew_mu_alpha=0.3)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-2-4)mu_est = build_mu_estimator(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-2-5)# Returns an EWMu(alpha=0.3) instance ready for .fit(X)

```

### build_cov_estimator[¶](https://silviobaratto.github.io/optimizer/guide/moments/#build_cov_estimator "Permanent link")
Maps the `cov_estimator` field to a concrete skfolio `BaseCovariance` instance.

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-3-1)from optimizer.moments import MomentEstimationConfig, build_cov_estimator
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-3-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-3-3)config = MomentEstimationConfig(cov_estimator=CovEstimatorType.GERBER, gerber_threshold=0.4)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-3-4)cov_est = build_cov_estimator(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-3-5)# Returns a GerberCovariance(threshold=0.4) instance

```

### build_prior[¶](https://silviobaratto.github.io/optimizer/guide/moments/#build_prior "Permanent link")
Composes `build_mu_estimator` and `build_cov_estimator` into an `EmpiricalPrior`, and optionally wraps it in a `FactorModel`.

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-1)from optimizer.moments import MomentEstimationConfig, build_prior
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-3)# Default prior: EmpiricalMu + LedoitWolf
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-4)prior = build_prior()
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-6)# Prior from a preset
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-7)config = MomentEstimationConfig.for_shrunk_denoised()
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-8)prior = build_prior(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-9)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-10)# Factor model prior
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-11)config = MomentEstimationConfig(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-12)    mu_estimator=MuEstimatorType.EMPIRICAL,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-13)    cov_estimator=CovEstimatorType.LEDOIT_WOLF,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-14)    use_factor_model=True,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-15)    residual_variance=True,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-16))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-17)prior = build_prior(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-4-18)# Returns a FactorModel wrapping EmpiricalPrior

```

When `use_factor_model=True`, the resulting `FactorModel` expects factor returns as the `y` argument during `fit(X, y)`. The fitted prior attribute is `return_distribution_` (not `prior_model_`), containing `mu`, `covariance`, `returns`, `sample_weight`, and `cholesky`.
* * *
## Hidden Markov Model Regime Blending[¶](https://silviobaratto.github.io/optimizer/guide/moments/#hidden-markov-model-regime-blending "Permanent link")
The HMM subsystem fits a Gaussian Hidden Markov Model to a panel of asset returns, extracts regime-conditional moments, and produces probability-weighted blended estimates suitable for portfolio optimization.
### HMMConfig[¶](https://silviobaratto.github.io/optimizer/guide/moments/#hmmconfig "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-1)@dataclass(frozen=True)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-2)class HMMConfig:
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-3)    n_states: int = 2          # Number of latent regimes
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-4)    n_iter: int = 100          # Max Baum-Welch EM iterations
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-5)    tol: float = 1e-4          # Convergence tolerance on log-likelihood
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-6)    covariance_type: str = "full"  # "full", "diag", "tied", or "spherical"
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-5-7)    random_state: int | None = None

```

### HMMResult[¶](https://silviobaratto.github.io/optimizer/guide/moments/#hmmresult "Permanent link")
After fitting, `fit_hmm()` returns an `HMMResult` dataclass containing:  
| Attribute  | Shape  | Description  |  
| --- | --- | --- |  
| `transition_matrix`  | `(n_states, n_states)`  | Row-stochastic matrix   |  
| `regime_means`  | `DataFrame (n_states, n_assets)`  | Per-regime expected return vectors   |  
| `regime_covariances`  | `(n_states, n_assets, n_assets)`  | Per-regime covariance matrices   |  
| `filtered_probs`  | `DataFrame (n_dates, n_states)`  | Forward-only causal probabilities   |  
| `smoothed_probs`  | `DataFrame (n_dates, n_states)`  | Full-sequence posterior probabilities   |  
| `log_likelihood`  | `float`  | Log-likelihood of the data under the fitted model  |  
### Fitting an HMM[¶](https://silviobaratto.github.io/optimizer/guide/moments/#fitting-an-hmm "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-1)from optimizer.moments import HMMConfig, fit_hmm
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-3)config = HMMConfig(n_states=2, random_state=42)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-4)result = fit_hmm(returns, config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-6)print(result.transition_matrix)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-7)print(result.regime_means)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-6-8)print(result.filtered_probs.tail())

```

The function drops NaN rows before fitting and raises `DataError` if fewer than `n_states + 1` observations remain.
### Filtered vs. Smoothed Probabilities[¶](https://silviobaratto.github.io/optimizer/guide/moments/#filtered-vs-smoothed-probabilities "Permanent link")
The HMM produces two sets of state probabilities, and the distinction between them is critical for correct usage:
**Filtered probabilities** **causal** -- they do not use future data -- and are therefore the correct choice for online blending in backtests and live trading.
**Smoothed probabilities** **entire** observation sequence. They provide the best point estimate of the regime at each time step but introduce **look-ahead bias** and must only be used for diagnostics, regime labelling, and parameter estimation -- never for causal blending in backtests.  
| Property  | Filtered  | Smoothed  |  
| --- | --- | --- |  
| Conditioning  |   |   |  
| Causal  | Yes  | No  |  
| Look-ahead bias  | None  | Yes  |  
| Use for backtests  | Yes  | No  |  
| Use for diagnostics  | Yes  | Yes  |  
### Model Selection: AIC / BIC[¶](https://silviobaratto.github.io/optimizer/guide/moments/#model-selection-aic-bic "Permanent link")
`select_hmm_n_states()` evaluates multiple candidate state counts and returns the one that minimises the chosen information criterion.
Free parameters for a model with 
where the three terms count the transition matrix rows (each sums to 1, so 
The criteria are:
[ \text{AIC} = -2 \ln L + 2k ] [ \text{BIC} = -2 \ln L + k \ln T ]

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-1)from optimizer.moments import select_hmm_n_states
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-3)best_n = select_hmm_n_states(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-4)    returns,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-5)    candidate_n_states=(2, 3, 4),
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-6)    criterion="bic",
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-7))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-7-8)print(f"Optimal number of regimes: {best_n}")

```

### Blending Moments by Regime[¶](https://silviobaratto.github.io/optimizer/guide/moments/#blending-moments-by-regime "Permanent link")
#### Simple blend: `blend_moments_by_regime()`[¶](https://silviobaratto.github.io/optimizer/guide/moments/#simple-blend-blend_moments_by_regime "Permanent link")
Computes a probability-weighted blend using the filtered probabilities at the final time step:
[ \mu = \sum_s p_s \cdot \mu_s ] [ \Sigma = \sum_s p_s \cdot \Sigma_s ]
where 

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-8-1)from optimizer.moments import fit_hmm, blend_moments_by_regime
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-8-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-8-3)result = fit_hmm(returns, HMMConfig(n_states=2, random_state=42))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-8-4)mu_blended, cov_blended = blend_moments_by_regime(result)

```

> **Gotcha** : This function computes only the **within-regime** weighted covariance and **omits** the between-regime mean-dispersion term. The blended covariance will underestimate total uncertainty when regime means differ materially. For optimizer inputs, use `HMMBlendedCovariance` instead.
#### Full blend: `HMMBlendedCovariance`[¶](https://silviobaratto.github.io/optimizer/guide/moments/#full-blend-hmmblendedcovariance "Permanent link")
The `HMMBlendedCovariance` class implements the full law of total variance:
The second term **between-regime mean dispersion** -- the additional uncertainty that arises because the true mean itself is uncertain across regimes. This term can be substantial when regime means differ (e.g., bull vs. bear markets) and omitting it leads to systematically underestimated risk.
### skfolio-Compatible Estimator Classes[¶](https://silviobaratto.github.io/optimizer/guide/moments/#skfolio-compatible-estimator-classes "Permanent link")
Both `HMMBlendedMu` and `HMMBlendedCovariance` conform to the skfolio `BaseMu` / `BaseCovariance` API, which means they expose the standard `mu_` and `covariance_` attributes after `.fit(X)` and can be plugged directly into `EmpiricalPrior` or any skfolio pipeline.
#### HMMBlendedMu[¶](https://silviobaratto.github.io/optimizer/guide/moments/#hmmblendedmu "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-1)from optimizer.moments import HMMBlendedMu, HMMConfig
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-3)mu_est = HMMBlendedMu(hmm_config=HMMConfig(n_states=2, random_state=42))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-4)mu_est.fit(X_returns)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-6)print(mu_est.mu_)              # ndarray of shape (n_assets,)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-9-7)print(mu_est.hmm_result_)      # Full HMMResult for inspection

```

After fitting, `mu_` contains the probability-weighted blended expected return vector:
#### HMMBlendedCovariance[¶](https://silviobaratto.github.io/optimizer/guide/moments/#hmmblendedcovariance "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-1)from optimizer.moments import HMMBlendedCovariance, HMMConfig
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-3)cov_est = HMMBlendedCovariance(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-4)    hmm_config=HMMConfig(n_states=2, random_state=42),
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-5)    nearest=True,      # project to nearest PSD if needed
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-6)    higham=False,       # use eigenvalue clipping (not Higham)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-7))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-8)cov_est.fit(X_returns)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-9)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-10)print(cov_est.covariance_)     # ndarray of shape (n_assets, n_assets)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-10-11)print(cov_est.hmm_result_)     # Full HMMResult for inspection

```

The `nearest` parameter controls whether the blended covariance is projected to the nearest positive semi-definite matrix (via eigenvalue clipping or the Higham algorithm). This is enabled by default because the law-of-total- variance blend is not guaranteed to be PSD in finite samples.
### Using HMM Blending in the Prior[¶](https://silviobaratto.github.io/optimizer/guide/moments/#using-hmm-blending-in-the-prior "Permanent link")
The recommended way to use HMM blending is through the `MomentEstimationConfig` preset, which wires everything together:

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-1)from optimizer.moments import MomentEstimationConfig, build_prior
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-3)config = MomentEstimationConfig.for_hmm_blended(n_states=2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-4)prior = build_prior(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-6)# Use in a MeanRisk optimizer
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-7)from skfolio.optimization import MeanRisk
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-8)model = MeanRisk(prior_estimator=prior)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-11-9)model.fit(X_returns)

```

* * *
## Deep Markov Model (Optional)[¶](https://silviobaratto.github.io/optimizer/guide/moments/#deep-markov-model-optional "Permanent link")
The DMM module implements the architecture from Krishnan et al. (2016), "Structured Inference Networks for Nonlinear State Space Models," using Pyro's stochastic variational inference (SVI) with KL annealing.
> **Dependency note** : The DMM requires `torch` and `pyro-ppl`, which are **not** declared in `pyproject.toml`. The module is effectively optional. Import it with: 
> 
```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-12-1)pip install torch pyro-ppl

```

> If the dependencies are missing, importing `DMMConfig` or `fit_dmm` from `optimizer.moments` will silently be suppressed (via `contextlib.suppress` in `__init__.py`).
### Architecture[¶](https://silviobaratto.github.io/optimizer/guide/moments/#architecture "Permanent link")
The generative model factorises as:
The variational guide uses a backward-RNN inference network:
where   
| Component  | Class  | Role  |  
| --- | --- | --- |  
| Emitter  | `Emitter`  | Maps   |  
| Transition  | `GatedTransition`  | Gated residual MLP for   |  
| Combiner  | `Combiner`  | Fuses   |  
| Inference RNN  | `nn.GRU`  | Backward-running GRU encoding   |  
### DMMConfig[¶](https://silviobaratto.github.io/optimizer/guide/moments/#dmmconfig "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-1)@dataclass(frozen=True)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-2)class DMMConfig:
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-3)    z_dim: int = 16                    # Latent state dimension
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-4)    emission_dim: int = 64             # Emitter hidden layer size
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-5)    transition_dim: int = 64           # Transition hidden layer size
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-6)    rnn_dim: int = 128                 # GRU hidden state size
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-7)    num_epochs: int = 1000             # SVI training epochs
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-8)    learning_rate: float = 3e-4        # ClippedAdam learning rate
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-9)    annealing_epochs: int = 50         # KL annealing ramp length
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-10)    minimum_annealing_factor: float = 0.2  # Starting KL weight
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-13-11)    random_state: int | None = None

```

### DMMResult[¶](https://silviobaratto.github.io/optimizer/guide/moments/#dmmresult "Permanent link")  
| Attribute  | Shape  | Description  |  
| --- | --- | --- |  
| `latent_means`  | `DataFrame (T, z_dim)`  | Variational posterior means for each time step  |  
| `latent_stds`  | `DataFrame (T, z_dim)`  | Variational posterior standard deviations  |  
| `elbo_history`  | `list[float]`  | ELBO value per training epoch (for convergence monitoring)  |  
| `model`  | `DMM`  | Trained PyTorch module instance  |  
| `tickers`  | `list[str]`  | Asset names in training order  |  
| `input_mean`  | `ndarray (n_assets,)`  | Per-asset mean used for input standardisation  |  
| `input_std`  | `ndarray (n_assets,)`  | Per-asset std used for input standardisation  |  
### Fitting and Blending[¶](https://silviobaratto.github.io/optimizer/guide/moments/#fitting-and-blending "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-1)from optimizer.moments import DMMConfig, fit_dmm, blend_moments_dmm
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-2)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-3)config = DMMConfig(z_dim=16, num_epochs=500, random_state=42)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-4)result = fit_dmm(returns, config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-5)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-6)# Check convergence
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-7)import matplotlib.pyplot as plt
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-8)plt.plot(result.elbo_history)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-9)plt.xlabel("Epoch")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-10)plt.ylabel("ELBO")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-11)plt.title("DMM Training Convergence")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-12)plt.show()
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-13)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-14)# Produce blended moments via Monte Carlo posterior-predictive sampling
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-14-15)mu, cov = blend_moments_dmm(result, n_mc_samples=500, seed=42)

```

`blend_moments_dmm()` works by:
  1. Sampling 
  2. Propagating through the transition: 
  3. Emitting: 
  4. Applying the law of total variance across Monte Carlo samples.
  5. Un-standardising back to the original return scale.


> **Critical limitation** : The DMM produces **diagonal covariance only**. The law-of-total-variance computation yields 
* * *
## Log-Normal Multi-Period Scaling[¶](https://silviobaratto.github.io/optimizer/guide/moments/#log-normal-multi-period-scaling "Permanent link")
When working with multi-period investment horizons, daily log-return moments must be scaled to the target horizon. The `_scaling` module provides two methods: an exact log-normal formula and a linear (delta-method) approximation.
### The Scaling Problem[¶](https://silviobaratto.github.io/optimizer/guide/moments/#the-scaling-problem "Permanent link")
If daily log-returns 
Because the sum of normals is normal, **not** normal -- it is log-normally distributed. The scaling functions convert log-return parameters to simple-return space.
### Expected Return (Both Methods)[¶](https://silviobaratto.github.io/optimizer/guide/moments/#expected-return-both-methods "Permanent link")
Jensen's inequality correction gives the expected simple return:
where 
### Covariance: Exact Method[¶](https://silviobaratto.github.io/optimizer/guide/moments/#covariance-exact-method "Permanent link")
The exact log-normal covariance is:
where 
### Covariance: Linear Method[¶](https://silviobaratto.github.io/optimizer/guide/moments/#covariance-linear-method "Permanent link")
The delta-method (first-order Taylor) approximation:
This is accurate for short horizons and small variances but increasingly biased as 
### Function Signatures[¶](https://silviobaratto.github.io/optimizer/guide/moments/#function-signatures "Permanent link")
####  `apply_lognormal_correction`[¶](https://silviobaratto.github.io/optimizer/guide/moments/#apply_lognormal_correction "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-1)def apply_lognormal_correction(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-2)    mu: pd.Series,        # Daily log-return expected values
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-3)    cov: pd.DataFrame,    # Daily log-return covariance matrix
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-4)    horizon: int,         # Trading days (21=monthly, 63=quarterly, 252=annual)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-5)    method: str = "exact" # "exact" or "linear"
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-6)) -> tuple[pd.Series, pd.DataFrame]:
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-15-7)    ...

```

####  `scale_moments_to_horizon`[¶](https://silviobaratto.github.io/optimizer/guide/moments/#scale_moments_to_horizon "Permanent link")
A higher-level wrapper that validates inputs (square covariance, aligned indices, non-negative diagonal) before delegating to `apply_lognormal_correction`.

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-1)def scale_moments_to_horizon(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-2)    mu: pd.Series,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-3)    cov: pd.DataFrame,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-4)    daily_horizon: int,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-5)    method: str = "exact"
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-6)) -> tuple[pd.Series, pd.DataFrame]:
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-16-7)    ...

```

### Usage[¶](https://silviobaratto.github.io/optimizer/guide/moments/#usage_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-2)from optimizer.moments import apply_lognormal_correction, scale_moments_to_horizon
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-3)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-4)# Daily log-return moments
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-5)mu_daily = pd.Series({"AAPL": 0.0005, "MSFT": 0.0004, "GOOG": 0.0003})
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-6)cov_daily = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-7)    [[0.0004, 0.0001, 0.0001],
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-8)     [0.0001, 0.0003, 0.0001],
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-9)     [0.0001, 0.0001, 0.0005]],
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-10)    index=mu_daily.index,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-11)    columns=mu_daily.index,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-12))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-13)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-14)# Scale to quarterly horizon (63 trading days), exact method
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-15)mu_q, cov_q = apply_lognormal_correction(mu_daily, cov_daily, horizon=63, method="exact")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-16)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-17)# Scale to annual horizon (252 trading days), linear approximation
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-17-18)mu_a, cov_a = scale_moments_to_horizon(mu_daily, cov_daily, daily_horizon=252, method="linear")

```

> **Important** : Inputs must be **log-return** parameters (mean and covariance of log-returns). The outputs are in **simple-return** space (
* * *
## Common Gotchas[¶](https://silviobaratto.github.io/optimizer/guide/moments/#common-gotchas "Permanent link")
### 1. `blend_moments_by_regime()` vs. `HMMBlendedCovariance`[¶](https://silviobaratto.github.io/optimizer/guide/moments/#1-blend_moments_by_regime-vs-hmmblendedcovariance "Permanent link")
`blend_moments_by_regime()` computes only the within-regime weighted covariance:
`HMMBlendedCovariance` adds the between-regime mean-dispersion term:
The difference 
**Rule** : For optimizer inputs, always use `HMMBlendedCovariance`. Reserve `blend_moments_by_regime()` for quick diagnostics or situations where you explicitly want to ignore between-regime uncertainty.
### 2. Filtered vs. Smoothed Probabilities for Backtests[¶](https://silviobaratto.github.io/optimizer/guide/moments/#2-filtered-vs-smoothed-probabilities-for-backtests "Permanent link")
The `HMMBlendedMu` and `HMMBlendedCovariance` classes use **filtered** (forward-only) probabilities from the last time step. This is the correct causal choice for backtesting. If you manually call `blend_moments_by_regime()`, it also uses the filtered probabilities from `result.filtered_probs.iloc[-1]`.
Never use `result.smoothed_probs` for weight computation in a backtest -- it conditions on the entire sequence and introduces look-ahead bias.
### 3. Log-Return vs. Simple-Return Inputs for Scaling[¶](https://silviobaratto.github.io/optimizer/guide/moments/#3-log-return-vs-simple-return-inputs-for-scaling "Permanent link")
The `apply_lognormal_correction` and `scale_moments_to_horizon` functions expect **log-return** (continuously compounded) parameters as input. The output is in **simple-return** space. If you accidentally pass simple-return moments as input, the resulting expected returns and covariances will be biased upward.
### 4. DMM Produces Diagonal Covariance[¶](https://silviobaratto.github.io/optimizer/guide/moments/#4-dmm-produces-diagonal-covariance "Permanent link")
The Deep Markov Model's `blend_moments_dmm()` returns a diagonal covariance matrix. All off-diagonal covariances are zero. This means the DMM cannot capture cross-asset dependencies and should not be used as a standalone covariance estimator. Consider combining the DMM's variance estimates with a separate cross-sectional covariance model.
### 5. The Fitted Prior Attribute[¶](https://silviobaratto.github.io/optimizer/guide/moments/#5-the-fitted-prior-attribute "Permanent link")
After fitting a prior with `build_prior()`, the estimated distribution is stored in the `return_distribution_` attribute (not `prior_model_`). It contains `mu`, `covariance`, `returns`, `sample_weight`, and `cholesky`.

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-18-1)prior = build_prior(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-18-2)prior.fit(X_returns)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-18-3)print(prior.return_distribution_.mu)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-18-4)print(prior.return_distribution_.covariance)

```

### 6. Factor Model Views[¶](https://silviobaratto.github.io/optimizer/guide/moments/#6-factor-model-views "Permanent link")
When the prior is wrapped in a `FactorModel` (via `use_factor_model=True`), any downstream views (e.g., Black-Litterman) must reference **factor names** (e.g., `MTUM`, `QUAL`), not asset names.
* * *
## Complete Example[¶](https://silviobaratto.github.io/optimizer/guide/moments/#complete-example "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-2)from optimizer.moments import (
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-3)    MomentEstimationConfig,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-4)    MuEstimatorType,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-5)    CovEstimatorType,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-6)    ShrinkageMethod,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-7)    HMMConfig,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-8)    build_prior,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-9)    build_mu_estimator,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-10)    build_cov_estimator,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-11)    fit_hmm,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-12)    select_hmm_n_states,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-13)    apply_lognormal_correction,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-14))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-15)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-16)# --- 1. Basic prior construction ---
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-17)config = MomentEstimationConfig.for_shrunk_denoised()
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-18)prior = build_prior(config)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-19)prior.fit(X_returns)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-20)print("Expected returns:", prior.return_distribution_.mu)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-21)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-22)# --- 2. HMM regime analysis ---
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-23)hmm_cfg = HMMConfig(n_states=2, random_state=42)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-24)result = fit_hmm(returns, hmm_cfg)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-25)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-26)# Transition probabilities
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-27)print("Transition matrix:\n", result.transition_matrix)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-28)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-29)# Current regime belief (causal)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-30)print("Filtered probs (last):", result.filtered_probs.iloc[-1].to_dict())
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-31)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-32)# --- 3. Model selection ---
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-33)best_n = select_hmm_n_states(returns, candidate_n_states=(2, 3, 4), criterion="bic")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-34)print(f"BIC-optimal states: {best_n}")
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-35)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-36)# --- 4. HMM-blended prior in optimizer ---
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-37)config_hmm = MomentEstimationConfig.for_hmm_blended(n_states=best_n)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-38)prior_hmm = build_prior(config_hmm)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-39)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-40)from skfolio.optimization import MeanRisk
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-41)model = MeanRisk(prior_estimator=prior_hmm)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-42)model.fit(X_returns)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-43)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-44)# --- 5. Multi-period scaling ---
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-45)mu_daily = pd.Series({"AAPL": 0.0005, "MSFT": 0.0004})
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-46)cov_daily = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-47)    [[0.0004, 0.0001], [0.0001, 0.0003]],
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-48)    index=mu_daily.index,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-49)    columns=mu_daily.index,
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-50))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-51)mu_annual, cov_annual = apply_lognormal_correction(
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-52)    mu_daily, cov_daily, horizon=252, method="exact"
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-53))
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-54)print("Annual expected return:", mu_annual)
[](https://silviobaratto.github.io/optimizer/guide/moments/#__codelineno-19-55)print("Annual covariance:\n", cov_annual)

```

