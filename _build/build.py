import os
import pandas as pd
import json
import datetime
# import keras

# define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), '../_data/atdb.092116023143.ALL.csv')
fileOutPath = os.path.join(os.path.dirname(__file__), '../_data/stats.json')

# constants
TYPE_COL = 'type'
NAME_COL = 'name'
STATE_COL = 'state'
LAT_COL = 'lat'
LONG_COL = 'lon'
DATE_COL = 'dt_reached'
TO_SPRINGER_COL = 'to_spgr'
TO_KATAHDIN_COL = 'to_ktd'

ESTIMATED_START_DT = '2017-03-13'


def get_completed(df):
    return df[df[DATE_COL].notnull()]


def current_location(df):
    df = df.copy()  # work on a copy

    # concat name and state
    df[NAME_COL] = df[NAME_COL] + ', ' + df[STATE_COL]
    df.drop(STATE_COL, axis=1, inplace=True)

    # fix rounding issue with lat longs
    df[LAT_COL] = df[LAT_COL].apply(lambda x: "{:.4f}".format(x))
    df[LONG_COL] = df[LONG_COL].apply(lambda x: "{:.4f}".format(x))

    # find the completed sections
    completed = get_completed(df)[[LAT_COL, LONG_COL, DATE_COL, NAME_COL]]

    if len(completed) > 0:
        completed[DATE_COL] = completed[DATE_COL].dt.strftime('%Y-%m-%d')
        last_completed = completed.iloc[-1]
    else:
        last_completed = df.iloc[0]
        last_completed.set_value(DATE_COL, ESTIMATED_START_DT)

    return {'current_location': last_completed.to_dict()}


def miles_hiked_miles_remaining(df):
    miles_hiked = 0
    miles_remaining = df.ix[0, TO_KATAHDIN_COL]

    completed = get_completed(df)[[TO_SPRINGER_COL, TO_KATAHDIN_COL, DATE_COL]]

    if len(completed) > 0:
        last_completed = completed.iloc[-1]
        miles_hiked = last_completed[TO_SPRINGER_COL]
        miles_remaining = last_completed[TO_KATAHDIN_COL]

    return {'miles_hiked': miles_hiked, 'miles_remaining': miles_remaining}


def miles_hiked_per_day(df):
    completed = get_completed(df)[[DATE_COL, TO_SPRINGER_COL]]
    completed[DATE_COL] = completed[DATE_COL].dt.strftime('%Y-%m-%d')

    # need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed['to_spgr_shifted'] = completed.to_spgr.shift(1)

    # group by day
    f = {TO_SPRINGER_COL: 'last', 'to_spgr_shifted': 'first'}
    miles_per_day = completed.groupby(DATE_COL).agg(f)
    miles_per_day['miles'] = miles_per_day.to_spgr - miles_per_day.to_spgr_shifted

    # fix rounding issue by converting each mileage value into a string
    miles_per_day = miles_per_day['miles'].apply(lambda x: '{:.1f}'.format(x))

    return {'miles_per_day': miles_per_day.to_dict()}


def start_date(df):
    dt = datetime.datetime.strptime(ESTIMATED_START_DT, '%Y-%m-%d')

    completed = get_completed(df)

    if len(completed) > 0:
        dt = df.iloc[0][DATE_COL]

    # output is formatted like "Mar 3, 2017"
    return {'start_date': "{d:%b} {d.day}, {d.year}".format(d=dt)}


def days_on_trail(df):
    days = 0

    completed = get_completed(df)[DATE_COL]

    if len(completed) > 0:
        start = completed.iloc[0].date()
        end = completed.iloc[-1].date()
        days = (end - start).days + 1  # +1 to include the last day too

    return {'days_on_trail': days}


def estimated_completion(df):
    features = df[df[TYPE_COL] == 'FEATURE']

    return {'estimated_completion': '2017-08-15'}


if __name__ == "__main__":
    checkpoints = pd.read_csv(fileInPath, parse_dates=[DATE_COL], infer_datetime_format=True)

    cl = current_location(checkpoints)
    mhmr = miles_hiked_miles_remaining(checkpoints)
    mpd = miles_hiked_per_day(checkpoints)
    sd = start_date(checkpoints)
    dat = days_on_trail(checkpoints)
    ec = estimated_completion(checkpoints)

    # write json file
    with open(fileOutPath, 'w') as outfile:
        json.dump({**cl, **mhmr, **mpd, **sd, **dat, **ec}, outfile)
