import os
import pandas as pd
import json

# define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), '../_data/atdb.092116023143.ALL.csv')
fileOutPath = os.path.join(os.path.dirname(__file__), '../_data/stats.json')

# column names
dtCol = 'dt_reached'


def get_current_location(df):
    completed = df[df[dtCol].notnull()][['lat', 'lon', dtCol]]
    completed[dtCol] = completed[dtCol].dt.strftime('%Y-%m-%d')
    last_completed = completed.iloc[-1]

    return {'current_location': last_completed.to_dict()}


def get_miles_hiked_per_day(df):
    completed = df[df[dtCol].notnull()][[dtCol, 'to_spgr']]
    completed['dt'] = completed[dtCol].dt.strftime('%Y-%m-%d')

    # need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed['to_spgr_shifted'] = completed.to_spgr.shift(1)

    # group by day
    group_day = completed.groupby('dt')

    f = {'to_spgr': 'last', 'to_spgr_shifted': 'first'}
    miles_per_day = group_day.agg(f)
    miles_per_day['miles'] = miles_per_day.to_spgr - miles_per_day.to_spgr_shifted

    return {'miles_per_day': miles_per_day['miles'].to_dict()}


def get_estimated_completion(df):
    features = df[df['type'] == 'FEATURE']

    return {'estimated_completion': '2017-08-15'}


df = pd.read_csv(fileInPath, index_col='id', parse_dates=[dtCol], infer_datetime_format=True)
# print(df[:5])
# print("\n\n")

# buffer to store output
out = []


cl = get_current_location(df)
mpd = get_miles_hiked_per_day(df)
ec = get_estimated_completion(df)


print("\n")
print(json.dumps([cl, mpd, ec]))


# write json file
with open(fileOutPath, 'w') as outfile:
    json.dump([cl, mpd, ec], outfile)
