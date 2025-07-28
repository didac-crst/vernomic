from datetime import datetime
from vernomic import Vernomic, CONSTANTS

from hypothesis import given, strategies as st

# Aliases for better readability
CYCLE_DAYS = CONSTANTS["CYCLE_DAYS"]
CYCLE_NAMES = CONSTANTS["CYCLE_NAMES"]

# Strategy to generate any datetime in a year
@st.composite
def datetimes_within_year(draw):
    year = draw(st.integers(min_value=2000, max_value=2100))
    day_of_year = draw(st.integers(min_value=1, max_value=365))
    hour = draw(st.integers(min_value=0, max_value=23))
    minute = draw(st.integers(min_value=0, max_value=59))
    return datetime.strptime(f"{year} {day_of_year} {hour} {minute}", "%Y %j %H %M")


@given(date=datetimes_within_year(), root_name=st.text(min_size=1, max_size=20))
def test_cycle_and_day_ranges(date, root_name):
    """Ensure cycle and day indexes are within bounds."""
    v = Vernomic(root_name=root_name, date=date)
    c = v.cycle_and_day
    assert 0 <= c["cycle_number"] < 366 // 28 + 1  # max possible weeks
    assert 0 <= c["day_of_cycle"] < 28
    print(f"Cycle: {c['cycle_number']}, Day: {c['day_of_cycle']} for date {date}")


@given(date=datetimes_within_year(), root_name=st.text(min_size=1, max_size=20))
def test_day_name_validity(date, root_name):
    """Check that day_name components are in the predefined lists."""
    v = Vernomic(root_name=root_name, date=date)
    cycle, day = v.day_name.split("_")
    assert cycle in CYCLE_NAMES
    assert day in CYCLE_DAYS
    print(f"Day Name: {v.day_name} for date {date}")


@given(date=datetimes_within_year(), root_name=st.text(min_size=4, max_size=10, alphabet=st.characters(whitelist_categories=("Ll", "Lu"))))
def test_str_output_format(date, root_name):
    """Ensure the __str__ output contains expected components and structure."""
    v = Vernomic(root_name=root_name, date=date)
    output = str(v)

    parts = output.split("_")
    assert parts[0] == root_name
    assert len(parts[1]) == 2 and parts[1].isdigit()  # year
    assert parts[2] in CYCLE_NAMES
    assert parts[3] in CYCLE_DAYS
    assert len(parts[4]) == 4 and parts[4].isdigit()  # HHMM
    print(f"String Output: {output} for date {date}")
