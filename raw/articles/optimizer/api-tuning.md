<!-- source: https://silviobaratto.github.io/optimizer/api/tuning/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/tuning/#tuning)
# tuning[¶](https://silviobaratto.github.io/optimizer/api/tuning/#tuning "Permanent link")
###  `optimizer.tuning` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning "Permanent link")
Hyperparameter tuning with temporal cross-validation.
Wraps sklearn GridSearchCV and RandomizedSearchCV with temporal cross-validation defaults that prevent look-ahead bias.
####  `GridSearchConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.GridSearchConfig "Permanent link")
Immutable configuration for :class:`sklearn.model_selection.GridSearchCV`.
Enforces temporal cross-validation by default (walk-forward) to prevent look-ahead bias in financial time series.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.GridSearchConfig--parameters "Permanent link")
cv_config : WalkForwardConfig Temporal cross-validation configuration. Defaults to quarterly rolling with one-year training window. scorer_config : ScorerConfig Scoring function configuration. Defaults to Sharpe ratio. n_jobs : int or None Number of parallel jobs. `-1` uses all cores. return_train_score : bool Whether to compute training scores (increases runtime).
#####  `for_quick_search()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.GridSearchConfig.for_quick_search "Permanent link")
Fast grid search with monthly windows.
#####  `for_thorough_search()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.GridSearchConfig.for_thorough_search "Permanent link")
Thorough grid search with quarterly expanding windows.
####  `RandomizedSearchConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.RandomizedSearchConfig "Permanent link")
Immutable configuration for :class:`sklearn.model_selection.RandomizedSearchCV`.
Samples parameter configurations from specified distributions rather than exhaustive grid enumeration. Enforces temporal cross-validation by default.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.RandomizedSearchConfig--parameters "Permanent link")
n_iter : int Number of random parameter samples. cv_config : WalkForwardConfig Temporal cross-validation configuration. scorer_config : ScorerConfig Scoring function configuration. n_jobs : int or None Number of parallel jobs. random_state : int or None Seed for reproducibility. return_train_score : bool Whether to compute training scores.
#####  `for_quick_search(n_iter=20)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.RandomizedSearchConfig.for_quick_search "Permanent link")
Fast randomised search with few iterations.
#####  `for_thorough_search(n_iter=100)` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.RandomizedSearchConfig.for_thorough_search "Permanent link")
Thorough randomised search with many iterations.
####  `build_grid_search_cv(estimator, param_grid, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_grid_search_cv "Permanent link")
Build a :class:`GridSearchCV` with temporal cross-validation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_grid_search_cv--parameters "Permanent link")
estimator : BaseEstimator The skfolio optimiser or pipeline to tune. param_grid : dict Parameter grid. Keys use sklearn double-underscore notation for nested estimators (e.g. `"prior_estimator__mu_estimator__alpha"`). config : GridSearchConfig or None Tuning configuration. Defaults to `GridSearchConfig()` (quarterly walk-forward, Sharpe ratio scoring).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_grid_search_cv--returns "Permanent link")
GridSearchCV A fitted-ready grid search estimator.
####  `build_randomized_search_cv(estimator, param_distributions, config=None)` [¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_randomized_search_cv "Permanent link")
Build a :class:`RandomizedSearchCV` with temporal cross-validation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_randomized_search_cv--parameters "Permanent link")
estimator : BaseEstimator The skfolio optimiser or pipeline to tune. param_distributions : dict Parameter distributions. Values may be lists (discrete) or `scipy.stats` distributions (continuous, e.g. `scipy.stats.loguniform(0.01, 1)`). config : RandomizedSearchConfig or None Tuning configuration. Defaults to `RandomizedSearchConfig()` (50 iterations, quarterly walk-forward, Sharpe ratio scoring).
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/tuning/#optimizer.tuning.build_randomized_search_cv--returns "Permanent link")
RandomizedSearchCV A fitted-ready randomised search estimator.
