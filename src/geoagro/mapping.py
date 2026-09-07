from __future__ import annotations

from html import escape
from pathlib import Path

from .data import DataBundle
from .ranking import RankingResult


def save_map(
    results: list[RankingResult],
    data: DataBundle,
    output: str | Path,
    *,
    user_latitude: float,
    user_longitude: float,
) -> Path:
    """Save ranking markers to an interactive Folium HTML map."""
    try:
        import folium
    except ImportError as exc:  # pragma: no cover - depends on optional package
        raise RuntimeError('install map support with: pip install -e ".[map]"') from exc

    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    locality_by_name = {item.name: item for item in data.localities}
    map_object = folium.Map(location=[user_latitude, user_longitude], zoom_start=10)
    folium.Marker(
        [user_latitude, user_longitude],
        tooltip="Local informado",
        icon=folium.Icon(color="red", icon="user"),
    ).add_to(map_object)

    for result in results:
        locality = locality_by_name[result.locality]
        popup = (
            f"<strong>{escape(result.association)}</strong><br>"
            f"Localidade: {escape(result.locality)}<br>"
            f"Distância: {result.distance_km:.2f} km<br>"
            f"Pontuação total: {result.total_score}"
        )
        folium.Marker(
            [locality.latitude, locality.longitude],
            tooltip=f"{result.position}º — {escape(result.acronym)}",
            popup=folium.Popup(popup, max_width=360),
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(map_object)

    map_object.save(str(destination))
    return destination
