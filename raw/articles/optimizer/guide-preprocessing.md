<!-- source: https://silviobaratto.github.io/optimizer/guide/preprocessing/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/preprocessing/#preprocessing)
# Preprocessing[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#preprocessing "Permanent link")
The preprocessing module provides sklearn-compatible transformers that clean, validate, and impute asset return data before it enters the optimization pipeline. Every transformer follows the `BaseEstimator + TransformerMixin` API and composes naturally in `sklearn.pipeline.Pipeline`.
* * *
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#overview "Permanent link")
### The Problem[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#the-problem "Permanent link")
Raw return data from market data vendors is rarely clean. Common issues include:
  * **Infinite values** from division-by-zero in return calculations
  * **Extreme outliers** from stock splits, corporate actions, or data feed errors
  * **Missing values** from trading halts, delistings, holidays, or late-starting assets
  * **Survivorship bias** when delisted securities silently disappear from datasets


Left untreated, these issues distort moment estimates, break optimizers, and produce unreliable portfolios.
### Design Philosophy[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#design-philosophy "Permanent link")
The preprocessing module addresses each issue with a dedicated transformer:  
| Step  | Transformer  | Purpose  |  
| --- | --- | --- |  
| 1  | `DataValidator`  | Replace infinities and physically impossible returns with `NaN`  |  
| 2  | `OutlierTreater`  | Classify observations into normal / outlier / error via z-scores  |  
| 3  |  `SectorImputer` or `RegressionImputer`  | Fill remaining `NaN` values  |  
Plus a standalone utility function:  
| Function  | Purpose  |  
| --- | --- |  
| `apply_delisting_returns`  | Inject terminal delisting returns to prevent survivorship bias  |  
All transformers accept and return `pd.DataFrame` objects (dates as rows, tickers as columns). They are stateless or store only lightweight statistics (`mu_`, `sigma_`, correlation rankings) during `fit()`.
* * *
## DataValidator[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#datavalidator "Permanent link")
**Module** : `optimizer.preprocessing._validation`
The first line of defense. `DataValidator` replaces infinities and physically impossible returns with `NaN`, ensuring downstream transformers receive well-formed numeric data.
### Algorithm[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#algorithm "Permanent link")
  1. Replace all `+inf` and `-inf` values with `NaN`.
  2. Replace any return where `|r| > max_abs_return` with `NaN`.


The transformer is **stateless** : `fit()` stores only metadata (`n_features_in_`, `feature_names_in_`) but no learned statistics. This means train/test behavior is identical.
### Parameters[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#parameters "Permanent link")  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `max_abs_return`  | `float`  | `10.0`  | Absolute return threshold. Values with `|r| > max_abs_return` become `NaN`. The default of 10.0 (1,000%) is deliberately generous -- it catches data errors while preserving legitimate large moves.  |  
### Example[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#example "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-3)from optimizer.preprocessing import DataValidator
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-4)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-5)returns = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-6)    {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-7)        "AAPL": [0.01, -0.02, np.inf, 0.005],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-8)        "MSFT": [0.02, 15.0, -0.01, 0.003],  # 15.0 = 1500%, likely an error
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-9)        "GOOG": [0.015, -np.inf, 0.008, -0.003],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-10)    },
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-11)    index=pd.date_range("2024-01-01", periods=4, freq="B"),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-12))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-13)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-14)validator = DataValidator(max_abs_return=10.0)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-15)clean = validator.fit_transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-16)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-17)print(clean)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-18)#              AAPL   MSFT   GOOG
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-19)# 2024-01-01  0.010  0.020  0.015
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-20)# 2024-01-02 -0.020    NaN    NaN   <-- inf and 15.0 replaced
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-21)# 2024-01-03    NaN -0.010  0.008
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-0-22)# 2024-01-04  0.005  0.003 -0.003

```

* * *
## OutlierTreater[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#outliertreater "Permanent link")
**Module** : `optimizer.preprocessing._outliers`
Applies a three-group z-score methodology to classify each observation and treat it accordingly. This is a **stateful** transformer: `fit()` computes per-column mean and standard deviation from training data.
### Algorithm[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#algorithm_1 "Permanent link")
During `fit()`:
  * Compute per-column mean (`mu_`) and standard deviation (`sigma_`) from the training data.


During `transform()`:
  * Compute z-scores for each observation: `z = (x - mu_) / sigma_`.
  * Classify into three groups based on `|z|`:



```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-1-1)                      winsorize_threshold    remove_threshold
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-1-2)|z| ──────────────────────┼───────────────────────┼──────────────►
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-1-3)     Group 3: Keep        │  Group 2: Winsorize   │  Group 1: NaN
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-1-4)     (normal data)        │  (clip to bounds)     │  (data errors)

