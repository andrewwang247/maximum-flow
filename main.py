"""Compute maximum flow on flow network.

Copyright 2026. Andrew Wang.
"""

import logging
from typing import TextIO

import numpy as np
from click import File, command, option

from src import create_network


@command()
@option(
    "--input_nw",
    "-i",
    required=True,
    type=File("r", encoding="UTF-8"),
    help="Where to read network specification.",
)
@option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Set verbosity of solving process.",
)
def main(input_nw: TextIO, *, verbose: bool) -> None:
    """Compute maximum flow on flow network."""
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)
    network = create_network(input_nw)
    max_flow, flow_matrix = network.maximum_flow()
    print(f"Maximum flow = {max_flow}")
    dim_1, dim_2 = np.nonzero(network.capacity)
    for src, dst in zip(dim_1, dim_2, strict=True):
        flow = flow_matrix[src, dst]
        capacity = network.capacity[src, dst]
        print(f"{src} -> {dst} : {flow} / {capacity}")


if __name__ == "__main__":
    main()
