def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [0]*(n+1)
    for i in range(1, m+1):
        prev = 0
        for j in range(1, n+1):
            cur = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = cur
    return dp[n]
