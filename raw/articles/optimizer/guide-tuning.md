<!-- source: https://silviobaratto.github.io/optimizer/guide/tuning/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/tuning/#tuning)
# Tuning[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#tuning "Permanent link")
The tuning module wraps sklearn's `GridSearchCV` and `RandomizedSearchCV` with temporal cross-validation defaults that prevent look-ahead bias. It enforces walk-forward validation by default, ensuring that hyperparameter selection respects the time-series nature of financial data.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#overview "Permanent link")
Hyperparameter tuning for portfolio optimization requires special care: standard k-fold CV would use future returns to select parameters, introducing look-ahead bias. The tuning module addresses this by coupling sklearn's search algorithms with temporal cross-validation from the [validation](https://silviobaratto.github.io/optimizer/guide/validation/) module.
Because the portfolio pipeline is a single sklearn `Pipeline` object, all nested parameters are accessible via the double-underscore `__` notation (e.g., `"optimizer__l2_coef"`, `"drop_correlated__threshold"`).
## Grid Search[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#grid-search "Permanent link")
Exhaustive search over a specified parameter grid with temporal CV.
### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#configuration "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-1)from optimizer.tuning import GridSearchConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-2)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-3)from optimizer.scoring import ScorerConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-4)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-5)config = GridSearchConfig(
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-6)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-7)    scorer_config=ScorerConfig.for_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-8)    n_jobs=None,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-9)    return_train_score=False,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-0-10))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `cv_config`  | `WalkForwardConfig`  | default (quarterly rolling)  | Temporal cross-validation strategy  |  
| `scorer_config`  | `ScorerConfig`  | default (Sharpe ratio)  | Portfolio scoring function  |  
| `n_jobs`  |  `int` or `None`  | `None`  | Parallel jobs; `-1` uses all cores  |  
| `return_train_score`  | `bool`  | `False`  | Compute training scores (slower)  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#presets "Permanent link")  
| Preset  | CV Config  | n_jobs  | Description  |  
| --- | --- | --- | --- |  
| `for_quick_search()`  | Monthly rolling  | -1  | Fast evaluation, all cores  |  
| `for_thorough_search()`  | Quarterly expanding  | -1  | Comprehensive with train scores  |  
## Randomized Search[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#randomized-search "Permanent link")
Samples parameter configurations from specified distributions rather than exhaustive enumeration. Preferred when the parameter space is large or continuous.
### Configuration[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#configuration_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-1)from optimizer.tuning import RandomizedSearchConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-2)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-3)config = RandomizedSearchConfig(
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-4)    n_iter=50,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-5)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-6)    scorer_config=ScorerConfig.for_sharpe(),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-7)    n_jobs=None,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-8)    random_state=42,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-9)    return_train_score=False,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-1-10))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `n_iter`  | `int`  | 50  | Number of random parameter samples  |  
| `cv_config`  | `WalkForwardConfig`  | default  | Temporal CV strategy  |  
| `scorer_config`  | `ScorerConfig`  | default (Sharpe)  | Scoring function  |  
| `n_jobs`  |  `int` or `None`  | `None`  | Parallel jobs  |  
| `random_state`  |  `int` or `None`  | `None`  | Seed for reproducibility  |  
| `return_train_score`  | `bool`  | `False`  | Compute training scores  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#presets_1 "Permanent link")  
| Preset  | n_iter  | CV Config  | Description  |  
| --- | --- | --- | --- |  
| `for_quick_search(20)`  | 20  | Monthly rolling  | Fast random sampling  |  
| `for_thorough_search(100)`  | 100  | Quarterly expanding  | Comprehensive search  |  
## Nested Parameter Addressing[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#nested-parameter-addressing "Permanent link")
The sklearn `Pipeline` flattens all transformer and optimizer parameters, making them tunable via the double-underscore `__` notation. The step names come from `build_portfolio_pipeline()`:

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-1)validate__max_abs_return
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-2)outliers__winsorize_threshold
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-3)outliers__remove_threshold
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-4)impute__sector_mapping
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-5)drop_correlated__threshold
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-6)optimizer__risk_measure
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-7)optimizer__l2_coef
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-2-8)optimizer__prior_estimator__mu_estimator__alpha

