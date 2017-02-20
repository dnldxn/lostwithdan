import unittest
import pandas as pd

from build import current_location


class TestCurrentLocation(unittest.TestCase):
    def setUp(self):
        lats = [34.62673, 34.64, 45.904362]
        longs = [-84.193656, -84.17, -68.921392]
        names = ['Springer Mt', 'Gooch Mountain Shelter', 'Mt Katahdin']
        states = ['GA', 'GA', 'ME']

        self.df = pd.DataFrame({'lat': lats, 'lon': longs, 'name': names, 'state': states})

    def test_normal_location(self):
        # Should output the last known location and time

        dt_reached = ['2017-03-08T15:33:00', pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])
        bak = self.df.copy()

        loc = current_location(self.df)
        expected = {'current_location': {'lon': '-84.1937', 'dt_reached': '2017-03-08', 'lat': '34.6267', 'name': 'Springer Mt, GA'}}
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
        expected = {'current_location': {"lon": '-84.1937', 'dt_reached': '2017-03-13', 'lat': '34.6267', 'name': 'Springer Mt, GA'}}

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
        expected = {'current_location': {'lon': '-68.9214', 'dt_reached': '2017-03-10', 'lat': '45.9044', 'name': 'Mt Katahdin, ME'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.df.equals(bak))


if __name__ == '__main__':
    unittest.main()
