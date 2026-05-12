<!-- source: https://silviobaratto.github.io/optimizer/api/preprocessing/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/api/preprocessing/#preprocessing)
# preprocessing[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#preprocessing "Permanent link")
###  `optimizer.preprocessing` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing "Permanent link")
Custom sklearn-compatible preprocessing transformers.
####  `SectorImputer` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.SectorImputer "Permanent link")
Bases: `BaseEstimator`, `TransformerMixin`
Fill NaN values using sector cross-sectional averages.
For each timestep (row), missing values in a given asset column are replaced with the mean of all _other_ assets in the same sector for that timestep (leave-one-out sector average). If the entire sector is `NaN` for a timestep, the global cross-sectional mean is used as a fallback.
When `sector_mapping` is `None`, all assets are treated as belonging to a single sector — effectively a global cross-sectional mean imputation.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.SectorImputer--parameters "Permanent link")
sector_mapping : dict[str, str] or None, default=None Maps column name (ticker) → sector label. Columns absent from the mapping are assigned to a `"__unmapped__"` catch-all sector. fallback_strategy : str, default="global_mean" What to do when the sector has no data for a timestep. Currently only `"global_mean"` is supported.
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.SectorImputer.fit "Permanent link")
Build the internal sector → columns index.
#####  `transform(X)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.SectorImputer.transform "Permanent link")
Fill NaN with leave-one-out sector averages.
#####  `get_feature_names_out(input_features=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.SectorImputer.get_feature_names_out "Permanent link")
Return feature names (pass-through).
####  `OutlierTreater` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.OutlierTreater "Permanent link")
Bases: `BaseEstimator`, `TransformerMixin`
Three-group outlier methodology on per-column z-scores.
During `fit`, compute per-column mean (`mu_`) and standard deviation (`sigma_`) from the training data.
During `transform`, classify each observation into one of three groups based on its z-score `z = (x - mu) / sigma`:
  1. **Data errors** — `|z| > remove_threshold` → replaced with `NaN`.
  2. **Outliers** — `winsorize_threshold <= |z| <= remove_threshold` → winsorised to `mu ± winsorize_threshold * sigma`.
  3. **Normal** — `|z| < winsorize_threshold` → kept as-is.


###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.OutlierTreater--parameters "Permanent link")
winsorize_threshold : float, default=3.0 Z-score boundary between normal observations and outliers. remove_threshold : float, default=10.0 Z-score boundary between outliers and data errors.
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.OutlierTreater.fit "Permanent link")
Compute per-column mean and std from training data.
#####  `transform(X)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.OutlierTreater.transform "Permanent link")
Apply three-group treatment based on z-scores.
#####  `get_feature_names_out(input_features=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.OutlierTreater.get_feature_names_out "Permanent link")
Return feature names (pass-through).
####  `RegressionImputer` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer "Permanent link")
Bases: `BaseEstimator`, `TransformerMixin`
Fill NaN values using OLS regression from top-K correlated assets.
For each asset with missing data, fits a linear regression over the training window using the `n_neighbors` most correlated assets as predictors::

```
r_{i,t} = α + Σ_j β_j · r_{j,t} + ε_{i,t}

```

This preserves the covariance structure of imputed values better than sector-mean imputation.
**Cold-start handling** : if fewer than `min_train_periods` complete observations exist for an asset in training, the asset falls back to the `fallback` strategy at transform time. The same fallback applies per-row when any neighbor is itself `NaN` at the imputation timestep.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer--parameters "Permanent link")
n_neighbors : int, default=5 Number of most-correlated assets used as regression predictors. min_train_periods : int, default=60 Minimum complete-row count required to fit the OLS regression for an asset. Assets below this threshold use the fallback strategy. fallback : str, default="sector_mean" Imputation strategy when regression is unavailable. Only `"sector_mean"` is currently supported (delegates to :class:`SectorImputer`). sector_mapping : dict[str, str] or None, default=None Maps ticker → sector label. Passed to the internal :class:`SectorImputer` used for fallback imputation. When `None`, the fallback uses a global cross-sectional mean.
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.fit "Permanent link")
Compute neighbor rankings and fit per-asset OLS regressions.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.fit--parameters "Permanent link")
X : pd.DataFrame Asset return DataFrame (dates × assets). May contain NaN. y : ignored
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.fit--returns "Permanent link")
self
#####  `transform(X)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.transform "Permanent link")
Impute NaN values using fitted regressions and/or fallback.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.transform--parameters "Permanent link")
X : pd.DataFrame Asset return DataFrame (dates × assets). May contain NaN.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.transform--returns "Permanent link")
pd.DataFrame Copy of `X` with NaN values filled.
#####  `get_feature_names_out(input_features=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.RegressionImputer.get_feature_names_out "Permanent link")
Return feature names (pass-through).
####  `DataValidator` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.DataValidator "Permanent link")
Bases: `BaseEstimator`, `TransformerMixin`
Replace infinities and extreme values with NaN.
Operates on a return DataFrame. Designed as the first step in a pre-selection pipeline so that downstream transformers receive well-formed numeric data.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.DataValidator--parameters "Permanent link")
max_abs_return : float, default=10.0 Any return whose absolute value exceeds this threshold is replaced with `NaN`. The default of 10.0 (i.e. 1 000 %) is deliberately generous — it catches data errors while preserving legitimate large moves.
#####  `fit(X, y=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.DataValidator.fit "Permanent link")
Store metadata. This transformer is stateless.
#####  `transform(X)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.DataValidator.transform "Permanent link")
Replace `inf` / `-inf` and extreme returns with `NaN`.
#####  `get_feature_names_out(input_features=None)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.DataValidator.get_feature_names_out "Permanent link")
Return feature names (pass-through).
####  `apply_delisting_returns(returns, delisting_returns)` [¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.apply_delisting_returns "Permanent link")
Replace each ticker's last valid return with its delisting return.
This prevents survivorship bias by incorporating the terminal return that investors would have experienced when a stock was delisted.
###### Parameters[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.apply_delisting_returns--parameters "Permanent link")
returns : pd.DataFrame Dates x tickers return matrix. delisting_returns : dict[str, float] Mapping of ticker to delisting return value. Each ticker's last valid (non-NaN) return is replaced with this value.
###### Returns[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.apply_delisting_returns--returns "Permanent link")
pd.DataFrame A copy of _returns_ with delisting returns applied.
###### Raises[¶](https://silviobaratto.github.io/optimizer/api/preprocessing/#optimizer.preprocessing.apply_delisting_returns--raises "Permanent link")
DataError If a ticker in _delisting_returns_ is not in _returns_ columns.
