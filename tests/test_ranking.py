import unittest

from geoagro.data import (
    Association,
    AssociationLocality,
    DataBundle,
    Locality,
    Product,
)
from geoagro.ranking import rank_associations, season_id


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.data = DataBundle(
            associations=(Association(1, "A", "Associação A"), Association(2, "B", "Associação B")),
            localities=(
                Locality(1, "Perto", 0.0, 0.0),
                Locality(2, "Longe", 0.0, 1.0),
            ),
            association_localities=(AssociationLocality(1, 1), AssociationLocality(2, 2)),
            products=(
                Product(1, "Alface", frozenset({2})),
                Product(2, "Repolho", frozenset({4})),
            ),
            reviews=(),
        )

    def test_season_accepts_accented_portuguese(self):
        self.assertEqual(season_id("verão"), 2)

    def test_nearest_association_ranks_first(self):
        results = rank_associations(
            self.data,
            latitude=0,
            longitude=0,
            season="verao",
            offers={1: frozenset({1}), 2: frozenset({1})},
        )
        self.assertEqual([item.acronym for item in results], ["A", "B"])
        self.assertEqual([item.total_score for item in results], [0, 1])

    def test_product_and_season_filters_are_combined(self):
        results = rank_associations(
            self.data,
            latitude=0,
            longitude=0,
            season="inverno",
            products=["Repolho"],
            offers={1: frozenset({1}), 2: frozenset({2})},
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].acronym, "B")

    def test_unknown_product_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown products"):
            rank_associations(
                self.data,
                latitude=0,
                longitude=0,
                products=["Produto inexistente"],
                offers={1: frozenset({1}), 2: frozenset({2})},
            )
