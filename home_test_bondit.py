import csv
import pandas as pd
from datetime import datetime, timedelta


# Load data into a pandas DataFrame
df = pd.read_csv('bigger_sample.csv')
# Define time rules 180/60 =3
time_rule = 3


def get_Sucsess(df, time_rule=3):

    TIME_RULE = timedelta(hours=time_rule)

    # if success not part of the df
    df['Success'] = range(len(df.index))

    # Clean up time columns and sort by arrival time
    df['Arrival'] = df['Arrival'].str.strip().apply(
        lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))
    df['Departure'] = df['Departure'].str.strip().apply(
        lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))

    # sort by Arrival time
    df = df.sort_values(by=['Arrival'])

    # new index for non deplication index
    df.index = range(len(df.index))

    # Calculate success column
    success_count = 0
    for idx, row in df.iterrows():
        time_success = pd.to_datetime(
            row['Departure']) - pd.to_datetime(row['Arrival']) >= TIME_RULE
        if time_success and (success_count < 20):
            df.loc[idx, 'Success'] = 'success'
            success_count += 1
        else:
            df.loc[idx, 'Success'] = 'fail'

    # Save updated DataFrame back to the CSV file
    return df


get_Sucsess(df)
