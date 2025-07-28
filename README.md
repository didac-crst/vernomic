# Vernomic

**Mnemonic version generator** using a 4-week cycle logic. Combines gemstone/metals + animal names 
to create memorable version strings like:

    model_23_Turquoise_Monkey_1523

This is useful for naming experiments, models, snapshots, or backups with more memorable identifiers than timestamps or UUIDs.

## 🔧 Installation

```bash
poetry install
```

## 🧠 How it works

- The year is split into 13 cycles of 28 days.
- Each cycle is given a gemstone/metal name (`Amber`, `Gold`, etc.).
- Each day in the cycle gets an animal name (`Tiger`, `Owl`, etc.).
- The final name follows this structure:

    <root>_<yy>_<CycleName>_<AnimalName>_<HHMM>

## 🐍 Example

```python
from vernomic import Vernomic
from datetime import datetime

v = Vernomic(root_name="model", date=datetime(2025, 7, 28, 15, 23))
print(str(v))  # → model_25_Turquoise_Monkey_1523
```

## 🧪 Running Tests

```bash
poetry run pytest -s --hypothesis-show-statistics
```

## 📁 Repository Structure

- `vernomic/` – main package code
- `tests/` – unit & property-based tests using Hypothesis
- `examples/` – sample script to generate names

## 📜 License

[`MIT`](LICENSE) – do whatever you want, just give credit.
