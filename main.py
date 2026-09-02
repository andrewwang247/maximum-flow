"""Compute maximum flow on flow network.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path

import numpy as np
from click import Path as cPath
from click import command, option

from src import create_network


@command()
@option(
    "--filename",
    "-f",
    required=True,
    type=cPath(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to flow network specification.",
)
@option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Set verbosity of solving process.",
)
def main(filename: str, *, verbose: bool) -> None:
    """Compute maximum flow on flow network."""
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)
    network = create_network(Path(filename))
    max_flow, flow_matrix = network.maximum_flow()
    print(f"Maximum flow = {max_flow}")
    dim_1, dim_2 = np.nonzero(network.capacity)
    for src, dst in zip(dim_1, dim_2, strict=True):
        flow = flow_matrix[src, dst]
        capacity = network.capacity[src, dst]
        print(f"{src} -> {dst} : {flow} / {capacity}")


if __name__ == "__main__":
    main()