```
  
| Group  | Condition  | Action  |  
| --- | --- | --- |  
| 1 -- Data errors  | `|z| >= remove_threshold`  | Replaced with `NaN`  |  
| 2 -- Outliers  | `winsorize_threshold <= |z| < remove_threshold`  | Clipped to `mu +/- winsorize_threshold * sigma`  |  
| 3 -- Normal  | `|z| < winsorize_threshold`  | Kept as-is  |  
### Parameters[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#parameters_1 "Permanent link")  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `winsorize_threshold`  | `float`  | `3.0`  | Z-score boundary between normal observations (Group 3) and outliers (Group 2).  |  
| `remove_threshold`  | `float`  | `10.0`  | Z-score boundary between outliers (Group 2) and data errors (Group 1). Values at exactly this threshold are treated as errors.  |  
### Fitted Attributes[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#fitted-attributes "Permanent link")  
| Attribute  | Type  | Description  |  
| --- | --- | --- |  
| `mu_`  | `pd.Series`  | Per-column mean from training data  |  
| `sigma_`  | `pd.Series`  | Per-column standard deviation from training data  |  
### Example[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#example_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-3)from optimizer.preprocessing import OutlierTreater
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-4)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-5)np.random.seed(42)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-6)dates = pd.date_range("2024-01-01", periods=200, freq="B")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-7)returns = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-8)    np.random.normal(0.0005, 0.02, size=(200, 3)),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-9)    columns=["AAPL", "MSFT", "GOOG"],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-10)    index=dates,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-11))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-12)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-13)# Inject a data error and an outlier
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-14)returns.iloc[50, 0] = 0.50   # ~25 sigma, data error
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-15)returns.iloc[100, 1] = 0.10  # ~5 sigma, moderate outlier
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-16)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-17)treater = OutlierTreater(winsorize_threshold=3.0, remove_threshold=10.0)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-18)treater.fit(returns)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-19)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-20)print(f"AAPL mean: {treater.mu_['AAPL']:.6f}, std: {treater.sigma_['AAPL']:.6f}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-21)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-22)treated = treater.transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-23)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-24)# Data error at row 50 is now NaN
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-25)print(f"Row 50 AAPL (original): {returns.iloc[50, 0]:.4f}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-26)print(f"Row 50 AAPL (treated):  {treated.iloc[50, 0]}")  # NaN
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-27)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-28)# Outlier at row 100 is winsorized
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-29)print(f"Row 100 MSFT (original): {returns.iloc[100, 1]:.4f}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-2-30)print(f"Row 100 MSFT (treated):  {treated.iloc[100, 1]:.4f}")  # clipped

```

* * *
## SectorImputer[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#sectorimputer "Permanent link")
**Module** : `optimizer.preprocessing._imputation`
Fills `NaN` values using leave-one-out sector cross-sectional averages at each timestep. This approach preserves the cross-sectional return structure better than forward-filling or global mean imputation.
### Algorithm[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#algorithm_2 "Permanent link")
For each `NaN` at position `(t, asset_i)`:
  1. Identify the sector of `asset_i` using `sector_mapping`.
  2. Compute the mean return at timestep `t` across all **other** assets in the same sector (leave-one-out to avoid self-influence).
  3. If the entire sector is `NaN` at timestep `t`, fall back to the global cross-sectional mean (mean of all non-NaN assets at that timestep).


