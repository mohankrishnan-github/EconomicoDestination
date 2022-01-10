from sqlalchemy import create_engine
import pandas as pd
import pymysql


def processReviews(airline, engine):
    """
    Output: x_df: airline dataframes created by extracting data from corresponding airline table in psql database
    dfs: list of all dataframes available for analysis
    """
    airline_df = pd.read_sql(f'SELECT * FROM {airline};', engine)
    dfs = [airline_df]
    for df in dfs:
        df['words'] = df['headline'] + ' ' + df['body']
        df['positive'] = df['rating'] > 5
        df['positive'] = df['positive'].apply(lambda x: 1 if x == True else 0)
        df['date_flown'] = pd.to_datetime(df['date_flown'])
        df['year'] = pd.DatetimeIndex(df['date_flown']).year
        df['month'] = pd.DatetimeIndex(df['date_flown']).month
    return dfs