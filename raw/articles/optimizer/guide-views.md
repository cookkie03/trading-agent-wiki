<!-- source: https://silviobaratto.github.io/optimizer/guide/views/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/views/#view-integration)
# View Integration[¶](https://silviobaratto.github.io/optimizer/guide/views/#view-integration "Permanent link")
Frameworks for incorporating investor views into portfolio construction. The views module provides three complementary approaches -- Black-Litterman, Entropy Pooling, and Opinion Pooling -- each offering different tradeoffs between expressiveness, computational cost, and theoretical grounding.
All three frameworks produce skfolio `BasePrior` objects that plug directly into any skfolio optimiser via the `prior_estimator` parameter. The module follows the standard project convention: **frozen`@dataclass` config** + **factory function**. Configs hold only serialisable primitives; non-serialisable objects (estimator instances, numpy arrays) are passed as factory keyword arguments.
**Important** : Views use `tuple[str, ...]` in configs (hashable for frozen dataclasses). Factory functions convert these to `list[str]` before passing to skfolio.
* * *
## Module Overview[¶](https://silviobaratto.github.io/optimizer/guide/views/#module-overview "Permanent link")  
| Framework  | Config  | Factory  | Use Case  |  
| --- | --- | --- | --- |  
| Black-Litterman  | `BlackLittermanConfig`  | `build_black_litterman()`  | Equilibrium-based return tilting with absolute/relative views  |  
| Entropy Pooling  | `EntropyPoolingConfig`  | `build_entropy_pooling()`  | Non-parametric views on any distributional moment  |  
| Opinion Pooling  | `OpinionPoolingConfig`  | `build_opinion_pooling()`  | Combining multiple expert prior estimators  |  
| Omega Calibration  | --  | `calibrate_omega_from_track_record()`  | Empirical uncertainty from forecast track records  |  

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-1)from optimizer.views import (
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-2)    BlackLittermanConfig,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-3)    EntropyPoolingConfig,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-4)    OpinionPoolingConfig,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-5)    ViewUncertaintyMethod,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-6)    build_black_litterman,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-7)    build_entropy_pooling,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-8)    build_opinion_pooling,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-9)    calibrate_omega_from_track_record,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-0-10))

```

* * *
## 1. Black-Litterman[¶](https://silviobaratto.github.io/optimizer/guide/views/#1-black-litterman "Permanent link")
The Black-Litterman (BL) model starts from a market equilibrium prior and tilts expected returns toward investor views. The posterior blends equilibrium returns 
### Posterior Formula[¶](https://silviobaratto.github.io/optimizer/guide/views/#posterior-formula "Permanent link")
Given:
The BL posterior expected returns are:
The BL posterior covariance is:
### View Syntax[¶](https://silviobaratto.github.io/optimizer/guide/views/#view-syntax "Permanent link")
Views are expressed as strings that skfolio parses into the picking matrix 
**Absolute views** -- a single asset will achieve a specific return:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-1-1)"AAPL == 0.05"    # AAPL expected return is 5%
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-1-2)"JPM == 0.03"     # JPM expected return is 3%

```

**Relative views** -- the difference in returns between two assets:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-2-1)"AAPL - MSFT == 0.02"   # AAPL outperforms MSFT by 2%

