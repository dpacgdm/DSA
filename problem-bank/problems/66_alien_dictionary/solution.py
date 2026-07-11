from collections import defaultdict, deque
def alien_order(words: list[str]) -> str:
    g=defaultdict(set); indeg={c:0 for w in words for c in w}
    for a,b in zip(words, words[1:]):
        if len(a)>len(b) and a.startswith(b):
            return ""
        for ca,cb in zip(a,b):
            if ca!=cb:
                if cb not in g[ca]:
                    g[ca].add(cb); indeg[cb]+=1
                break
    q=deque([c for c,d in indeg.items() if d==0])
    out=[]
    while q:
        u=q.popleft(); out.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    return "".join(out) if len(out)==len(indeg) else ""
