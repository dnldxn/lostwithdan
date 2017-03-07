import unittest
import pandas as pd
import numpy as np

from generate_map_img import generate_url


class TestGenerateMapImage(unittest.TestCase):
    def setUp(self):
        labels = ['type', 'lat', 'lon', 'name', 'state', 'to_spgr', 'elev', 'dt_reached']
        checkpoints = [
            ('FEATURE', 34.557789,  -84.249489,  'Amicalola Falls SP',   'GA', -8.8,   1800, '2017-03-08T08:01:00'),
            ('SHELTER', 34.62673,   -84.193656,  'Springer Mt',          'GA', 0,      3782, '2017-03-08T13:02:00'),

            ('SHELTER', np.NaN,     np.NaN,      'Springer Mt',          'GA', 0,      3782, '2017-03-09T07:03:00'),
            ('FEATURE', 34.6659577, -84.1363386, 'Hawk Mt Shelter',      'GA', 8.1,    3194, '2017-03-09T10:30:00'),
            ('SHELTER', 34.6533256, -84.0342084, 'Gooch Mt Shelter',     'GA', 15.8,   2789, '2017-03-09T13:04:00'),

            ('SHELTER', 39.227215,  -77.7792448, 'David Lesser Shelter', 'VA', 1014.4, 1421, '2017-03-15T07:03:00'),
            ('FEATURE', 39.3165,    -77.7558,    'Harpers Ferry, WV',    'VA', 1023.7, 274,  '2017-03-15T10:43:00'),

            ('SHELTER', 45.8815981, -68.995052,  'The Birches Shelters', 'ME', 2184.6, 1089, '2017-08-25T12:05:00'),
            ('FEATURE', 45.904362,  -68.921392,  'Mt Katahdin',          'ME', 2189.8, 5268, '2017-08-25T14:06:00')
        ]

        df = pd.DataFrame.from_records(checkpoints, columns=labels)
        df['dt_reached'] = pd.to_datetime(df['dt_reached'])

        # define the center and the offsets for the 4 quadrants
        CENTER = (40, -76)
        self.LATITUDE_OFFSET = 3.35  # vertical
        self.LONGITUDE_OFFSET = 7.027  # horizontal

        # calculate the center of each of the four quadrants
        self.TOP_LEFT = (CENTER[0] + self.LATITUDE_OFFSET, CENTER[1] - self.LONGITUDE_OFFSET)
        self.TOP_RIGHT = (CENTER[0] + self.LATITUDE_OFFSET, CENTER[1] + self.LONGITUDE_OFFSET)
        self.BOTTOM_RIGHT = (CENTER[0] - self.LATITUDE_OFFSET, CENTER[1] + self.LONGITUDE_OFFSET)
        self.BOTTOM_LEFT = (CENTER[0] - self.LATITUDE_OFFSET, CENTER[1] - self.LONGITUDE_OFFSET)

        self.normal_df = df.copy()
        complete = self.normal_df['dt_reached'].ix[:4]
        incomplete = pd.Series([pd.NaT for i in range(len(df) - 5)])
        self.normal_df['dt_reached'] = complete.append(incomplete, ignore_index=True)

        self.empty_df = df.copy()
        self.empty_df['dt_reached'] = [pd.NaT for i in range(len(df))]

        assert (len(df) == len(self.normal_df) == len(self.empty_df))

    def test_normal_hike(self):
        # Build the 4 quadrant URLs
        url1 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url2 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url3 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url4 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)

        for url in [url1, url2, url3, url4]:
            self.assertLess(len(url), 8192)
            self.assertFalse("|nan," in url, url)
            self.assertFalse(",nan|" in url, url)

    def test_no_location_data(self):
        # Build the 4 quadrant URLs
        url1 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url2 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url3 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url4 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)

        for url in [url1, url2, url3, url4]:
            self.assertLess(len(url), 8192)
            self.assertFalse("|nan," in url, url)
            self.assertFalse(",nan|" in url, url)

    def image_quadrants_dont_overlap(self):
        # as
        # calculate the bounds of this box
        # left = center_lat - offset_lat
        # right = center_lat + offset_lat
        # top = center_long + offset_long
        # bottom = center_long - offset_long

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
