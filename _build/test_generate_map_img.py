import unittest
import pandas as pd

from generate_map_img import generate_url


class TestGenerateMapImage(unittest.TestCase):
    def setUp(self):
        mtype = ['SHELTER', 'SHELTER', 'SHELTER', 'SHELTER']
        lats = [34.61, 34.64, 34.66, 34.69]
        longs = [-84.19, -84.17, -84.12, -84.09]

        dt_reached = ['2017-03-13T12:31:00', '2017-03-14T13:32:00', '2017-03-15T14:33:00', pd.NaT]
        self.normal_df = pd.DataFrame({'dt_reached': dt_reached, 'lat': lats, 'lon': longs, 'type': mtype})

        dt_reached = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        self.empty_df = pd.DataFrame({'dt_reached': dt_reached, 'lat': lats, 'lon': longs, 'type': mtype})

    def test_normal_hike(self):
        # Should output the first date in the dt_reached column
        url = generate_url(self.normal_df)

        self.assertLess(len(url), 8192)

    def test_no_location_data(self):
        # Should output the expected start date, since we have no date information
        url = generate_url(self.empty_df)

        self.assertLess(len(url), 8192)


if __name__ == '__main__':
    unittest.main()