When `sector_mapping` is `None`, all assets are treated as belonging to a single sector, which reduces the imputer to a global cross-sectional mean.
### Parameters[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#parameters_2 "Permanent link")  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `sector_mapping`  |  `dict[str, str]` or `None`  | `None`  | Maps ticker to sector label. Columns absent from the mapping are assigned to `"__unmapped__"`. When `None`, all assets share one group.  |  
| `fallback_strategy`  | `str`  | `"global_mean"`  | Strategy when the entire sector is `NaN`. Only `"global_mean"` is supported.  |  
### Fitted Attributes[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#fitted-attributes_1 "Permanent link")  
| Attribute  | Type  | Description  |  
| --- | --- | --- |  
| `sector_groups_`  | `dict[str, list[str]]`  | Mapping of sector label to list of column names in that sector  |  
### Example[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#example_2 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-3)from optimizer.preprocessing import SectorImputer
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-4)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-5)returns = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-6)    {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-7)        "AAPL": [0.01, np.nan, 0.005, -0.01],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-8)        "MSFT": [0.02, 0.015, np.nan, 0.008],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-9)        "GOOG": [0.015, 0.012, 0.007, np.nan],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-10)        "JPM":  [0.005, np.nan, -0.003, 0.01],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-11)        "BAC":  [0.008, 0.006, -0.005, 0.012],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-12)    },
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-13)    index=pd.date_range("2024-01-01", periods=4, freq="B"),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-14))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-15)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-16)sector_mapping = {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-17)    "AAPL": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-18)    "MSFT": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-19)    "GOOG": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-20)    "JPM": "Financials",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-21)    "BAC": "Financials",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-22)}
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-23)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-24)imputer = SectorImputer(sector_mapping=sector_mapping)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-25)filled = imputer.fit_transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-26)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-27)# AAPL NaN at row 1 is filled with mean of MSFT and GOOG at that timestep
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-28)# (0.015 + 0.012) / 2 = 0.0135
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-29)print(f"AAPL row 1 (imputed): {filled.loc['2024-01-02', 'AAPL']:.4f}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-30)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-31)# JPM NaN at row 1 is filled with BAC's value (only other Financials asset)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-3-32)print(f"JPM row 1 (imputed):  {filled.loc['2024-01-02', 'JPM']:.4f}")

```

* * *
## RegressionImputer[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#regressionimputer "Permanent link")
**Module** : `optimizer.preprocessing._regression_imputer`
The most sophisticated imputer. Fills `NaN` values using OLS regression from each asset's most correlated neighbors. This approach preserves the covariance structure of the imputed values better than mean-based methods.
### Algorithm[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#algorithm_3 "Permanent link")
**During`fit()` :**
  1. Compute pairwise absolute correlations across all assets (using pairwise complete observations).
  2. For each asset, select the `n_neighbors` most correlated other assets.
  3. For each asset, fit an OLS regression on complete rows: `r_{i,t} = alpha + sum_j(beta_j * r_{j,t}) + epsilon`
  4. Fit an internal `SectorImputer` on the training data for fallback use.


**During`transform()` :**
  1. Pre-compute fallback values using the internal `SectorImputer`.
  2. For each asset with `NaN` values:
     * If OLS coefficients are available **and** all neighbors have data at that timestep: predict using `r_hat = alpha + beta @ r_neighbors`.
     * Otherwise: use the `SectorImputer` fallback value.


**Cold-start handling** : if an asset has fewer than `min_train_periods` complete observations across itself and its neighbors during `fit()`, no regression is fitted and all imputation falls back to the `SectorImputer`.
### Parameters[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#parameters_3 "Permanent link")  
| Parameter  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `n_neighbors`  | `int`  | `5`  | Number of most-correlated assets used as regression predictors.  |  
| `min_train_periods`  | `int`  | `60`  | Minimum complete-row count required to fit OLS. Assets below this threshold fall back to sector mean.  |  
| `fallback`  | `str`  | `"sector_mean"`  | Fallback imputation strategy. Only `"sector_mean"` is supported.  |  
| `sector_mapping`  |  `dict[str, str]` or `None`  | `None`  | Passed to the internal `SectorImputer` for fallback imputation.  |  
### Fitted Attributes[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#fitted-attributes_2 "Permanent link")  
| Attribute  | Type  | Description  |  
| --- | --- | --- |  
| `neighbors_`  | `dict[str, list[str]]`  | Top-K neighbor tickers per asset, ranked by absolute correlation  |  
| `coefs_`  | `dict[str, np.ndarray or None]`  | OLS coefficients per asset. Shape `(K+1,)` where index 0 is the intercept. `None` if cold-start.  |  
### Example[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#example_3 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-3)from optimizer.preprocessing import RegressionImputer
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-4)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-5)np.random.seed(42)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-6)dates = pd.date_range("2023-01-01", periods=252, freq="B")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-7)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-8)# Generate correlated returns
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-9)market = np.random.normal(0.0004, 0.01, size=252)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-10)returns = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-11)    {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-12)        "AAPL": market + np.random.normal(0, 0.005, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-13)        "MSFT": market + np.random.normal(0, 0.006, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-14)        "GOOG": market + np.random.normal(0, 0.007, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-15)        "AMZN": market + np.random.normal(0, 0.008, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-16)        "META": market + np.random.normal(0, 0.006, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-17)        "NVDA": market + np.random.normal(0, 0.009, 252),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-18)    },
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-19)    index=dates,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-20))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-21)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-22)# Inject some NaN values
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-23)returns.iloc[100:103, 0] = np.nan  # AAPL missing for 3 days
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-24)returns.iloc[200, 3] = np.nan      # AMZN missing for 1 day
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-25)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-26)sector_mapping = {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-27)    "AAPL": "Technology", "MSFT": "Technology", "GOOG": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-28)    "AMZN": "Consumer", "META": "Technology", "NVDA": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-29)}
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-30)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-31)imputer = RegressionImputer(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-32)    n_neighbors=3,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-33)    min_train_periods=60,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-34)    sector_mapping=sector_mapping,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-35))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-36)filled = imputer.fit_transform(returns)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-37)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-38)# Check that NaN values are filled
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-39)print(f"NaN count before: {returns.isna().sum().sum()}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-40)print(f"NaN count after:  {filled.isna().sum().sum()}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-41)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-42)# Inspect which neighbors were selected for AAPL
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-43)print(f"AAPL neighbors: {imputer.neighbors_['AAPL']}")
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-44)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-45)# Check if regression was fitted (not cold-start)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-4-46)print(f"AAPL has OLS coefs: {imputer.coefs_['AAPL'] is not None}")

```

* * *
## apply_delisting_returns[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#apply_delisting_returns "Permanent link")
**Module** : `optimizer.preprocessing._delisting`
A standalone utility function (not a transformer) that injects delisting returns into the return matrix. This prevents survivorship bias by ensuring that the terminal return experienced by investors when a stock was delisted is reflected in the data.
### Algorithm[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#algorithm_4 "Permanent link")
For each ticker in `delisting_returns`:
  1. Find the last valid (non-NaN) index in that ticker's column.
  2. Replace the return at that position with the provided delisting return value.


If a ticker's column is entirely `NaN`, it is skipped. If a ticker in the mapping is not found in the DataFrame columns, a `DataError` is raised.
### Parameters[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#parameters_4 "Permanent link")  
| Parameter  | Type  | Description  |  
| --- | --- | --- |  
| `returns`  | `pd.DataFrame`  | Dates-by-tickers return matrix.  |  
| `delisting_returns`  | `dict[str, float]`  | Mapping of ticker to its delisting return value.  |  
### Returns[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#returns "Permanent link")
A copy of the input DataFrame with delisting returns applied.
### Example[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#example_4 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-3)from optimizer.preprocessing import apply_delisting_returns
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-4)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-5)returns = pd.DataFrame(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-6)    {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-7)        "AAPL": [0.01, -0.02, 0.005, 0.003, 0.008],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-8)        "LEHMQ": [0.02, -0.05, -0.15, -0.30, np.nan],  # delisted, last trade day 4
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-9)        "MSFT": [0.015, 0.008, -0.003, 0.01, 0.005],
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-10)    },
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-11)    index=pd.date_range("2024-01-01", periods=5, freq="B"),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-12))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-13)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-14)# Lehman Brothers delisted with ~100% loss
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-15)adjusted = apply_delisting_returns(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-16)    returns,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-17)    delisting_returns={"LEHMQ": -1.0},
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-18))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-19)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-20)# The last valid return for LEHMQ is replaced with -1.0
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-21)print(adjusted["LEHMQ"])
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-22)# 2024-01-01    0.02
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-23)# 2024-01-02   -0.05
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-24)# 2024-01-03   -0.15
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-25)# 2024-01-04   -1.00  <-- replaced
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-5-26)# 2024-01-05      NaN

