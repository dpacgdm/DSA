def total_nqueens(n: int) -> int:
    cols=set(); d1=set(); d2=set(); ans=0
    def dfs(r):
        nonlocal ans
        if r==n:
            ans+=1; return
        for c in range(n):
            if c in cols or r-c in d1 or r+c in d2:
                continue
            cols.add(c); d1.add(r-c); d2.add(r+c)
            dfs(r+1)
            cols.remove(c); d1.remove(r-c); d2.remove(r+c)
    dfs(0)
    return ans
