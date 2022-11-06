"""
Compute maximum flow on flow network.

Copyright 2020. Siwei Wang.
"""
from typing import List
import numpy as np  # type: ignore
from click import command, option, Path
from flow_network import FlowNetwork
# pylint: disable=no-value-for-parameter


def create_network(filename: str) -> FlowNetwork:
    """Create a network from given DIMACS file."""
    num_arcs = 0
    with open(filename, encoding='UTF-8') as fin:
        first_tokens: List[str] = fin.readline().strip().split()
        assert len(first_tokens) == 4
        assert first_tokens[0] == 'p'
        assert first_tokens[1] == 'max'
        nodes = int(first_tokens[2])
        arcs = int(first_tokens[3])
        second_tokens: List[str] = fin.readline().strip().split()
        assert len(second_tokens) == 3
        assert second_tokens[2] == 's'
        source = int(second_tokens[1])
        third_tokens: List[str] = fin.readline().strip().split()
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


@command()
@option('--filename', '-f', type=Path(exists=True,
                                      file_okay=True,
                                      dir_okay=False,
                                      readable=True),
        required=True, help='Path to flow network specification.')
def main(filename: str):
    """Compute maximum flow on flow network."""
    network = create_network(filename)
    print(f'Received network with {network.vertices} nodes',
          f'and {np.count_nonzero(network.capacity)} arcs.')
    max_flow, flow_matrix = network.maximum_flow()
    print(f'Maximum flow = {max_flow}')
    dim_1, dim_2 = np.nonzero(network.capacity)
    for src, dst in zip(dim_1, dim_2):
        flow = flow_matrix[src, dst]
        capacity = network.capacity[src, dst]
        print(f'{src} -> {dst} : {flow} / {capacity}')


if __name__ == '__main__':
    main()