```

### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/views/#configuration "Permanent link")
`BlackLittermanConfig` is a frozen dataclass with the following fields:  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `views`  | `tuple[str, ...]`  | _(required)_  | View expressions (absolute or relative)  |  
| `tau`  | `float`  | `0.05`  | Uncertainty scaling; must be strictly positive  |  
| `risk_free_rate`  | `float`  | `0.0`  | Risk-free rate added to posterior returns  |  
| `uncertainty_method`  | `ViewUncertaintyMethod`  | `HE_LITTERMAN`  | How to calibrate the   |  
| `view_confidences`  | `tuple[float, ...] \| None`  | `None`  | Per-view confidence levels in   |  
| `groups`  | `dict[str, list[str]] \| None`  | `None`  | Asset group mapping for group-relative views  |  
| `prior_config`  | `MomentEstimationConfig \| None`  | `None`  | Inner prior config; defaults to `EquilibriumMu` + `LedoitWolf`  |  
| `use_factor_model`  | `bool`  | `False`  | Wrap BL in a `FactorModel`  |  
| `residual_variance`  | `bool`  | `True`  | Include residual variance in `FactorModel`  |  
**Validation** : `tau` must be strictly positive. Setting `tau=0` or a negative value raises `ValueError`.
### Uncertainty Methods[¶](https://silviobaratto.github.io/optimizer/guide/views/#uncertainty-methods "Permanent link")
The `ViewUncertaintyMethod` enum controls how the diagonal uncertainty matrix   
| Method  | Enum Value  | Description  |  
| --- | --- | --- |  
| He-Litterman  | `HE_LITTERMAN`  |   |  
| Idzorek  | `IDZOREK`  | Per-view confidence levels in   |  
| Empirical Track Record  | `EMPIRICAL_TRACK_RECORD`  |   |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/views/#presets "Permanent link")
Three factory methods provide common configurations:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-1)# Standard BL with EquilibriumMu + LedoitWolf prior
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-2)cfg = BlackLittermanConfig.for_equilibrium(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-3)    views=("AAPL == 0.05", "JPM == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-6)# BL wrapped in a FactorModel
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-7)cfg = BlackLittermanConfig.for_factor_model(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-8)    views=("MTUM == 0.05",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-9))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-10)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-11)# Idzorek method with per-view confidence levels
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-12)cfg = BlackLittermanConfig.for_idzorek(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-13)    views=("AAPL == 0.05", "MSFT == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-14)    view_confidences=(0.9, 0.6),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-3-15))

```

### Factory Function[¶](https://silviobaratto.github.io/optimizer/guide/views/#factory-function "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-1)def build_black_litterman(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-2)    config: BlackLittermanConfig,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-3)    view_history: pd.DataFrame | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-4)    return_history: pd.DataFrame | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-5)    omega: npt.NDArray[np.float64] | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-4-6)) -> BasePrior:

```

**Parameters** :
  * `config` -- the `BlackLittermanConfig` instance
  * `view_history` -- historical forecasted `EMPIRICAL_TRACK_RECORD` unless `omega` is pre-supplied
  * `return_history` -- realised returns aligned to each view (dates x views); required together with `view_history`
  * `omega` -- pre-computed diagonal `EMPIRICAL_TRACK_RECORD`, used directly (skips history computation)


**Returns** : a `BlackLitterman` instance (or `FactorModel` wrapping one if `use_factor_model=True`).
### Examples[¶](https://silviobaratto.github.io/optimizer/guide/views/#examples "Permanent link")
#### Absolute and Relative Views[¶](https://silviobaratto.github.io/optimizer/guide/views/#absolute-and-relative-views "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-1)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-2)from optimizer.views import BlackLittermanConfig, build_black_litterman
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-3)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-4)returns = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-6)cfg = BlackLittermanConfig.for_equilibrium(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-7)    views=("AAPL == 0.05", "AAPL - MSFT == 0.02", "JPM == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-8))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-9)prior = build_black_litterman(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-10)prior.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-11)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-12)mu_posterior = prior.return_distribution_.mu
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-5-13)cov_posterior = prior.return_distribution_.covariance

```

#### Idzorek Confidence Levels[¶](https://silviobaratto.github.io/optimizer/guide/views/#idzorek-confidence-levels "Permanent link")
Higher confidence values pull the posterior closer to the view target:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-1)cfg = BlackLittermanConfig.for_idzorek(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-2)    views=("AAPL == 0.10", "MSFT == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-3)    view_confidences=(0.9, 0.5),   # 90% confident on AAPL, 50% on MSFT
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-5)prior = build_black_litterman(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-6-6)prior.fit(returns)

```

#### Empirical Track Record[¶](https://silviobaratto.github.io/optimizer/guide/views/#empirical-track-record "Permanent link")
When historical forecast data is available, the uncertainty matrix can be calibrated from realised forecast errors:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-3)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-4)cfg = BlackLittermanConfig(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-5)    views=("AAPL == 0.05",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-6)    uncertainty_method=ViewUncertaintyMethod.EMPIRICAL_TRACK_RECORD,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-7))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-8)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-9)# Option A: supply view/return history, let the factory calibrate omega
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-10)prior = build_black_litterman(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-11)    cfg,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-12)    view_history=view_history_df,     # shape (n_dates, n_views)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-13)    return_history=return_history_df,  # same shape
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-14))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-15)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-16)# Option B: supply a pre-computed omega directly
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-17)omega = np.diag([1e-4])
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-18)prior = build_black_litterman(cfg, omega=omega)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-19)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-7-20)prior.fit(returns)

```

