"""
Parse DIMACS networks.

Copyright 2026. Andrew Wang.
"""
from typing import List, TextIO
from flow_network import FlowNetwork


def _is_statement(line: str) -> bool:
    """Determine if the line is a statament."""
    return len(line) > 0 and not line.startswith('c')


def _get_next_line(fin: TextIO) -> List[str]:
    """Get the next non-comment line from file."""
    line = fin.readline().strip()
    while not _is_statement(line):
        line = fin.readline().strip()
    return line.split()


def create_network(filename: str) -> FlowNetwork:
    """Create a network from given DIMACS file."""
    num_arcs = 0
    with open(filename, encoding='UTF-8') as fin:
        first_tokens = _get_next_line(fin)
        assert len(first_tokens) == 4
        assert first_tokens[0] == 'p', \
            'Problem statements begin with "p"'
        assert first_tokens[1] == 'max', \
            'Only max flow problems are allowed.'
        nodes = int(first_tokens[2])
        arcs = int(first_tokens[3])

        second_tokens = _get_next_line(fin)
        assert second_tokens[0] == 'n', \
            'Source statements begin with "n"'
        assert len(second_tokens) == 3, \
            'Source statements require 2 values.'
        assert second_tokens[2] == 's', \
            'Source statements end with "s"'
        source = int(second_tokens[1])

        third_tokens = _get_next_line(fin)
        assert third_tokens[0] == 'n', \
            'Sink statements begin with "n"'
        assert len(third_tokens) == 3, \
            'Sink statements require 2 values.'
        assert third_tokens[2] == 't', \
            'Sink statements end with "t"'
        sink = int(third_tokens[1])

        network = FlowNetwork(nodes, source, sink)
        for raw_line in fin:
            line = raw_line.strip()
            if not _is_statement(line):
                continue
            tokens = line.split()
            assert tokens[0] == 'a', \
                'Arc statements begin with "a"'
            assert len(tokens) == 4, \
                'Arc statements require 3 values.'
            network.add_edge(*[int(token) for token in tokens[1:]])
            num_arcs += 1

    assert arcs == num_arcs, f'Expected {arcs} arcs, but got {num_arcs}.'
    return network
