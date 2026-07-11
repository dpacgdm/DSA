def min_assignment_cost(cost: list[list[int]]) -> int:
    n = len(cost)
    N = 1 << n
    INF = 10**18
    dp = [INF]*N
    dp[0] = 0
    for mask in range(N):
        i = mask.bit_count()
        if i >= n:
            continue
        for j in range(n):
            if mask & (1 << j):
                continue
            nxt = mask | (1 << j)
            dp[nxt] = min(dp[nxt], dp[mask] + cost[i][j])
    return dp[N-1]
