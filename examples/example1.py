# ─────────────────────────────────────────────
# example.py – usage example
# ─────────────────────────────────────────────

from datetime import datetime, timedelta
import random
from vernomic import Vernomic

if __name__ == "__main__":
    start = datetime(2023, 12, 20)  # Start date and time
    for i in range(20):
        dt = start + timedelta(days=i) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))  # Add time to the date
        vernomic = Vernomic(root_name="model", date=dt)
        print(f"Date: {dt.date()} -> {vernomic}")
