<!-- source: https://silviobaratto.github.io/optimizer/guide/pre-selection/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/pre-selection/#pre-selection)
# Pre-Selection[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#pre-selection "Permanent link")
Assemble data cleaning and asset filtering into a single sklearn `Pipeline`.
The pre-selection module takes a raw return `DataFrame`, cleans it (validation, outlier treatment, imputation), and then progressively narrows the asset universe through a series of skfolio selectors. The result is a tidy, NaN-free `DataFrame` containing only the assets that pass every filter -- ready to feed into moment estimation and portfolio optimization.
* * *
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#overview "Permanent link")
The module follows the same **frozen dataclass config + factory function** pattern used throughout the optimizer library:  
| Component  | Role  |  
| --- | --- |  
| `PreSelectionConfig`  | Frozen `@dataclass` holding every pipeline parameter as a plain primitive, enum, or `None`. Serialisable and suitable for hyperparameter sweeps.  |  
| `build_preselection_pipeline()`  | Factory function that reads a `PreSelectionConfig` and returns a fully assembled `sklearn.pipeline.Pipeline`.  |  
Because the config stores only primitives, it can be serialised to JSON/YAML, persisted to a database, or passed across process boundaries without issue. Non-serialisable objects (such as the `sector_mapping` dictionary) are passed as keyword arguments to the factory, not stored in the config.

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-1)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-3)config = PreSelectionConfig(correlation_threshold=0.90, top_k=30)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-4)pipeline = build_preselection_pipeline(config, sector_mapping={"AAPL": "Tech", "JPM": "Financials"})
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-5)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-0-6)clean_returns = pipeline.fit_transform(returns_df)

```

* * *
## Pipeline Steps[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#pipeline-steps "Permanent link")
`build_preselection_pipeline` assembles the following steps **in this exact order**. The first six steps are always present; the last three are conditional on config flags.

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-1-1)validate --> outliers --> impute --> SelectComplete --> DropZeroVariance
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-1-2)--> DropCorrelated --> [SelectKExtremes] --> [SelectNonDominated]
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-1-3)--> [SelectNonExpiring]

```