```

* * *
## Composing Transformers in a Pipeline[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#composing-transformers-in-a-pipeline "Permanent link")
All preprocessing transformers are designed to compose in an `sklearn.pipeline.Pipeline`. The recommended order is: validate, treat outliers, then impute.

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-1)from sklearn.pipeline import Pipeline
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-2)from optimizer.preprocessing import (
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-3)    DataValidator,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-4)    OutlierTreater,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-5)    RegressionImputer,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-6))
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-7)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-8)sector_mapping = {
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-9)    "AAPL": "Technology", "MSFT": "Technology", "GOOG": "Technology",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-10)    "JPM": "Financials", "BAC": "Financials", "GS": "Financials",
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-11)}
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-12)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-13)preprocessing_pipeline = Pipeline([
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-14)    ("validate", DataValidator(max_abs_return=10.0)),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-15)    ("outliers", OutlierTreater(winsorize_threshold=3.0, remove_threshold=10.0)),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-16)    ("impute", RegressionImputer(
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-17)        n_neighbors=5,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-18)        min_train_periods=60,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-19)        sector_mapping=sector_mapping,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-20)    )),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-21)])
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-22)
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-23)# Single call handles the entire cleaning workflow
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-6-24)clean_returns = preprocessing_pipeline.fit_transform(returns)

```

