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
    start = datetime(2020, 1, 1)  # Start date and time
    for i in range(20):
        # Generate a random date and time
        dt = start + timedelta(days=random.randint(0, 10000)) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))  # Add time to the date
        add_description = random.choice([True, False])
        add_suffix = random.choice([True, False])
        display_version_time = random.choice([True, False])
        divide_char = random.choice(["_", "-"])
        if add_description:
            description = f"Example description {i + 1}"
        else:
            description = None
        if add_suffix:
            suffix_name = f"v{random.randint(1, 10)}"
        else:
            suffix_name = None
        vernomic = Vernomic(root_name=root_name,
                            suffix_name=suffix_name,
                            file_extension=file_extension,
                            display_version_time=display_version_time,
                            date=dt,
                            description=description,
                            divide_char=divide_char)
        print(f"Date: {dt.date()} -> {vernomic}")
        vernomic.to_yaml("../test_output/")