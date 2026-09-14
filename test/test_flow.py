"""Pytest to run unit tests.

Copyright 2026. Andrew Wang.
"""

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .conftest import Solution


def test_flow(solution: Solution) -> None:
    """Test network flow on filename."""
    network = solution.network
    max_flow, flow = network.maximum_flow()

    assert max_flow == solution.max_flow
    assert np.array_equal(flow.T, -flow), "Flow is not skew symmetric"
    assert (flow <= network.capacity).all(), "Flow exceeds capacity."

    from_source = np.sum(flow[network.source, :])
    to_sink = np.sum(flow[:, network.sink])
    assert from_source == solution.max_flow == to_sink

    for idx, net_flow in enumerate(np.sum(flow, axis=1)):
        if idx in (network.source, network.sink):
            continue
        assert net_flow == 0, f"Flow conservation violated at vertex {idx}."
