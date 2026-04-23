'''
Preprocessing module for the dot plot (viz5), using the Steam games dataset.

This module:
- computes satisfaction, visibility, rounded satisfaction, and playtime in hours
- filters invalid rows and sorts by visibility

These steps are required before plotting satisfaction vs playtime with colour by review volume.
'''
import pandas as pd

from utils.constants import (
    COL_NEG,
    COL_PLAYTIME,
    COL_PLAYTIME_FOREVER,
    COL_POS,
    COL_SAT,
    COL_SAT_ROUNDED,
    COL_VIS,
)


def compute_metrics(df):
    """
        Compute satisfaction, visibility, rounded satisfaction, and playtime (hours).

        Args:
            df (pd.DataFrame): Raw dataframe (games.csv).

        Returns:
            pd.DataFrame: Copy with derived columns COL_SAT, COL_VIS, COL_SAT_ROUNDED, COL_PLAYTIME.
    """
    df = df.copy()

    df[COL_VIS] = df[COL_POS] + df[COL_NEG]
    df[COL_SAT] = df[COL_POS] / df[COL_VIS]
    df[COL_SAT] = df[COL_SAT].fillna(0)
    df[COL_SAT_ROUNDED] = df[COL_SAT].round(1)
    df[COL_PLAYTIME] = df[COL_PLAYTIME_FOREVER] / 60

    return df


def filter_data(df):
    """
        Remove invalid rows and sort by ascending visibility.

        Args:
            df (pd.DataFrame): Dataframe after compute_metrics.

        Returns:
            pd.DataFrame: Filtered and sorted dataframe.
    """
    df = df[(df[COL_VIS] > 0) & (df[COL_PLAYTIME] >= 0)]
    df = df.sort_values(by=COL_VIS, ascending=True)

    return df
