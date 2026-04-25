'''
Preprocessing module for the scatter plot visualization, using the Steam dataset.

This module:
- converts Steam ownership intervals into numeric averages
- cleans missing values
- creates a categorical variable distinguishing free and paid games

These transformations are required to enable quantitative visual analysis for the scatter plot.
'''
import numpy as np
import pandas as pd

from utils.constants import (
    COL_ESTIMATED_OWNERS,
    COL_ESTIMATED_OWNERS_AVG,
    COL_PRICE,
    COL_NAME,
    COL_TYPE
)


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


def add_average_estimated_owners(df):
    """
        Add numeric estimated owners column.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The dataframe with the added column for average estimated owners.
    """
    df = df.copy()
    df[COL_ESTIMATED_OWNERS_AVG] = df[COL_ESTIMATED_OWNERS].apply(
        convert_owners_range_to_avg
    )
    return df


def clean_price_and_game_type(df):
    """
        Clean price values and create the game type column.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The cleaned dataframe with the game type column added.
    """
    df = df.copy()

    df[COL_PRICE] = pd.to_numeric(df[COL_PRICE], errors="coerce")
    df = df.dropna(subset=[COL_PRICE, COL_ESTIMATED_OWNERS_AVG, COL_NAME])
    df = df[df[COL_ESTIMATED_OWNERS_AVG] > 0]

    df[COL_TYPE] = np.where(df[COL_PRICE] == 0, "Gratuit", "Payant")

    return df


def preprocess_data(df):
    """
        Full preprocessing pipeline.
        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
        Returns:
            pd.DataFrame: The preprocessed dataframe, ready for visualization.
    """
    df = add_average_estimated_owners(df)
    df = clean_price_and_game_type(df)
    return df