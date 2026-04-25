'''
Preprocessing module for the beeswarm plot visualization, using the Steam dataset.

This module:
- converts Steam ownership intervals into numeric sampled values (log-uniform)
- classifies games by play mode (Solo, Hybride, Multijoueur)
- filters out games with unknown owners or unclassified play modes

These transformations are required to enable quantitative visual analysis for the beeswarm plot.
'''
import numpy as np
import pandas as pd
from utils.constants import (COL_CATEGORIES, COL_OWNERS, COL_OWNERS_AVG, COL_GAME_TYPE, SOLO_KEYWORDS, MULTI_KEYWORDS, COL_NAME)

def _parse_owners_bounds(value):
    """
    Parse an owners range string like '20,000 - 50,000' into (low, high) integers.

    Args:
        value: Raw value from the 'Estimated owners' column.

    Returns:
        tuple: (low, high) as integers, or (np.nan, np.nan) if parsing fails.
    """
    if pd.isna(value):
        return np.nan, np.nan
    try:
        value = str(value).replace(",", "").strip()
        parts = value.split(" - ")
        if len(parts) == 2:
            return int(parts[0].strip()), int(parts[1].strip())
        return np.nan, np.nan
    except (ValueError, AttributeError):
        return np.nan, np.nan


def _sample_owners_range_log(low, high, rng):
    """
    Sample a single value log-uniformly within [low, high].

    Uses log-uniform sampling so points spread evenly on the log-scale x-axis.
    For ranges starting at 0 (e.g. "0 - 20,000"), the lower bound is clamped
    to high/10 to keep the swarm concentrated and visually dense.

    Args:
        low: Lower bound (may be 0).
        high: Upper bound.
        rng: numpy Generator instance.

    Returns:
        float: Sampled value, or np.nan if bounds are invalid.
    """
    if np.isnan(low) or np.isnan(high):
        return np.nan
    low = int(low)
    high = int(high)
    if low == 0:
        low = high // 10
    low = max(1, low)
    if low >= high:
        return float(low)
    return float(np.exp(rng.uniform(np.log(low), np.log(high))))


def _classify_game_type(genres_str):
    """
    Classify a game as Solo, Hybride, or Multijoueur based on its categories.

    Args:
        genres_str: Comma-separated string of Steam categories.

    Returns:
        str: One of 'Solo', 'Hybride', 'Multijoueur', or 'Autre'.
    """
    if pd.isna(genres_str):
        return "Autre"
    genres = str(genres_str)
    has_solo = any(kw in genres for kw in SOLO_KEYWORDS)
    has_multi = any(kw in genres for kw in MULTI_KEYWORDS)
    if has_solo and has_multi:
        return "Hybride"
    if has_multi:
        return "Multijoueur"
    if has_solo:
        return "Solo"
    return "Autre"


def sample_owners_and_classify(df):
    """
    Sample a random owner count within each game's ownership range (log-uniform)
    and classify each game by play mode.

    Args:
        df: Raw games DataFrame.

    Returns:
        pd.DataFrame: DataFrame with added 'Estimated owners (average)' and 'game_type' columns.
    """
    df = df.copy()
    rng = np.random.default_rng(42)
    bounds = df[COL_OWNERS].apply(_parse_owners_bounds)
    lows = bounds.apply(lambda b: b[0])
    highs = bounds.apply(lambda b: b[1])
    df[COL_OWNERS_AVG] = [
        _sample_owners_range_log(l, h, rng)
        for l, h in zip(lows, highs)
    ]
    df[COL_GAME_TYPE] = df[COL_CATEGORIES].apply(_classify_game_type)
    return df


def filter_valid_games(df):
    """
    Filter to games with known owners and a classified play mode.
    Removes games with zero owners and unclassified types.

    Args:
        df: DataFrame from sample_owners_and_classify.

    Returns:
        pd.DataFrame: Cleaned DataFrame ready for plotting.
    """
    df = df.copy()
    df = df.dropna(subset=[COL_OWNERS_AVG, COL_NAME])
    df = df[df[COL_OWNERS_AVG] > 0]
    df = df[df[COL_GAME_TYPE] != "Autre"]
    return df
