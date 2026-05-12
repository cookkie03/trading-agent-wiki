<!-- source: https://silviobaratto.github.io/optimizer/guide/synthetic/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/synthetic/#synthetic-data)
# Synthetic Data[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#synthetic-data "Permanent link")
The synthetic module generates synthetic return scenarios using vine copula models. It enables scenario generation for portfolio stress testing, Monte Carlo simulation, and conditional what-if analysis by modeling the full joint distribution of asset returns including tail dependencies.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#overview "Permanent link")
Traditional mean-variance optimization assumes normally distributed returns, which underestimates the probability of extreme co-movements. Vine copulas address this by decomposing the multivariate return distribution into:
  1. **Marginal distributions** — fitted independently per asset (capturing skewness, kurtosis)
  2. **Bivariate copulas** — capturing pairwise dependence structure (including tail dependence)


The copulas are organized in a vine (tree) structure that efficiently represents high-dimensional dependencies. The resulting model can generate synthetic scenarios that preserve the empirical dependence structure, including fat tails and asymmetric tail dependence.
## Vine Copula Configuration[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#vine-copula-configuration "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-1)from optimizer.synthetic import VineCopulaConfig
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-2)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-3)config = VineCopulaConfig(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-4)    fit_marginals=True,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-5)    max_depth=4,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-6)    log_transform=False,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-7)    dependence_method=DependenceMethodType.KENDALL_TAU,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-8)    selection_criterion=SelectionCriterionType.AIC,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-9)    independence_level=0.05,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-10)    n_jobs=None,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-11)    random_state=None,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-0-12))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `fit_marginals`  | `bool`  | `True`  | Whether to fit univariate marginal distributions  |  
| `max_depth`  | `int`  | 4  | Maximum depth of the vine tree structure  |  
| `log_transform`  | `bool`  | `False`  | Apply log transformation before fitting  |  
| `dependence_method`  | `DependenceMethodType`  | `KENDALL_TAU`  | Pairwise dependence measure for tree construction  |  
| `selection_criterion`  | `SelectionCriterionType`  | `AIC`  | Information criterion for copula family selection  |  
| `independence_level`  | `float`  | 0.05  | Significance level for independence testing  |  
| `n_jobs`  |  `int` or `None`  | `None`  | Number of parallel jobs  |  
| `random_state`  |  `int` or `None`  | `None`  | Seed for reproducibility  |  
### Dependence Methods[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#dependence-methods "Permanent link")  
| Method  | Description  |  
| --- | --- |  
| `KENDALL_TAU`  | Rank-based concordance measure; robust to outliers  |  
| `MUTUAL_INFORMATION`  | Information-theoretic dependence; captures nonlinear relationships  |  
| `WASSERSTEIN_DISTANCE`  | Optimal transport distance between marginals  |  
### Selection Criteria[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#selection-criteria "Permanent link")  
| Criterion  | Description  |  
| --- | --- |  
| `AIC`  | Akaike Information Criterion — balances fit and complexity  |  
| `BIC`  | Bayesian Information Criterion — penalizes complexity more than AIC  |  
## Synthetic Data Configuration[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#synthetic-data-configuration "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-1)from optimizer.synthetic import SyntheticDataConfig
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-3)config = SyntheticDataConfig(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-4)    n_samples=1_000,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-5)    vine_copula_config=VineCopulaConfig(),
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-1-6))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `n_samples`  | `int`  | 1,000  | Number of synthetic scenarios to generate  |  
| `vine_copula_config`  |  `VineCopulaConfig` or `None`  | `None`  | Vine copula configuration; ignored when `distribution_estimator` is passed directly  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#presets "Permanent link")  
| Preset  | n_samples  | Vine Config  | Use Case  |  
| --- | --- | --- | --- |  
| `for_scenario_generation(10_000)`  | 10,000  | Default  | Large-sample Monte Carlo simulation  |  
| `for_stress_test(10_000)`  | 10,000  | BIC + max_depth=6  | Deep tree for tail dependence capture  |  
## Building and Using Synthetic Data[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#building-and-using-synthetic-data "Permanent link")
### Basic scenario generation[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#basic-scenario-generation "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-1)from optimizer.synthetic import SyntheticDataConfig, build_synthetic_data
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-3)config = SyntheticDataConfig.for_scenario_generation(n_samples=10_000)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-4)synthetic_prior = build_synthetic_data(config)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-5)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-6)# Use as prior estimator in optimization
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-7)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-8)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-9)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-10)    MeanRiskConfig.for_max_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-11)    prior_estimator=synthetic_prior,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-12))
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-13)optimizer.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-2-14)portfolio = optimizer.predict(returns)

