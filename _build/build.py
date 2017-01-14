import os
import pandas as pd
import json
# import keras

# define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), '../_data/atdb.092116023143.ALL.csv')
fileOutPath = os.path.join(os.path.dirname(__file__), '../_data/stats.json')

# column names
dtCol = 'dt_reached'
estimated_start_dt = '2017-03-09'


def current_location(df):
    completed = df[df[dtCol].notnull()][['lat', 'lon', dtCol]]

    if len(completed) > 0:
        completed[dtCol] = completed[dtCol].dt.strftime('%Y-%m-%d')
        last_completed = completed.iloc[-1]
    else:
        last_completed = df.iloc[0]
        last_completed.set_value(dtCol, estimated_start_dt)

    return {'current_location': last_completed.to_dict()}


def miles_hiked_per_day(df):
    completed = df[df[dtCol].notnull()][[dtCol, 'to_spgr']]
    completed['dt'] = completed[dtCol].dt.strftime('%Y-%m-%d')

    # need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed['to_spgr_shifted'] = completed.to_spgr.shift(1)

    # group by day
    group_day = completed.groupby('dt')

    f = {'to_spgr': 'last', 'to_spgr_shifted': 'first'}
    miles_per_day = group_day.agg(f)
    miles_per_day['miles'] = miles_per_day.to_spgr - miles_per_day.to_spgr_shifted

    # TODO: Rounding issue with unit tests
    return {'miles_per_day': miles_per_day.to_dict()}


def estimated_completion(df):
    features = df[df['type'] == 'FEATURE']

    return {'estimated_completion': '2017-08-15'}


if __name__ == "__main__":
    checkpoints = pd.read_csv(fileInPath, index_col='id', parse_dates=[dtCol], infer_datetime_format=True)

    cl = current_location(checkpoints)
    mpd = miles_hiked_per_day(checkpoints)
    ec = estimated_completion(checkpoints)

    # write json file
    with open(fileOutPath, 'w') as outfile:
        json.dump([cl, mpd, ec], outfile)
