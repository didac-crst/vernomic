# Vernomic

**Mnemonic version generator** using a 4-week cycle logic. Combines gemstone/metals + animal names 
to create memorable version strings like:

    model_23_Turquoise_Monkey_1523

## Usage

```python
from vernomic import Vernomic
from datetime import datetime

v = Vernomic(root_name="model", date=datetime.now())
print(str(v))  # → model_25_Gold_Owl_1430
```
