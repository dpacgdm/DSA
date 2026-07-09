# Network Delay Time (LC 743) — Dijkstra

You are given a network of `n` nodes labeled `1` to `n`.
`times[i] = [u, v, w]` is a directed edge from `u` to `v` with travel time `w`.

Send a signal from node `k`. Return how long it takes for all nodes to receive it,
or `-1` if it is impossible.

## API

```python
def network_delay_time(times: list[list[int]], n: int, k: int) -> int
```
