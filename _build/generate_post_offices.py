import constants
import pandas as pd
import json
from googleplaces import GooglePlaces, types


def get_post_offices(df, num_future_checkpoints = 25, search_radius=20000):
    # Get all unhiked poi's
    upcoming = df[pd.isnull(df[constants.DATE_COL])]
    upcoming.reset_index(inplace=True, drop=True)

    # Initialize some variables
    google_places = GooglePlaces(constants.GOOGLE_API_KEY)
    query_results = []
    available_indices = upcoming.index.values

    # If available, query several checkpoints into the future
    if num_future_checkpoints in available_indices:
        upcoming_poi = upcoming.iloc[num_future_checkpoints]
        location = {'lat': upcoming_poi.lat, 'lng': upcoming_poi.lon}
        results = google_places.nearby_search(lat_lng=location, radius=search_radius, types=[types.TYPE_POST_OFFICE])
        query_results.extend(results.places)

    # If available, jump back two spots from the future checkpoint and query there as well
    if num_future_checkpoints - 2 in available_indices:
        upcoming_poi = upcoming.iloc[num_future_checkpoints-2]
        location = {'lat': upcoming_poi.lat, 'lng': upcoming_poi.lon}
        results = google_places.nearby_search(lat_lng=location, radius=search_radius, types=[types.TYPE_POST_OFFICE])
        query_results.extend(results.places)

    # If available, jump back four spots from the future checkpoint and query there as well
    if num_future_checkpoints - 4 in available_indices:
        upcoming_poi = upcoming.iloc[num_future_checkpoints-4]
        location = {'lat': upcoming_poi.lat, 'lng': upcoming_poi.lon}
        results = google_places.nearby_search(lat_lng=location, radius=search_radius, types=[types.TYPE_POST_OFFICE])
        query_results.extend(results.places)

    # If available, jump back six spots from the future checkpoint and query there as well
    if num_future_checkpoints - 6 in available_indices:
        upcoming_poi = upcoming.iloc[num_future_checkpoints-6]
        location = {'lat': upcoming_poi.lat, 'lng': upcoming_poi.lon}
        results = google_places.nearby_search(lat_lng=location, radius=search_radius, types=[types.TYPE_POST_OFFICE])
        query_results.extend(results.places)

    # Loop through all the results and extracting and formatting the important info
    post_offices = []
    for place in query_results:
        po = {}
        po['nm'] = place.name
        po['lat'] = "{:.4f}".format(place.geo_location['lat'])
        po['lng'] = "{:.4f}".format(place.geo_location['lng'])

        place.get_details()
        po['url'] = place.url
        po['addr'] = place.formatted_address
        po['phone'] = place.local_phone_number

        post_offices.append(po)

    unique_post_offices = [dict(p) for p in set(tuple(i.items()) for i in post_offices)]

    return unique_post_offices

if __name__ == "__main__":
    checkpoints = constants.read_poi_file()
    pos = get_post_offices(checkpoints)

    # Write json file
    with open(constants.postOfficesFilePath, 'w') as outfile:
        json.dump(pos, outfile)
