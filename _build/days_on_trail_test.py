import unittest
import pandas as pd

from build import days_on_trail


class TestDaysOnTrail(unittest.TestCase):
    def setUp(self):
        dt_reached = ['2017-03-08T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', pd.NaT]
        self.normal_df = pd.DataFrame({'dt_reached': dt_reached})
        self.normal_df['dt_reached'] = pd.to_datetime(self.normal_df['dt_reached'])

        dt_reached = ['2017-03-08T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', '2017-03-20T14:33:00']
        self.complete_df = pd.DataFrame({'dt_reached': dt_reached})
        self.complete_df['dt_reached'] = pd.to_datetime(self.complete_df['dt_reached'])

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.empty_df = pd.DataFrame({'dt_reached': dt_reached})
        self.empty_df['dt_reached'] = pd.to_datetime(self.empty_df['dt_reached'])

    def test_normal_hike(self):
        # Should output number of days between the first and last date listed
        dat = days_on_trail(self.normal_df)
        expected = {'days_on_trail': 8}
        self.assertDictEqual(expected, dat)

    def test_complete_hike(self):
        # Should output number of days between the first and last date listed
        dat = days_on_trail(self.complete_df)
        expected = {'days_on_trail': 13}
        self.assertDictEqual(expected, dat)

    def test_no_location_data(self):
        # Should output 0
        dat = days_on_trail(self.empty_df)
        expected = {'days_on_trail': 0}
        self.assertDictEqual(expected, dat)


if __name__ == '__main__':
    unittest.main()