#### Factor Model Variant[¶](https://silviobaratto.github.io/optimizer/guide/views/#factor-model-variant "Permanent link")
When using BL inside a `FactorModel`, views must reference **factor names** (not asset names):

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-1)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-2)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-3)asset_returns = prices_to_returns(asset_prices)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-4)factor_returns = prices_to_returns(factor_prices)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-6)cfg = BlackLittermanConfig.for_factor_model(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-7)    views=("MTUM == 0.05", "QUAL == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-8))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-9)prior = build_black_litterman(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-8-10)prior.fit(asset_returns, y=factor_returns)

```

#### Composing with MeanRisk[¶](https://silviobaratto.github.io/optimizer/guide/views/#composing-with-meanrisk "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-1)from skfolio.optimization import MeanRisk
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-2)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-3)cfg = BlackLittermanConfig.for_equilibrium(views=("AAPL == 0.05",))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-4)prior = build_black_litterman(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-6)model = MeanRisk(prior_estimator=prior)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-7)model.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-9-8)portfolio = model.predict(returns)

```

* * *
## 2. Entropy Pooling[¶](https://silviobaratto.github.io/optimizer/guide/views/#2-entropy-pooling "Permanent link")
Entropy Pooling (Meucci, 2008) is a non-parametric framework that finds the probability distribution closest to an empirical prior (in the Kullback-Leibler divergence sense) subject to moment constraints derived from investor views.
### Mathematical Formulation[¶](https://silviobaratto.github.io/optimizer/guide/views/#mathematical-formulation "Permanent link")
Given a prior probability vector 
subject to:
where 
This approach is strictly more general than Black-Litterman: it supports views on any distributional moment, not just expected returns.
### Supported View Types[¶](https://silviobaratto.github.io/optimizer/guide/views/#supported-view-types "Permanent link")  
| View Type  | Config Field  | Example  | Description  |  
| --- | --- | --- | --- |  
| Mean equality  | `mean_views`  | `"AAPL == 0.05"`  | Expected return equals 5%  |  
| Mean inequality  | `mean_inequality_views`  | `"AAPL >= 0.03"`  | Expected return at least 3%  |  
| Variance  | `variance_views`  | `"AAPL == 0.04"`  | Variance equals 0.04  |  
| Correlation  | `correlation_views`  | `"(AAPL, JPM) == 0.5"`  | Pairwise correlation equals 0.5  |  
| Skewness  | `skew_views`  | `"AAPL == -0.5"`  | Skewness equals -0.5  |  
| Kurtosis  | `kurtosis_views`  | `"AAPL == 5.0"`  | Kurtosis equals 5.0  |  
| CVaR  | `cvar_views`  | `"AAPL <= -0.05"`  | CVaR at `cvar_beta` level  |  
| Relative mean  | `relative_mean_views`  | `("AAPL", 0.01)`  | Shift mean by +1% from prior  |  
| Relative variance  | `relative_variance_views`  | `("AAPL", 2.0)`  | Scale variance by 2x from prior  |  
**Note on correlation view syntax** : In the config, correlation views use parenthesised pairs: `"(AAPL, JPM) == 0.5"`. In skfolio, these are passed with semicolon separators: `"AAPL; JPM == 0.5"`. The factory handles this conversion.
**Note on inequality operators** : Both `mean_views` (equality, `==`) and `mean_inequality_views` (inequality, `>=` / `<=`) are merged into a single list before being passed to skfolio's `EntropyPooling`, which handles all three operators.
### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/views/#configuration_1 "Permanent link")
`EntropyPoolingConfig` is a frozen dataclass:  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `mean_views`  | `tuple[str, ...] \| None`  | `None`  | Mean equality view expressions  |  
| `mean_inequality_views`  | `tuple[str, ...] \| None`  | `None`  | Mean inequality view expressions  |  
| `variance_views`  | `tuple[str, ...] \| None`  | `None`  | Variance view expressions  |  
| `relative_mean_views`  | `tuple[tuple[str, float], ...] \| None`  | `None`  | Relative mean shifts from prior  |  
| `relative_variance_views`  | `tuple[tuple[str, float], ...] \| None`  | `None`  | Relative variance multipliers from prior  |  
| `correlation_views`  | `tuple[str, ...] \| None`  | `None`  | Correlation view expressions  |  
| `skew_views`  | `tuple[str, ...] \| None`  | `None`  | Skewness view expressions  |  
| `kurtosis_views`  | `tuple[str, ...] \| None`  | `None`  | Kurtosis view expressions  |  
| `cvar_views`  | `tuple[str, ...] \| None`  | `None`  | CVaR view expressions  |  
| `cvar_beta`  | `float`  | `0.95`  | Confidence level for CVaR views  |  
| `groups`  | `dict[str, list[str]] \| None`  | `None`  | Asset group mapping  |  
| `solver`  | `str`  | `"TNC"`  | Scipy solver for the dual optimisation  |  
| `solver_params`  | `dict[str, object] \| None`  | `None`  | Additional solver parameters  |  
| `prior_config`  | `MomentEstimationConfig \| None`  | `None`  | Inner prior; defaults to `EmpiricalPrior()`  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/views/#presets_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-1)# Mean-only views
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-2)cfg = EntropyPoolingConfig.for_mean_views(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-3)    mean_views=("AAPL == 0.05", "JPM == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-6)# Stress testing with variance and correlation views
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-7)cfg = EntropyPoolingConfig.for_stress_test(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-8)    variance_views=("AAPL == 0.04",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-9)    correlation_views=("(AAPL, JPM) == 0.5",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-10))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-11)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-12)# Group-relative views
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-13)cfg = EntropyPoolingConfig.for_group_views(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-14)    mean_views=("tech == 0.05",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-15)    groups={"tech": ["AAPL", "MSFT", "GOOGL"]},
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-10-16))

