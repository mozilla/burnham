import dataclasses
import logging
import pathlib
import typing

import fake_glean as glean

logging.basicConfig(level=logging.DEBUG)

CONFIG_DIR = pathlib.Path("config")


@dataclasses.dataclass
class App:
    metrics_path: dataclasses.InitVar[pathlib.Path]
    pings_path: dataclasses.InitVar[pathlib.Path]
    metrics: typing.Any = dataclasses.field(init=False)
    pings: typing.Any = dataclasses.field(init=False)

    def __post_init__(self, metrics_path, pings_path):
        glean.set_upload_enabled(True)
        glean.initialize(app_id="burnham")

        self.metrics = glean.load_metrics(metrics_path)
        self.pings = glean.load_pings(pings_path)

    def __del__(self) -> None:
        """Send built-in Glean pings when the app is about to be destroyed."""
        glean.send_all_pings()
        glean.shutdown()

    def search(self, text: str) -> None:
        self.metrics.test.burnham.search_count["search_engine1"].record()


def run_app() -> None:
    app = App(CONFIG_DIR / "metrics.yaml", CONFIG_DIR / "pings.yaml",)
    app.search("mozilla firefox")

    print(f"📊 {dataclasses.asdict(app.metrics)}")

    app.pings.hello.send()


if __name__ == "__main__":
    run_app()
