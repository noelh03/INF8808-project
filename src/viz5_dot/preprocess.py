'''
    Contains some functions to preprocess the data used in the visualisation.
'''

from utils.constants import COL_POS, COL_NEG, COL_SAT, COL_VIS, COL_SAT_ROUNDED, COL_PLAYTIME, COL_PLAYTIME, COL_PLAYTIME_FOREVER


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
    df[COL_PLAYTIME] = df[COL_PLAYTIME_FOREVER] / 60

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
        (df[COL_VIS] > 0) &
        (df[COL_PLAYTIME] >= 0)
    ]
    df = df.sort_values(by=COL_VIS, ascending=True)

    return df