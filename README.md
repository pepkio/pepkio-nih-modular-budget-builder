# pepkio-nih-modular-budget-builder

Python client for Pepkio NIH Modular Budget Builder tool.

## Installation

```bash
pip install pepkio-nih-modular-budget-builder
```

## Quick Start

```python
from pepkio_nih_modular_budget_builder import PepkioClient

with PepkioClient() as client:
    result = client.run({"action": "load_example"})
    print(result.status)
    print(result.result)
```

## CLI Usage

```bash
pepkio-nih-modular-budget-builder manifest
pepkio-nih-modular-budget-builder run --example calculate_r01
```