```

### Factory Function[¶](https://silviobaratto.github.io/optimizer/guide/views/#factory-function_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-11-1)def build_entropy_pooling(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-11-2)    config: EntropyPoolingConfig,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-11-3)    prior_moments: tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]] | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-11-4)    asset_names: list[str] | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-11-5)) -> EntropyPooling:

```

**Parameters** :
  * `config` -- the `EntropyPoolingConfig` instance
  * `prior_moments` -- `(mu, cov)` arrays from a fitted prior; required when `relative_mean_views` or `relative_variance_views` are set
  * `asset_names` -- asset names corresponding to rows/columns of `prior_moments`; required together with `prior_moments`


**Returns** : an `EntropyPooling` instance.
**Raises** : `ConfigurationError` if relative views are specified without providing `prior_moments` and `asset_names`.
### Examples[¶](https://silviobaratto.github.io/optimizer/guide/views/#examples_1 "Permanent link")
#### Mean Equality and Inequality Views[¶](https://silviobaratto.github.io/optimizer/guide/views/#mean-equality-and-inequality-views "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-1)from optimizer.views import EntropyPoolingConfig, build_entropy_pooling
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-2)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-3)cfg = EntropyPoolingConfig(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-4)    mean_views=("AAPL == 0.05",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-5)    mean_inequality_views=("JPM >= 0.02",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-6))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-7)prior = build_entropy_pooling(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-12-8)prior.fit(returns)

```

Both equality and inequality mean views are merged into a single list internally.
#### Higher-Moment Views[¶](https://silviobaratto.github.io/optimizer/guide/views/#higher-moment-views "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-1)cfg = EntropyPoolingConfig(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-2)    skew_views=("AAPL == -0.5",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-3)    kurtosis_views=("AAPL == 5.0",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-4)    cvar_views=("AAPL <= -0.05",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-5)    cvar_beta=0.99,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-6))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-7)prior = build_entropy_pooling(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-13-8)prior.fit(returns)

```

