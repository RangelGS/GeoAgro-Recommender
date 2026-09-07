import unittest

from geoagro.collaborative import recommend_from_similar_users
from geoagro.data import Review


class CollaborativeTests(unittest.TestCase):
    def test_recommends_unseen_products_from_shared_history(self):
        reviews = [
            Review("Ana", "Alface", 5, ""),
            Review("Bruno", "Alface", 4, ""),
            Review("Bruno", "Manga", 5, "doce"),
            Review("Bruno", "Banana", 4, "boa"),
            Review("Carla", "Tomate", 5, ""),
        ]
        results = recommend_from_similar_users("Ana", reviews)
        self.assertEqual([item.product for item in results], ["Manga", "Banana"])
        self.assertNotIn("Alface", [item.product for item in results])

    def test_unknown_user_returns_empty_list(self):
        self.assertEqual(recommend_from_similar_users("Ninguém", []), [])
