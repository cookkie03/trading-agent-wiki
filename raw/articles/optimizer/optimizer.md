<!-- source: https://silviobaratto.github.io/optimizer/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/#portfolio-optimizer)
# Portfolio Optimizer[¶](https://silviobaratto.github.io/optimizer/#portfolio-optimizer "Permanent link")
Quantitative portfolio construction and optimization platform built on [skfolio](https://skfolio.org/) and scikit-learn. Every component follows the frozen-config + factory pattern and composes in standard sklearn pipelines.
## Features[¶](https://silviobaratto.github.io/optimizer/#features "Permanent link")
  * **[Pipeline](https://silviobaratto.github.io/optimizer/guide/pipeline/)** -- End-to-end orchestration from prices to validated, rebalanced weights in a single function call
  * **[Preprocessing](https://silviobaratto.github.io/optimizer/guide/preprocessing/)** -- Data validation, three-group outlier treatment, sector imputation, OLS regression imputation
  * **[Pre-selection](https://silviobaratto.github.io/optimizer/guide/pre-selection/)** -- Asset filtering pipeline: completeness, variance, correlation, dominance, expiry
  * **[Moments](https://silviobaratto.github.io/optimizer/guide/moments/)** -- 5 expected return + 11 covariance estimators with HMM regime blending, DMM, and multi-period scaling
  * **[Views](https://silviobaratto.github.io/optimizer/guide/views/)** -- Black-Litterman, Entropy Pooling (9 view types), Opinion Pooling with omega calibration
  * **[Optimization](https://silviobaratto.github.io/optimizer/guide/optimization/)** -- 10+ models: Mean-Risk, Risk Budgeting, HRP/HERC/NCO, robust ellipsoidal, DR-CVaR, regime-conditional
  * **[Validation](https://silviobaratto.github.io/optimizer/guide/validation/)** -- Walk-Forward, Combinatorial Purged CV, Multiple Randomized CV
  * **[Scoring](https://silviobaratto.github.io/optimizer/guide/scoring/)** -- 19 ratio measures for model selection (Sharpe, Sortino, Calmar, CVaR ratio, ...)
  * **[Tuning](https://silviobaratto.github.io/optimizer/guide/tuning/)** -- Grid and randomized search with temporal CV defaults
  * **[Rebalancing](https://silviobaratto.github.io/optimizer/guide/rebalancing/)** -- Calendar-based, threshold-based, and hybrid rebalancing with turnover/cost utilities
  * **[Factors](https://silviobaratto.github.io/optimizer/guide/factors/)** -- 17 factors across 9 groups: construction, standardization, scoring, selection, regime tilts, validation
  * **[Synthetic Data](https://silviobaratto.github.io/optimizer/guide/synthetic/)** -- Vine copula models for scenario generation and conditional stress testing
  * **[Universe Screening](https://silviobaratto.github.io/optimizer/guide/universe/)** -- 8 investability screens with hysteresis entry/exit thresholds


## Design Principles[¶](https://silviobaratto.github.io/optimizer/#design-principles "Permanent link")
**Config + Factory pattern** : Every module uses frozen `@dataclass` configs that hold only serializable primitives/enums. Factory functions create the actual estimator objects. This separation keeps configs serializable for storage, logging, and hyperparameter sweeps.
**sklearn compatibility** : All transformers follow the `BaseEstimator + TransformerMixin` API and compose in `sklearn.pipeline.Pipeline`. This means the full pre-selection + optimization chain can be cross-validated, tuned, and serialized as a single sklearn object.
**skfolio foundation** : Optimization models wrap [skfolio](https://skfolio.org/) estimators — a mature library for portfolio optimization with the sklearn API. The optimizer library adds regime blending, robust uncertainty sets, factor research, and rebalancing on top.
## Quick Start[¶](https://silviobaratto.github.io/optimizer/#quick-start "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/#__codelineno-0-1)pip install -e ".[dev]"

```


```
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-2)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-3)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-4)
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-5)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-6)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-7)    prices=price_df,
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-8)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-9)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-10))
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-11)
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-12)print(result.weights)          # pd.Series of asset weights
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-13)print(result.summary)          # dict with Sharpe, max drawdown, etc.
[](https://silviobaratto.github.io/optimizer/#__codelineno-1-14)print(result.backtest)         # out-of-sample MultiPeriodPortfolio

```

See the [Quickstart guide](https://silviobaratto.github.io/optimizer/getting-started/quickstart/) for more examples.
## Pipeline Data Flow[¶](https://silviobaratto.github.io/optimizer/#pipeline-data-flow "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/#__codelineno-2-1)prices → returns → [preprocess → pre-select → optimize] → backtest → weights
[](https://silviobaratto.github.io/optimizer/#__codelineno-2-2)                    └──── sklearn Pipeline ────┘

```

The pipeline follows a linear data flow. Prices are converted to returns **outside** the pipeline (semantic change), then everything inside is a single sklearn `Pipeline` that can be cross-validated and tuned.
See the [Pipeline Overview](https://silviobaratto.github.io/optimizer/guide/pipeline/) for architectural details.