Steps in brackets are **optional** and only added when the corresponding config parameter is set.
### 1. `validate` -- DataValidator[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#1-validate-datavalidator "Permanent link")
Replaces `inf`, `-inf`, and returns whose absolute value exceeds `max_abs_return` with `NaN`. This is a stateless transformer that acts as a first-pass sanity check, catching data errors (e.g. a return of 50 000%) before they corrupt downstream statistics.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `max_abs_return`  | `max_abs_return`  |  `10.0` (i.e. 1 000%)  |  
Why so generous?
The default threshold of 10.0 (1 000%) is deliberately high. It catches obvious data errors while preserving legitimate large moves such as penny-stock spikes or circuit-breaker events. Tighten it to 5.0 or lower for conservative universes.
### 2. `outliers` -- OutlierTreater[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#2-outliers-outliertreater "Permanent link")
Three-group z-score methodology applied per-column:  
| Group  | Condition  | Action  |  
| --- | --- | --- |  
| **Data errors**  | `|z| >= remove_threshold`  | Replaced with `NaN`  |  
| **Outliers**  | `winsorize_threshold <= |z| < remove_threshold`  | Winsorised to `mu +/- winsorize_threshold * sigma`  |  
| **Normal**  | `|z| < winsorize_threshold`  | Kept as-is  |  
The z-scores are computed from the **training data** statistics (`mu_` and `sigma_` stored during `fit`). Constant-variance columns (sigma = 0) are assigned a z-score of 0 and left for `DropZeroVariance` to handle.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `winsorize_threshold`  | `winsorize_threshold`  | `3.0`  |  
| `remove_threshold`  | `remove_threshold`  | `10.0`  |  
Validation constraint
`winsorize_threshold` must be **strictly less than** `remove_threshold`. The config raises `ValueError` at construction time if this invariant is violated.
### 3. `impute` -- SectorImputer[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#3-impute-sectorimputer "Permanent link")
Fills remaining `NaN` values using leave-one-out sector cross-sectional averages. For each timestep and each missing cell, the imputer computes the mean of all _other_ assets in the same sector. When the entire sector is `NaN` for a given row, it falls back to the global cross-sectional mean.
When `sector_mapping` is `None`, all assets are treated as a single sector, which reduces to plain global cross-sectional mean imputation.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `fallback_strategy`  | `imputation_fallback`  | `"global_mean"`  |  
| `sector_mapping`  | Factory kwarg (not in config)  | `None`  |  
sector_mapping is a factory argument
The sector mapping is a `dict[str, str]` passed directly to `build_preselection_pipeline(sector_mapping=...)`, not stored in the frozen config. This keeps the config serialisable. Columns absent from the mapping are assigned to a catch-all `"__unmapped__"` sector.
### 4. `select_complete` -- SelectComplete[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#4-select_complete-selectcomplete "Permanent link")
Drops any asset (column) that still contains `NaN` after imputation. In practice, when `SectorImputer` runs correctly this step is a no-op, but it acts as a safety net to guarantee a fully complete matrix for downstream selectors that cannot handle missing data.
This step has **no configurable parameters**.
### 5. `drop_zero_variance` -- DropZeroVariance[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#5-drop_zero_variance-dropzerovariance "Permanent link")
Drops any asset with zero variance (constant return series). Constant columns add no information and cause numerical issues in covariance estimation.
This step has **no configurable parameters**.
### 6. `drop_correlated` -- DropCorrelated[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#6-drop_correlated-dropcorrelated "Permanent link")
Drops one asset from each pair whose pairwise correlation exceeds the threshold. This reduces redundancy in the universe and improves conditioning of the covariance matrix.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `threshold`  | `correlation_threshold`  | `0.95`  |  
| `absolute`  | `correlation_absolute`  | `False`  |  
Absolute correlation
When `correlation_absolute=True`, the selector uses `|corr|` rather than raw correlation, so that strong _negative_ correlations are also flagged. This is useful when you want to reduce all forms of linear dependence.
### 7. `select_k` -- SelectKExtremes (optional)[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#7-select_k-selectkextremes-optional "Permanent link")
Only added when `top_k is not None`. Keeps the _k_ assets with the highest (or lowest) mean return, as measured by `SelectKExtremes`.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `k`  | `top_k`  |  `None` (step omitted)  |  
| `highest`  | `top_k_highest`  | `True`  |  
### 8. `select_pareto` -- SelectNonDominated (optional)[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#8-select_pareto-selectnondominated-optional "Permanent link")
Only added when `use_pareto=True`. Applies a Pareto non-dominance filter across risk-return dimensions, retaining only assets that lie on the efficient frontier of mean return vs. variance.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `min_n_assets`  | `pareto_min_assets`  | `None`  |  
### 9. `select_non_expiring` -- SelectNonExpiring (optional)[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#9-select_non_expiring-selectnonexpiring-optional "Permanent link")
Only added when **both** `use_non_expiring=True` **and** `expiration_lookahead is not None`. Removes assets that expire within the specified lookahead window, which is relevant for futures and options universes.  
| Parameter  | Config field  | Default  |  
| --- | --- | --- |  
| `expiration_lookahead`  | `expiration_lookahead`  |  `None` (step omitted)  |  
Both flags required
Setting `use_non_expiring=True` without providing `expiration_lookahead` silently skips this step. The step is only added when both conditions are met.
* * *
## Configuration Reference[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#configuration-reference "Permanent link")
All fields of `PreSelectionConfig` with their types, defaults, and the pipeline step they control:  
| Field  | Type  | Default  | Pipeline step  | Description  |  
| --- | --- | --- | --- | --- |  
| `max_abs_return`  | `float`  | `10.0`  | `validate`  | Maximum absolute return before treating as data error  |  
| `winsorize_threshold`  | `float`  | `3.0`  | `outliers`  | Z-score boundary between normal observations and outliers  |  
| `remove_threshold`  | `float`  | `10.0`  | `outliers`  | Z-score boundary between outliers and data errors  |  
| `outlier_method`  | `str`  | `"time_series"`  | `outliers`  | Outlier detection approach (only `"time_series"` supported)  |  
| `imputation_fallback`  | `str`  | `"global_mean"`  | `impute`  | Fallback when sector data unavailable  |  
| `correlation_threshold`  | `float`  | `0.95`  | `drop_correlated`  | Pairwise correlation above which an asset is dropped  |  
| `correlation_absolute`  | `bool`  | `False`  | `drop_correlated`  | Whether to use absolute correlation values  |  
| `top_k`  | `int | None`  | `None`  | `select_k`  | If set, keep only the _k_ assets with highest/lowest mean return  |  
| `top_k_highest`  | `bool`  | `True`  | `select_k`  | Select highest (`True`) or lowest (`False`) mean return  |  
| `use_pareto`  | `bool`  | `False`  | `select_pareto`  | Whether to apply Pareto non-dominance filter  |  
| `pareto_min_assets`  | `int | None`  | `None`  | `select_pareto`  | Minimum assets to retain after Pareto filtering  |  
| `use_non_expiring`  | `bool`  | `False`  | `select_non_expiring`  | Whether to remove soon-expiring assets  |  
| `expiration_lookahead`  | `int | None`  | `None`  | `select_non_expiring`  | Calendar days to look ahead for expiring assets  |  
| `is_log_normal`  | `bool`  | `True`  | _(stored for downstream use)_  | Whether returns are assumed log-normal for multi-period scaling  |  
### Validation rules[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#validation-rules "Permanent link")
The config validates the following constraints at construction time (`__post_init__`):
  * `winsorize_threshold < remove_threshold` -- winsorisation boundary must be stricter than the removal boundary.
  * `0.0 < correlation_threshold <= 1.0` -- must be a valid correlation value.
  * `max_abs_return > 0` -- must be strictly positive.


