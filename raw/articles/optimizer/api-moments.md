<!-- source: https://silviobaratto.github.io/optimizer/api/moments/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/moments/#moments)
# moments[¶](https://silviobaratto.github.io/optimizer/api/moments/#moments "Permanent link")
###  `optimizer.moments` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments "Permanent link")
Moment estimation and prior construction.
####  `CovEstimatorType` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.CovEstimatorType "Permanent link")
Bases: `str`, `Enum`
Covariance estimator selection.
####  `MomentEstimationConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig "Permanent link")
Immutable configuration for moment estimation and prior construction.
All parameters map 1:1 to skfolio estimator constructor arguments, making the config serialisable and suitable for hyperparameter sweeps.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig--parameters "Permanent link")
mu_estimator : MuEstimatorType Which expected return estimator to use. shrinkage_method : ShrinkageMethod Shrinkage flavour when `mu_estimator` is `SHRUNK`. ew_mu_alpha : float Exponential weighting decay for `EWMu`. risk_aversion : float Risk-aversion coefficient for `EquilibriumMu`. cov_estimator : CovEstimatorType Which covariance estimator to use. ew_cov_alpha : float Exponential weighting decay for `EWCovariance`. shrunk_cov_shrinkage : float Shrinkage intensity for `ShrunkCovariance`. gerber_threshold : float Threshold for `GerberCovariance`. is_log_normal : bool Whether returns are log-normal (for multi-period scaling in `EmpiricalPrior`). investment_horizon : float or None Investment horizon forwarded to `EmpiricalPrior`. use_factor_model : bool If `True`, wrap the prior in a `FactorModel`. residual_variance : bool Whether to include residual variance in `FactorModel`.
#####  `for_equilibrium_ledoitwolf()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig.for_equilibrium_ledoitwolf "Permanent link")
Black-Litterman-ready prior: EquilibriumMu + LedoitWolf.
#####  `for_shrunk_denoised()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig.for_shrunk_denoised "Permanent link")
Conservative prior: ShrunkMu (James-Stein) + DenoiseCovariance.
#####  `for_adaptive()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig.for_adaptive "Permanent link")
Responsive prior: EW on both mu and covariance.
#####  `for_hmm_blended(n_states=2)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MomentEstimationConfig.for_hmm_blended "Permanent link")
HMM-blended prior: regime-probability-weighted mu and covariance.
####  `MuEstimatorType` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.MuEstimatorType "Permanent link")
Bases: `str`, `Enum`
Expected return estimator selection.
####  `ShrinkageMethod` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.ShrinkageMethod "Permanent link")
Bases: `str`, `Enum`
Shrinkage method for :class:`ShrunkMu`.
Maps to :class:`skfolio.moments.expected_returns._shrunk_mu.ShrunkMuMethods`.
####  `DMMConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.DMMConfig "Permanent link")
Hyper-parameters for the Deep Markov Model.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.DMMConfig--attributes "Permanent link")
z_dim : int Dimension of the continuous latent state z_t. emission_dim : int Hidden layer size of the Emitter MLP. transition_dim : int Hidden layer size of the GatedTransition MLP. rnn_dim : int GRU hidden state size for the backward inference network. num_epochs : int Number of SVI training epochs. learning_rate : float Initial learning rate for ClippedAdam. annealing_epochs : int Epochs over which the KL weight is linearly annealed from _minimum_annealing_factor_ to 1.0. minimum_annealing_factor : float Starting KL annealing weight (prevents posterior collapse). random_state : int or None Seed for reproducible initialisation.
####  `DMMResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.DMMResult "Permanent link")
Result of fitting a Deep Markov Model.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.DMMResult--attributes "Permanent link")
latent_means : pd.DataFrame, shape (T, z_dim) Variational posterior means for each time step. latent_stds : pd.DataFrame, shape (T, z_dim) Variational posterior standard deviations. elbo_history : list[float] ELBO value (= −SVI loss) per training epoch. model : Any Trained DMM nn.Module instance. tickers : list[str] Asset names, in training order. input_mean : ndarray, shape (n_assets,) Per-asset mean used for input standardisation. input_std : ndarray, shape (n_assets,) Per-asset std used for input standardisation.
####  `HMMBlendedCovariance` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance "Permanent link")
Bases: `BaseCovariance`
Covariance estimator that blends regime covariances via HMM.
Fits a Gaussian HMM with :func:`fit_hmm` and computes the blended covariance matrix using the full law of total variance formula::

```
Σ = Σ_s p(z_T=s | r_{1:T}) · [Σ_s + (μ_s - μ)(μ_s - μ)ᵀ]

```

