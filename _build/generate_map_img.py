import os
import pandas as pd
from urllib.request import urlopen

wd = os.path.dirname(__file__)
locationsPath = os.path.join(wd, "../_data/atdb.092116023143.ALL.csv")
imgOutPath = os.path.join(wd, "../img/googlemap.png")

baseurl = "https://maps.googleapis.com/maps/api/staticmap?"
options = "size=640x350&zoom=5&scale=2"
style = "style=feature:landscape|lightness:40&style=feature:road|visibility:simplified"
api_key = "key=AIzaSyCpNlAW16ash3_DakQeeIwzPs5KxTz_lmI"

# Read in locations from csv file
locations = pd.read_csv(locationsPath, index_col='id')
shelters = locations[locations['type'] == 'SHELTER']

# Append the lat-long of each shelter to the url path
path = 'path=weight:2'
for index, row in shelters.iterrows():
    lat = "{:.4f}".format(row['lat'])
    long = "{:.4f}".format(row['lon'])
    path = path + '|' + lat + ',' + long

url = baseurl + options + '&' + style + '&' + path  + '&' + api_key

# The Google Maps api has a max length on urls.  Make sure our url is shorter than that
assert(len(url) < 8192)
print(url)

# Use the url to download the image and save in the img folder
r = urlopen(url)
with open(imgOutPath, 'w+b') as f:
    image = r.read()
    f.write(image)
