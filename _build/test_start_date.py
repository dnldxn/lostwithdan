import unittest
import pandas as pd

from build import start_date


class TestStartDate(unittest.TestCase):
    def setUp(self):
        dt_reached = ['2017-03-08T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', pd.NaT]
        self.normal_df = pd.DataFrame({'dt_reached': dt_reached})
        self.normal_df['dt_reached'] = pd.to_datetime(self.normal_df['dt_reached'])

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.empty_df = pd.DataFrame({'dt_reached': dt_reached})
        self.empty_df['dt_reached'] = pd.to_datetime(self.empty_df['dt_reached'])

    def test_normal_hike(self):
        # Should output the first date in the dt_reached column
        sd = start_date(self.normal_df)
        expected = {'start_date': 'Mar 8, 2017'}
        self.assertDictEqual(expected, sd)

    def test_no_location_data(self):
        # Should output the expected start date, since we have no date information
        sd = start_date(self.empty_df)
        expected = {'start_date': 'Mar 13, 2017'}
        self.assertDictEqual(expected, sd)


if __name__ == '__main__':
    unittest.main()
