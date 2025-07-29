[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

# Vernomic

A **mnemonic versioning system** on a four-week cycle that fuses vivid, object-based color names
with animals — making each release as memorable as it is meaningful.

    model_26_Indigo_Duck_0732_v1

This is useful for naming experiments, models, snapshots, or backups with more memorable identifiers than timestamps or UUIDs.

## 🔧 Installation

```bash
# Install from PyPI (development)
poetry install

# Or install directly from GitHub (SSH)
poetry add git+ssh://git@github.com/didac-crst/vernomic.git#main

# Alternatively, using pip
pip install git+ssh://git@github.com/didac-crst/vernomic.git
```

## 🔄 Compatibility & Requirements

- **Python**: ≥ 3.8  
- **Package Manager**: Poetry (recommended)  
- **Core Dependencies**:  
    - `PyYAML` (for `to_yaml` metadata export)  
- **Dev Dependencies**:  
    - `pytest` (unit testing)  
    - `hypothesis` (property-based testing)  

## 🧠 How it works

- The year is split into 13 cycles of 28 days.  
- Each cycle is given a vivid, object-based color name (`Amber`, `Golden`, etc.).  
- Each day in the cycle gets an animal name (`Tiger`, `Owl`, etc.).  
- The final name follows this structure:

    `<root>_<yy>_<CycleName>_<AnimalName>_<HHMM>_<suffix>`

## ⚙️ Initialization Options

When creating a `Vernomic` instance, you can customize the following additional parameters beyond the basics:

- `display_version_time` (bool, default `True`):  
    Include the time component (`HHMM`) in the generated identifier.  
- `divide_char` (str, default `"_"`):  
    Character used to separate each part of the version ID.  
- `description` (Optional[str], default `None`):  
    Free‑form text stored in the metadata YAML for human context.  
- `date` (`datetime` | `int` | `float`, default `datetime.now()`):  
    The point in time to base the identifier on.  
    - If you pass a Unix timestamp (`int`/`float`), it’s converted via `datetime.fromtimestamp(...)`.  
    - If you omit it, the current local datetime is used.

## 🐍 Example

```python
from vernomic import Vernomic
from datetime import datetime

v = Vernomic(
    root_name="model",
    suffix_name="v1",
    file_extension="pkl",
    display_version_time=True,
    divide_char="-",
    description="Baseline experiment",
    date=datetime(2025, 6, 24, 7, 32)
)
print(v)                # → model-25-Indigo-Duck-0732-v1
print(v.file_name)      # → model-25-Indigo-Duck-0732-v1.pkl
v.to_yaml("metadata/")  # writes metadata/model-26-Indigo-Duck-0732-v1.yaml
```

## 📝 Metadata Export

Use the `to_yaml(...)` method to record all relevant metadata to a `.yaml` file:

- Pass a **directory** (path ends with `/` or an existing folder) to auto-name  
    `<vernomic_id>.yaml` inside it.  
- Or pass a **file path** (with or without `.yaml`) to control the exact output.

The resulting YAML preserves key order and includes every attribute, for example:

```yaml
vernomic_id: model-25-Indigo-Duck-0732-v1
file_name: model-25-Indigo-Duck-0732-v1.pkl
root_name: model
suffix_name: v1
file_extension: pkl
datetime_iso: '2025-06-24T07:32:00'
year: 2025
month: 6
day: 24
hour: 7
minute: 32
second: 0
cycle_number: 6
day_of_cycle: 6
cycle_name: Indigo
day_name: Duck
version_year: '25'
version_day: Indigo-Duck
version_time: '0732'
description: Baseline experiment  # Only present if you set `description`
```

## 🧪 Running Tests

```bash
poetry run pytest -s --hypothesis-show-statistics
```

## 📁 Repository Structure

- `vernomic/` – main package code  
- `tests/` – unit & property-based tests using Hypothesis  
- `examples/` – sample scripts to generate names  

## 📜 License

MIT – do whatever you want, just give credit.
