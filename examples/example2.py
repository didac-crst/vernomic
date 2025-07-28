# ─────────────────────────────────────────────
# example.py – usage example
# ─────────────────────────────────────────────

from datetime import datetime, timedelta
import random
from vernomic import Vernomic

if __name__ == "__main__":
    # Generate 20 random dates starting from a specific date
    file_extension = ".h5"
    root_name = "model"
    suffix_name = "v1"
    start = datetime(2024, 1, 1)  # Start date and time
    for i in range(20):
        dt = start + timedelta(days=random.randint(0, 1000)) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))  # Add time to the date
        vernomic = Vernomic(root_name=root_name, suffix_name=suffix_name, file_extension=file_extension, date=dt)
        print(f"Date: {dt.date()} -> {vernomic}")
        vernomic.to_yaml("../test_output/")