import pandas as pd


def preprocess(df, region_df):
    
    # filter for summer olympics
    df = df[df.Season == 'Summer']

    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # drop duplicates
    df.drop_duplicates(inplace=True)

    # one-hot encode medals column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    df['Gold'] = df['Gold'].astype('int')
    df['Silver'] = df['Silver'].astype('int')
    df['Bronze'] = df['Bronze'].astype('int')

    return df