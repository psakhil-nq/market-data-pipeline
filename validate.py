import pandas as pd


def validate_data(data):

    missing_values = data.isnull().sum()
    duplicate_count = data.index.duplicated().sum()

    has_duplicates = duplicate_count > 0
    timestamps_ordered = data.index.is_monotonic_increasing

    gaps = data.index.to_series().diff()
    large_gaps = gaps[gaps > pd.Timedelta("00:01:00")]

    has_missing_values = missing_values.any()

    return {
        "passed": not has_missing_values and not has_duplicates and timestamps_ordered,
        "missing_values": missing_values,
        "duplicate_count": duplicate_count,
        "timestamps_ordered": timestamps_ordered,
        "large_gaps": large_gaps,
    }