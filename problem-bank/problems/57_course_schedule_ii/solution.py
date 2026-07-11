from collections import defaultdict, deque
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    g = defaultdict(list)
    indeg = [0]*num_courses
    for a,b in prerequisites:
        g[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num_courses) if indeg[i]==0])
    out = []
    while q:
        u = q.popleft(); out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v]==0:
                q.append(v)
    return out if len(out)==num_courses else []
