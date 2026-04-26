'''
    Contains some functions to preprocess the data used in the violin plot visualisation.
'''
import pandas as pd

OWNER_ORDER = [
    "0 - 20000",
    "20000 - 50000",
    "50000 - 100000",
    "100000 - 200000",
    "200000 - 500000",
    "500000 - 1000000",
    "1000000 - 2000000",
    "2000000 - 5000000",
    "5000000 - 10000000",
    "10000000 - 20000000",
]

def _parse_owner_range(x: str) -> float | None:
    '''
        Converts an "low - high" owner range string to its midpoint.
 
        Args:
            x: A string like "20000 - 50000"
        Returns:
            The midpoint as a float, or None if the format is unexpected
    '''
    if isinstance(x, str) and " - " in x:
        low, high = x.split(" - ")
        return (int(low) + int(high)) / 2
    return None

def step1(my_df):
    '''
        Adds a column counting how many games each publisher has released.
 
        Args:
            my_df: DataFrame with at least 'Publishers' and 'Name' columns
        Returns:
            The input DataFrame with an additional 'nb_games_dev' column
    '''
    my_df['nb_games_dev'] = my_df.groupby('Publishers')['Name'].transform('count')
    return my_df

def step2(my_df: pd.DataFrame) -> pd.DataFrame:
    '''
        Cleans and prepares data for the violin plot.
 
        Steps:
            - Drops rows with missing Publishers or Estimated owners
            - Renames columns to snake_case
            - Classifies publishers as Independent (indie tag) or Major
            - Computes a numeric midpoint for each owner range
            - Converts estimated_owners to an ordered Categorical
 
        Args:
            my_df: DataFrame with game data (expects Publishers, Name,
                   Estimated owners, Tags, nb_games_dev columns)
        Returns:
            Processed DataFrame ready for visualisation
    '''
    my_df = my_df.copy()
    my_df = my_df.dropna(subset=['Publishers', 'Estimated owners'])

    my_df = my_df.rename(columns={
        'Publishers': 'publisher',
        'Name': 'name',
        'Estimated owners': 'estimated_owners',
    })

    my_df['publisher_type'] = (
        my_df['Tags'].str.lower().str.contains('indie', na=False)
        .map({True: 'Independent', False: 'Major'})
    )

    my_df['estimated_owners_num'] = my_df['estimated_owners'].apply(_parse_owner_range)

    my_df['estimated_owners'] = pd.Categorical(
        my_df['estimated_owners'],
        categories=OWNER_ORDER,
        ordered=True,
    )

    return my_df
