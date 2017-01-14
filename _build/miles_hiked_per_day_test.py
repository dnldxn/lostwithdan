import unittest
import pandas as pd

from build import miles_hiked_per_day

to_spgr = [0, 1.1, 2.3, 3.6]


class TestMilesHikedPerDay(unittest.TestCase):

    def test_normal_multi_day_hike(self):
        # Should output the mileage for one day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', '']
        d = {'to_spgr': to_spgr, 'dt_reached': dt_reached}
        df = pd.DataFrame(d, index=[1, 2, 3, 4])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        mpd = miles_hiked_per_day(df)
        self.assertDictEqual(mpd, {'miles_per_day': {"2017-03-08": 1.1, "2017-03-09": 1.2}})

    def test_single_day_hike(self):
        # Should output mileage for a single day

        dt_reached = ['2017-03-08T12:33:00', '2017-03-08T13:33:00', '', '']
        d = {'to_spgr': to_spgr, 'dt_reached': dt_reached}
        df = pd.DataFrame(d, index=[1, 2, 3, 4])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        mpd = miles_hiked_per_day(df)
        self.assertDictEqual(mpd, {'miles_per_day': {"2017-03-08": 1.1}})

    def test_no_location_data(self):
        # Should output an empty list

        d = {'to_spgr': to_spgr, 'dt_reached': ['', '', '', '']}
        df = pd.DataFrame(d, index=[1, 2, 3, 4])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        mpd = miles_hiked_per_day(df)
        self.assertDictEqual(mpd, {'miles_per_day': {}})

    def test_completed_hike_with_missing_days(self):
        # Should output miles for every day

        dt_reached = ['2017-03-08T12:31:00', '2017-03-08T13:32:00', '2017-03-09T14:33:00', '2017-03-12T15:33:00']
        d = {'to_spgr': to_spgr, 'dt_reached': dt_reached}
        df = pd.DataFrame(d, index=[1, 2, 3, 4])
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        mpd = miles_hiked_per_day(df)
        self.assertEqual(str(mpd), str({'miles_per_day': {
            "2017-03-08": 1.1,
            "2017-03-09": 1.2,
            "2017-03-12": 1.3
        }}))
