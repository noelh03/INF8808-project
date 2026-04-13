'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

def step1(my_df):
    '''
        Computes the number of games published by each publisher (developer experience).

        Args:
            my_df: The input DataFrame containing game data with 'Publishers' and 'Name' columns
        Returns:
            DataFrame: The input DataFrame with an additional 'nb_games_dev' column
    '''
    my_df['nb_games_dev'] = my_df.groupby('Publishers')['Name'].transform('count')
    return my_df

def step2(my_df):
    '''
        Cleans and prepares data for the violin plot: removes missing values, renames columns,
        classifies publishers as Independent/Major, and orders estimated owners categories.

        Args:
            my_df: The input DataFrame with game data
        Returns:
            DataFrame: Processed DataFrame ready for visualization
    '''
    my_df = my_df.copy()
    my_df = my_df.dropna(subset=['Publishers', 'Estimated owners'])

    my_df = my_df.rename(columns={
        'Publishers': 'publisher',
        'Name': 'name',
        'Estimated owners': 'estimated_owners'
    })

    my_df['publisher_type'] = my_df['Tags'].str.lower().str.contains('indie', na=False).map(
        {True: 'Independent', False: 'Major'}
    )

    def parse_range(x):
        if isinstance(x, str) and " - " in x:
            low, high = x.split(" - ")
            return (int(low) + int(high)) / 2
        return None

    my_df['estimated_owners_num'] = my_df['estimated_owners'].apply(parse_range)

    order = [
        "0 - 20000",
        "20000 - 50000",
        "50000 - 100000",
        "100000 - 200000",
        "200000 - 500000",
        "500000 - 1000000",
        "1000000 - 2000000",
        "2000000 - 5000000",
        "5000000 - 10000000",
        "10000000 - 20000000"
    ]

    my_df['estimated_owners'] = pd.Categorical(
        my_df['estimated_owners'],
        categories=order,
        ordered=True
    )

    return my_df
