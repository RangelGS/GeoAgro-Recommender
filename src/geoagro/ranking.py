from __future__ import annotations

from dataclasses import asdict, dataclass

from .data import DataBundle, generate_association_products, normalize_text
from .distance import haversine_km


SEASONS = {
    "primavera": 1,
    "verao": 2,
    "outono": 3,
    "inverno": 4,
}


@dataclass(frozen=True)
class RankingResult:
    position: int
    association_id: int
    acronym: str
    association: str
    locality: str
    distance_km: float
    seasonal_products: int
    distance_score: int
    seasonal_score: int
    total_score: int

    def as_dict(self) -> dict[str, int | float | str]:
        return asdict(self)


def season_id(value: str | int) -> int:
    if isinstance(value, int):
        if value not in SEASONS.values():
            raise ValueError("season must be between 1 and 4")
        return value
    key = normalize_text(value)
    if key not in SEASONS:
        raise ValueError("season must be primavera, verao, outono or inverno")
    return SEASONS[key]


def _dense_scores(values: dict[int, float | int], *, ascending: bool) -> dict[int, int]:
    unique = sorted(set(values.values()), reverse=not ascending)
    score_by_value = {value: index for index, value in enumerate(unique)}
    return {identifier: score_by_value[value] for identifier, value in values.items()}


def rank_associations(
    data: DataBundle,
    *,
    latitude: float,
    longitude: float,
    max_distance_km: float = -1,
    season: str | int = "verao",
    products: list[str] | tuple[str, ...] = (),
    offers: dict[int, frozenset[int]] | None = None,
    seed: int = 42,
) -> list[RankingResult]:
    """Rank associations using the original distance + season heuristic."""
    selected_season = season_id(season)
    association_by_id = {item.id: item for item in data.associations}
    locality_by_id = {item.id: item for item in data.localities}
    product_by_name = {normalize_text(item.name): item for item in data.products}

    requested_ids: set[int] = set()
    unknown: list[str] = []
    for name in products:
        product = product_by_name.get(normalize_text(name))
        if product:
            requested_ids.add(product.id)
        else:
            unknown.append(name)
    if unknown:
        raise ValueError(f"unknown products: {', '.join(unknown)}")

    if offers is None:
        offers = generate_association_products(
            tuple(association_by_id), tuple(product.id for product in data.products), seed=seed
        )

    nearest: dict[int, tuple[int, float]] = {}
    for link in data.association_localities:
        locality = locality_by_id[link.locality_id]
        distance = haversine_km(latitude, longitude, locality.latitude, locality.longitude)
        current = nearest.get(link.association_id)
        if current is None or distance < current[1]:
            nearest[link.association_id] = (locality.id, distance)

    if max_distance_km >= 0:
        nearest = {
            identifier: value
            for identifier, value in nearest.items()
            if value[1] <= max_distance_km
        }
    if not nearest:
        return []

    distance_scores = _dense_scores(
        {identifier: round(value[1], 9) for identifier, value in nearest.items()},
        ascending=True,
    )

    seasonal_counts: dict[int, int] = {}
    for association_id in nearest:
        offered = offers.get(association_id, frozenset())
        relevant = offered & requested_ids if requested_ids else set(offered)
        count = sum(
            1
            for product in data.products
            if product.id in relevant and selected_season in product.seasons
        )
        if count:
            seasonal_counts[association_id] = count
    if not seasonal_counts:
        return []

    seasonal_scores = _dense_scores(seasonal_counts, ascending=False)
    provisional: list[RankingResult] = []
    for association_id, count in seasonal_counts.items():
        locality_id, distance = nearest[association_id]
        association = association_by_id[association_id]
        distance_score = distance_scores[association_id]
        seasonal_score = seasonal_scores[association_id]
        provisional.append(
            RankingResult(
                position=0,
                association_id=association_id,
                acronym=association.acronym,
                association=association.name,
                locality=locality_by_id[locality_id].name,
                distance_km=round(distance, 3),
                seasonal_products=count,
                distance_score=distance_score,
                seasonal_score=seasonal_score,
                total_score=distance_score + seasonal_score,
            )
        )

    ordered = sorted(
        provisional,
        key=lambda item: (item.total_score, item.distance_km, item.acronym.casefold()),
    )
    return [
        RankingResult(position=index, **{k: v for k, v in item.as_dict().items() if k != "position"})
        for index, item in enumerate(ordered, start=1)
    ]