```

### Stress testing with conditioning[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#stress-testing-with-conditioning "Permanent link")
Conditional sampling generates scenarios where specific assets are fixed at extreme values:

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-1)config = SyntheticDataConfig.for_stress_test(n_samples=10_000)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-2)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-3)# Condition on a market crash: SPY drops 10%
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-4)synthetic_prior = build_synthetic_data(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-5)    config,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-6)    sample_args={"conditioning": {"SPY": -0.10}},
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-7))
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-8)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-9)# Optimize under stress scenario
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-10)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-11)    MeanRiskConfig.for_min_cvar(),
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-12)    prior_estimator=synthetic_prior,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-3-13))

```

### Building just the vine copula[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#building-just-the-vine-copula "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-1)from optimizer.synthetic import VineCopulaConfig, build_vine_copula
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-3)vine = build_vine_copula(VineCopulaConfig(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-4)    max_depth=6,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-5)    selection_criterion=SelectionCriterionType.BIC,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-4-6)))

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#code-examples "Permanent link")
### Scenario-based portfolio optimization[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#scenario-based-portfolio-optimization "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-1)from optimizer.synthetic import SyntheticDataConfig, build_synthetic_data
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-3)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-4)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-5)# Build synthetic prior from historical data
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-6)config = SyntheticDataConfig.for_scenario_generation(n_samples=50_000)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-7)prior = build_synthetic_data(config)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-8)
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-9)# Optimize using synthetic scenarios
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-10)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-11)    MeanRiskConfig.for_min_cvar(beta=0.95),
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-12)    prior_estimator=prior,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-13))
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-5-14)result = run_full_pipeline(prices=prices, optimizer=optimizer)

```

### Stress test: sector crash[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#stress-test-sector-crash "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-1)# What if financials drop 15%?
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-2)prior = build_synthetic_data(
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-3)    SyntheticDataConfig.for_stress_test(),
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-4)    sample_args={"conditioning": {
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-5)        "JPM": -0.15,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-6)        "BAC": -0.15,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-7)        "GS": -0.15,
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-8)    }},
[](https://silviobaratto.github.io/optimizer/guide/synthetic/#__codelineno-6-9))

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#gotchas-and-tips "Permanent link")
Use BIC for stress tests
The `for_stress_test` preset uses BIC instead of AIC for copula selection. BIC penalizes complexity more heavily, producing simpler copula structures that are less likely to overfit — important when extrapolating to tail events.
Deeper trees capture more tail dependence
Increasing `max_depth` allows the vine to model higher-order dependencies between assets. The default (4) is sufficient for most equity portfolios; stress tests benefit from `max_depth=6`.
Computational cost scales with n_samples and assets
Fitting a vine copula to 50+ assets with deep trees can be slow. Use `n_jobs=-1` for parallelism and consider reducing `max_depth` for large universes.
Conditioning dict for stress tests
Pass conditioning values via `sample_args={"conditioning": {"TICKER": value}}` to the factory. The synthetic prior then generates scenarios conditioned on those asset returns being fixed at the specified values.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/synthetic/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Scenario generation  | `SyntheticDataConfig.for_scenario_generation(10_000)`  |  
| Stress test config  | `SyntheticDataConfig.for_stress_test(10_000)`  |  
| Build prior  | `build_synthetic_data(config)`  |  
| Conditional stress  | `build_synthetic_data(config, sample_args={"conditioning": {"SPY": -0.10}})`  |  
| Build vine copula  | `build_vine_copula(VineCopulaConfig())`  |
