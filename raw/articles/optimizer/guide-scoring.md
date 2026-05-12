<!-- source: https://silviobaratto.github.io/optimizer/guide/scoring/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/scoring/#scoring)
# Scoring[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#scoring "Permanent link")
The scoring module wraps skfolio ratio measures and custom scoring functions into callables compatible with sklearn cross-validation and hyperparameter tuning. It provides a consistent interface for evaluating portfolio performance during model selection.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#overview "Permanent link")
When using `GridSearchCV` or `RandomizedSearchCV` with portfolio optimizers, you need a scoring function that evaluates the quality of each portfolio. The scoring module maps ratio measure names to sklearn-compatible scorer callables via the frozen-config + factory pattern.
## ScorerConfig[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#scorerconfig "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-1)from optimizer.scoring import ScorerConfig
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-2)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-3)config = ScorerConfig(
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-4)    ratio_measure=RatioMeasureType.SHARPE_RATIO,
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-5)    greater_is_better=None,  # auto-detected from measure
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-0-6))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `ratio_measure`  |  `RatioMeasureType` or `None`  | `SHARPE_RATIO`  | Built-in ratio measure; `None` for custom scorer  |  
| `greater_is_better`  |  `bool` or `None`  | `None`  | Whether higher scores are better; auto-detected when `None`  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#presets "Permanent link")  
| Preset  | Ratio Measure  | Use Case  |  
| --- | --- | --- |  
| `ScorerConfig.for_sharpe()`  | Sharpe Ratio  | General-purpose risk-adjusted return  |  
| `ScorerConfig.for_sortino()`  | Sortino Ratio  | Downside-risk-focused evaluation  |  
| `ScorerConfig.for_calmar()`  | Calmar Ratio  | Drawdown-focused evaluation  |  
| `ScorerConfig.for_cvar_ratio()`  | CVaR Ratio  | Tail-risk-focused evaluation  |  
| `ScorerConfig.for_information_ratio()`  | Information Ratio  | Active return vs benchmark  |  
| `ScorerConfig.for_custom()`  | `None`  | Custom callable passed to factory  |  
## Available Ratio Measures[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#available-ratio-measures "Permanent link")
All 19 ratio measures available in `RatioMeasureType`:  
| Measure  | Description  |  
| --- | --- |  
| `SHARPE_RATIO`  | Excess return / standard deviation  |  
| `ANNUALIZED_SHARPE_RATIO`  | Annualized Sharpe ratio  |  
| `SORTINO_RATIO`  | Excess return / downside deviation  |  
| `ANNUALIZED_SORTINO_RATIO`  | Annualized Sortino ratio  |  
| `MEAN_ABSOLUTE_DEVIATION_RATIO`  | Return / mean absolute deviation  |  
| `FIRST_LOWER_PARTIAL_MOMENT_RATIO`  | Return / first lower partial moment  |  
| `VALUE_AT_RISK_RATIO`  | Return / VaR  |  
| `CVAR_RATIO`  | Return / CVaR  |  
| `ENTROPIC_RISK_MEASURE_RATIO`  | Return / entropic risk  |  
| `EVAR_RATIO`  | Return / EVaR  |  
| `WORST_REALIZATION_RATIO`  | Return / worst realization  |  
| `DRAWDOWN_AT_RISK_RATIO`  | Return / drawdown-at-risk  |  
| `CDAR_RATIO`  | Return / CDaR  |  
| `CALMAR_RATIO`  | Return / max drawdown  |  
| `AVERAGE_DRAWDOWN_RATIO`  | Return / average drawdown  |  
| `EDAR_RATIO`  | Return / EDaR  |  
| `ULCER_INDEX_RATIO`  | Return / ulcer index  |  
| `GINI_MEAN_DIFFERENCE_RATIO`  | Return / Gini mean difference  |  
| `INFORMATION_RATIO`  | Active return / tracking error (custom)  |  
## Building Scorers[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#building-scorers "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-1)from optimizer.scoring import ScorerConfig, build_scorer
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-3)# Built-in ratio measure
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-4)scorer = build_scorer(ScorerConfig.for_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-5)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-6)# Information ratio (requires benchmark)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-7)scorer = build_scorer(
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-8)    ScorerConfig.for_information_ratio(),
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-9)    benchmark_returns=benchmark_returns,
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-10))
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-11)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-12)# Custom scoring function
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-13)def my_scorer(portfolio):
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-14)    return portfolio.annualized_mean / portfolio.max_drawdown
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-15)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-1-16)scorer = build_scorer(ScorerConfig.for_custom(), custom_func=my_scorer)

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#code-examples "Permanent link")
### Using with hyperparameter tuning[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#using-with-hyperparameter-tuning "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-1)from optimizer.scoring import ScorerConfig
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-2)from optimizer.tuning import GridSearchConfig
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-3)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-4)# Grid search scored by Sortino ratio
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-5)tuning_config = GridSearchConfig(
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-6)    scorer_config=ScorerConfig.for_sortino(),
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-7)    n_jobs=-1,
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-2-8))

```

### Using with cross-validation[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#using-with-cross-validation "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-3-1)from optimizer.scoring import ScorerConfig, build_scorer
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-3-2)from optimizer.validation import WalkForwardConfig, run_cross_val
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-3-3)
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-3-4)scorer = build_scorer(ScorerConfig.for_calmar())
[](https://silviobaratto.github.io/optimizer/guide/scoring/#__codelineno-3-5)# scorer is a callable compatible with sklearn CV

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#gotchas-and-tips "Permanent link")
Information Ratio requires benchmark
The `INFORMATION_RATIO` is not a native skfolio ratio measure — it is implemented as a custom scorer (active return / tracking error). You must pass `benchmark_returns` to `build_scorer()`.
Scorer sign convention
All built-in ratio measures follow the sklearn convention where `greater_is_better=True`. The scorer returns positive values for good portfolios and the search maximizes the score.
Default scorer
When no `ScorerConfig` is provided to tuning, the default is Sharpe ratio — a reasonable choice for most equity portfolio strategies.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/scoring/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Sharpe scorer  | `build_scorer(ScorerConfig.for_sharpe())`  |  
| Sortino scorer  | `build_scorer(ScorerConfig.for_sortino())`  |  
| Calmar scorer  | `build_scorer(ScorerConfig.for_calmar())`  |  
| CVaR ratio scorer  | `build_scorer(ScorerConfig.for_cvar_ratio())`  |  
| Information ratio  | `build_scorer(ScorerConfig.for_information_ratio(), benchmark_returns=bm)`  |  
| Custom scorer  | `build_scorer(ScorerConfig.for_custom(), custom_func=fn)`  |
