"""
Prepare lighter CSV files for each visualization.

This script:
- reads the raw Steam dataset once
- keeps only the columns needed by each visualization
- applies preprocessing when it meaningfully reduces work at runtime
- writes smaller CSV files into assets/data/processed

Run from src/:
    python prepare_data.py
"""

from pathlib import Path
import pandas as pd

from viz1_scatter.preprocess import preprocess_data as preprocess_viz1
from viz2_box.preprocess import step1 as viz2_step1, step2 as viz2_step2
from viz3_line.preprocess import preprocess_data as preprocess_viz3
from viz4_bubble.preprocess import preprocess_data as preprocess_viz4
from viz5_dot.preprocess import compute_metrics as viz5_compute_metrics, filter_data as viz5_filter_data
from viz6_violin.preprocess import step1 as viz6_step1, step2 as viz6_step2


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "assets" / "data" / "games.csv"
OUTPUT_DIR = BASE_DIR / "assets" / "data" / "processed"


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} ({len(df):,} rows, {len(df.columns)} cols)")


def build_viz1(df_raw: pd.DataFrame) -> None:
    """
    Viz1 needs:
    - Name
    - Price
    - Estimated owners
    It also benefits from having preprocessing already done.
    """
    cols = ["Name", "Price", "Estimated owners"]
    df = df_raw[cols].copy()
    df = preprocess_viz1(df)

    keep_cols = [
        "Name",
        "Price",
        "Estimated owners",
        "Estimated owners (average)",
        "Type de jeu",
    ]
    df = df[keep_cols].copy()
    save_csv(df, "viz1_scatter.csv")


def build_viz2(df_raw: pd.DataFrame) -> None:
    """
    Viz2 needs:
    - Name
    - Estimated owners
    - Categories
    Precompute the sampled owners + game type classification once.
    """
    cols = ["Name", "Estimated owners", "Categories"]
    df = df_raw[cols].copy()
    df = viz2_step1(df)
    df = viz2_step2(df)

    keep_cols = [
        "Name",
        "Estimated owners",
        "Estimated owners (average)",
        "game_type",
    ]
    df = df[keep_cols].copy()
    save_csv(df, "viz2_box.csv")


def build_viz3(df_raw: pd.DataFrame) -> None:
    """
    Viz3 can be heavily reduced because the final chart uses an aggregated table.
    """
    cols = ["Release date", "Estimated owners", "Genres"]
    df = df_raw[cols].copy()
    df = preprocess_viz3(df)

    keep_cols = ["Year", "Genre", "Owners"]
    df = df[keep_cols].copy()
    save_csv(df, "viz3_line.csv")


def build_viz4(df_raw: pd.DataFrame) -> None:
    """
    Viz4 needs:
    - Name
    - Positive
    - Negative
    - Estimated owners
    Precompute visibility / satisfaction / owners average once.
    """
    cols = ["Name", "Positive", "Negative", "Estimated owners"]
    df = df_raw[cols].copy()
    df = preprocess_viz4(df)

    keep_cols = [
        "Name",
        "Positive",
        "Negative",
        "Estimated owners",
        "Estimated owners (average)",
        "Visibility",
        "Satisfaction",
    ]
    df = df[keep_cols].copy()
    save_csv(df, "viz4_bubble.csv")


def build_viz5(df_raw: pd.DataFrame) -> None:
    """
    Viz5 needs:
    - Name
    - Positive
    - Negative
    - Average playtime forever
    Precompute metrics once.
    """
    cols = ["Name", "Positive", "Negative", "Average playtime forever"]
    df = df_raw[cols].copy()
    df = viz5_compute_metrics(df)
    df = viz5_filter_data(df)

    keep_cols = [
        "Name",
        "Positive",
        "Negative",
        "Average playtime forever",
        "Visibility",
        "Satisfaction",
        "Satisfaction rounded",
        "Playtime hours",
    ]
    df = df[keep_cols].copy()
    save_csv(df, "viz5_dot.csv")


def build_viz6(df_raw: pd.DataFrame) -> None:
    """
    Viz6 needs:
    - Publishers
    - Name
    - Estimated owners
    - Tags
    Precompute publisher counts and cleaned categories once.
    """
    cols = ["Publishers", "Name", "Estimated owners", "Tags"]
    df = df_raw[cols].copy()
    df = viz6_step1(df)
    df = viz6_step2(df)

    keep_cols = [
        "publisher",
        "name",
        "estimated_owners",
        "Tags",
        "publisher_type",
        "estimated_owners_num",
        "nb_games_dev",
    ]
    # Keep Tags only if still present after preprocess
    keep_cols = [col for col in keep_cols if col in df.columns]
    df = df[keep_cols].copy()
    save_csv(df, "viz6_violin.csv")


def main() -> None:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found: {RAW_DATA_PATH}")

    ensure_output_dir()

    print(f"Reading raw dataset: {RAW_DATA_PATH}")
    df_raw = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded raw dataset: {len(df_raw):,} rows, {len(df_raw.columns)} cols")

    build_viz1(df_raw)
    build_viz2(df_raw)
    build_viz3(df_raw)
    build_viz4(df_raw)
    build_viz5(df_raw)
    build_viz6(df_raw)

    print("\nDone. Processed files are in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()