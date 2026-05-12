<!-- source: https://silviobaratto.github.io/optimizer/getting-started/quickstart/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#quickstart)
# Quickstart[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#quickstart "Permanent link")
This guide walks through five progressively complex examples — from a minimal optimization to a full pipeline with stock selection, regime blending, and rebalancing.
## 1. Basic Optimization[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#1-basic-optimization "Permanent link")
The simplest use case: maximize the Sharpe ratio with walk-forward validation.

```
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-1)import pandas as pd
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-3)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-4)from optimizer.validation import WalkForwardConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-5)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-6)# Load price data (DatetimeIndex, one column per asset)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-7)prices = pd.read_csv("prices.csv", index_col=0, parse_dates=True)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-8)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-9)# Build optimizer from config
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-10)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-11)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-12)# Run end-to-end pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-13)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-14)    prices=prices,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-15)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-16)    cv_config=WalkForwardConfig.for_quarterly_rolling(),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-17))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-18)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-19)print(result.weights)          # pd.Series of asset weights
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-20)print(result.summary)          # dict with Sharpe, max drawdown, etc.
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-0-21)print(result.backtest)         # out-of-sample MultiPeriodPortfolio

```

`run_full_pipeline` handles everything internally: price-to-return conversion, pre-selection, optimization, cross-validation, and backtesting. See the [Pipeline Overview](https://silviobaratto.github.io/optimizer/guide/pipeline/) for the full data flow.
## 2. Custom Pre-selection and Moments[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#2-custom-pre-selection-and-moments "Permanent link")
Control which assets survive filtering and how expected returns and covariance are estimated.

```
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-1)from optimizer.pre_selection import PreSelectionConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-2)from optimizer.moments import MomentEstimationConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-3)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-4)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-5)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-6)# Drop correlated assets (>85%) and keep top 30 by variance
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-7)preselection = PreSelectionConfig(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-8)    correlation_threshold=0.85,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-9)    top_k=30,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-10))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-11)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-12)# Shrunk mu + denoised covariance
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-13)moments = MomentEstimationConfig.for_shrunk_denoised()
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-14)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-15)# Minimum CVaR optimization
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-16)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-17)    MeanRiskConfig.for_min_cvar(beta=0.95),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-18)    moment_config=moments,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-19))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-20)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-21)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-22)    prices=prices,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-23)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-24)    preselection_config=preselection,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-25)    sector_mapping={"AAPL": "Tech", "JPM": "Financials", ...},
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-1-26))

```

The `sector_mapping` dict enables sector-aware imputation during preprocessing. See [Preprocessing](https://silviobaratto.github.io/optimizer/guide/preprocessing/) and [Pre-selection](https://silviobaratto.github.io/optimizer/guide/pre-selection/).
## 3. Black-Litterman Views[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#3-black-litterman-views "Permanent link")
Incorporate analyst views into the optimization through the Black-Litterman framework.

```
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-1)from optimizer.views import BlackLittermanConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-2)from optimizer.moments import MomentEstimationConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-3)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-4)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-5)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-6)# Define views: AAPL returns 12%, MSFT outperforms GOOG by 3%
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-7)bl_config = BlackLittermanConfig.for_equilibrium(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-8)    views=("AAPL == 0.12", "MSFT - GOOG == 0.03"),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-9)    tau=0.05,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-10))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-11)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-12)# Build optimizer with BL prior
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-13)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-14)    MeanRiskConfig.for_max_utility(risk_aversion=1.0),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-15)    bl_config=bl_config,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-16))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-17)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-18)result = run_full_pipeline(prices=prices, optimizer=optimizer)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-2-19)print(result.weights)

```

Views use a string syntax: `"TICKER == value"` for absolute views, `"TICKER1 - TICKER2 == value"` for relative views. See [Views](https://silviobaratto.github.io/optimizer/guide/views/) for Entropy Pooling and Opinion Pooling alternatives.
## 4. HMM Regime Blending[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#4-hmm-regime-blending "Permanent link")
Use a Hidden Markov Model to blend moments across market regimes, producing estimates that adapt to the current regime.

```
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-1)from skfolio.preprocessing import prices_to_returns
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-2)from optimizer.moments import (
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-3)    HMMConfig,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-4)    fit_hmm,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-5)    HMMBlendedMu,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-6)    HMMBlendedCovariance,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-7)    MomentEstimationConfig,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-8))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-9)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-10)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-11)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-12)returns = prices_to_returns(prices)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-13)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-14)# Fit 2-state HMM
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-15)hmm_result = fit_hmm(returns.values, config=HMMConfig(n_states=2))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-16)print(f"Current regime: {hmm_result.filtered_probs[-1]}")
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-17)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-18)# Build optimizer with regime-blended moments
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-19)optimizer = build_mean_risk(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-20)    MeanRiskConfig.for_max_sharpe(),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-21)    moment_config=MomentEstimationConfig.for_hmm_blended(),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-22))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-23)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-3-24)result = run_full_pipeline(prices=prices, optimizer=optimizer)

```

`HMMBlendedCovariance` uses the full law of total variance (including between-regime mean dispersion), while `blend_moments_by_regime()` uses within-regime covariance only. Use the class for optimizer inputs. See [Moments](https://silviobaratto.github.io/optimizer/guide/moments/) for details.
## 5. Full Pipeline with Rebalancing[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#5-full-pipeline-with-rebalancing "Permanent link")
Combine optimization with threshold-based rebalancing to determine whether to trade.

```
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-1)import numpy as np
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-2)import pandas as pd
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-3)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-4)from optimizer.rebalancing import HybridRebalancingConfig
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-5)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-6)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-7)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-8)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-9)# Current portfolio weights (from previous period)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-10)previous_weights = np.array([0.25, 0.25, 0.25, 0.25])
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-11)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-12)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-13)    prices=prices,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-14)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-15)    previous_weights=previous_weights,
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-16)    rebalancing_config=HybridRebalancingConfig.for_monthly_with_5pct_threshold(),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-17)    current_date=pd.Timestamp("2024-06-28"),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-18)    last_review_date=pd.Timestamp("2024-05-31"),
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-19))
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-20)
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-21)if result.rebalance_needed:
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-22)    print(f"Rebalance! Turnover: {result.turnover:.2%}")
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-23)    print(f"New weights: {result.weights}")
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-24)else:
[](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#__codelineno-4-25)    print("No rebalance needed — drift within threshold")

```

Hybrid rebalancing checks drift only at calendar review dates, preventing over-trading between reviews. See [Rebalancing](https://silviobaratto.github.io/optimizer/guide/rebalancing/) for calendar, threshold, and hybrid strategies.
## Next Steps[¶](https://silviobaratto.github.io/optimizer/getting-started/quickstart/#next-steps "Permanent link")  
| Want to...  | Read  |  
| --- | --- |  
| Understand the full data flow  | [Pipeline Overview](https://silviobaratto.github.io/optimizer/guide/pipeline/)  |  
| Clean and impute return data  | [Preprocessing](https://silviobaratto.github.io/optimizer/guide/preprocessing/)  |  
| Estimate expected returns and covariance  | [Moments](https://silviobaratto.github.io/optimizer/guide/moments/)  |  
| Add analyst views  | [Views](https://silviobaratto.github.io/optimizer/guide/views/)  |  
| Choose an optimization model  | [Optimization](https://silviobaratto.github.io/optimizer/guide/optimization/)  |  
| Validate out-of-sample  | [Validation](https://silviobaratto.github.io/optimizer/guide/validation/)  |  
| Tune hyperparameters  | [Tuning](https://silviobaratto.github.io/optimizer/guide/tuning/)  |  
| Run factor-based stock selection  | [Factors](https://silviobaratto.github.io/optimizer/guide/factors/)  |  
| Generate synthetic scenarios  | [Synthetic Data](https://silviobaratto.github.io/optimizer/guide/synthetic/)  |  
| Screen an investable universe  | [Universe Screening](https://silviobaratto.github.io/optimizer/guide/universe/)  |  
See the [`examples/`](https://github.com/SilvioBaratto/optimizer/tree/main/examples) directory for complete, runnable scripts.
