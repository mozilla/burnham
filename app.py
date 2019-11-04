import pathlib

import fake_glean as glean

DATA_DIR = pathlib.Path("data")


def run_app():
    metrics = glean.load_metrics(DATA_DIR / "metrics.yaml")


if __name__ == "__main__":
    run_app()
