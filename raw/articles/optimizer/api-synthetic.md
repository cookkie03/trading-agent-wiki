<!-- source: https://silviobaratto.github.io/optimizer/api/synthetic/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/synthetic/#synthetic)
# synthetic[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#synthetic "Permanent link")
###  `optimizer.synthetic` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic "Permanent link")
Synthetic data generation and vine copula models.
####  `DependenceMethodType` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.DependenceMethodType "Permanent link")
Bases: `str`, `Enum`
Dependence method for vine copula tree construction.
Maps to :class:`skfolio.distribution.DependenceMethod`.
####  `SelectionCriterionType` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.SelectionCriterionType "Permanent link")
Bases: `str`, `Enum`
Information criterion for copula family selection.
Maps to :class:`skfolio.distribution.SelectionCriterion`.
####  `SyntheticDataConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.SyntheticDataConfig "Permanent link")
Immutable configuration for :class:`skfolio.prior.SyntheticData`.
Generates synthetic return scenarios from a fitted distribution model (typically a vine copula). Supports conditional stress testing via the `sample_args` factory parameter.
Non-serialisable objects (`distribution_estimator`, `sample_args`) are passed as keyword arguments to the factory function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.SyntheticDataConfig--parameters "Permanent link")
n_samples : int Number of synthetic scenarios to generate. vine_copula_config : VineCopulaConfig or None Configuration for building a `VineCopula` distribution estimator. Ignored when `distribution_estimator` is passed to the factory directly.
#####  `for_scenario_generation(n_samples=10000)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.SyntheticDataConfig.for_scenario_generation "Permanent link")
Large-sample scenario generation with default vine copula.
#####  `for_stress_test(n_samples=10000)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.SyntheticDataConfig.for_stress_test "Permanent link")
Stress-test configuration (conditioning dict passed to factory).
Uses BIC for copula selection (penalises complexity more than AIC) and deeper vine trees (`max_depth=6`) to capture tail dependence.
####  `VineCopulaConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.VineCopulaConfig "Permanent link")
Immutable configuration for :class:`skfolio.distribution.VineCopula`.
Vine copulas decompose a multivariate distribution into marginal distributions and bivariate copulas organised in a tree structure.
Non-serialisable objects (`marginal_candidates`, `copula_candidates`, `central_assets`) are passed as keyword arguments to the factory function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.VineCopulaConfig--parameters "Permanent link")
fit_marginals : bool Whether to fit univariate marginals. max_depth : int Maximum depth of the vine tree. log_transform : bool Whether to apply log transformation. dependence_method : DependenceMethodType Method for measuring pairwise dependence when building the vine structure. selection_criterion : SelectionCriterionType Information criterion for selecting copula families. independence_level : float Significance level for independence testing. n_jobs : int or None Number of parallel jobs. random_state : int or None Random state for reproducibility.
####  `build_synthetic_data(config=None, *, distribution_estimator=None, sample_args=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_synthetic_data "Permanent link")
Build a skfolio :class:`SyntheticData` prior from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_synthetic_data--parameters "Permanent link")
config : SyntheticDataConfig or None Synthetic data configuration. Defaults to `SyntheticDataConfig()`. distribution_estimator : VineCopula or None Pre-built distribution estimator. When `None`, one is built from `config.vine_copula_config` (or skfolio default). sample_args : dict or None Arguments passed to the distribution's `sample` method. Use `{"conditioning": {"AAPL": -0.10}}` for conditional stress testing. **kwargs Additional keyword arguments forwarded to the :class:`SyntheticData` constructor.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_synthetic_data--returns "Permanent link")
SyntheticData A fitted-ready skfolio prior estimator generating synthetic return scenarios.
####  `build_vine_copula(config=None, **kwargs)` [¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_vine_copula "Permanent link")
Build a skfolio :class:`VineCopula` from _config_.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_vine_copula--parameters "Permanent link")
config : VineCopulaConfig or None Vine copula configuration. Defaults to `VineCopulaConfig()`. **kwargs Additional keyword arguments forwarded to the :class:`VineCopula` constructor (for non-serialisable parameters such as `marginal_candidates`, `copula_candidates`, `central_assets`).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/synthetic/#optimizer.synthetic.build_vine_copula--returns "Permanent link")
VineCopula A fitted-ready skfolio vine copula estimator.
