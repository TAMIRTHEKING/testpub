import csv
import pandas as pd
from datetime import datetime, timedelta


def get_Sucsess(df, time_rule=3):

    TIME_RULE = timedelta(hours=time_rule)

    # if success not part of the df
    df['success'] = range(len(df.index))

    # Clean up time columns and sort by arrival time
    df['Arrival'] = df['Arrival'].str.strip().apply(
        lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))
    df['Departure'] = df['Departure'].str.strip().apply(
        lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))

    # sort by Arrival time
    df = df.sort_values(by=['Arrival'])

    # Calculate success column
    success_count = 0
    for idx, row in df.iterrows():
        time_success = pd.to_datetime(
            row['Departure']) - pd.to_datetime(row['Arrival']) >= TIME_RULE
        if time_success and (success_count < 20):
            df.loc[idx, 'success'] = 'success'
            success_count += 1
        else:
            df.loc[idx, 'success'] = 'fail'

    # Save updated DataFrame back to the CSV file
    return df
