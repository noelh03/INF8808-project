'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

#TODO: each function should have a specific purpose

def step1(my_df):
    '''
        #TODO: add detailed descriptions of the function and its arguments and return value

        Args:
            #TODO: add description of the arguments
        Returns:
            #TODO: add description of the return value
    '''
    my_df['nb_games_dev'] = my_df.groupby('Publishers')['Name'].transform('count')
    return my_df

def step2(my_df):
    '''
        #TODO: add detailed descriptions of the function and its arguments and return value

        Args:
            #TODO: add description of the arguments
        Returns:
            #TODO: add description of the return value
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
