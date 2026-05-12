<!-- source: https://silviobaratto.github.io/optimizer/api/pre_selection/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/pre_selection/#pre_selection)
# pre_selection[¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#pre_selection "Permanent link")
###  `optimizer.pre_selection` [¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection "Permanent link")
Pre-selection pipeline assembly.
####  `PreSelectionConfig` `dataclass` [¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.PreSelectionConfig "Permanent link")
Immutable configuration for the pre-selection pipeline.
All parameters map 1:1 to transformer/selector constructor arguments, making the config serialisable and suitable for hyperparameter sweeps.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.PreSelectionConfig--parameters "Permanent link")
max_abs_return : float Maximum absolute return before treating as data error (DataValidator). winsorize_threshold : float Z-score threshold for winsorisation (OutlierTreater). remove_threshold : float Z-score threshold for removal as data error (OutlierTreater). outlier_method : str Outlier detection approach. Currently only `"time_series"` is supported (per-column z-scores). imputation_fallback : str Fallback when sector data is unavailable. `"global_mean"` uses the cross-sectional mean across all assets. correlation_threshold : float Pairwise correlation above which an asset is dropped (`DropCorrelated`). correlation_absolute : bool If `True`, use absolute correlation values. top_k : int or None If set, keep only the _k_ assets with the highest (or lowest) mean return via `SelectKExtremes`. top_k_highest : bool Select assets with the highest mean when `True`, lowest when `False`. use_pareto : bool If `True`, apply `SelectNonDominated` Pareto filter. pareto_min_assets : int or None Minimum number of assets to retain after Pareto filtering. use_non_expiring : bool If `True`, apply `SelectNonExpiring` to remove soon-expiring assets. expiration_lookahead : int or None Number of calendar days to look ahead for expiring assets, forwarded to `SelectNonExpiring` as a `timedelta`. is_log_normal : bool Whether returns are assumed log-normal for multi-period scaling (deferred to Chapter 2, stored here for completeness).
#####  `for_daily_annual()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.PreSelectionConfig.for_daily_annual "Permanent link")
Sensible defaults for daily returns over a ~1-year horizon.
#####  `for_conservative()` `classmethod` [¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.PreSelectionConfig.for_conservative "Permanent link")
Tighter filters for a more conservative universe.
####  `build_preselection_pipeline(config=None, sector_mapping=None)` [¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.build_preselection_pipeline "Permanent link")
Build an sklearn Pipeline for data cleaning and asset pre-selection.
The pipeline is assembled from _config_ and follows this order::

```
validate → outliers → impute → SelectComplete → DropZeroVariance
→ DropCorrelated → [SelectKExtremes] → [SelectNonDominated]
→ [SelectNonExpiring]

```

Optional steps (in brackets) are only included when the corresponding config flag or parameter is set.
All transformer hyper-parameters are accessible via `pipeline.get_params()` for cross-validation tuning (e.g. `outliers__winsorize_threshold`).
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.build_preselection_pipeline--parameters "Permanent link")
config : PreSelectionConfig or None Pipeline configuration. Defaults to `PreSelectionConfig()` (sensible defaults for daily equity returns). sector_mapping : dict[str, str] or None Ticker → sector mapping forwarded to :class:`SectorImputer`. When `None`, global cross-sectional mean imputation is used.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/pre_selection/#optimizer.pre_selection.build_preselection_pipeline--returns "Permanent link")
sklearn.pipeline.Pipeline
