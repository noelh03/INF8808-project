'''
Preprocessing module for the bubble plot visualization, using the steam dataset.

This module:
- converts Steam ownership intervals into numeric averages
- computes satisfaction and visibility metrics
- cleans missing values

These transformations are required to enable quantitative visual analysis for the bubble plot.
'''
import numpy as np
import pandas as pd

from utils.constants import (COL_NAME, COL_OWNERS, COL_POS, COL_NEG, COL_SAT, COL_VIS, COL_OWNERS_AVG)


def convert_owners_range_to_avg(value):
    """
        Convert an owners range like '20,000-50,000' into its numeric average.
        Args: 
            value (str): The input string representing the owners range.
        Returns:
            float: The average number of owners, or NaN if the input is invalid.
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
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The dataframe with the computed metrics for satisfaction and visibility.
    """
    df = df.copy()

    df[COL_VIS] = df[COL_POS] + df[COL_NEG]
    df[COL_SAT] = df[COL_POS] / df[COL_VIS]
    df[COL_SAT] = df[COL_SAT].fillna(0)

    return df


def add_average_owners(df):
    """
        Add numeric owners column.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The dataframe with the added column for average owners.
    """
    df = df.copy()
    df[COL_OWNERS_AVG] = df[COL_OWNERS].apply(convert_owners_range_to_avg)
    return df


def clean_data(df):
    """
        Remove invalid rows.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The dataframe with invalid rows removed.
    """
    df = df.copy()

    df = df.dropna(subset=[COL_SAT, COL_VIS, COL_OWNERS_AVG, COL_NAME])
    df = df[df[COL_VIS] > 0]
    df = df[df[COL_OWNERS_AVG] > 0]

    return df


def preprocess_data(df):
    """
        Full preprocessing pipeline.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The preprocessed dataframe, ready for visualization.
    """
    df = compute_metrics(df)
    df = add_average_owners(df)
    df = clean_data(df)
    return df