The second term `(μ_s - μ)(μ_s - μ)ᵀ` is the cross-state mean dispersion contribution, which the simpler blend in :func:`blend_moments_by_regime` omits.
Conforms to the skfolio `BaseCovariance` API: exposes `covariance_` (`ndarray` of shape `(n_assets, n_assets)`) after `fit`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance--parameters "Permanent link")
hmm_config : HMMConfig or None, default=None HMM hyper-parameters. `None` falls back to `HMMConfig()`. nearest : bool, default=True Project the blended covariance to the nearest positive-definite matrix if it is not already PSD. higham : bool, default=False Use the Higham (2002) algorithm for the PSD projection instead of eigenvalue clipping. higham_max_iteration : int, default=100 Maximum iterations for the Higham algorithm.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance--attributes "Permanent link")
covariance_ : ndarray of shape (n_assets, n_assets) Blended covariance matrix (with mean-dispersion term). hmm_result_ : HMMResult The fitted HMM result. n_features_in_ : int Number of assets seen during `fit`. feature_names_in_ : ndarray of shape (n_features_in_,) Asset names seen during `fit` (only when input is a DataFrame with string column names).
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance.fit "Permanent link")
Fit the HMM and compute the blended covariance matrix.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance.fit--parameters "Permanent link")
X : array-like of shape (n_observations, n_assets) Linear returns of the assets. y : ignored
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedCovariance.fit--returns "Permanent link")
self
####  `HMMBlendedMu` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu "Permanent link")
Bases: `BaseMu`
Expected-return estimator that blends regime-conditional means via HMM.
Fits a Gaussian HMM with :func:`fit_hmm` and computes the probability-weighted blended expected return vector::

```
μ = Σ_s p(z_T=s | r_{1:T}) · μ_s

```

