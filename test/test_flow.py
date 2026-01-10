"""
Pytest to run unit tests.

Copyright 2026. Andrew Wang.
"""
from os import path
from json import load
from typing import Dict, Iterable, Tuple
from pytest import mark
import numpy as np
from src import create_network

_TEST_DIR = 'test'


def _get_tests() -> Iterable[Tuple[str, int]]:
    """Get parametrized tests for pytest."""
    with open(path.join(_TEST_DIR, 'answers.json'),
              encoding='UTF-8') as fp:
        answers: Dict[str, int] = load(fp)
    for network, solution in answers.items():
        fname = path.join(_TEST_DIR, f'{network}.txt')
        assert path.isfile(fname), \
            f'Test file {fname} does not exist'
        yield fname, solution


@mark.parametrize('filename,expected_max', _get_tests())
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
