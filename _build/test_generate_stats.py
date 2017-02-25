import unittest
import pandas as pd
from datetime import datetime
from datetime import date

from generate_stats import current_location
from generate_stats import days_on_trail
# from generate_stats import miles_hiked_miles_remaining
from generate_stats import miles_hiked_per_day
from generate_stats import predict_completion
from generate_stats import start_date


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        types = ['FEATURE', 'SHELTER', 'SHELTER', 'SHELTER', 'SHELTER', 'FEATURE']
        lats = [34.62673, 34.6533256, 36.5810973, 39.227215, 45.8815981, 45.904362]
        longs = [-84.193656, -84.0342084, -81.902055, -77.7792448, -68.995052, -68.921392]
        names = ['Springer Mt', 'Gooch Mountain Shelter', 'Abingdon Gap Shelter', 'David Lesser Shelter',
                 'The Birches Shelters', 'Mt Katahdin']
        states = ['GA', 'GA', 'NC', 'VA', 'ME', 'ME']
        to_spgrs = [0, 15.8, 458.8, 1014.4, 2184.6, 2189.8]
        elevs = [3782, 2789, 3780, 1421, 1089, 5268]

        df = pd.DataFrame({'type': types, 'lat': lats, 'lon': longs, 'name': names, 'state': states,
                                'to_spgr': to_spgrs, 'elev': elevs})

        cls.normal_df = df.copy()
        dt_reached = ['2017-03-08T08:01:00', '2017-03-08T16:02:00', '2017-03-15T07:03:00', '2017-03-15T17:04:00',
                      pd.NaT, pd.NaT]
        cls.normal_df['dt_reached'] = pd.to_datetime(dt_reached)

        cls.complete_df = df.copy()
        dt_reached = ['2017-03-08T08:01:00', '2017-03-08T16:02:00', '2017-03-15T07:03:00', '2017-03-15T17:04:00',
                      '2017-08-15T12:05:00', '2017-08-15T14:06:00']
        cls.complete_df['dt_reached'] = pd.to_datetime(dt_reached)

        cls.empty_df = df.copy()
        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        cls.empty_df['dt_reached'] = pd.to_datetime(dt_reached)


class TestCurrentLocation(Test):
    def test_normal_location(self):
        # Should output the last known location and time
        bak = self.normal_df.copy()

        loc = current_location(self.normal_df)
        expected = {'current_location':
                    {'lon': '-77.7792', 'dt_reached': '2017-03-15', 'lat': '39.2272',
                     'name': 'David Lesser Shelter, VA', 'miles_hiked': '1014.4', 'miles_remaining': '1175.4'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_no_location_data(self):
        # Should output the first location position and the expected start date
        bak = self.empty_df.copy()

        loc = current_location(self.empty_df)
        expected = {'current_location':
                    {"lon": '-84.1937', 'dt_reached': '2017-03-13', 'lat': '34.6267', 'name': 'Springer Mt, GA',
                     'miles_hiked': '0.0', 'miles_remaining': '2189.8'}}

        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))

    def test_completed_hike(self):
        # Should output the last location point and date
        bak = self.complete_df.copy()

        loc = current_location(self.complete_df)
        expected = {'current_location':
                        {'lon': '-68.9214', 'dt_reached': '2017-08-15', 'lat': '45.9044', 'name': 'Mt Katahdin, ME',
                         'miles_hiked': '2189.8', 'miles_remaining': '0.0'}}
        self.assertDictEqual(expected, loc)

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))


class TestDaysOnTrail(Test):
    def test_normal_hike(self):
        # Should output number of days between the first and last date listed
        bak = self.normal_df.copy()

        dat = days_on_trail(self.normal_df)
        expected = {'days_on_trail': 8}
        self.assertDictEqual(expected, dat)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_complete_hike(self):
        # Should output number of days between the first and last date listed
        bak = self.complete_df.copy()

        dat = days_on_trail(self.complete_df)
        expected = {'days_on_trail': 161}
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
        expected = {'miles_per_day': {"2017-03-08": '15.8', "2017-03-15": '555.6'}}
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_no_location_data(self):
        # Should output an empty list
        bak = self.empty_df.copy()

        mpd = miles_hiked_per_day(self.empty_df)
        expected = {'miles_per_day': {}}
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))

    def test_completed_hike(self):
        # Should output miles for every day, except the missing days
        bak = self.complete_df.copy()

        mpd = miles_hiked_per_day(self.complete_df)
        expected = {'miles_per_day': {"2017-03-08": '15.8', "2017-03-15": '555.6', "2017-08-15": '5.2'}}
        self.assertDictEqual(expected, mpd)

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))


class TestPredictCompletion(Test):
    # def setUp(self):
    #     elev = [100, -200, 300, -400, 500, -600]
    #     to_spgr = [0.0, 1.1, 1.1, 2.2, 3.4, 4.7]
    #     type = ['SHELTER', 'SHELTER', 'SHELTER', 'SHELTER', 'SHELTER']

    #     dt_reached = ['2017-03-08T12:30:00', '2017-03-08T13:01:00', '2017-03-09T08:00:00', '2017-03-09T08:31:00', pd.NaT]
    #     self.normal_df = pd.DataFrame({'dt_reached': dt_reached, 'elev': elev, 'to_spgr': to_spgr, 'type': type})
    #     self.normal_df['dt_reached'] = pd.to_datetime(self.normal_df['dt_reached'])

    #     dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT]
    #     self.empty_df = pd.DataFrame({'dt_reached': dt_reached, 'elev': elev, 'to_spgr': to_spgr, 'type': type})
    #     self.empty_df['dt_reached'] = pd.to_datetime(self.empty_df['dt_reached'])

    #     dt_reached = ['2017-03-08T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', pd.NaT]
    #     self.zeros_df = pd.DataFrame({'dt_reached': dt_reached, 'elev': elev, 'to_spgr': to_spgr, 'type': type})
    #     self.zeros_df['dt_reached'] = pd.to_datetime(self.empty_df['dt_reached'])

    def test_normal_hike(self):
        pc = predict_completion(self.normal_df)

        estimated_dt = datetime.strptime(pc['estimated_completion']['date'] , '%b %d, %Y').date()
        range_start = date(2017, 6, 1)
        range_finish = date(2017, 10, 1)
        self.assertTrue( range_start <= estimated_dt <= range_finish )

    def test_no_location_data(self):
        # Should output the expected start date, since we have no date information
        pc = predict_completion(self.empty_df)
        expected = {'estimated_completion': {'date': 'Sep 1, 2017'}}
        self.assertDictEqual(expected, pc)

    # def test_zero_days(self):
    #     # Should output the expected start date, since we have no date information
    #     pc = predict_completion(self.zeros_df)
    #     expected = {'estimated_completion': 'Sep 1, 2017'}
    #     self.assertDictEqual(expected, pc)


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