Violating any of these raises `ValueError` immediately.
* * *
## Presets[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#presets "Permanent link")
`PreSelectionConfig` provides two class-method presets for common scenarios.
###  `for_daily_annual()`[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#for_daily_annual "Permanent link")
Sensible defaults for daily equity returns over an approximately one-year horizon. This is equivalent to `PreSelectionConfig()` with all defaults.

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-2-1)cfg = PreSelectionConfig.for_daily_annual()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-2-2)# max_abs_return=10.0, winsorize_threshold=3.0, remove_threshold=10.0,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-2-3)# correlation_threshold=0.95, is_log_normal=True
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-2-4)# No optional steps (top_k, pareto, non_expiring all off)

```

###  `for_conservative()`[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#for_conservative "Permanent link")
Tighter filters for a more conservative universe. Lowers the data-error and outlier thresholds, tightens the correlation filter, and activates `SelectKExtremes` to cap the universe at 50 assets.

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-3-1)cfg = PreSelectionConfig.for_conservative()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-3-2)# max_abs_return=5.0, winsorize_threshold=2.5, remove_threshold=8.0,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-3-3)# correlation_threshold=0.85, top_k=50, top_k_highest=True,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-3-4)# is_log_normal=True

```

* * *
## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#code-examples "Permanent link")
### Basic usage with default config[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#basic-usage-with-default-config "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-1)from skfolio.datasets import load_sp500_dataset
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-2)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-3)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-4)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-5)# Load data and convert to returns
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-6)prices = load_sp500_dataset()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-7)returns = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-8)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-9)# Build pipeline with sensible defaults
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-10)config = PreSelectionConfig.for_daily_annual()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-11)pipeline = build_preselection_pipeline(config)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-12)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-13)# Fit and transform
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-14)clean_returns = pipeline.fit_transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-4-15)print(f"Input: {returns.shape[1]} assets -> Output: {clean_returns.shape[1]} assets")

```

### Conservative preset with sector-aware imputation[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#conservative-preset-with-sector-aware-imputation "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-1)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-3)# Sector mapping for imputation
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-4)sector_mapping = {
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-5)    "AAPL": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-6)    "MSFT": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-7)    "JPM": "Financials",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-8)    "BAC": "Financials",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-9)    "JNJ": "Healthcare",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-10)    "PFE": "Healthcare",
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-11)    # ... more tickers
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-12)}
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-13)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-14)config = PreSelectionConfig.for_conservative()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-15)pipeline = build_preselection_pipeline(config, sector_mapping=sector_mapping)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-5-16)clean_returns = pipeline.fit_transform(returns)

```

### Custom configuration[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#custom-configuration "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-1)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-3)config = PreSelectionConfig(
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-4)    max_abs_return=5.0,              # Strict data-error threshold
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-5)    winsorize_threshold=2.5,         # Tighter winsorisation
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-6)    remove_threshold=8.0,            # Lower removal boundary
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-7)    correlation_threshold=0.90,      # Drop assets correlated above 90%
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-8)    correlation_absolute=True,       # Use |corr| (catches negative correlation too)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-9)    top_k=30,                        # Keep top 30 by mean return
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-10)    top_k_highest=True,              # Highest mean return
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-11)    use_pareto=True,                 # Apply Pareto filter after top-k
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-12)    pareto_min_assets=15,            # Keep at least 15 assets from Pareto
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-13))
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-14)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-15)pipeline = build_preselection_pipeline(config)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-6-16)clean_returns = pipeline.fit_transform(returns)

```

### Futures universe with expiration filtering[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#futures-universe-with-expiration-filtering "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-1)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-3)config = PreSelectionConfig(
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-4)    use_non_expiring=True,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-5)    expiration_lookahead=90,  # Drop contracts expiring within 90 days
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-6))
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-7)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-8)pipeline = build_preselection_pipeline(config)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-7-9)clean_returns = pipeline.fit_transform(futures_returns)

```

