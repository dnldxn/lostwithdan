import unittest
import pandas as pd

from build import miles_hiked_per_day


class TestMilesHikedPerDay(unittest.TestCase):
    def setUp(self):
        to_spgr = [0, 1.1, 2.3, 3.6]
        self.df = pd.DataFrame({'to_spgr': to_spgr})

    def test_normal_multi_day_hike(self):
        # Should output the mileage for one day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])

        mpd = miles_hiked_per_day(self.df)
        expected = {'miles_per_day': {"2017-03-08": '1.1', "2017-03-09": '1.2'}}
        self.assertDictEqual(expected, mpd)

    def test_single_day_hike(self):
        # Should output mileage for a single day

        dt_reached = ['2017-03-08T12:33:00', '2017-03-08T13:33:00', pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])

        mpd = miles_hiked_per_day(self.df)
        expected = {'miles_per_day': {"2017-03-08": '1.1'}}
        self.assertDictEqual(expected, mpd)

    def test_no_location_data(self):
        # Should output an empty list

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])

        mpd = miles_hiked_per_day(self.df)
        expected = {'miles_per_day': {}}
        self.assertDictEqual(expected, mpd)

    def test_completed_hike_with_missing_days(self):
        # Should output miles for every day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', '2017-03-12T15:33:00']
        self.df['dt_reached'] = dt_reached
        self.df['dt_reached'] = pd.to_datetime(self.df['dt_reached'])

        mpd = miles_hiked_per_day(self.df)
        expected = {'miles_per_day': {"2017-03-08": '1.1', "2017-03-09": '1.2', "2017-03-12": '1.3'}}
        self.assertDictEqual(expected, mpd)


if __name__ == '__main__':
    unittest.main()
