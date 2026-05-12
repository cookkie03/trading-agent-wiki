<!-- source: https://silviobaratto.github.io/optimizer/api/scoring/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/scoring/#scoring)
# scoring[¶](https://silviobaratto.github.io/optimizer/api/scoring/#scoring "Permanent link")
###  `optimizer.scoring` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring "Permanent link")
Performance scoring for model selection and hyperparameter tuning.
Wraps skfolio ratio measures and custom scoring functions into callables compatible with sklearn cross-validation.
####  `ScorerConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig "Permanent link")
Immutable configuration for building a scoring function.
When `ratio_measure` is set, the scorer evaluates portfolios using the corresponding built-in ratio measure (Sharpe, Sortino, Calmar, etc.). When `ratio_measure` is `None`, a custom callable must be passed to the factory function.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig--parameters "Permanent link")
ratio_measure : RatioMeasureType or None Built-in ratio measure. `None` indicates a custom scorer. greater_is_better : bool or None Whether higher scores are better. `None` auto-detects from the ratio measure. risk_free_rate : float Daily risk-free rate used for ratio computation. Defaults to 0.0 for backward compatibility.
#####  `for_sharpe()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_sharpe "Permanent link")
Sharpe ratio scorer.
#####  `for_sortino()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_sortino "Permanent link")
Sortino ratio scorer.
#####  `for_calmar()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_calmar "Permanent link")
Calmar ratio scorer.
#####  `for_cvar_ratio()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_cvar_ratio "Permanent link")
CVaR ratio scorer.
#####  `for_information_ratio()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_information_ratio "Permanent link")
Information Ratio scorer (active return / tracking error).
Requires `benchmark_returns` to be passed to :func:`~optimizer.scoring.build_scorer`.
#####  `for_sharpe_with_rf(rf_daily)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_sharpe_with_rf "Permanent link")
Sharpe ratio scorer with explicit daily risk-free rate.
#####  `for_custom()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.ScorerConfig.for_custom "Permanent link")
Custom scoring function (callable passed to factory).
####  `build_scorer(config=None, *, score_func=None, benchmark_returns=None)` [¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.build_scorer "Permanent link")
Build a scoring callable compatible with sklearn cross-validation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.build_scorer--parameters "Permanent link")
config : ScorerConfig or None Scorer configuration. Defaults to `ScorerConfig()` (Sharpe ratio). score_func : callable or None Custom scoring function that accepts a portfolio and returns a scalar. Required when `config.ratio_measure` is `None`. benchmark_returns : pd.Series or None Full benchmark return series indexed by date. Required when `config.ratio_measure` is `RatioMeasureType.INFORMATION_RATIO`; ignored otherwise.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.build_scorer--returns "Permanent link")
callable A scorer callable compatible with `GridSearchCV` and `RandomizedSearchCV`.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/scoring/#optimizer.scoring.build_scorer--raises "Permanent link")
ValueError If `config.ratio_measure` is `None` and no `score_func` is provided. ValueError If `config.ratio_measure` is `RatioMeasureType.INFORMATION_RATIO` and `benchmark_returns` is `None`.
