from __future__ import annotations

import csv
import random
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Association:
    id: int
    acronym: str
    name: str


@dataclass(frozen=True)
class Locality:
    id: int
    name: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    seasons: frozenset[int]


@dataclass(frozen=True)
class AssociationLocality:
    association_id: int
    locality_id: int


@dataclass(frozen=True)
class Review:
    user: str
    product: str
    rating: int
    comment: str


@dataclass(frozen=True)
class DataBundle:
    associations: tuple[Association, ...]
    localities: tuple[Locality, ...]
    association_localities: tuple[AssociationLocality, ...]
    products: tuple[Product, ...]
    reviews: tuple[Review, ...]


def normalize_text(value: str) -> str:
    """Return a lowercase, accent-insensitive comparison key."""
    decomposed = unicodedata.normalize("NFKD", value.strip())
    return "".join(char for char in decomposed if not unicodedata.combining(char)).casefold()


def default_data_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "sample"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_data(data_dir: str | Path | None = None) -> DataBundle:
    base = Path(data_dir) if data_dir else default_data_dir()

    associations = tuple(
        Association(int(row["id"]), row["acronym"], row["name"])
        for row in _rows(base / "associations.csv")
    )
    localities = tuple(
        Locality(
            int(row["id"]),
            row["name"],
            float(row["latitude"]),
            float(row["longitude"]),
        )
        for row in _rows(base / "localities.csv")
    )
    association_localities = tuple(
        AssociationLocality(int(row["association_id"]), int(row["locality_id"]))
        for row in _rows(base / "association_localities.csv")
    )
    products = tuple(
        Product(
            int(row["id"]),
            row["name"],
            frozenset(int(item) for item in row["season_ids"].split(";")),
        )
        for row in _rows(base / "products.csv")
    )
    reviews = tuple(
        Review(row["user"], row["product"], int(row["rating"]), row["comment"])
        for row in _rows(base / "reviews.csv")
    )
    return DataBundle(
        associations,
        localities,
        association_localities,
        products,
        reviews,
    )


def generate_association_products(
    association_ids: list[int] | tuple[int, ...],
    product_ids: list[int] | tuple[int, ...],
    *,
    seed: int = 42,
    minimum: int = 5,
    maximum: int = 10,
) -> dict[int, frozenset[int]]:
    """Create deterministic demonstration offers while covering every product."""
    if not association_ids or not product_ids:
        raise ValueError("association_ids and product_ids cannot be empty")
    if minimum < 1 or maximum < minimum or maximum > len(product_ids):
        raise ValueError("invalid minimum/maximum product limits")

    rng = random.Random(seed)
    offers: dict[int, set[int]] = {identifier: set() for identifier in association_ids}

    for product_id in product_ids:
        offers[rng.choice(association_ids)].add(product_id)

    for association_id in association_ids:
        while len(offers[association_id]) < minimum:
            offers[association_id].add(rng.choice(product_ids))
        target = rng.randint(len(offers[association_id]), maximum)
        while len(offers[association_id]) < target:
            offers[association_id].add(rng.choice(product_ids))

    return {key: frozenset(value) for key, value in offers.items()}
