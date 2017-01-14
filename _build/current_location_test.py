import unittest
import pandas as pd

from build import current_location

lats = [34.61, 34.64, 34.66]
longs = [-84.19, -84.17, -84.12]


class TestMilesHikedPerDay(unittest.TestCase):

    def test_normal_location(self):
        # Should output the last known location and time

        d = {'lat': lats, 'lon': longs, 'dt_reached': ['2017-03-08T15:33:00', '', '']}
        df = pd.DataFrame(d, index=[1, 2, 3])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        loc = current_location(df)
        self.assertDictEqual(loc, {'current_location': {"lon": -84.19, "dt_reached": "2017-03-08", "lat": 34.61}})

    def test_no_location_data(self):
        # Should output the first location position and the expected start date

        d = {'lat': lats, 'lon': longs, 'dt_reached': ['', '', '']}
        df = pd.DataFrame(d, index=[1, 2, 3])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        loc = current_location(df)
        self.assertDictEqual(loc, {'current_location': {"lon": -84.19, "dt_reached": "2017-03-09", "lat": 34.61}})

    def test_completed_hike(self):
        # Should output the last location point and date

        dt_reached = ['2017-03-08T12:31:00', '2017-03-09T13:32:00', '2017-03-10T14:33:00']
        d = {'lat': lats, 'lon': longs, 'dt_reached': dt_reached}
        df = pd.DataFrame(d, index=[1, 2, 3])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        loc = current_location(df)
        self.assertDictEqual(loc, {'current_location': {"lon": -84.12, "dt_reached": "2017-03-10", "lat": 34.66}})
