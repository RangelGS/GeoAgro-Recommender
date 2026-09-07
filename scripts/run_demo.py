from geoagro.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main(
            [
                "recommend",
                "--latitude",
                "-15.7939",
                "--longitude",
                "-47.8828",
                "--max-distance",
                "30",
                "--season",
                "verao",
                "--products",
                "Alface",
                "Tomate",
            ]
        )
    )
