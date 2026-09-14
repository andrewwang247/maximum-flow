"""Configure pytest fixtures.

Copyright 2026. Andrew Wang.
"""

from dataclasses import dataclass
from json import load
from pathlib import Path

import pytest

from src import FlowNetwork, create_network

_RESOURCE_DIR = Path("resources")


def get_index() -> dict[str, int]:
    """Get answers index from JSON."""
    solutions = _RESOURCE_DIR / "answers.json"
    with solutions.open(encoding="UTF-8") as fp:
        index: dict[str, int] = load(fp)
    return index


@dataclass
class Solution:
    """Max flow for a single network."""

    network: FlowNetwork
    max_flow: int


@pytest.fixture(scope="session", params=get_index().items())
def solution(request: pytest.FixtureRequest) -> Solution:
    """Provide solution for a given network."""
    index_item: tuple[str, int] = request.param
    nw, max_flow = index_item

    filepath = _RESOURCE_DIR / f"{nw}.txt"
    assert filepath.is_file()
    assert max_flow > 0

    network = create_network(filepath.open(encoding="UTF-8"))
    return Solution(network, max_flow)
