from __future__ import annotations

from math import asin, cos, radians, sin, sqrt


EARTH_RADIUS_KM = 6371.0088


def haversine_km(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> float:
    """Calculate great-circle distance between two WGS84 coordinates."""
    if not (-90 <= latitude_a <= 90 and -90 <= latitude_b <= 90):
        raise ValueError("latitude must be between -90 and 90")
    if not (-180 <= longitude_a <= 180 and -180 <= longitude_b <= 180):
        raise ValueError("longitude must be between -180 and 180")

    lat_a, lat_b = radians(latitude_a), radians(latitude_b)
    delta_lat = radians(latitude_b - latitude_a)
    delta_lon = radians(longitude_b - longitude_a)
    value = sin(delta_lat / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(value))
