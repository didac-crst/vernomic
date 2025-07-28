# ─────────────────────────────────────────────
# vernomic.py – core class logic
# ─────────────────────────────────────────────
"""
Vernomic Module

Provides the `Vernomic` class for generating human-friendly, mnemonic version
identifiers based on custom 4-week (28-day) cycles.

Each cycle is named after a vivid, object-based color, and each day within a cycle
uses an animal name. The full identifier includes date and time components
for uniqueness.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union, Optional
import os
import yaml
from pathlib import Path
from .constants import CYCLE_DAYS, CYCLE_NAMES

@dataclass
class Vernomic:
    """
    Generate a mnemonic version identifier using 4-week cycles.

    Attributes:
        root_name (str): Base name for the version (e.g., "model").
        suffix_name (str): Optional extra tag to append (e.g., "v1").
        file_extension (str): Extension for file naming (e.g., "h5", "pkl").
        date (datetime | int | float): Timestamp or datetime for naming.
    """
    root_name: str
    suffix_name: str = ""
    file_extension: str = ""
    date: Union[datetime, int, float] = datetime.now()

    def __post_init__(self):
        """Convert numeric timestamp to datetime if needed."""
        if isinstance(self.date, (int, float)):
            self.date = datetime.fromtimestamp(self.date)

    @property
    def cycle_and_day(self) -> dict[str, int]:
        """
        Compute cycle index and day index within that cycle.

        The year is divided into 13 cycles of 28 days (plus overflow).
        - cycle_number: 0-based index of the 28-day cycle.
        - day_of_cycle: 0-based index of the day within the 28-day cycle.

        Returns:
            dict: {
                "cycle_number": int,
                "day_of_cycle": int
            }
        """
        # Day of year: 1 through 365 (or 366)
        day_of_year = self.date.timetuple().tm_yday
        cycle_number = (day_of_year - 1) // 28
        day_of_cycle = (day_of_year - 1) % 28
        return {"cycle_number": cycle_number, "day_of_cycle": day_of_cycle}

    @property
    def day_name(self) -> str:
        """
        Combine cycle name and animal day name.

        Uses CYCLE_NAMES and CYCLE_DAYS to map indexes to names.

        Returns:
            str: "<CycleName>_<AnimalName>"
        """
        info = self.cycle_and_day
        cycle_label = CYCLE_NAMES[info["cycle_number"]]
        day_label = CYCLE_DAYS[info["day_of_cycle"]]
        return f"{cycle_label}_{day_label}"
    
    @property
    def version_time(self) -> str:
        """
        Format the time component for the identifier.

        Returns:
            str: Two-digit hour and two-digit minute (HHMM).
        """
        return f"{self.date.hour:02d}{self.date.minute:02d}"
    
    @property
    def version_year(self) -> str:
        """
        Format the year component for the identifier.

        Returns:
            str: Last two digits of the year (YY).
        """
        return str(self.date.year)[-2:]

    @property
    def vernomic_id(self) -> str:
        """
        Build the core Vernomic identifier string.

        Combines root_name, year, day_name, time, and optional suffix.

        Format:
            <root_name>_<YY>_<CycleName>_<AnimalName>_<HHMM>[_<suffix_name>]

        Returns:
            str: The full mnemonic version ID.
        """
        parts = [self.root_name, self.version_year, self.day_name, self.version_time]
        if self.suffix_name:
            parts.append(self.suffix_name)
        return "_".join(parts)

    @property
    def file_name(self) -> str:
        """
        Construct the filename with extension.

        Raises:
            ValueError: If `file_extension` is empty.

        Returns:
            str: "<vernomic_id>.<file_extension>"
        """
        if not self.file_extension:
            raise ValueError("`file_extension` must be set before calling file_name.")
        ext = self.file_extension.lstrip(".")
        return f"{self.vernomic_id}.{ext}"

    def to_yaml(self, path: str = "./", description: Optional[str] = None) -> None:
        """
        Export metadata to a YAML file.

        If `path` is a directory (path ends with os.sep or exists as a dir),
        the file will be saved as:
            <path>/<vernomic_id>.yaml
        Otherwise, if no extension is provided, ".yaml" is appended.

        Args:
            path (str | Path): Directory or file path for output.

        Raises:
            FileExistsError: If a parent path exists and is not a directory.
        """
        # Assemble metadata dictionary
        info = self.cycle_and_day
        data = {
            "vernomic_id": self.vernomic_id,
            "file_name": self.file_name,
            "root_name": self.root_name,
            "suffix_name": self.suffix_name,
            "file_extension": self.file_extension,
            "datetime_iso": self.date.isoformat(),
            "year": self.date.year,
            "month": self.date.month,
            "day": self.date.day,
            "hour": self.date.hour,
            "minute": self.date.minute,
            "second": self.date.second,
            "cycle_number": info["cycle_number"],
            "day_of_cycle": info["day_of_cycle"],
            "cycle_name": CYCLE_NAMES[info["cycle_number"]],
            "day_name": CYCLE_DAYS[info["day_of_cycle"]],
            "version_year": self.version_year,
            "version_day": self.day_name,
            "version_time": self.version_time,
        }
        if description:
            data["description"] = description

        # Normalize to Path
        p = Path(path)
        # Detect directory intent
        is_dir = str(path).endswith(os.sep) or p.is_dir()
        if is_dir:
            # Use vernomic_id as filename
            p = p / f"{self.vernomic_id}.yaml"

        # Ensure .yaml extension
        if not p.suffix:
            p = p.with_suffix(".yaml")

        # Validate parent directory
        parent = p.parent
        if parent.exists() and not parent.is_dir():
            raise FileExistsError(
                f"Cannot create directory {parent!r}: not a directory."
            )
        # Create directory if needed
        parent.mkdir(parents=True, exist_ok=True)

        # Write YAML file
        p.write_text(yaml.dump(data, sort_keys=False))

    def __str__(self) -> str:
        """
        Return the Vernomic identifier string.

        Equivalent to `self.vernomic_id`.

        Returns:
            str: The mnemonic version ID.
        """
        return self.vernomic_id