### Inspecting and tuning pipeline parameters[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#inspecting-and-tuning-pipeline-parameters "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-1)pipeline = build_preselection_pipeline()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-3)# List all accessible parameters
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-4)params = pipeline.get_params()
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-5)for key in sorted(params):
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-6)    if "__" in key:
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-7)        print(f"  {key} = {params[key]}")
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-8)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-9)# Modify parameters after construction
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-10)pipeline.set_params(
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-11)    outliers__winsorize_threshold=2.5,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-12)    drop_correlated__threshold=0.90,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-13)    validate__max_abs_return=5.0,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-8-14))

```

### Using pre-selection inside a full optimization pipeline[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#using-pre-selection-inside-a-full-optimization-pipeline "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-1)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-2)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-3)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-4)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-5)prices = ...  # pd.DataFrame of asset prices
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-6)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-7)# Pre-selection is handled internally by run_full_pipeline,
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-8)# but you can also run it explicitly for inspection:
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-9)config = PreSelectionConfig(correlation_threshold=0.90, top_k=50)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-10)preselection_pipe = build_preselection_pipeline(config)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-11)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-12)returns = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-13)clean_returns = preselection_pipe.fit_transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-9-14)print(f"Selected {clean_returns.shape[1]} assets from {returns.shape[1]}")

```

* * *
## Gotchas[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#gotchas "Permanent link")
Pre-selection must run inside CV folds
When using cross-validation (walk-forward, CPCV, etc.), the pre-selection pipeline **must** be part of the overall sklearn pipeline that gets re-fit on each training fold. If you run pre-selection once on the full dataset and then cross-validate, you introduce data leakage -- the `OutlierTreater` z-score statistics and `DropCorrelated` correlation matrix will have been computed on data that includes the validation period.
The optimizer library handles this correctly when the pre-selection pipeline is composed inside the broader sklearn `Pipeline` that `run_full_pipeline` builds.
Parameter names use double-underscore notation
All transformer hyper-parameters are accessible via `get_params()` using sklearn's `step_name__param_name` notation. For example:
  * `validate__max_abs_return`
  * `outliers__winsorize_threshold`
  * `outliers__remove_threshold`
  * `drop_correlated__threshold`
  * `drop_correlated__absolute`
  * `select_k__k` (only when `top_k` is set)


This is the notation you must use for `set_params()` and for hyperparameter tuning grids.
prices_to_returns runs outside the pipeline
The pre-selection pipeline operates on a **return** `DataFrame`, not a price `DataFrame`. The conversion from prices to returns (`skfolio.preprocessing.prices_to_returns`) changes data semantics and is therefore performed upstream, before the pipeline runs. This is a project-wide convention.
SelectNonExpiring requires both flags
Setting `use_non_expiring=True` alone does **not** add the step. You must also provide `expiration_lookahead` (an integer number of calendar days). Without it, the step is silently skipped.
The config is frozen
`PreSelectionConfig` is a frozen dataclass. You cannot mutate fields after construction. To change a parameter, create a new config instance:

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-1)# This raises AttributeError:
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-2)config.correlation_threshold = 0.85
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-3)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-4)# Do this instead:
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-5)from dataclasses import replace
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-10-6)new_config = replace(config, correlation_threshold=0.85)

```

* * *
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/pre-selection/#quick-reference "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-1)from optimizer.pre_selection import PreSelectionConfig, build_preselection_pipeline
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-2)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-3)# Presets
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-4)cfg = PreSelectionConfig.for_daily_annual()    # sensible defaults
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-5)cfg = PreSelectionConfig.for_conservative()    # tighter filters, top_k=50
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-6)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-7)# Factory
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-8)pipe = build_preselection_pipeline(config=cfg, sector_mapping=None)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-9)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-10)# Pipeline step names (default)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-11)# validate -> outliers -> impute -> select_complete -> drop_zero_variance -> drop_correlated
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-12)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-13)# Optional steps (added when config flags are set)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-14)# select_k            (top_k is not None)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-15)# select_pareto       (use_pareto=True)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-16)# select_non_expiring (use_non_expiring=True AND expiration_lookahead is not None)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-17)
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-18)# Key parameter paths for tuning
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-19)# validate__max_abs_return
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-20)# outliers__winsorize_threshold
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-21)# outliers__remove_threshold
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-22)# drop_correlated__threshold
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-23)# drop_correlated__absolute
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-24)# select_k__k
[](https://silviobaratto.github.io/optimizer/guide/pre-selection/#__codelineno-11-25)# select_k__highest

```

