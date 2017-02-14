import os
import pandas as pd
from urllib.request import urlopen


# file locations
wd = os.path.dirname(__file__)
locationsPath = os.path.join(wd, "../_data/atdb.092116023143.ALL.csv")
statsFilePath = os.path.join(wd, "../_data/stats.json")
imgOutPath = os.path.join(wd, "../img/googlemap.png")

# constants
TYPE_COL = 'type'
LAT_COL = 'lat'
LONG_COL = 'lon'
DATE_COL = 'dt_reached'

# map options
baseurl = "https://maps.googleapis.com/maps/api/staticmap?"
options = "size=640x400&zoom=5&scale=2"
current_location_marker = "markers=scale:2|anchor:center|icon:https://goo.gl/otDBv3"
style = "style=feature:landscape|lightness:40&style=feature:road|visibility:simplified"
api_key = "key=AIzaSyCpNlAW16ash3_DakQeeIwzPs5KxTz_lmI"

# read in locations from csv file
locations = pd.read_csv(locationsPath, usecols=[TYPE_COL, LAT_COL, LONG_COL, DATE_COL])
shelters = locations[locations[TYPE_COL] == 'SHELTER']

# append the lat-long of each shelter to the url path
path = 'path=weight:2'
for index, row in shelters.iterrows():
    lat = "{:.4f}".format(row[LAT_COL])
    long = "{:.4f}".format(row[LONG_COL])
    path = path + '|' + lat + ',' + long

# get the last know current location
completed = locations[locations[DATE_COL].notnull()][[LAT_COL, LONG_COL]]
last_completed = locations[[LAT_COL, LONG_COL]].iloc[0]    # by default, use first location if nothing is completed
if len(completed) > 0:
    last_completed = completed.iloc[-1]

current_location_marker = current_location_marker + '|' + str(last_completed[LAT_COL]) + ',' + str(last_completed[LONG_COL])

# build final url
url = baseurl + options + '&' + current_location_marker + '&' + style + '&' + path + '&' + api_key

# The Google Maps api has a max length on urls.  Make sure our url is shorter than that
assert(len(url) < 8192)
print(url)

# Use the url to download the image and save in the img folder
r = urlopen(url)
with open(imgOutPath, 'w+b') as f:
    image = r.read()
    f.write(image)
