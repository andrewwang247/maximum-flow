"""
Compute maximum flow on flow network.

Copyright 2026. Andrew Wang.
"""
import numpy as np  # type: ignore
from click import command, option, Path
from parse import create_network
# pylint: disable=no-value-for-parameter


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
