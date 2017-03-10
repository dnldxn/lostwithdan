import unittest
import pandas as pd

from generate_post_offices import get_post_offices

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        labels = ['lat', 'lon', 'dt_reached']
        checkpoints = [
            # First group is all GA locations
            (34.557789,  -84.249489,  '2017-03-09T07:03:00'),
            (34.61768,   -84.19871,   '2017-03-09T07:03:00'),
            (34.62673,   -84.193656,  '2017-03-09T07:03:00'),
            (34.6292728, -84.192975,  '2017-03-09T07:03:00'),
            (34.6495767, -84.1997597, '2017-03-09T07:03:00'),
            (34.6659577, -84.1363386, '2017-03-09T07:03:00'),
            (34.6533256, -84.0342084, '2017-03-09T07:03:00'),
            (34.677734,  -84.000137,  '2017-03-09T07:03:00'),
            (34.7372479, -83.954924,  '2017-03-09T07:03:00'),
            (34.7400792, -83.9374442, '2017-03-09T07:03:00'),
            (34.741067,  -83.920617,  '2017-03-09T07:03:00'),
            (34.7125074, -83.8342857, '2017-03-09T07:03:00'),
            (34.7763053, -83.8245496, '2017-03-09T07:03:00'),
            (34.8172349, -83.7667067, '2017-03-09T07:03:00'),

            (35.448432,  -83.7940435, '2017-03-10T07:03:00'),
            (35.460515,  -83.811105,  '2017-03-10T07:03:00'),
            (35.5458893, -83.7935136, '2017-03-10T07:03:00'),
            (35.5618399, -83.7665112, '2017-03-10T07:03:00'),
            (35.5619025, -83.7326211, '2017-03-10T07:03:00'),
            (35.5663517, -83.6417974, '2017-03-10T07:03:00'),
            (35.5643093, -83.5682326, '2017-03-10T07:03:00'),
            (35.5652725, -83.5427482, '2017-03-10T07:03:00'),
            (35.562747,  -83.498511,  '2017-03-10T07:03:00'),

            (39.227215,  -77.7792448, '2017-03-15T07:03:00'),
            (39.3165,    -77.7558, '2017-03-15T10:43:00'),

            (45.8815981, -68.995052, '2017-08-25T12:05:00'),
            (45.904362,  -68.921392, '2017-08-25T14:06:00')
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

class TestGetPostOffices(Test):
    def test_normal_location(self):
        # Should output the last known location and time
        bak = self.normal_df.copy()

        pos = get_post_offices(self.normal_df, num_future_checkpoints=3, search_radius=30000)

        self.assertGreater(len(pos), 1)
        for po in pos:
            self.assertGreater(len(po['nm']), 0)
            self.assertGreater(len(po['lat']), 0)
            self.assertGreater(len(po['lng']), 0)
            self.assertGreater(len(po['url']), 0)
            self.assertGreater(len(po['addr']), 0)
            self.assertTrue(", GA" in po['addr'] or ", NC" in po['addr'])   # the post offices should be somewhere in GA or NC
            self.assertTrue( 'phone' in po )   # there isn't always a phone number listed, just assert the key exists


        # make sure we didn't alter the original data
        self.assertTrue(self.normal_df.equals(bak))

    def test_no_location_data(self):
        # Should output the first location position and the expected start date
        bak = self.empty_df.copy()

        pos = get_post_offices(self.empty_df, num_future_checkpoints=3, search_radius=30000)

        self.assertGreater(len(pos), 1)
        for po in pos:
            self.assertGreater(len(po['nm']), 0)
            self.assertGreater(len(po['lat']), 0)
            self.assertGreater(len(po['lng']), 0)
            self.assertGreater(len(po['url']), 0)
            self.assertGreater(len(po['addr']), 0)
            self.assertIn(", GA", po['addr'])   # the post office should be somewhere in GA
            self.assertTrue( 'phone' in po )   # there isn't always a phone number listed, just assert the key exists

        # make sure we didn't alter the original data
        self.assertTrue(self.empty_df.equals(bak))

    def test_completed_hike(self):
        # Should output the last location point and date
        bak = self.complete_df.copy()

        pos = get_post_offices(self.complete_df)

        self.assertEqual(0, len(pos))

        # make sure we didn't alter the original data
        self.assertTrue(self.complete_df.equals(bak))


if __name__ == '__main__':
    unittest.main()
