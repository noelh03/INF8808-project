"""
Preprocessing module for the genre evolution line chart.

This module:
- converts Steam ownership intervals into numeric averages
- extracts the release year from the 'Release date' column
- explodes the comma-separated 'Genres' column (Steam store genres, not user Tags)
  so each game×genre pair is a row
- aggregates total estimated owners per (Year, Genre) pair
- excludes 2026 (incomplete data) and keeps years 1997–2025
- keeps every genre as its own series; minor genres become individual gray lines
"""

import numpy as np
import pandas as pd
from utils.constants import (COL_GENRES, COL_OWNERS, COL_YEAR, MAIN_GENRES, YEAR_MIN, YEAR_MAX)


def _parse_owners_range(value):
    """
    Convert an owners range like '20,000 - 50,000' into its numeric average.

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
    except (ValueError, AttributeError):
        return np.nan


def preprocess_data(df):
    """
    Transform the raw games DataFrame into a long-format year × genre table.

    Steps:
        1. Convert 'Estimated owners' ranges to numeric averages.
        2. Drop rows with missing year, zero owners, or missing genres.
        3. Filter to years YEAR_MIN–YEAR_MAX (excludes 2026).
        4. Split the comma-separated 'Genres' column and explode to one row per genre.
        5. Group by (Year, Genre) and sum the estimated owners.

    Each game contributes its owner count to every one of its Steam genres, so
    genres are not mutually exclusive.

    Args:
        df: The raw games DataFrame loaded from games.csv.

    Returns:
        pd.DataFrame: Long-format DataFrame with columns [Year, Genre, Owners].
    """
    df = df.copy()

    df["Owners_avg"] = df[COL_OWNERS].apply(_parse_owners_range)
    df[COL_YEAR] = pd.to_numeric(df[COL_YEAR], errors="coerce")

    if COL_GENRES not in df.columns:
        raise ValueError(
            f"Column '{COL_GENRES}' is missing from the dataset. "
            "Viz3 expects Steam 'Genres' (not user 'Tags')."
        )

    df = df.dropna(subset=[COL_YEAR, "Owners_avg", COL_GENRES])
    df = df[df[COL_GENRES].astype(str).str.strip() != ""]
    df = df[df["Owners_avg"] > 0]
    df[COL_YEAR] = df[COL_YEAR].astype(int)
    df = df[(df[COL_YEAR] >= YEAR_MIN) & (df[COL_YEAR] <= YEAR_MAX)]

    df["Genres_list"] = df[COL_GENRES].astype(str).str.split(",")
    df_exploded = df.explode("Genres_list")
    df_exploded["Genre"] = df_exploded["Genres_list"].str.strip()
    df_exploded = df_exploded[df_exploded["Genre"] != ""]

    df_agg = (
        df_exploded
        .groupby([COL_YEAR, "Genre"])["Owners_avg"]
        .sum()
        .rename("Owners")
    )

    # Reindex so every genre has a row for every year in range,
    # filling missing year-genre pairs with 0 (e.g. "Free To Play" before 2007).
    all_years = range(YEAR_MIN, YEAR_MAX + 1)
    all_genres = df_agg.index.get_level_values("Genre").unique()
    full_index = pd.MultiIndex.from_product([all_years, all_genres],
                                            names=[COL_YEAR, "Genre"])
    df_agg = df_agg.reindex(full_index, fill_value=0).reset_index()
    df_agg = df_agg.rename(columns={COL_YEAR: "Year"})

    df_long = df_agg.sort_values(["Genre", "Year"]).reset_index(drop=True)

    return df_long


def get_other_genres(df_long):
    """
    Return the sorted list of genre names present in the long DataFrame
    that are not in MAIN_GENRES.

    Args:
        df_long: Long-format DataFrame produced by preprocess_data.

    Returns:
        list[str]: Sorted list of minor genre names.
    """
    all_genres = df_long["Genre"].unique().tolist()
    return sorted([g for g in all_genres if g not in MAIN_GENRES])