#### Relative Views[¶](https://silviobaratto.github.io/optimizer/guide/views/#relative-views "Permanent link")
Relative views express shifts from the fitted prior rather than absolute targets. This requires passing the fitted prior moments:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-1)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-2)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-3)# Fit a prior first to obtain moments
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-4)from skfolio.prior import EmpiricalPrior
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-5)base_prior = EmpiricalPrior()
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-6)base_prior.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-7)mu = base_prior.return_distribution_.mu
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-8)cov = base_prior.return_distribution_.covariance
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-9)asset_names = list(returns.columns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-10)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-11)# Relative mean: shift AAPL's expected return up by 1%
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-12)# Relative variance: double MSFT's variance
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-13)cfg = EntropyPoolingConfig(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-14)    relative_mean_views=(("AAPL", 0.01),),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-15)    relative_variance_views=(("MSFT", 2.0),),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-16))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-17)prior = build_entropy_pooling(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-18)    cfg,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-19)    prior_moments=(mu, cov),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-20)    asset_names=asset_names,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-21))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-14-22)prior.fit(returns)

```

Internally, relative mean views are converted to absolute views by adding the shift to the prior mean: `AAPL == {mu[i] + 0.01}`. Relative variance views multiply the prior diagonal variance: `MSFT == {cov[j,j] * 2.0}`.
#### Stress Testing[¶](https://silviobaratto.github.io/optimizer/guide/views/#stress-testing "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-1)cfg = EntropyPoolingConfig.for_stress_test(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-2)    variance_views=("AAPL == 0.04", "JPM == 0.06"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-3)    correlation_views=("(AAPL, JPM) == 0.8",),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-5)prior = build_entropy_pooling(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-15-6)prior.fit(returns)

```

* * *
## 3. Opinion Pooling[¶](https://silviobaratto.github.io/optimizer/guide/views/#3-opinion-pooling "Permanent link")
Opinion Pooling combines forecasts from multiple expert prior estimators into a single posterior distribution. Each expert independently produces a return distribution, and the pooling operator aggregates them.
### Pooling Methods[¶](https://silviobaratto.github.io/optimizer/guide/views/#pooling-methods "Permanent link")
**Linear (arithmetic) pooling** :
**Logarithmic (geometric) pooling** :
where `opinion_probabilities`) and 
### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/views/#configuration_2 "Permanent link")
`OpinionPoolingConfig` is a frozen dataclass:  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `opinion_probabilities`  | `tuple[float, ...] \| None`  | `None`  | Per-expert weights; each in   |  
| `is_linear_pooling`  | `bool`  | `True`  |  `True` for linear pooling, `False` for logarithmic  |  
| `divergence_penalty`  | `float`  | `0.0`  | KL-divergence penalty for robust pooling  |  
| `n_jobs`  | `int \| None`  | `None`  | Number of parallel jobs for expert fitting  |  
| `prior_config`  | `MomentEstimationConfig \| None`  | `None`  | Common prior configuration  |  
**Validation** : - Each probability must be in `opinion_probabilities` must be at most 1.0 (with numerical tolerance of `opinion_probabilities=None` gives equal weight to all experts.
### Factory Function[¶](https://silviobaratto.github.io/optimizer/guide/views/#factory-function_2 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-16-1)def build_opinion_pooling(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-16-2)    estimators: Sequence[tuple[str, BasePrior]],
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-16-3)    config: OpinionPoolingConfig | None = None,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-16-4)) -> OpinionPooling:

```

**Parameters** :
  * `estimators` -- named expert prior estimators as a sequence of `(name, estimator)` tuples. These are passed directly because estimator objects are not serialisable in a frozen dataclass.
  * `config` -- optional `OpinionPoolingConfig`; defaults to `OpinionPoolingConfig()` (linear pooling, equal weights, no penalty).


**Returns** : an `OpinionPooling` instance.
### Examples[¶](https://silviobaratto.github.io/optimizer/guide/views/#examples_2 "Permanent link")
#### Combining Expert Forecasts[¶](https://silviobaratto.github.io/optimizer/guide/views/#combining-expert-forecasts "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-1)from skfolio.prior import EntropyPooling
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-2)from optimizer.views import OpinionPoolingConfig, build_opinion_pooling
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-3)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-4)expert_1 = EntropyPooling(mean_views=["AAPL == 0.05"])
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-5)expert_2 = EntropyPooling(mean_views=["JPM == 0.03"])
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-6)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-7)estimators = [
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-8)    ("fundamental_analyst", expert_1),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-9)    ("quant_model", expert_2),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-10)]
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-11)cfg = OpinionPoolingConfig(opinion_probabilities=(0.6, 0.4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-12)prior = build_opinion_pooling(estimators, cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-17-13)prior.fit(returns)

```

