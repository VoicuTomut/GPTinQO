from pathlib import Path
from box import Box
import toml


def get_config(path: Path) -> Box:
    return Box(toml.load(path))


def update_config(config: Box, path: Path) -> Box:
    return config.update(toml.load(path))
