<!-- source: https://silviobaratto.github.io/optimizer/guide/rebalancing/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/guide/rebalancing/#rebalancing)
# Rebalancing[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#rebalancing "Permanent link")
The rebalancing module implements calendar-based, threshold-based, and hybrid rebalancing strategies for portfolio management. It determines **when** to trade (the rebalancing signal) and provides utility functions for computing drift, turnover, and transaction costs.
## Overview[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#overview "Permanent link")
After optimization produces target weights, the rebalancing module answers the question: "Should we actually trade to reach these weights?" Trading too frequently incurs unnecessary transaction costs, while trading too infrequently allows the portfolio to drift far from optimal allocations. The three strategies offer different trade-offs:
  * **Calendar** — rebalance at fixed intervals regardless of drift
  * **Threshold** — rebalance only when drift exceeds a limit
  * **Hybrid** — check drift only at calendar review dates (best of both worlds)


## Calendar Rebalancing[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#calendar-rebalancing "Permanent link")
Triggers portfolio reconstruction at fixed time intervals regardless of how much the portfolio has drifted.

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-0-1)from optimizer.rebalancing import CalendarRebalancingConfig, RebalancingFrequency
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-0-2)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-0-3)config = CalendarRebalancingConfig(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-0-4)    frequency=RebalancingFrequency.QUARTERLY,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-0-5))

```
  
| Frequency  | Trading Days  | Approximate Period  |  
| --- | --- | --- |  
| `MONTHLY`  | 21  | 1 month  |  
| `QUARTERLY`  | 63  | 3 months  |  
| `SEMIANNUAL`  | 126  | 6 months  |  
| `ANNUAL`  | 252  | 1 year  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#presets "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-1-1)CalendarRebalancingConfig.for_monthly()      # 21 trading days
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-1-2)CalendarRebalancingConfig.for_quarterly()     # 63 trading days
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-1-3)CalendarRebalancingConfig.for_semiannual()    # 126 trading days
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-1-4)CalendarRebalancingConfig.for_annual()        # 252 trading days

```

## Threshold Rebalancing[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#threshold-rebalancing "Permanent link")
Rebalances only when portfolio drift exceeds specified limits. This avoids unnecessary turnover during stable periods while catching significant deviations.

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-1)from optimizer.rebalancing import ThresholdRebalancingConfig, ThresholdType
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-2)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-3)config = ThresholdRebalancingConfig(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-4)    threshold_type=ThresholdType.ABSOLUTE,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-5)    threshold=0.05,  # 5 percentage points
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-2-6))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `threshold_type`  | `ThresholdType`  | `ABSOLUTE`  | Drift measurement method  |  
| `threshold`  | `float`  | 0.05  | Drift limit triggering rebalance  |  
### Absolute vs Relative Thresholds[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#absolute-vs-relative-thresholds "Permanent link")
  * **Absolute** (`ThresholdType.ABSOLUTE`): Triggers when any asset's weight deviates by more than `threshold` percentage points from its target. E.g., `threshold=0.05` means a 25% target weight triggers rebalancing when it drifts below 20% or above 30%.
  * **Relative** (`ThresholdType.RELATIVE`): Triggers when any asset's weight deviates by more than `threshold` fraction of its target. E.g., `threshold=0.25` means a 20% target triggers at 15% or 25% (25% of 20% = 5pp).


### Presets[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#presets_1 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-3-1)ThresholdRebalancingConfig.for_absolute(threshold=0.05)  # 5pp absolute
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-3-2)ThresholdRebalancingConfig.for_relative(threshold=0.25)   # 25% relative

```

## Hybrid Rebalancing[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#hybrid-rebalancing "Permanent link")
Combines calendar and threshold strategies: the portfolio is reviewed at regular calendar intervals, but trades are executed only when drift exceeds the threshold at the review date. Between review dates, `should_rebalance_hybrid` always returns `False` regardless of drift.
This is the recommended strategy for most institutional portfolios — it reduces monitoring overhead (only check at review dates) while avoiding unnecessary trades (only trade when drift is significant).

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-1)from optimizer.rebalancing import HybridRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-2)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-3)config = HybridRebalancingConfig(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-4)    calendar=CalendarRebalancingConfig.for_monthly(),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-5)    threshold=ThresholdRebalancingConfig.for_absolute(threshold=0.05),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-4-6))

```
  
| Field  | Type  | Default  | Description  |  
| --- | --- | --- | --- |  
| `calendar`  | `CalendarRebalancingConfig`  | Quarterly  | Review schedule  |  
| `threshold`  | `ThresholdRebalancingConfig`  | 5pp absolute  | Drift threshold at review  |  
### Presets[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#presets_2 "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-5-1)HybridRebalancingConfig.for_monthly_with_5pct_threshold()
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-5-2)# Monthly reviews, rebalance only if 5pp drift
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-5-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-5-4)HybridRebalancingConfig.for_quarterly_with_10pct_threshold()
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-5-5)# Quarterly reviews, rebalance only if 10pp drift

```

## Decision Functions[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#decision-functions "Permanent link")
### should_rebalance[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#should_rebalance "Permanent link")
Checks whether the portfolio should be rebalanced based on threshold drift:

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-1)from optimizer.rebalancing import should_rebalance, ThresholdRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-4)previous = np.array([0.25, 0.25, 0.25, 0.25])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-5)current = np.array([0.30, 0.20, 0.28, 0.22])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-6)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-7)config = ThresholdRebalancingConfig(threshold=0.05)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-8)needs_rebalance = should_rebalance(previous, current, config=config)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-6-9)print(needs_rebalance)  # True — 5pp drift in first asset

```

