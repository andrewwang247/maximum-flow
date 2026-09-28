"""Parse DIMACS networks.

Copyright 2026. Andrew Wang.
"""

from typing import TYPE_CHECKING, TextIO

from .flow_network import FlowNetwork

if TYPE_CHECKING:
    from collections.abc import Iterator


def _tokenize(fin: TextIO) -> Iterator[list[str]]:
    """Get the next non-comment line from file."""
    for line in fin:
        stripped = line.strip()
        if stripped and not stripped.startswith("c"):
            yield stripped.split()


def create_network(fin: TextIO) -> FlowNetwork:
    """Create a network from given DIMACS file."""
    tokenized = _tokenize(fin)

    problem_tokens = next(tokenized)
    assert len(problem_tokens) == 4
    assert problem_tokens[0] == "p", 'Problem statements begin with "p"'
    assert problem_tokens[1] == "max", "Only max flow problems are allowed."
    nodes = int(problem_tokens[2])
    arcs = int(problem_tokens[3])

    source_tokens = next(tokenized)
    assert len(source_tokens) == 3, "Source statements require 2 values."
    assert source_tokens[0] == "n", 'Source statements begin with "n"'
    assert source_tokens[2] == "s", 'Source statements end with "s"'
    source = int(source_tokens[1])

    sink_tokens = next(tokenized)
    assert len(sink_tokens) == 3, "Sink statements require 2 values."
    assert sink_tokens[0] == "n", 'Sink statements begin with "n"'
    assert sink_tokens[2] == "t", 'Sink statements end with "t"'
    sink = int(sink_tokens[1])

    network = FlowNetwork(nodes, source, sink)
    num_arcs = 0
    for arc_tokens in tokenized:
        assert len(arc_tokens) == 4, "Arc statements require 3 values."
        assert arc_tokens[0] == "a", 'Arc statements begin with "a"'
        src, dst, cap = [int(tk) for tk in arc_tokens[1:]]
        network.add_edge(src, dst, cap)
        num_arcs += 1

    assert arcs == num_arcs, f"Expected {arcs} arcs, but got {num_arcs}."
    return network
