"""
Pytest to run unit tests.

Copyright 2020. Siwei Wang.
"""
from os import path
from typing import List, Tuple
from pytest import mark
import numpy as np  # type: ignore
from max_flow import create_network


def get_tests(solutions: List[int]) -> List[Tuple[str, int]]:
    """Get parametrized tests for pytest."""
    files: List[str] = [path.join('Tests', f'test_{idx}.txt')
                        for idx in range(len(solutions))]
    assert all(path.isfile(filename) for filename in files)
    return list(zip(files, solutions))


@mark.parametrize('filename,expected_max', get_tests([10, 5, 7, 6]))
def test_flow(filename: str, expected_max: int):
    """Test network flow on filename."""
    network = create_network(filename)
    max_flow, flow = network.maximum_flow()
    assert max_flow == expected_max, 'Max flow is incorrect.'
    assert np.array_equal(np.transpose(flow), -flow), \
        'Flow is not skew symmetric'
    assert (flow <= network.capacity).all(), \
        'Flow exceeds capacity.'
    assert np.sum(flow[network.source, :]) == expected_max, \
        'Input from source is incorrect.'
    assert np.sum(flow[:, network.sink]) == expected_max, \
        'Output to sink is incorrect.'
    for idx, net_flow in enumerate(np.sum(flow, axis=1)):
        assert net_flow == 0 or idx in (network.source, network.sink), \
            f'Flow conservation is violated at vertex {idx}.'