### should_rebalance_hybrid[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#should_rebalance_hybrid "Permanent link")
Checks both the calendar gate and the threshold:

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-1)from optimizer.rebalancing import should_rebalance_hybrid, HybridRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-2)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-4)config = HybridRebalancingConfig.for_monthly_with_5pct_threshold()
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-5)needs_rebalance = should_rebalance_hybrid(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-6)    previous, current, config,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-7)    current_date=pd.Timestamp("2024-03-15"),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-8)    last_review_date=pd.Timestamp("2024-02-15"),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-7-9))

```

## Utility Functions[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#utility-functions "Permanent link")
### compute_drifted_weights[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#compute_drifted_weights "Permanent link")
Compute what weights would be after one period of returns (without rebalancing):

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-1)from optimizer.rebalancing import compute_drifted_weights
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-4)weights = np.array([0.50, 0.30, 0.20])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-5)returns = np.array([0.02, -0.01, 0.03])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-6)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-7)drifted = compute_drifted_weights(weights, returns)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-8-8)print(drifted)  # Weights after market movements, normalized to sum to 1

```

### compute_turnover[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#compute_turnover "Permanent link")
One-way turnover between two weight vectors:

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-1)from optimizer.rebalancing import compute_turnover
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-4)old_weights = np.array([0.25, 0.25, 0.25, 0.25])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-5)new_weights = np.array([0.30, 0.20, 0.30, 0.20])
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-6)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-7)turnover = compute_turnover(old_weights, new_weights)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-9-8)print(f"Turnover: {turnover:.2%}")  # 10%

```

### compute_rebalancing_cost[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#compute_rebalancing_cost "Permanent link")
Transaction cost estimation based on turnover:

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-1)from optimizer.rebalancing import compute_rebalancing_cost
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-2)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-4)cost = compute_rebalancing_cost(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-5)    old_weights=np.array([0.25, 0.25, 0.25, 0.25]),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-6)    new_weights=np.array([0.30, 0.20, 0.30, 0.20]),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-7)    cost_bps=10.0,  # 10 basis points per unit of turnover
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-8))
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-10-9)print(f"Cost: {cost:.4%}")

```

## Code Examples[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#code-examples "Permanent link")
### Rebalancing in the pipeline[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#rebalancing-in-the-pipeline "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-1)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-2)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-3)from optimizer.rebalancing import ThresholdRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-4)import numpy as np
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-5)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-6)optimizer = build_mean_risk(MeanRiskConfig.for_max_sharpe())
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-7)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-8)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-9)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-10)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-11)    previous_weights=np.array([0.25, 0.25, 0.25, 0.25]),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-12)    rebalancing_config=ThresholdRebalancingConfig(threshold=0.05),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-13))
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-14)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-15)if result.rebalance_needed:
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-16)    print(f"Rebalance! Turnover: {result.turnover:.2%}")
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-17)    print(f"New weights: {result.weights}")
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-18)else:
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-11-19)    print("No rebalance needed — drift within threshold")

```

### Hybrid rebalancing in the pipeline[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#hybrid-rebalancing-in-the-pipeline "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-1)from optimizer.rebalancing import HybridRebalancingConfig
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-2)import pandas as pd
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-3)
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-4)result = run_full_pipeline(
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-5)    prices=prices,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-6)    optimizer=optimizer,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-7)    previous_weights=current_portfolio_weights,
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-8)    rebalancing_config=HybridRebalancingConfig.for_monthly_with_5pct_threshold(),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-9)    current_date=pd.Timestamp("2024-06-28"),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-10)    last_review_date=pd.Timestamp("2024-05-31"),
[](https://silviobaratto.github.io/optimizer/guide/rebalancing/#__codelineno-12-11))

```

## Gotchas and Tips[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#gotchas-and-tips "Permanent link")
Hybrid always returns False between reviews
`should_rebalance_hybrid` returns `False` between calendar review dates regardless of drift. This is by design — it prevents over-trading. If you need continuous monitoring, use `ThresholdRebalancingConfig` alone.
previous_weights alignment
When passed to `run_full_pipeline()`, previous weights are automatically aligned to the post-pre-selection universe and re-normalized. Assets dropped by pre-selection have their weights set to zero.
Calendar frequency constants
The `TRADING_DAYS` dictionary maps each `RebalancingFrequency` to its trading-day count: `{MONTHLY: 21, QUARTERLY: 63, SEMIANNUAL: 126, ANNUAL: 252}`.
Cost estimation
`compute_rebalancing_cost` uses a simple proportional model: `cost = turnover * cost_bps / 10000`. For more realistic costs, consider bid-ask spreads, market impact, and commission schedules.
## Quick Reference[¶](https://silviobaratto.github.io/optimizer/guide/rebalancing/#quick-reference "Permanent link")  
| Task  | Code  |  
| --- | --- |  
| Monthly calendar  | `CalendarRebalancingConfig.for_monthly()`  |  
| 5pp absolute threshold  | `ThresholdRebalancingConfig.for_absolute(0.05)`  |  
| 25% relative threshold  | `ThresholdRebalancingConfig.for_relative(0.25)`  |  
| Monthly + 5pp hybrid  | `HybridRebalancingConfig.for_monthly_with_5pct_threshold()`  |  
| Check rebalance  | `should_rebalance(prev, new, config=cfg)`  |  
| Compute turnover  | `compute_turnover(old, new)`  |  
| Estimate costs  | `compute_rebalancing_cost(old, new, cost_bps=10)`  |  
| Drifted weights  | `compute_drifted_weights(weights, returns)`  |
