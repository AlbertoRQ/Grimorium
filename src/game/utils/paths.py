from pathlib import Path
import sys


def project_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[3]


def asset_path(*parts: str) -> Path:
    return project_root().joinpath("assets", *parts)


def data_path(*parts: str) -> Path:
    return project_root().joinpath("data", *parts)
