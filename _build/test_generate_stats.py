import unittest
import pandas as pd
from datetime import datetime
from datetime import date

from generate_stats import current_location
from generate_stats import days_on_trail
from generate_stats import miles_hiked_per_day
from generate_stats import predict_completion
from generate_stats import start_date


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        labels = ['type', 'lat', 'lon', 'name', 'state', 'to_spgr', 'elev', 'dt_reached']
        checkpoints = [
            ('FEATURE', 34.557789,  -84.249489,  'Amicalola Falls SP',   'GA', -8.8,   1800, '2017-03-08T08:01:00'),
            ('FEATURE', 34.62673,   -84.193656,  'Springer Mt',          'GA', 0,      3782, '2017-03-08T13:02:00'),

            ('FEATURE', 34.62673,   -84.193656,  'Springer Mt',          'GA', 0,      3782, '2017-03-09T07:03:00'),
            ('FEATURE', 34.6659577, -84.1363386, 'Hawk Mt Shelter',      'GA', 8.1,    3194, '2017-03-09T10:30:00'),
            ('SHELTER', 34.6533256, -84.0342084, 'Gooch Mt Shelter',     'GA', 15.8,   2789, '2017-03-09T13:04:00'),

            ('SHELTER', 39.227215,  -77.7792448, 'David Lesser Shelter', 'VA', 1014.4, 1421, '2017-03-15T07:03:00'),
            ('FEATURE', 39.3165,    -77.7558,    'Harpers Ferry, WV',    'VA', 1023.7, 274,  '2017-03-15T10:43:00'),

            ('SHELTER', 45.8815981, -68.995052,  'The Birches Shelters', 'ME', 2184.6, 1089, '2017-08-25T12:05:00'),
            ('FEATURE', 45.904362,  -68.921392,  'Mt Katahdin',          'ME', 2189.8, 5268, '2017-08-25T14:06:00')
        ]

        df = pd.DataFrame.from_records(checkpoints, columns=labels)
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        cls.normal_df = df.copy()
        complete = cls.normal_df['dt_reached'].ix[:4]
        incomplete = pd.Series([pd.NaT for i in range(len(df) - 5)])
        cls.normal_df['dt_reached'] = complete.append(incomplete, ignore_index=True)

        cls.complete_df = df.copy()

        cls.empty_df = df.copy()
        cls.empty_df['dt_reached'] = [pd.NaT for i in range(len(df))]

        assert (len(df) == len(cls.normal_df) == len(cls.complete_df) == len(cls.empty_df))

class TestCurrentLocation(Test):
    def test_normal_location(self):
        # Should output the last known location and time
        bak = self.normal_df.copy()

        loc = current_location(self.normal_df)
        expected = {'current_location':
                    {'lat': '34.6533', 'lon': '-84.0342', 'dt_reached': '2017-03-09', 'name': 'Gooch Mt Shelter, GA',
                     'miles_hiked': '24.6', 'miles_remaining': '2174.0'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_no_location_data(self):
        # Should output the first location position and the expected start date
        bak = self.empty_df.copy()

        loc = current_location(self.empty_df)
        expected = {'current_location':
                    {'lat': '34.5578', 'lon': '-84.2495', 'dt_reached': '2017-03-13', 'name': 'Amicalola Falls SP, GA',
                     'miles_hiked': '0.0', 'miles_remaining': '2198.6'}}

        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))

    def test_completed_hike(self):
        # Should output the last location point and date
        bak = self.complete_df.copy()

        loc = current_location(self.complete_df)
        expected = {'current_location':
                        {'lat': '45.9044', 'lon': '-68.9214', 'dt_reached': '2017-08-25',  'name': 'Mt Katahdin, ME',
                         'miles_hiked': '2198.6', 'miles_remaining': '0.0'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))


class TestDaysOnTrail(Test):
    def test_normal_hike(self):
        # Should output number of days between the first and last date listed
        bak = self.normal_df.copy()

        dat = days_on_trail(self.normal_df)
        expected = {'days_on_trail': 2}
        self.assertDictEqual(expected, dat)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_complete_hike(self):
        # Should output number of days between the first and last date listed
        bak = self.complete_df.copy()

        dat = days_on_trail(self.complete_df)
        expected = {'days_on_trail': 171}
        self.assertDictEqual(expected, dat)

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))

    def test_no_location_data(self):
        # Should output 0
        bak = self.empty_df.copy()

        dat = days_on_trail(self.empty_df)
        expected = {'days_on_trail': 0}
        self.assertDictEqual(expected, dat)

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))


class TestMilesHikedPerDay(Test):
    def test_normal_multi_day_hike(self):
        # Should output the mileage for one day
        bak = self.normal_df.copy()

        mpd = miles_hiked_per_day(self.normal_df)
        expected = {'miles_per_day': {"2017-03-08": '8.8', "2017-03-09": '15.8'}, 'avg_mileage': '12.3', 'num_zeros': 0}
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_no_location_data(self):
        # Should output an empty list
        bak = self.empty_df.copy()

        mpd = miles_hiked_per_day(self.empty_df)
        expected = {'miles_per_day': {}, 'avg_mileage': '0.0', 'num_zeros': 0}
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))

    def test_completed_hike(self):
        # Should output miles for every day, except the missing days
        bak = self.complete_df.copy()

        mpd = miles_hiked_per_day(self.complete_df)
        expected = {
            'miles_per_day': {"2017-03-08": '8.8', "2017-03-09": '15.8', "2017-03-15": '9.3', "2017-08-25": '5.2'},
            'avg_mileage': '9.8',
            'num_zeros': 167
        }
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))


class TestPredictCompletion(Test):
    def test_normal_hike(self):
        pc = predict_completion(self.normal_df)
        print(pc)
        estimated_dt = datetime.strptime(pc['estimated_completion']['date'] , '%b %d, %Y').date()
        range_start = date(2017, 6, 1)
        range_finish = date(2017, 10, 1)
        self.assertTrue( range_start <= estimated_dt <= range_finish )

    def test_no_location_data(self):
        # Should output the expected start date, since we have no date information
        pc = predict_completion(self.empty_df)
        expected = {'estimated_completion': {'date': 'Sep 1, 2017'}}
        self.assertDictEqual(expected, pc)

    def test_completed_hike(self):
        pc = predict_completion(self.complete_df)
        print(pc)
        estimated_dt = datetime.strptime(pc['estimated_completion']['date'] , '%b %d, %Y').date()
        range_start = date(2017, 8, 1)
        range_finish = date(2017, 10, 1)
        self.assertTrue( range_start <= estimated_dt <= range_finish )


class TestStartDate(Test):
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
