import unittest
import pandas as pd

from build import current_location


class TestCurrentLocation(unittest.TestCase):
    def setUp(self):
        lats = [34.61, 34.64, 34.66]
        longs = [-84.19, -84.17, -84.12]
        names = ['Springer Mt', 'Gooch Mountain Shelter', 'Muskrat Creek Shelter']
        states = ['GA', 'GA', 'NC']

        self.df = pd.DataFrame({'lat': lats, 'lon': longs, 'name': names, 'state': states})

    def test_normal_location(self):
        # Should output the last known location and time

        dt_reached = ['2017-03-08T15:33:00', pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])
        bak = self.df.copy()

        loc = current_location(self.df)
        expected = {'current_location': {'lon': '-84.19', 'dt_reached': '2017-03-08', 'lat': '34.61', 'name': 'Springer Mt, GA'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.df.equals(bak))

    def test_no_location_data(self):
        # Should output the first location position and the expected start date

        dt_reached = [pd.NaT, pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])
        bak = self.df.copy()

        loc = current_location(self.df)
        expected = {'current_location': {"lon": '-84.19', 'dt_reached': '2017-03-09', 'lat': '34.61', 'name': 'Springer Mt, GA'}}

        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.df.equals(bak))

    def test_completed_hike(self):
        # Should output the last location point and date

        dt_reached = ['2017-03-08T12:31:00', '2017-03-09T13:32:00', '2017-03-10T14:33:00']
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])
        bak = self.df.copy()

        loc = current_location(self.df)
        expected = {'current_location': {'lon': '-84.12', 'dt_reached': '2017-03-10', 'lat': '34.66', 'name': 'Muskrat Creek Shelter, NC'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.df.equals(bak))


if __name__ == '__main__':
    unittest.main()
