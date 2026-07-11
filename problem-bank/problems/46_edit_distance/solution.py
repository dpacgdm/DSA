def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = list(range(n+1))
    for i in range(1, m+1):
        ndp = [i] + [0]*n
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                ndp[j] = dp[j-1]
            else:
                ndp[j] = 1 + min(dp[j], ndp[j-1], dp[j-1])
        dp = ndp
    return dp[n]
