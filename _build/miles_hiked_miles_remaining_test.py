import unittest
import pandas as pd

from build import miles_hiked_miles_remaining


class TestMilesHikedMilesRemaining(unittest.TestCase):
    def setUp(self):
        to_spgr = [0, 1.1, 2.3, 3.6]
        to_ktd = [3.6, 2.5, 1.3, 0.0]
        self.df = pd.DataFrame({'to_spgr': to_spgr, 'to_ktd': to_ktd})

    def test_normal_multi_day_hike(self):
        # Should output the mileage for one day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', pd.NaT]
        self.df['dt_reached'] = dt_reached

        mhmr = miles_hiked_miles_remaining(self.df)
        self.assertDictEqual(mhmr, {'miles_hiked': 2.3, 'miles_remaining': 1.3})

    def test_single_day_hike(self):
        # Should output mileage for a single day

        dt_reached = ['2017-03-08T12:33:00', '2017-03-08T13:33:00', pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached

        mhmr = miles_hiked_miles_remaining(self.df)
        self.assertDictEqual(mhmr, {'miles_hiked': 1.1, 'miles_remaining': 2.5})

    def test_no_location_data(self):
        # Should output an empty list

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached

        mhmr = miles_hiked_miles_remaining(self.df)
        self.assertDictEqual(mhmr, {'miles_hiked': 0.0, 'miles_remaining': 3.6})

    def test_completed_hike_with_missing_days(self):
        # Should output miles for every day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', '2017-03-12T15:33:00']
        self.df['dt_reached'] = dt_reached

        mhmr = miles_hiked_miles_remaining(self.df)
        self.assertDictEqual(mhmr, {'miles_hiked': 3.6, 'miles_remaining': 0.0})


if __name__ == '__main__':
    unittest.main()
