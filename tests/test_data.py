import unittest

from geoagro.data import generate_association_products, load_data


class DataTests(unittest.TestCase):
    def test_sample_counts(self):
        data = load_data()
        self.assertEqual(len(data.associations), 17)
        self.assertEqual(len(data.localities), 14)
        self.assertEqual(len(data.products), 35)
        self.assertEqual({1, 2, 3, 4}, set().union(*(p.seasons for p in data.products)))

    def test_generated_offers_are_deterministic_and_complete(self):
        first = generate_association_products(tuple(range(1, 18)), tuple(range(1, 36)), seed=42)
        second = generate_association_products(tuple(range(1, 18)), tuple(range(1, 36)), seed=42)
        self.assertEqual(first, second)
        self.assertEqual(set(range(1, 36)), set().union(*first.values()))
        self.assertTrue(all(5 <= len(products) <= 10 for products in first.values()))
