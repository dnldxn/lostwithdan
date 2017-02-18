import unittest
import pandas as pd

from generate_map_img import generate_url


class TestGenerateMapImage(unittest.TestCase):
    def setUp(self):
        mtype = ['SHELTER', 'SHELTER', 'SHELTER', 'SHELTER']
        lats = [34.61, 34.64, 34.66, 34.69]
        longs = [-84.19, -84.17, -84.12, -84.09]

        # define the center and the offsets for the 4 quadrants
        CENTER = (40, -76)
        self.LATITUDE_OFFSET = 3.35  # vertical
        self.LONGITUDE_OFFSET = 7.027  # horizontal

        # calculate the center of each of the four quadrants
        self.TOP_LEFT = (CENTER[0] + self.LATITUDE_OFFSET, CENTER[1] - self.LONGITUDE_OFFSET)
        self.TOP_RIGHT = (CENTER[0] + self.LATITUDE_OFFSET, CENTER[1] + self.LONGITUDE_OFFSET)
        self.BOTTOM_RIGHT = (CENTER[0] - self.LATITUDE_OFFSET, CENTER[1] + self.LONGITUDE_OFFSET)
        self.BOTTOM_LEFT = (CENTER[0] - self.LATITUDE_OFFSET, CENTER[1] - self.LONGITUDE_OFFSET)

        dt_reached = ['2017-03-13T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', pd.NaT]
        self.normal_df = pd.DataFrame({'dt_reached': dt_reached, 'lat': lats, 'lon': longs, 'type': mtype})

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.empty_df = pd.DataFrame({'dt_reached': dt_reached, 'lat': lats, 'lon': longs, 'type': mtype})

    def test_normal_hike(self):
        # Build the 4 quadrant URLs
        url1 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url2 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url3 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url4 = generate_url(self.normal_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)

        for url in [url1, url2, url3, url4]:
            self.assertLess(len(url), 8192)

    def test_no_location_data(self):
        # Build the 4 quadrant URLs
        url1 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url2 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url3 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)
        url4 = generate_url(self.empty_df, self.TOP_LEFT[0], self.TOP_LEFT[1], self.LATITUDE_OFFSET, self.LONGITUDE_OFFSET)

        for url in [url1, url2, url3, url4]:
            self.assertLess(len(url), 8192)

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