where the weights are the smoothed posterior at the final observation.
Conforms to the skfolio `BaseMu` API: exposes `mu_` (`ndarray` of shape `(n_assets,)`) after `fit`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu--parameters "Permanent link")
hmm_config : HMMConfig or None, default=None HMM hyper-parameters. `None` falls back to `HMMConfig()` (2 states, full covariance, 100 EM iterations).
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu--attributes "Permanent link")
mu_ : ndarray of shape (n_assets,) Probability-weighted blended expected return vector. hmm_result_ : HMMResult The fitted HMM result (for inspection or downstream use). n_features_in_ : int Number of assets seen during `fit`. feature_names_in_ : ndarray of shape (n_features_in_,) Asset names seen during `fit` (only when input is a DataFrame with string column names).
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu.fit "Permanent link")
Fit the HMM and compute the blended expected return vector.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu.fit--parameters "Permanent link")
X : array-like of shape (n_observations, n_assets) Linear returns of the assets. y : ignored
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMBlendedMu.fit--returns "Permanent link")
self
####  `HMMConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMConfig "Permanent link")
Configuration for the Gaussian HMM.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMConfig--attributes "Permanent link")
n_states : int Number of latent regimes (hidden states). n_iter : int Maximum number of Baum-Welch EM iterations. tol : float Convergence tolerance on log-likelihood improvement. covariance_type : str Covariance structure: `"full"`, `"diag"`, `"tied"`, or `"spherical"`. random_state : int or None Seed for reproducible initialisation.
####  `HMMResult` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMResult "Permanent link")
Result of fitting a Gaussian HMM to return data.
###### Attributes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.HMMResult--attributes "Permanent link")
transition_matrix : ndarray, shape (n_states, n_states) Row-stochastic transition probability matrix `A[i, j] = P(z_t=j | z_{t-1}=i)`. regime_means : pd.DataFrame, shape (n_states, n_assets) Per-regime mean return vectors. Index is integer state label (0, 1, ..., n_states-1); columns are asset tickers. regime_covariances : ndarray, shape (n_states, n_assets, n_assets) Per-regime covariance matrices. Axis-0 indexes the state. filtered_probs : pd.DataFrame, shape (n_dates, n_states) Forward-only filtered state probabilities `α_t(s) ∝ P(r_t | z_t=s) · Σ_{s'} A[s', s] · α_{t-1}(s')`, conditioned only on past and current observations `r_{1:t}`. These are causal (no look-ahead bias) and suitable for online blending in backtests. Rows sum to 1.0. smoothed_probs : pd.DataFrame, shape (n_dates, n_states) Baum-Welch smoothed posterior probabilities `γ_t(s) = P(z_t=s | r_{1:T})` conditioned on the **entire** sequence. Use for diagnostics and regime labeling, but NOT for causal blending in backtests. log_likelihood : float Log-likelihood of the data under the fitted model.
####  `blend_moments_dmm(result, n_mc_samples=500, seed=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_dmm "Permanent link")
Project the last latent state through the generative model via MC sampling.
Draws `n_mc_samples` from the variational posterior `q(z_T)`, propagates each through the transition `p(z_{T+1} | z_T)` and emission `p(x_{T+1} | z_{T+1})`, then applies the law of total variance to produce the blended mean and covariance.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_dmm--parameters "Permanent link")
result : DMMResult Output of :func:`fit_dmm`. n_mc_samples : int, default=500 Number of Monte Carlo samples for posterior-predictive estimation. seed : int or None, default=None Random seed for reproducibility.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_dmm--returns "Permanent link")
tuple[pd.Series, pd.DataFrame] `(mu, cov)` — expected returns and covariance matrix in the original (un-standardised) return scale.
####  `fit_dmm(returns, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_dmm "Permanent link")
Fit a Deep Markov Model to a panel of asset returns.
Uses Pyro SVI with ClippedAdam and KL annealing. Input returns are standardised to zero mean / unit variance per asset before fitting.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_dmm--parameters "Permanent link")
returns : pd.DataFrame Dates × assets matrix of linear returns. NaN rows are dropped. config : DMMConfig or None Model hyper-parameters. Defaults to `DMMConfig()`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_dmm--returns "Permanent link")
DMMResult
####  `build_cov_estimator(config)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_cov_estimator "Permanent link")
Build a skfolio covariance estimator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_cov_estimator--parameters "Permanent link")
config : MomentEstimationConfig Moment estimation configuration.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_cov_estimator--returns "Permanent link")
BaseCovariance A fitted-ready skfolio covariance estimator.
####  `build_mu_estimator(config)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_mu_estimator "Permanent link")
Build a skfolio expected return estimator from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_mu_estimator--parameters "Permanent link")
config : MomentEstimationConfig Moment estimation configuration.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_mu_estimator--returns "Permanent link")
BaseMu A fitted-ready skfolio expected return estimator.
####  `build_prior(config=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_prior "Permanent link")
Build a complete prior estimator from _config_.
Composes expected return and covariance estimators into an `EmpiricalPrior`, optionally wrapping it in a `FactorModel` when `config.use_factor_model` is `True`.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_prior--parameters "Permanent link")
config : MomentEstimationConfig or None Moment estimation configuration. Defaults to `MomentEstimationConfig()` (EmpiricalMu + LedoitWolf).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.build_prior--returns "Permanent link")
BasePrior A fitted-ready skfolio prior estimator.
####  `blend_moments_by_regime(result)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_by_regime "Permanent link")
Compute probability-weighted moments from the last filtered time step.
Uses the smoothed posterior at the final observation `γ_T(s)` to produce a single blended expected-return vector and covariance matrix:

```
μ = Σ_s γ_T(s) · μ_s
Σ = Σ_s γ_T(s) · Σ_s

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_by_regime--parameters "Permanent link")
result : HMMResult Output of :func:`fit_hmm`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_by_regime--returns "Permanent link")
tuple[pd.Series, pd.DataFrame] `(mu, cov)` — blended expected returns (indexed by ticker) and blended covariance matrix (tickers × tickers).
###### Notes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.blend_moments_by_regime--notes "Permanent link")
This function computes only the within-regime weighted covariance `Σ = Σ_s γ(s) · Σ_s` and **omits** the cross-state mean-dispersion term `Σ_s γ(s) · (μ_s − μ)(μ_s − μ)ᵀ` from the full law of total variance. As a result, the blended covariance will under-estimate total uncertainty when regime means differ materially.
For optimizer inputs that require the full variance decomposition, use :class:`HMMBlendedCovariance` instead, which includes both the within-regime and between-regime components.
####  `fit_hmm(returns, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_hmm "Permanent link")
Fit a Gaussian HMM to a panel of asset returns.
Uses the Baum-Welch (EM) algorithm implemented by `hmmlearn` to estimate the transition matrix, regime-conditional means and covariances, and the smoothed filtered probabilities.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_hmm--parameters "Permanent link")
returns : pd.DataFrame Dates × assets matrix of linear returns. Rows with any NaN are dropped before fitting. config : HMMConfig or None Model hyper-parameters. Defaults to `HMMConfig()` (2 states, full covariance, 100 EM iterations).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_hmm--returns "Permanent link")
HMMResult Fitted HMM parameters and smoothed state probabilities.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_hmm--raises "Permanent link")
ValueError If fewer than 2 assets or fewer than `n_states + 1` observations remain after dropping NaN rows.
###### Notes[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.fit_hmm--notes "Permanent link")
State ordering is deterministic after fitting. States are sorted by ascending mean return (averaged across assets), so state 0 is always the lowest-return regime (bear/stress) and state `n_states - 1` is the highest-return regime (bull/calm).
####  `select_hmm_n_states(returns, candidate_n_states=(2, 3, 4), criterion='bic', hmm_config=None)` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.select_hmm_n_states "Permanent link")
Select the optimal number of HMM states via AIC or BIC.
For each candidate state count, fits an HMM via :func:`fit_hmm` and computes the information criterion. Returns the candidate that minimises the chosen criterion.
Free parameters per state count S with d assets::