#### Logarithmic Pooling[¶](https://silviobaratto.github.io/optimizer/guide/views/#logarithmic-pooling "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-18-1)cfg = OpinionPoolingConfig(is_linear_pooling=False)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-18-2)prior = build_opinion_pooling(estimators, cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-18-3)prior.fit(returns)

```

#### Anchoring to a Base Prior[¶](https://silviobaratto.github.io/optimizer/guide/views/#anchoring-to-a-base-prior "Permanent link")
When expert weights are small, the posterior is anchored to the common prior. This is useful for blending mild expert views with a strong empirical baseline:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-19-1)cfg = OpinionPoolingConfig(opinion_probabilities=(0.01, 0.01))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-19-2)prior = build_opinion_pooling(estimators, cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-19-3)prior.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-19-4)# Posterior will be very close to the empirical prior

```

* * *
## 4. Omega Calibration from Track Record[¶](https://silviobaratto.github.io/optimizer/guide/views/#4-omega-calibration-from-track-record "Permanent link")
The `calibrate_omega_from_track_record()` function computes an empirical diagonal 
### Formula[¶](https://silviobaratto.github.io/optimizer/guide/views/#formula "Permanent link")
For each view 
where `ddof=1`).
### Function Signature[¶](https://silviobaratto.github.io/optimizer/guide/views/#function-signature "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-20-1)def calibrate_omega_from_track_record(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-20-2)    view_history: pd.DataFrame,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-20-3)    return_history: pd.DataFrame,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-20-4)) -> npt.NDArray[np.float64]:

```

**Parameters** :
  * `view_history` -- DataFrame of shape `(n_dates, n_views)` with historical forecasted 
  * `return_history` -- DataFrame of same shape with realised returns aligned to each view


**Returns** : diagonal `(n_views, n_views)`.
**Raises** : `DataError` if: - The two DataFrames have different shapes - The column names do not match - Fewer than 5 aligned observations remain after dropping NaN rows
### Example[¶](https://silviobaratto.github.io/optimizer/guide/views/#example "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-3)from optimizer.views import calibrate_omega_from_track_record
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-4)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-5)# view_history: 30 dates, 2 views
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-6)view_history = pd.DataFrame({
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-7)    "view_aapl": np.random.normal(0.001, 0.005, 30),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-8)    "view_jpm": np.random.normal(0.002, 0.003, 30),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-9)})
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-10)return_history = pd.DataFrame({
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-11)    "view_aapl": np.random.normal(0.001, 0.02, 30),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-12)    "view_jpm": np.random.normal(0.002, 0.015, 30),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-13)})
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-14)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-15)omega = calibrate_omega_from_track_record(view_history, return_history)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-16)# omega is a (2, 2) diagonal matrix
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-21-17)print(omega)

```

This `build_black_litterman()`:

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-22-1)cfg = BlackLittermanConfig(
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-22-2)    views=("AAPL == 0.05", "JPM == 0.03"),
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-22-3)    uncertainty_method=ViewUncertaintyMethod.EMPIRICAL_TRACK_RECORD,
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-22-4))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-22-5)prior = build_black_litterman(cfg, omega=omega)

