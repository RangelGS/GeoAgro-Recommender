from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .data import generate_association_products, load_data
from .mapping import save_map
from .ranking import RankingResult, rank_associations


def _write_csv(results: list[RankingResult], output: str | Path) -> Path:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(RankingResult.__dataclass_fields__)
    with destination.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result.as_dict() for result in results)
    return destination


def _display(results: list[RankingResult]) -> None:
    if not results:
        print("Nenhuma associação encontrada para os critérios informados.")
        return
    print(f"{'#':>2}  {'Sigla':<16} {'Localidade':<20} {'km':>8} {'Sazonais':>9} {'Score':>6}")
    for item in results:
        print(
            f"{item.position:>2}  {item.acronym:<16.16} {item.locality:<20.20} "
            f"{item.distance_km:>8.2f} {item.seasonal_products:>9} {item.total_score:>6}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recomendador georreferenciado GeoAgro")
    subparsers = parser.add_subparsers(dest="command", required=True)
    recommend = subparsers.add_parser("recommend", help="gerar ranking de associações")
    recommend.add_argument("--latitude", type=float, required=True)
    recommend.add_argument("--longitude", type=float, required=True)
    recommend.add_argument("--max-distance", type=float, default=-1)
    recommend.add_argument("--season", default="verao")
    recommend.add_argument("--products", nargs="*", default=[])
    recommend.add_argument("--seed", type=int, default=42)
    recommend.add_argument("--data-dir")
    recommend.add_argument("--output", help="salvar ranking em CSV")
    recommend.add_argument("--map", dest="map_output", help="salvar mapa HTML")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    data = load_data(args.data_dir)
    offers = generate_association_products(
        tuple(item.id for item in data.associations),
        tuple(item.id for item in data.products),
        seed=args.seed,
    )
    try:
        results = rank_associations(
            data,
            latitude=args.latitude,
            longitude=args.longitude,
            max_distance_km=args.max_distance,
            season=args.season,
            products=args.products,
            offers=offers,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _display(results)
    if args.output:
        print(f"CSV salvo em {_write_csv(results, args.output)}")
    if args.map_output:
        print(
            f"Mapa salvo em {save_map(results, data, args.map_output, user_latitude=args.latitude, user_longitude=args.longitude)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
