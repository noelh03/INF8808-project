'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import numpy as np
import pandas as pd

COL_POS = "Positive"
COL_NEG = "Negative"
COL_OWNERS = "Estimated owners"
COL_OWNERS_AVG = "Estimated owners (average)"
COL_NAME = "Name"

COL_SAT = "Satisfaction"
COL_VIS = "Visibility"


def convert_owners_range_to_avg(value):
    """
    Convert an owners range like '20,000-50,000' into its numeric average.
    """
    if pd.isna(value):
        return np.nan

    try:
        value = str(value).replace(",", "").strip()
        low, high = [part.strip() for part in value.split("-")]
        return (int(low) + int(high)) / 2
    except:
        return np.nan


def compute_metrics(df):
    """
    Compute satisfaction and visibility metrics.
    """
    df = df.copy()

    df[COL_VIS] = df[COL_POS] + df[COL_NEG]
    df[COL_SAT] = df[COL_POS] / df[COL_VIS]
    df[COL_SAT] = df[COL_SAT].fillna(0)

    return df


def add_average_owners(df):
    """
    Add numeric owners column.
    """
    df = df.copy()
    df[COL_OWNERS_AVG] = df[COL_OWNERS].apply(convert_owners_range_to_avg)
    return df


def clean_data(df):
    """
    Remove invalid rows.
    """
    df = df.copy()

    df = df.dropna(subset=[COL_SAT, COL_VIS, COL_OWNERS_AVG, COL_NAME])
    df = df[df[COL_VIS] > 0]
    df = df[df[COL_OWNERS_AVG] > 0]

    return df


def preprocess_data(df):
    """
    Full preprocessing pipeline.
    """
    df = compute_metrics(df)
    df = add_average_owners(df)
    df = clean_data(df)
    return df