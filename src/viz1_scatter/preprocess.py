"""
Preprocessing module for Steam dataset.

This module:
- converts Steam ownership intervals into numeric averages
- cleans missing values
- creates a categorical variable distinguishing free vs paid games

These transformations are required to enable quantitative visual analysis.
"""

import numpy as np
import pandas as pd
from utils.constants import (COL_ESTIMATED_OWNERS, COL_ESTIMATED_OWNERS_AVG, COL_PRICE, COL_NAME, COL_TYPE)


def convert_owners_range_to_avg(value):
    """
    Convert an owners range like '20,000-50,000' into its numeric average.

    Args:
        value: Raw value from the 'Estimated owners' column.

    Returns:
        float: Average of the lower and upper bounds, or np.nan if parsing fails.
    """
    if pd.isna(value):
        return np.nan

    try:
        value = str(value).replace(",", "").strip()
        low, high = [part.strip() for part in value.split("-")]
        return (int(low) + int(high)) / 2
    except ValueError:
        return np.nan


def add_average_estimated_owners(df):
    """
    Add a numeric average owners column derived from the owners range column.
    """
    if COL_ESTIMATED_OWNERS not in df.columns:
        raise ValueError(f"Colonne manquante : {COL_ESTIMATED_OWNERS}")

    df = df.copy()
    df[COL_ESTIMATED_OWNERS_AVG] = df[COL_ESTIMATED_OWNERS].apply(convert_owners_range_to_avg)
    return df


def clean_price_and_game_type(df):
    """
    Clean the price column, remove invalid rows, and create the game type label.
    """
    required_columns = [COL_PRICE, COL_ESTIMATED_OWNERS_AVG, COL_NAME]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    df = df.copy()
    df[COL_PRICE] = pd.to_numeric(df[COL_PRICE], errors="coerce")
    df = df.dropna(subset=[COL_PRICE, COL_ESTIMATED_OWNERS_AVG, COL_NAME])
    df = df[df[COL_ESTIMATED_OWNERS_AVG] > 0]

    df[COL_TYPE] = np.where(df[COL_PRICE] == 0, "Gratuit", "Payant")

    return df


def preprocess_data(df):
    """
    Run the full preprocessing pipeline.
    """
    df = add_average_estimated_owners(df)
    df = clean_price_and_game_type(df)
    return df