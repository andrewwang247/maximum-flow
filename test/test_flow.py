"""Pytest to run unit tests.

Copyright 2026. Andrew Wang.
"""

from json import load
from pathlib import Path

import numpy as np
import pytest

from src import FlowNetwork, create_network

_TEST_DIR = Path("test")


def _get_tests() -> list[tuple[FlowNetwork, int]]:
    """Get parametrized tests for pytest."""
    solutions = _TEST_DIR / "answers.json"
    with solutions.open(encoding="UTF-8") as fp:
        answers: dict[str, int] = load(fp)
    params: list[tuple[FlowNetwork, int]] = []
    for nw, expected_max in answers.items():
        filepath = _TEST_DIR / f"{nw}.txt"
        assert filepath.is_file()
        assert expected_max > 0
        network = create_network(filepath.open(encoding="UTF-8"))
        params.append((network, expected_max))
    return params


@pytest.mark.parametrize(("network", "expected_max"), _get_tests())
def test_flow(network: FlowNetwork, expected_max: int) -> None:
    """Test network flow on filename."""
    max_flow, flow = network.maximum_flow()

    assert max_flow == expected_max
    assert np.array_equal(flow.T, -flow), "Flow is not skew symmetric"
    assert (flow <= network.capacity).all(), "Flow exceeds capacity."

    from_source = np.sum(flow[network.source, :])
    to_sink = np.sum(flow[:, network.sink])
    assert from_source == expected_max == to_sink

    for idx, net_flow in enumerate(np.sum(flow, axis=1)):
        if idx in (network.source, network.sink):
            continue
        assert net_flow == 0, f"Flow conservation violated at vertex {idx}."