```
k = S*(S-1) + S*d + S*d*(d+1)//2

```

where the three terms correspond to transition matrix rows (each row sums to 1, so S-1 free per row), per-regime means, and per-regime full covariance (lower triangle).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.select_hmm_n_states--parameters "Permanent link")
returns : pd.DataFrame Dates x assets matrix of linear returns. candidate_n_states : Sequence[int] State counts to evaluate (default `(2, 3, 4)`). criterion : str `"aic"` or `"bic"` (default `"bic"`). hmm_config : HMMConfig or None Base HMM config. `n_states` is overridden per candidate.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.select_hmm_n_states--returns "Permanent link")
int The state count that minimises the chosen criterion.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.select_hmm_n_states--raises "Permanent link")
ValueError If `criterion` is not `"aic"` or `"bic"`. DataError If no candidate succeeds.
####  `apply_lognormal_correction(mu, cov, horizon, method='exact')` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.apply_lognormal_correction "Permanent link")
Scale daily log-return moments to a multi-period horizon.
**Expected return** (Jensen's inequality correction, same for both methods):
.. math::

```
E[R_T] = \exp(\mu T + \tfrac{1}{2}\,\mathrm{diag}(\Sigma) T) - 1

```

**Covariance —`method="exact"`** (exact log-normal result):
.. math::

```
\mathrm{Cov}[R_T^i, R_T^j]
= \exp\!\bigl((\mu_i + \mu_j)T
  + \tfrac{1}{2}(\sigma_i^2 + \sigma_j^2)T\bigr)
  \cdot \bigl(\exp(\sigma_{ij}\,T) - 1\bigr)

```

**Covariance —`method="linear"`** (delta-method approximation):
.. math::

```
\Sigma_T \approx \Sigma \cdot T

```

###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.apply_lognormal_correction--parameters "Permanent link")
mu : pd.Series Daily log-return expected values, indexed by asset ticker. cov : pd.DataFrame Daily log-return covariance matrix. Must be square and share the same index/columns as _mu_. horizon : int Investment horizon in trading days (e.g. 21 for monthly, 63 for quarterly, 252 for annual). method : {"exact", "linear"}, default "exact" Covariance scaling method. `"exact"` applies the full log-normal formula; `"linear"` uses the simpler `Sigma * T` approximation (retained for backwards compatibility).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.apply_lognormal_correction--returns "Permanent link")
tuple[pd.Series, pd.DataFrame] `(mu_T, cov_T)` — horizon-scaled expected returns and covariance.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.apply_lognormal_correction--raises "Permanent link")
ValueError If _horizon_ is not a positive integer, if _mu_ and _cov_ do not share the same ticker index, or if _method_ is not recognised.
####  `scale_moments_to_horizon(mu, cov, daily_horizon, method='exact')` [¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.scale_moments_to_horizon "Permanent link")
Validate inputs and apply the log-normal moment correction.
A higher-level wrapper around :func:`apply_lognormal_correction` that validates array shapes and non-negativity of the covariance diagonal before delegating to the core scaling function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.scale_moments_to_horizon--parameters "Permanent link")
mu : pd.Series Daily log-return expected values, indexed by asset ticker. cov : pd.DataFrame Daily log-return covariance matrix. daily_horizon : int Investment horizon in trading days. method : {"exact", "linear"}, default "exact" Covariance scaling method. See :func:`apply_lognormal_correction`.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.scale_moments_to_horizon--returns "Permanent link")
tuple[pd.Series, pd.DataFrame] `(mu_T, cov_T)` — horizon-scaled expected returns and covariance.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/moments/#optimizer.moments.scale_moments_to_horizon--raises "Permanent link")
ValueError If inputs are not aligned, the covariance matrix is not square, the diagonal contains negative values, or _daily_horizon_ < 1.
