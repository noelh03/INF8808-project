'''
    Contains some functions to preprocess the data used in the visualisation.
'''

COL_POS = "Positive"
COL_NEG = "Negative"
COL_PLAYTIME = "Average playtime forever"
COL_NAME = "Name"

COL_VIS = "Visibility"
COL_SAT = "Satisfaction"
COL_SAT_ROUNDED = "Satisfaction rounded"
COL_PLAYTIME_HOURS = "Playtime hours"


def compute_metrics(df):
    '''
        Compute satisfaction, visibility and playtime.

        Args:
            df: Raw dataset

        Returns:
            pd.DataFrame: Enriched dataset
    '''
    df = df.copy()

    df[COL_VIS] = df[COL_POS] + df[COL_NEG]
    df[COL_SAT] = df[COL_POS] / df[COL_VIS]
    df[COL_SAT] = df[COL_SAT].fillna(0)
    df[COL_SAT_ROUNDED] = df[COL_SAT].round(1)
    df[COL_PLAYTIME_HOURS] = df[COL_PLAYTIME] / 60

    return df


def filter_data(df):
    '''
        Filter invalid rows and sort by visibility

        Args:
            df : The dataframe to filter

        Returns:
            DataFrame
    '''
    df = df[
        (df["Visibility"] > 0) &
        (df["Playtime hours"] >= 0)
    ]
    df = df.sort_values(by="Visibility", ascending=True)

    return df