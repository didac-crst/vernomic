# ─────────────────────────────────────────────
# vernomic.py – core class logic
# ─────────────────────────────────────────────

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union
from .constants import CYCLE_DAYS, CYCLE_NAMES

@dataclass
class Vernomic:
    """Represents a version name generator using custom 4-week cycles."""

    root_name: str
    date: Union[datetime, int, float]

    def __post_init__(self):
        """Ensure `self.date` is a datetime object."""
        if isinstance(self.date, (int, float)):
            self.date = datetime.fromtimestamp(self.date)

    @property
    def cycle_and_day(self) -> dict[str, int]:
        """
        Compute cycle and day within the 28-day cycle.

        Returns:
            dict: {"cycle_number": int, "day_of_cycle": int}
        """
        day_of_year = self.date.timetuple().tm_yday
        cycle_number = (day_of_year - 1) // 28
        day_of_cycle = (day_of_year - 1) % 28
        return {
            "cycle_number": cycle_number,
            "day_of_cycle": day_of_cycle
        }

    @property
    def day_name(self) -> str:
        """
        Generate the combined name using the cycle name and day name.

        Returns:
            str: <CycleName>_<AnimalName>
        """
        cycle_info = self.cycle_and_day
        cycle_name = CYCLE_NAMES[cycle_info['cycle_number'] % len(CYCLE_NAMES)]
        cycle_day = CYCLE_DAYS[cycle_info['day_of_cycle'] % len(CYCLE_DAYS)]
        return f"{cycle_name}_{cycle_day}"

    def __str__(self) -> str:
        """
        Format the full Vernomic identifier.

        Returns:
            str: <root_name>_<yy>_<CycleName>_<AnimalName>_<HHMM>
        """
        year = str(self.date.year)[-2:]  # Last two digits of year
        time = f"{self.date.hour:02d}{self.date.minute:02d}"
        return f"{self.root_name}_{year}_{self.day_name}_{time}"