For simpler use cases where sector structure is not available, swap `RegressionImputer` for `SectorImputer` with `sector_mapping=None` (global mean imputation):

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-7-1)simple_pipeline = Pipeline([
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-7-2)    ("validate", DataValidator()),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-7-3)    ("outliers", OutlierTreater()),
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-7-4)    ("impute", SectorImputer()),  # global cross-sectional mean
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-7-5)])

```

* * *
## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#gotchas-and-tips "Permanent link")
Order matters: validate before treating outliers
`DataValidator` must run **before** `OutlierTreater`. If infinities reach the outlier treater, they will corrupt the `mu_` and `sigma_` statistics computed during `fit()`, causing all subsequent z-scores to be meaningless.
OutlierTreater is stateful -- watch for train/test leakage
`OutlierTreater` computes `mu_` and `sigma_` from training data and applies them at transform time. If you call `fit_transform()` on your full dataset instead of fitting on the training fold only, you introduce look-ahead bias. Always `fit()` on training data and `transform()` on test data separately, or use the transformer inside a pipeline that is wrapped in cross-validation.
Zero-variance columns are handled gracefully
If a column has zero standard deviation (constant series), `OutlierTreater` treats its z-score as 0 (normal) rather than raising an error. These columns will typically be removed downstream by `DropZeroVariance` in the pre-selection pipeline.
RegressionImputer falls back per-row, not per-asset
Even when an asset has a fitted regression, individual rows where any neighbor is `NaN` fall back to `SectorImputer`. This means the imputation method can vary across timesteps for the same asset. The fallback is computed for the entire DataFrame upfront for efficiency.
Cold-start assets get sector mean imputation
Assets with fewer than `min_train_periods` (default 60) complete observations have no regression fitted. All their `NaN` values are filled by the internal `SectorImputer`. This commonly happens with recently listed stocks.
Apply delisting returns before preprocessing
Call `apply_delisting_returns()` on your raw return DataFrame **before** passing it into the preprocessing pipeline. The delisting return is a real economic event, not missing data -- it should flow through the pipeline as a valid observation.
All transformers require pandas DataFrames
Passing a NumPy array or other type raises `DataError`. This is by design: the transformers rely on column names for sector mapping, correlation lookups, and feature name tracking.
SectorImputer uses leave-one-out within sectors
The imputed value for a missing asset excludes that asset's own value from the sector mean. This prevents the imputed value from being influenced by itself (which would be circular when the value is `NaN` anyway) and produces more conservative fills when sectors have few members.
* * *
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/preprocessing/#quick-reference "Permanent link")  
| Component  | Type  | Stateful  | Key Parameters  | Output  |  
| --- | --- | --- | --- | --- |  
| `DataValidator`  | Transformer  | No  | `max_abs_return=10.0`  |  `inf` and extreme values replaced with `NaN`  |  
| `OutlierTreater`  | Transformer  | Yes  |  `winsorize_threshold=3.0`, `remove_threshold=10.0`  | Three-group z-score treatment  |  
| `SectorImputer`  | Transformer  | Yes  |  `sector_mapping`, `fallback_strategy="global_mean"`  |  `NaN` filled with leave-one-out sector mean  |  
| `RegressionImputer`  | Transformer  | Yes  |  `n_neighbors=5`, `min_train_periods=60`, `sector_mapping`  |  `NaN` filled via OLS regression with sector fallback  |  
| `apply_delisting_returns`  | Function  | N/A  |  `returns`, `delisting_returns`  | Terminal returns replaced with delisting values  |  
**Imports:**

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-1)from optimizer.preprocessing import (
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-2)    DataValidator,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-3)    OutlierTreater,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-4)    SectorImputer,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-5)    RegressionImputer,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-6)    apply_delisting_returns,
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-8-7))

```

**Recommended pipeline order:**

```
[](https://silviobaratto.github.io/optimizer/guide/preprocessing/#__codelineno-9-1)apply_delisting_returns() → DataValidator → OutlierTreater → RegressionImputer (or SectorImputer)

```

