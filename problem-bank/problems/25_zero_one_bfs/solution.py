from collections import defaultdict, deque

def zero_one_bfs(n: int, edges: list[list[int]], src: int) -> list[int]:
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    INF = 10**18
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in g[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist
