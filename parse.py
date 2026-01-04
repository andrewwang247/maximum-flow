"""
Parse DIMACS networks.

Copyright 2026. Andrew Wang.
"""
import logging
from typing import List, TextIO
from flow_network import FlowNetwork

logger = logging.getLogger(__name__)


def _get_next_line(fin: TextIO) -> List[str]:
    """Get the next non-comment line from file."""
    line = fin.readline().strip()
    while line.startswith('c'):
        line = fin.readline().strip()
    return line.split()


def create_network(filename: str) -> FlowNetwork:
    """Create a network from given DIMACS file."""
    num_arcs = 0
    with open(filename, encoding='UTF-8') as fin:
        first_tokens: List[str] = _get_next_line(fin)
        assert len(first_tokens) == 4
        assert first_tokens[0] == 'p'
        assert first_tokens[1] == 'max'
        nodes = int(first_tokens[2])
        arcs = int(first_tokens[3])
        second_tokens: List[str] = _get_next_line(fin)
        assert len(second_tokens) == 3
        assert second_tokens[2] == 's'
        source = int(second_tokens[1])
        third_tokens: List[str] = _get_next_line(fin)
        assert len(third_tokens) == 3
        assert third_tokens[2] == 't'
        sink = int(third_tokens[1])
        network = FlowNetwork(nodes, source, sink)
        for line in fin:
            tokens: List[str] = line.strip().split()
            identifier = tokens[0]
            assert identifier in ('a', 'c'), \
                f'Unrecognized identifer: {identifier}'
            if identifier == 'a':
                assert len(tokens) == 4
                network.add_edge(*[int(token) for token in tokens[1:]])
                num_arcs += 1
    assert arcs == num_arcs, f'Expected {arcs} arcs, but got {num_arcs}.'
    return network
