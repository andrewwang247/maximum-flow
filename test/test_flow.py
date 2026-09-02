"""Pytest to run unit tests.

Copyright 2026. Andrew Wang.
"""

from json import load
from pathlib import Path

import numpy as np
import pytest

from src import create_network

_TEST_DIR = "test"


def _get_tests() -> list[tuple[Path, int]]:
    """Get parametrized tests for pytest."""
    solutions = Path(_TEST_DIR) / "answers.json"
    with solutions.open(encoding="UTF-8") as fp:
        answers: dict[str, int] = load(fp)
    tests: list[tuple[Path, int]] = []
    for network, solution in answers.items():
        fpath = Path(_TEST_DIR) / f"{network}.txt"
        assert fpath.is_file(), f"Test file {fpath} does not exist"
        tests.append((fpath, solution))
    return tests


@pytest.mark.parametrize(("filepath", "expected_max"), _get_tests())
def test_flow(filepath: Path, expected_max: int) -> None:
    """Test network flow on filename."""
    network = create_network(filepath.open(encoding="UTF-8"))
    max_flow, flow = network.maximum_flow()
    assert max_flow == expected_max, "Max flow is incorrect."
    assert np.array_equal(np.transpose(flow), -flow), "Flow is not skew symmetric"
    assert (flow <= network.capacity).all(), "Flow exceeds capacity."
    assert np.sum(flow[network.source, :]) == expected_max, (
        "Input from source is incorrect."
    )
    assert np.sum(flow[:, network.sink]) == expected_max, "Output to sink is incorrect."
    for idx, net_flow in enumerate(np.sum(flow, axis=1)):
        assert net_flow == 0 or idx in (network.source, network.sink), (
            f"Flow conservation is violated at vertex {idx}."
        )