```

### Discovering tunable parameters[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#discovering-tunable-parameters "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-1)from optimizer.pipeline import build_portfolio_pipeline
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-3)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-4)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-5)pipeline = build_portfolio_pipeline(optimizer)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-6)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-7)# List all tunable parameters
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-8)for name, value in sorted(pipeline.get_params().items()):
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-3-9)    print(f"{name}: {value}")

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#code-examples "Permanent link")
### Grid search over regularization[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#grid-search-over-regularization "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-1)from optimizer.pipeline import build_portfolio_pipeline, tune_and_optimize
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-3)from optimizer.tuning import GridSearchConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-4)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-5)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-6)X = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-7)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-8)pipeline = build_portfolio_pipeline(optimizer)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-9)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-10)param_grid = {
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-11)    "optimizer__l2_coef": [0.0, 0.01, 0.05, 0.1],
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-12)}
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-13)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-14)result = tune_and_optimize(
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-15)    pipeline, X,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-16)    param_grid=param_grid,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-17)    tuning_config=GridSearchConfig.for_quick_search(),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-18))
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-4-19)print(f"Best L2 coef: {result.pipeline.get_params()['optimizer__l2_coef']}")

```

### Grid search over multiple parameters[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#grid-search-over-multiple-parameters "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-1)param_grid = {
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-2)    "optimizer__l2_coef": [0.0, 0.01, 0.1],
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-3)    "drop_correlated__threshold": [0.85, 0.90, 0.95],
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-4)    "outliers__winsorize_threshold": [2.5, 3.0, 3.5],
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-5)}
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-6)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-7)result = tune_and_optimize(
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-8)    pipeline, X,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-9)    param_grid=param_grid,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-10)    tuning_config=GridSearchConfig(n_jobs=-1),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-5-11))

```

### Randomized search with distributions[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#randomized-search-with-distributions "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-1)from scipy.stats import uniform, loguniform
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-2)from optimizer.tuning import RandomizedSearchConfig
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-3)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-4)param_distributions = {
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-5)    "optimizer__l2_coef": loguniform(1e-4, 1e-1),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-6)    "drop_correlated__threshold": uniform(0.80, 0.15),  # [0.80, 0.95]
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-7)}
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-8)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-9)result = tune_and_optimize(
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-10)    pipeline, X,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-11)    param_grid=param_distributions,
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-12)    tuning_config=RandomizedSearchConfig.for_thorough_search(n_iter=50),
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-6-13))

```

### Using build functions directly[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#using-build-functions-directly "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-1)from optimizer.tuning import build_grid_search_cv, build_randomized_search_cv
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-3)# Grid search
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-4)gs = build_grid_search_cv(pipeline, param_grid, config=GridSearchConfig())
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-5)gs.fit(X)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-6)print(f"Best score: {gs.best_score_:.4f}")
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-7)print(f"Best params: {gs.best_params_}")
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-8)
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-9)# Randomized search
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-10)rs = build_randomized_search_cv(pipeline, param_distributions, config=RandomizedSearchConfig())
[](https://silviobaratto.github.io/optimizer/guide/tuning/#__codelineno-7-11)rs.fit(X)

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#gotchas-and-tips "Permanent link")
Temporal CV is enforced by default
Both `GridSearchConfig` and `RandomizedSearchConfig` default to walk-forward validation. Do not override this with standard `KFold` — it introduces look-ahead bias.
Use double-underscore notation for nested parameters
Pipeline parameters are addressed as `"step_name__parameter"`. For deeply nested parameters, chain underscores: `"optimizer__prior_estimator__mu_estimator__alpha"`.
Grid search vs randomized search
Use grid search when the parameter space is small and discrete. Use randomized search when exploring continuous distributions or when the grid would be too large. Randomized search with `n_iter=50` often finds good parameters faster than exhaustive grid search.
Computation cost
Each combination is evaluated across all walk-forward folds. With 4 folds, 3 parameters, and 4 values each: 4^3 * 4 = 256 fits. Use `n_jobs=-1` for parallelism and start with `for_quick_search()`.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/tuning/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Quick grid search  | `GridSearchConfig.for_quick_search()`  |  
| Thorough grid search  | `GridSearchConfig.for_thorough_search()`  |  
| Quick random search  | `RandomizedSearchConfig.for_quick_search(n_iter=20)`  |  
| Thorough random search  | `RandomizedSearchConfig.for_thorough_search(n_iter=100)`  |  
| Tune + optimize  | `tune_and_optimize(pipeline, X, param_grid={...})`  |  
| Build grid search  | `build_grid_search_cv(pipeline, param_grid)`  |  
| List tunable params  | `pipeline.get_params().keys()`  |
