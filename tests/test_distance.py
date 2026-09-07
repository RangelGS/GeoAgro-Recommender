import unittest

from geoagro.distance import haversine_km


class DistanceTests(unittest.TestCase):
    def test_same_point_is_zero(self):
        self.assertEqual(haversine_km(-15.79, -47.88, -15.79, -47.88), 0.0)

    def test_one_degree_at_equator(self):
        self.assertAlmostEqual(haversine_km(0, 0, 1, 0), 111.195, places=3)

    def test_invalid_latitude_is_rejected(self):
        with self.assertRaises(ValueError):
            haversine_km(91, 0, 0, 0)
