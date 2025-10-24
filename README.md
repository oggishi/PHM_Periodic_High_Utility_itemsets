# PHM_Periodic_High_Utility_itemsets

Periodic High-Utility Itemset Mining (PHM) — a Python implementation and experimental framework for discovering periodic high-utility itemsets from transactional / temporal datasets. This repository implements algorithms, dataset parsers, experiment harnesses, and utilities to evaluate mining results and performance.

[![Language](https://img.shields.io/badge/Language-Python-blue)]()
[![Status](https://img.shields.io/badge/Status-Active-green)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

---

##Overview

PHM_Periodic_High_Utility_itemsets is a research-grade, production-aware codebase for mining periodic high-utility itemsets — patterns that not only contribute high utility but also occur periodically across time windows. The project is targeted at data scientists, researchers in data mining, and engineers building analytics pipelines requiring temporal utility-aware pattern discovery.

Key objectives:
- Provide a correct, testable implementation of PHM algorithms and baseline comparators.
- Offer reproducible experiment harnesses (dataset loading, parameter sweep, metrics).
- Be modular and efficient: reusable parsers, mining core, evaluation & export utilities.
- Support academic reporting and real-world workloads with options for optimization.

Intended audiences:
- Researchers and students in data mining
- Data engineers integrating pattern mining into analytics pipelines
- Developers who want an extendable implementation for productionization

---

## Highlights & features

- Reference implementation of periodic high-utility itemset mining (PHM) algorithms.
- Data parsers supporting common transactional formats and time-tagged transactions.
- CLI and Python API to run experiments, parameter sweeps, and export results.
- Output formats: CSV/JSON with itemset, utility, period information and metrics.
- Experiment harness: vary min-utility, periodicity thresholds, window sizes.
- Utilities: performance logging, memory profiling helpers, and benchmark scripts.
- Tests: unit tests for core logic and integration tests for end-to-end runs.
- Extensible: hooks for pruning strategies, parallelization, and alternative utility models.

---

## Technology & recommended stack

- Language: Python (100% of repository)
- Python version: 3.8+ (3.10/3.11 recommended)
- Suggested libraries: numpy, pandas, tqdm, Click (or argparse), pytest
- Optional for performance: numba, Cython, multiprocessing, joblib
- Experiment reproducibility: use virtualenv or poetry; Dockerfile and compose recommended
- Data storage: CSV / Parquet for inputs; results in CSV/JSON

---

## System requirements

- Python 3.8+
- 4+ GB RAM for small-medium datasets; more for large real-world data
- Optional: Docker for reproducible experiments

---

## Quick start — install & run

1. Create virtual environment and install:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Dataset format (transactional, time-tagged):
- Simple CSV example:
  transaction_id,timestamp,item,quantity,utility
  1,2020-01-01,itemA,2,5.0
  1,2020-01-01,itemB,1,3.0
  2,2020-01-08,itemA,1,2.5
- Or aggregated per transaction:
  transaction_id,timestamp,item1:qty:utility,item2:qty:utility,...

3. Run a CLI mining job:
```bash
python -m phm.cli run \
  --input data/transactions.csv \
  --min-utility 50 \
  --period-window 7d \
  --min-periodicity 0.6 \
  --output results/phm_results.csv
```
(Adjust flags to the CLI implemented in the repo; check `phm/cli.py` for exact parameter names.)

4. Run tests:
```bash
pytest tests/
```

---

## Data & input expectations

- Time resolution: timestamps should be parseable (ISO-8601 recommended).
- Utility model: per-item utilities can be provided or computed from price * quantity.
- Periodicity model: sliding windows, fixed windows, or event-based intervals — the repo supports configurable windowing strategies.
- Missing or inconsistent timestamps should be cleaned or preprocessed.

---

## API sketch (Python)

Example usage (high-level):
```python
from phm import loader, miner, evaluator

transactions = loader.load_csv("data/transactions.csv", time_col="timestamp")
results = miner.mine_periodic_high_utility_itemsets(
    transactions,
    min_utility=50,
    window="7d",
    min_periodicity=0.6,
    algorithm="phm_ref"
)
evaluator.save_results(results, "results/phm_results.csv")
```

---

## Functions & Tasks — combined (use this as the backlog)

This section provides a complete and prioritized list of functions and implementation tasks that let you convert items directly into issues, milestones, or development work.

Priority legend:
- P0 — must have for a working baseline and reproducible experiments
- P1 — important for usability, performance, and reproducibility
- P2 — nice-to-have features and advanced optimizations

### Core functions (overview)

1. Data Loading & Normalization
   - Parse CSV/Parquet/TSV transactional files with timestamps
   - Aggregate or expand item utilities if needed
   - Support mapping files for item metadata (values/prices)

2. Periodic High-Utility Mining Engine
   - Implement core PHM algorithm(s) with pruning strategies
   - Support fixed and sliding time windows, and configurable periodicity metrics
   - Provide pluggable utility models (total utility, unit utility, external utility)

3. CLI & Python API
   - CLI commands to run single jobs, parameter sweeps, and reproduce experiments
   - Programmatic API for integration into pipelines

4. Result Export & Visualization
   - Export itemsets with utility and periodicity metadata to CSV/JSON
   - Plot periodicity timelines, utility distributions, and support graphs

5. Experiment Harness & Benchmarks
   - Parameter sweep runner (min-utility, window sizes, algorithms)
   - Performance logging, time and memory capture, and reproducible seeds

6. Tests & CI
   - Unit tests for core algorithm components and utilities
   - Integration tests using small synthetic datasets
   - GitHub Actions CI for lint, tests, and optional benchmark jobs

7. Documentation & Examples
   - Dataset examples and expected formats
   - Jupyter notebooks demonstrating usage and visualization

8. Performance & Scalability
   - Profiling hooks and optional numba/Cython acceleration
   - Parallel worker implementations for independent window mining

---

### Suggested data model / internal structures

- Transaction { tid, timestamp (datetime), items: [{item_id, qty, utility}], total_utility }
- ItemStats { item_id, total_utility, occurrence_count, period_vector }
- ItemsetResult { items, support, total_utility, periodicity_score, windows_present[] }
- ExperimentRun { run_id, parameters, duration_seconds, memory_mb, results_path }

---

### Prioritized implementation tasks (backlog)

P0 — Core baseline
- Task: Implement robust CSV/Parquet loader and normalize transaction format
  - Complexity: low
  - Tests: parsers produce canonical transaction objects for sample datasets
- Task: Implement reference PHM algorithm (correctness over micro-optimizations)
  - Complexity: medium
  - Tests: unit tests validate itemset outputs on small crafted datasets
- Task: CLI `run` command to launch mining with minimal flags and export CSV
  - Complexity: low
  - Tests: end-to-end test using synthetic dataset; output comparison
- Task: Add basic experiment harness to run and log single experiments
  - Complexity: low
- Task: Add unit test suite and minimal GitHub Actions workflow (lint + tests)
  - Complexity: low

P1 — Usability & performance
- Task: Add windowing options (fixed, sliding, event-based) and min-periodicity parameter
  - Complexity: medium
  - Tests: parameterized tests across window types
- Task: Add JSON export with window-level detail and optionally compressed output
  - Complexity: low
- Task: Implement pruning optimizations (utility upper bounds, temporal pruning)
  - Complexity: medium-high
  - Tests: performance regression tests and correctness
- Task: Add plotting utilities / Jupyter notebooks for exploring results
  - Complexity: low-medium

P2 — Scalability & advanced features
- Task: Add parallel mining (per-window parallelization or partitioned dataset)
  - Complexity: high
- Task: Add numba/Cython acceleration for hot loops
  - Complexity: high
- Task: Add a web dashboard for interactive exploration and export
  - Complexity: high
- Task: Add streaming or incremental mining support for near-real-time analytics
  - Complexity: high

---

### Example experiments & acceptance criteria

- Reproduce a baseline experiment:
  - Given sample dataset `data/sample_transactions.csv` and params (min_utility=100, window=7d, min_periodicity=0.5), the CLI produces `results/baseline.csv` with expected counts and utilities (matches provided golden file).
- Windowing correctness:
  - For sliding windows, itemsets must be reported only when their periodicity across windows meets the threshold.
- Idempotency & reproducibility:
  - Given the same seed and parameters, an experiment run produces identical results and logs.

---

## Suggested repository structure

- phm/
  - __init__.py
  - loader.py
  - miner.py
  - utils.py
  - cli.py
  - evaluator.py
- data/
  - sample_transactions.csv
- notebooks/
  - demo.ipynb
- tests/
  - test_loader.py
  - test_miner.py
- requirements.txt
- Dockerfile
- README.md

---

## Performance tips & implementation notes

- Represent transactions in compact NumPy/Pandas structures for efficient aggregations.
- Precompute per-item utilities and frequency over windows to prune search space.
- Use memory-efficient data representations for large datasets; consider streaming readers.
- Wrap expensive loops with numba or move hot inner loops to Cython when needed.
- For parallel execution, prefer independent window jobs and aggregate results afterward to avoid synchronization overhead.

---

## Docker & reproducible experiments

Sample Dockerfile (high-level):
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "phm.cli", "run", "--input", "data/sample_transactions.csv", "--min-utility", "100"]
```

Use Docker to run experiments consistently across machines and CI.

---

## Contribution & code of conduct

- Please open issues for bugs, feature requests, or proposed enhancements.
- Use the `P0/P1/P2` labels when creating issue proposals to match this README's backlog.
- Add tests for new logic and update the experiment harness for new parameters.
- Consider adding CONTRIBUTING.md and CODE_OF_CONDUCT.md to standardize collaboration.

---

## License & maintainers

- License: MIT (change if you prefer another license)
- Maintainer: oggishi (https://github.com/oggishi)
- Contact: add an email or profile link in the repo

---

Thank you for checking out PHM_Periodic_High_Utility_itemsets — this README combines a professional overview, usage instructions, and a detailed Functions & Tasks backlog you can use to run reproducible experiments, create issues, and prioritize development.
