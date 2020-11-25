# Maximum Flow

Efficient computation of a flow that maximizes flow rate on a [flow network](https://en.wikipedia.org/wiki/Flow_network) from a source to a sink. See <https://en.wikipedia.org/wiki/Maximum_flow_problem> for more details.

```text
Usage: max_flow.py [OPTIONS]

  Compute maximum flow on flow network.

Options:
  -f, --filename FILE  Path to flow network specification.  [required]
  --help               Show this message and exit.
```

## Algorithm

The program implements the [Edmonds-Karp algorithm](https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm), which is based on the [Ford-Fulkerson method](https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm). The network capacity and resultant maximum flow are represented as numpy matrices of shape (|V|, |V|).

## File Format

Graph file should be in [DIMACS format](http://lpsolve.sourceforge.net/5.5/DIMACS_maxf.htm) for networks. See the `Tests` directory for examples. Running the first test case, we get the following output.

```text
$ python3 max_flow.py -f Tests/test_0.txt
Received network with 6 nodes and 9 arcs.
Maximum flow = 10
0 -> 1 : 7 / 7
0 -> 2 : 3 / 4
1 -> 3 : 5 / 5
1 -> 4 : 3 / 3
2 -> 1 : 1 / 3
2 -> 4 : 2 / 2
3 -> 5 : 5 / 8
4 -> 3 : 0 / 3
4 -> 5 : 5 / 5
```

The output line `u -> v : f / c` should be interpreted as saying that the directed edge from vertex `u` to vertex `v` gets flow `f` of its capacity `c`.

## Testing

Run `pytest` to test the program on inputs in the `Tests` directory. All properties of a valid flow are verified and the maximum flow rate is checked.
