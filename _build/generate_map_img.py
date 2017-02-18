import os
import pandas as pd
from urllib.request import urlopen
from PIL import Image


def generate_url(checkpoints, center_lat, center_long, offset_lat, offset_long):
    # constants
    TYPE_COL = 'type'
    LAT_COL = 'lat'
    LONG_COL = 'lon'
    DATE_COL = 'dt_reached'

    # map options
    baseurl = "https://maps.googleapis.com/maps/api/staticmap?"
    options = "center=" + str(center_lat) + "," + str(center_long) + "&size=640x420&zoom=6&scale=2"
    current_location_marker = "markers=scale:2|anchor:center|icon:https://goo.gl/I1t6o6"
    style = "style=feature:landscape|lightness:40&style=feature:road|visibility:simplified"
    api_key = "key=AIzaSyCpNlAW16ash3_DakQeeIwzPs5KxTz_lmI"

    # read in locations from csv file
    shelters = checkpoints[checkpoints[TYPE_COL] == 'SHELTER']

    # append the lat-long of each shelter to the url path
    path = 'path=weight:4'
    for index, row in shelters.iterrows():
        lat = "{:.4f}".format(row[LAT_COL])
        long = "{:.4f}".format(row[LONG_COL])

        path = path + '|' + lat + ',' + long

    # get the last know current location
    completed = checkpoints[checkpoints[DATE_COL].notnull()][[LAT_COL, LONG_COL]]
    last_completed = checkpoints[[LAT_COL, LONG_COL]].iloc[0]   # by default, use first location if nothing is completed
    if len(completed) > 0:
        last_completed = completed.iloc[-1]

    current_location_marker = current_location_marker + '|' + str(last_completed[LAT_COL]) + ',' + str(last_completed[LONG_COL])

    # build final url
    url = baseurl + options + '&' + current_location_marker + '&' + style + '&' + path + '&' + api_key

    # The Google Maps api has a max length on urls.  Make sure our url is shorter than that
    assert(len(url) < 8192)
    print(url)

    return url


def combine_images(img_path_out, top_left, top_right, bottom_right, bottom_left):
    top_left        = Image.open(top_left)
    top_right       = Image.open(top_right)
    bottom_right    = Image.open(bottom_right)
    bottom_left     = Image.open(bottom_left)

    # all four images should have the same heights and widths
    assert(top_left.height == top_right.height == bottom_right.height == bottom_left.height)
    assert(top_left.width == top_right.width == bottom_right.width == bottom_left.width)

    quad_height = top_left.height
    quad_width = top_left.width

    # Crop out Google logo
    crop_pixels = 45
    top_left        = top_left.crop((0, 0, quad_width, quad_height - crop_pixels))
    top_right       = top_right.crop((0, 0, quad_width, quad_height - crop_pixels))
    bottom_right    = bottom_right.crop((0, 0, quad_width, quad_height - crop_pixels))
    bottom_left     = bottom_left.crop((0, 0, quad_width, quad_height - crop_pixels))

    # create new image canvas
    new_width = 2 * quad_width
    new_height = 2 * quad_height - (2*crop_pixels)

    new_im = Image.new('RGB', (new_width, new_height))

    # paste the four quadrants into their respective locations
    new_im.paste(top_left,      (0, 0))
    new_im.paste(top_right,     (quad_width, 0))
    new_im.paste(bottom_right,  (quad_width, quad_height - crop_pixels))
    new_im.paste(bottom_left,   (0, quad_height - crop_pixels))

    # scale down the image to make it smaler
    new_width_scaled = round(new_width/1.6)
    new_height_scaled = round(new_height/1.7)

    new_im = new_im.resize((new_width_scaled, new_height_scaled), Image.ANTIALIAS)

    # save image to disk
    new_im.save(img_path_out, optimize=True, quality=85)


if __name__ == "__main__":

    # constants
    TYPE_COL = 'type'
    LAT_COL = 'lat'
    LONG_COL = 'lon'
    DATE_COL = 'dt_reached'

    # define the center and the offsets for the 4 quadrants
    CENTER = (40, -76)
    LATITUDE_OFFSET = 3.35  # vertical
    LONGITUDE_OFFSET = 7.027  # horizontal

    # calculate the center of each of the four quadrants
    TOP_LEFT =      (CENTER[0] + LATITUDE_OFFSET, CENTER[1] - LONGITUDE_OFFSET)
    TOP_RIGHT =     (CENTER[0] + LATITUDE_OFFSET, CENTER[1] + LONGITUDE_OFFSET)
    BOTTOM_RIGHT =  (CENTER[0] - LATITUDE_OFFSET, CENTER[1] + LONGITUDE_OFFSET)
    BOTTOM_LEFT =   (CENTER[0] - LATITUDE_OFFSET, CENTER[1] - LONGITUDE_OFFSET)

    # file locations
    wd = os.path.dirname(__file__)
    locationsPath = os.path.join(wd, "../_data/atdb.092116023143.ALL.csv")
    img_out_path_top_left = os.path.join(wd, "../img/googlemap_topleft.png")
    img_out_path_top_right = os.path.join(wd, "../img/googlemap_topright.png")
    img_out_path_bottom_right = os.path.join(wd, "../img/googlemap_bottomright.png")
    img_out_path_bottom_left = os.path.join(wd, "../img/googlemap_bottomleft.png")
    img_out_path = os.path.join(wd, "../img/googlemap.png")

    # read in location data to generate path and current location icon
    df = pd.read_csv(locationsPath, usecols=[TYPE_COL, LAT_COL, LONG_COL, DATE_COL])

    # Use the url to download the image and save in the img folder
    url = generate_url(df, TOP_LEFT[0], TOP_LEFT[1], LATITUDE_OFFSET, LONGITUDE_OFFSET)
    r = urlopen(url)
    with open(img_out_path_top_left, 'w+b') as f:
        image = r.read()
        f.write(image)

    url = generate_url(df, TOP_RIGHT[0], TOP_RIGHT[1], LATITUDE_OFFSET, LONGITUDE_OFFSET)
    r = urlopen(url)
    with open(img_out_path_top_right, 'w+b') as f:
        image = r.read()
        f.write(image)

    url = generate_url(df, BOTTOM_RIGHT[0], BOTTOM_RIGHT[1], LATITUDE_OFFSET, LONGITUDE_OFFSET)
    r = urlopen(url)
    with open(img_out_path_bottom_right, 'w+b') as f:
        image = r.read()
        f.write(image)

    url = generate_url(df, BOTTOM_LEFT[0], BOTTOM_LEFT[1], LATITUDE_OFFSET, LONGITUDE_OFFSET)
    r = urlopen(url)
    with open(img_out_path_bottom_left, 'w+b') as f:
        image = r.read()
        f.write(image)

    # combine images and save to disk
    combine_images(img_out_path, img_out_path_top_left, img_out_path_top_right, img_out_path_bottom_right, img_out_path_bottom_left)