"""
Representation of flow network.

Copyright 2020. Siwei Wang.
"""
from typing import Tuple, List
from collections import deque
import numpy as np  # type: ignore


class FlowNetwork:
    """Representation of flow network."""

    def __init__(self, vertices: int, source: int, sink: int):
        """Zero initialize all member variables."""
        assert 0 <= source < vertices, f'Source {source} is out of bounds.'
        assert 0 <= sink < vertices, f'Sink {sink} is out of bounds.'
        assert source != sink, 'Source and sink cannot be the same vertex.'
        self.vertices = vertices
        self.source = source
        self.sink = sink
        self.capacity = np.zeros((vertices, vertices), dtype=int)

    def add_edge(self, src: int, dst: int, cap: int):
        """Adds a directed edge src -> dst with the given capacity."""
        assert cap > 0, \
            f'Capacity {cap} assigned to {src} -> {dst} is non-positive.'
        assert src != self.sink, 'Sink cannot have outgoing capacity.'
        assert dst != self.source, 'Source cannot have incoming capacity.'
        assert self.capacity[src, dst] == 0, \
            f'Capacity of {src} -> {dst} has already been assigned.'
        assert self.capacity[dst, src] == 0, \
            f'Reverse capacity of {dst} -> {src} is non-zero.'
        self.capacity[src, dst] = cap

    def _gen_path(self, predecessor: np.ndarray) -> List[int]:
        """Return the path source -> sink given by predecessor list."""
        next_vertex = self.sink
        path: List[int] = []
        while next_vertex != self.source:
            path.append(next_vertex)
            next_vertex = predecessor[next_vertex]
        path.append(self.source)
        path.reverse()
        return path

    class PathError(Exception):
        """Custom exception for augmenting paths."""

    def _find_augmenting_path(self, flow: np.ndarray) \
            -> Tuple[int, List[int]]:
        """Finds an augmenting path and new flow. Throws if non-existent."""
        residual = self.capacity - flow
        queue = deque((self.source,))
        predecessor = np.full(self.vertices, -1, dtype=int)
        while queue:
            current: int = queue.popleft()
            unvisited = filter(
                lambda vert: predecessor[vert] == -1, range(self.vertices)
            )
            has_flow = filter(
                lambda vert: residual[current, vert] > 0, unvisited
            )
            for vert in has_flow:
                predecessor[vert] = current
                if vert == self.sink:
                    path = self._gen_path(predecessor)
                    new_flow: int = min(residual[src, dst] for src,
                                        dst in zip(path, path[1:]))
                    return new_flow, path
                queue.append(vert)
        raise self.PathError('No augmenting path found.')

    def maximum_flow(self) -> Tuple[int, np.ndarray]:
        """Compute maximum flow on the network and flow matrix."""
        max_flow = 0
        flow = np.zeros((self.vertices, self.vertices), dtype=int)
        while True:
            try:
                new_flow, path = self._find_augmenting_path(flow)
                max_flow += new_flow
                for src, dst in zip(path, path[1:]):
                    flow[src, dst] += new_flow
                    flow[dst, src] -= new_flow
            except self.PathError:
                return max_flow, flow
