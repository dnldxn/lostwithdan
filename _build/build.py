import os
import pandas as pd
import json
# import keras

# define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), '../_data/atdb.092116023143.ALL.csv')
fileOutPath = os.path.join(os.path.dirname(__file__), '../_data/stats.json')

# column names
name_col = 'name'
state_col = 'state'
lat_col = 'lat'
long_col = 'lon'
date_col = 'dt_reached'
to_springer_col = 'to_spgr'
to_katahdin_col = 'to_ktd'

estimated_start_dt = '2017-03-09'


def get_completed(df):
    return df[df[date_col].notnull()]


def current_location(df):
    df = df.copy()  # work on a copy

    # concat name and state
    df[name_col] = df[name_col] + ', ' + df[state_col]
    df.drop(state_col, axis=1, inplace=True)

    # fix rounding issue with lat longs
    df[lat_col] = df[lat_col].apply(lambda x: "{:.2f}".format(x))
    df[long_col] = df[long_col].apply(lambda x: "{:.2f}".format(x))

    # find the completed sections
    completed = get_completed(df)[[lat_col, long_col, date_col, name_col]]

    if len(completed) > 0:
        completed[date_col] = completed[date_col].dt.strftime('%Y-%m-%d')
        last_completed = completed.iloc[-1]
    else:
        last_completed = df.iloc[0]
        last_completed.set_value(date_col, estimated_start_dt)

    return {'current_location': last_completed.to_dict()}


def miles_hiked_miles_remaining(df):
    miles_hiked = 0
    miles_remaining = df.ix[0, 'to_ktd']

    completed = get_completed(df)[[to_springer_col, to_katahdin_col, date_col]]

    if len(completed) > 0:
        last_completed = completed.iloc[-1]
        miles_hiked = last_completed[to_springer_col]
        miles_remaining = last_completed[to_katahdin_col]

    return {'miles_hiked': miles_hiked, 'miles_remaining': miles_remaining}


def miles_hiked_per_day(df):
    completed = get_completed(df)[[date_col, 'to_spgr']]
    completed['dt'] = completed[date_col].dt.strftime('%Y-%m-%d')

    # need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed['to_spgr_shifted'] = completed.to_spgr.shift(1)

    # group by day
    f = {'to_spgr': 'last', 'to_spgr_shifted': 'first'}
    miles_per_day = completed.groupby('dt').agg(f)
    miles_per_day['miles'] = miles_per_day.to_spgr - miles_per_day.to_spgr_shifted

    # fix rounding issue by converting each mileage value into a string
    miles_per_day = miles_per_day['miles'].apply(lambda x: '{:.1f}'.format(x))

    return {'miles_per_day': miles_per_day.to_dict()}


def start_date(df):
    completed = get_completed(df)[[date_col]]


def estimated_completion(df):
    features = df[df['type'] == 'FEATURE']

    return {'estimated_completion': '2017-08-15'}


if __name__ == "__main__":
    checkpoints = pd.read_csv(fileInPath, parse_dates=[date_col], infer_datetime_format=True)

    cl = current_location(checkpoints)
    mhmr = miles_hiked_miles_remaining(checkpoints)
    mpd = miles_hiked_per_day(checkpoints)
    ec = estimated_completion(checkpoints)

    # write json file
    with open(fileOutPath, 'w') as outfile:
        json.dump({**cl, **mhmr, **mpd, **ec}, outfile)
