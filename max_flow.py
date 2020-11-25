"""
Compute maximum flow on flow network.

Copyright 2020. Siwei Wang.
"""
from typing import List
import numpy as np  # type: ignore
import click
from flow_network import FlowNetwork
# pylint: disable=no-value-for-parameter


def create_network(filename: str) -> FlowNetwork:
    """Create a network from given DIMACS file."""
    num_arcs = 0
    network_exists = False
    nodes = -1
    source_sink: List[int] = [-1, -1]
    with open(filename) as fin:
        for line in fin:
            if not network_exists and \
                    all(arg != -1 for arg in (nodes, *source_sink)):
                network = FlowNetwork(nodes, source_sink[0], source_sink[1])
                network_exists = True
            tokens: List[str] = line.strip().split()
            identifier = tokens[0]
            if identifier == 'c':
                continue
            if identifier == 'p':
                assert tokens[1] == 'max'
                assert len(tokens) == 4
                nodes = int(tokens[2])
                arcs = int(tokens[3])
            elif identifier == 'n':
                assert len(tokens) == 3
                idx = ('s', 't').index(tokens[2])
                source_sink[idx] = int(tokens[1])
            elif identifier == 'a':
                assert len(tokens) == 4
                network.add_edge(*[int(token) for token in tokens[1:]])
                num_arcs += 1
            else:
                raise RuntimeError(f'Designator {identifier} is unknown.')
    assert arcs == num_arcs, 'Incorrect number of arcs specified.'
    return network


@click.command()
@click.option('--filename', '-f', type=click.Path(exists=True,
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
    for src, dst in zip(*np.nonzero(network.capacity)):
        flow = flow_matrix[src, dst]
        capacity = network.capacity[src, dst]
        print(f'{src} -> {dst} : {flow} / {capacity}')


if __name__ == '__main__':
    main()