```

* * *
## Gotchas and Common Pitfalls[¶](https://silviobaratto.github.io/optimizer/guide/views/#gotchas-and-common-pitfalls "Permanent link")
### Factor Model Views Must Reference Factor Names[¶](https://silviobaratto.github.io/optimizer/guide/views/#factor-model-views-must-reference-factor-names "Permanent link")
When `use_factor_model=True`, the BL prior is wrapped in a `FactorModel`. In this case, views must reference **factor names** (e.g., `"MTUM"`, `"QUAL"`), not asset names. Using asset names will cause a fitting error because the picking matrix is constructed over the factor return space.

```
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-1)# CORRECT: views reference factor names
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-2)cfg = BlackLittermanConfig.for_factor_model(views=("MTUM == 0.05",))
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-3)prior = build_black_litterman(cfg)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-4)prior.fit(asset_returns, y=factor_returns)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-5)
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-6)# WRONG: views reference asset names inside a FactorModel
[](https://silviobaratto.github.io/optimizer/guide/views/#__codelineno-23-7)cfg = BlackLittermanConfig.for_factor_model(views=("AAPL == 0.05",))

```

### Tau Must Be Strictly Positive[¶](https://silviobaratto.github.io/optimizer/guide/views/#tau-must-be-strictly-positive "Permanent link")
The uncertainty scaling parameter `tau=0.0` or a negative value raises `ValueError` at config creation time. Typical values range from 0.01 to 0.10; the default is 0.05.
### Relative Views Require Prior Moments[¶](https://silviobaratto.github.io/optimizer/guide/views/#relative-views-require-prior-moments "Permanent link")
When using `relative_mean_views` or `relative_variance_views` in `EntropyPoolingConfig`, you must supply `prior_moments` and `asset_names` to `build_entropy_pooling()`. Without them, the factory raises `ConfigurationError`.
### Empirical Track Record Requires History or Pre-Computed Omega[¶](https://silviobaratto.github.io/optimizer/guide/views/#empirical-track-record-requires-history-or-pre-computed-omega "Permanent link")
When `uncertainty_method=EMPIRICAL_TRACK_RECORD`, one of the following must hold:
  1. Both `view_history` and `return_history` are supplied (at least 5 aligned non-NaN observations).
  2. A pre-computed `omega` array is supplied directly.


Supplying neither raises `ConfigurationError`.
### Opinion Probabilities Must Sum to At Most 1.0[¶](https://silviobaratto.github.io/optimizer/guide/views/#opinion-probabilities-must-sum-to-at-most-10 "Permanent link")
The `opinion_probabilities` tuple in `OpinionPoolingConfig` is validated:
  * Each value must be in 
  * The sum must not exceed 1.0.


Violating either constraint raises `ValueError`.
### Estimators Are Not Stored in OpinionPoolingConfig[¶](https://silviobaratto.github.io/optimizer/guide/views/#estimators-are-not-stored-in-opinionpoolingconfig "Permanent link")
Because skfolio estimator objects are not serialisable in a frozen dataclass, expert estimators for Opinion Pooling are passed as a factory argument, not stored in the config. This preserves the config-is-serialisable invariant.
### Config Tuples vs. skfolio Lists[¶](https://silviobaratto.github.io/optimizer/guide/views/#config-tuples-vs-skfolio-lists "Permanent link")
All view fields in configs use `tuple` types for hashability (required by frozen dataclasses). The factory functions convert these to `list` before passing to skfolio. You do not need to handle this conversion manually.
### Mean Equality and Inequality Views Are Merged[¶](https://silviobaratto.github.io/optimizer/guide/views/#mean-equality-and-inequality-views-are-merged "Permanent link")
`EntropyPoolingConfig` has separate fields for `mean_views` (equality, `==`) and `mean_inequality_views` (inequality, `>=` / `<=`). The factory merges both into a single list for skfolio's `EntropyPooling.mean_views` parameter, which handles all three operators natively.
* * *
## Choosing a Framework[¶](https://silviobaratto.github.io/optimizer/guide/views/#choosing-a-framework "Permanent link")  
| Criterion  | Black-Litterman  | Entropy Pooling  | Opinion Pooling  |  
| --- | --- | --- | --- |  
| View types  | Mean (absolute/relative)  | Mean, variance, correlation, skew, kurtosis, CVaR  | Any (via expert estimators)  |  
| Equilibrium anchor  | Yes (built-in)  | No (empirical prior)  | Configurable  |  
| Factor model support  | Yes (`use_factor_model`)  | No  | No  |  
| Closed-form solution  | Yes  | No (numerical optimisation)  | No  |  
| Number of experts  | Single analyst  | Single analyst  | Multiple experts  |  
| Computational cost  | Low  | Medium  | Depends on experts  |  
**Use Black-Litterman** when you have return views and want to tilt away from an equilibrium baseline, especially if you want closed-form updates and factor model integration.
**Use Entropy Pooling** when you have views on distributional moments beyond the mean (variance, correlation, tail risk) or need inequality constraints.
**Use Opinion Pooling** when you want to combine multiple independent expert forecasts (each represented as a prior estimator) into a single distribution.
