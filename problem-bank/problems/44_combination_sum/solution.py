def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    out = []
    def dfs(start, remain, path):
        if remain == 0:
            out.append(path[:]); return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            dfs(i, remain-c, path)
            path.pop()
    dfs(0, target, [])
    return out
