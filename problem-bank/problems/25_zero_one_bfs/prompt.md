# 0-1 BFS Shortest Path

Given `n` nodes labeled `0..n-1`, a list of directed edges `edges` where each edge is
`[u, v, w]` with `w` in `{0, 1}`, and a source `src`, return the shortest-path distances
from `src` to every node. Use `10**18` for unreachable.

## API

```python
def zero_one_bfs(n: int, edges: list[list[int]], src: int) -> list[int]
```
