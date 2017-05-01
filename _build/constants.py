import os
import pandas as pd

# Define input and output file locations
wd = os.path.dirname(__file__)
poiFilePath = os.path.join(wd, '../_data/atdb.092116023143.ALL.csv')
financesFilePath = os.path.join(wd, '../_data/finances.csv')
statsFilePath = os.path.join(wd, '../_data/stats.json')
postOfficesFilePath = os.path.join(wd, '../_data/post_offices.json')
staticMapImgPath = os.path.join(wd, "../assets/images/googlemap.png")

# Columns
TYPE_COL = 'type'
NAME_COL = 'name'
STATE_COL = 'state'
LAT_COL = 'lat'
LONG_COL = 'lon'
DATE_COL = 'dt_reached'
TO_SPRINGER_COL = 'to_spgr'
ELEV_COL = 'elev'

# Constants
ESTIMATED_START_DT = '2017-03-13'
ESTIMATED_FINISH_DT = '2017-08-24'
GOOGLE_API_KEY = 'AIzaSyCpNlAW16ash3_DakQeeIwzPs5KxTz_lmI'


def read_poi_file(usecols=None):
    return pd.read_csv(poiFilePath, parse_dates=[DATE_COL], infer_datetime_format=True, usecols=usecols)

def get_completed(df):
    return df[df[DATE_COL].notnull()]