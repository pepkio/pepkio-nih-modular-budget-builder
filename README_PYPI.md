# pepkio-nih-modular-budget-builder

Python client for the Pepkio NIH Modular Budget Builder REST API.

## What It Does

`pepkio-nih-modular-budget-builder` provides a Python client and CLI to convert personnel effort and salary into NIH modular budget modules ($25,000 increments) with cap-limited salary, fringe, F&A, consortium direct/F&A split, and PHS398 personnel justification text.

## Features

- **Salary Cap & Fringe Calculation**: Automatically computes cap-limited allowable salary and institutional cost sharing for 12-month calendar or 9-month academic appointments.
- **Modular Modules**: Groups direct costs into $25K NIH modular budget modules up to the $250K threshold.
- **Effort Ledger**: Tracks cross-grant effort across multiple grant commitments and flags over-commitment (>100%).
- **PHS398 Justification**: Generates formatted PHS398 personnel justification text.
- **Python API & CLI**: Full programmatic interface via `PepkioClient` and `pepkio-nih-modular-budget-builder` CLI.

## Installation

```bash
pip install pepkio-nih-modular-budget-builder
```

## Quick Start

```python
import os
from pepkio_nih_modular_budget_builder import PepkioClient

api_key = os.getenv("PEPKIO_API_KEY")

with PepkioClient(api_key=api_key) as client:
    # Run calculating an R01 budget example
    inp = client.get_example_input("calculate_r01")
    result = client.run(inp)
    
    print("Status:", result.status)
    print("Run ID:", result.run_id)
    print("Personnel Justification:\n", result.result["result"]["personnelJustification"])
```

## CLI Interface

```bash
export PEPKIO_API_KEY="your-api-key"

# View tool manifest
pepkio-nih-modular-budget-builder manifest

# Run example
pepkio-nih-modular-budget-builder run --example calculate_r01

# Run custom JSON input
pepkio-nih-modular-budget-builder run --input-json '{"action": "load_example"}'
```

## Web Application

Web UI: https://www.pepkio.com/tools/nih-modular-budget-builder
