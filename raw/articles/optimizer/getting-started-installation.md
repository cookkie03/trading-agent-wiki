<!-- source: https://silviobaratto.github.io/optimizer/getting-started/installation/ -->

[ Skip to content ](https://silviobaratto.github.io/optimizer/getting-started/installation/#installation)
# Installation[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#installation "Permanent link")
## Basic Install[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#basic-install "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-0-1)pip install -e .

```

This installs the optimizer library with all runtime dependencies: numpy, pandas, scipy, scikit-learn, skfolio, hmmlearn, and arch.
## Development Install[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#development-install "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-1-1)pip install -e ".[dev]"

```

This includes test, lint, typecheck, and docs dependencies — everything needed for development and CI.
## Optional Dependencies[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#optional-dependencies "Permanent link")  
| Group  | Install Command  | Includes  |  
| --- | --- | --- |  
| `test`  | `pip install -e ".[test]"`  | pytest, pytest-cov, hypothesis  |  
| `lint`  | `pip install -e ".[lint]"`  | ruff, pip-audit  |  
| `typecheck`  | `pip install -e ".[typecheck]"`  | mypy  |  
| `docs`  | `pip install -e ".[docs]"`  | mkdocs-material, mkdocstrings  |  
| `dmm`  | `pip install -e ".[dmm]"`  | torch, pyro-ppl  |  
| `dev`  | `pip install -e ".[dev]"`  | All of the above + pre-commit  |  
## Requirements[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#requirements "Permanent link")
  * Python >= 3.10
  * numpy, pandas, scipy, scikit-learn, skfolio, hmmlearn, arch


## Verifying the Installation[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#verifying-the-installation "Permanent link")
After installing, verify the library loads correctly:

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-1)import optimizer
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-2)from optimizer.optimization import MeanRiskConfig, build_mean_risk
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-3)from optimizer.pipeline import run_full_pipeline
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-4)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-5)# Quick sanity check
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-6)config = MeanRiskConfig.for_max_sharpe()
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-7)optimizer = build_mean_risk(config)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-2-8)print(f"Optimizer ready: {type(optimizer).__name__}")

```

## Deep Markov Model (Optional)[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#deep-markov-model-optional "Permanent link")
The DMM module (`optimizer.moments._dmm`) requires PyTorch and Pyro, which are **not** declared in the standard dependencies due to their size. Install them separately:

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-3-1)pip install -e ".[dmm]"

```

The DMM module is imported conditionally — if torch/pyro are not installed, the rest of the library works normally and DMM-related imports are silently skipped.
## Running Tests[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#running-tests "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-1)# All tests
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-2)pytest tests/ -v
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-3)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-4)# Single module
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-5)pytest tests/rebalancing/ -v
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-6)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-7)# Single test
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-4-8)pytest -k "test_name"

```

## Linting and Type Checking[¶](https://silviobaratto.github.io/optimizer/getting-started/installation/#linting-and-type-checking "Permanent link")

```
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-1)# Lint
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-2)ruff check optimizer/ tests/
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-3)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-4)# Lint + auto-fix
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-5)ruff check . --fix
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-6)
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-7)# Type check
[](https://silviobaratto.github.io/optimizer/getting-started/installation/#__codelineno-5-8)mypy optimizer/

```

