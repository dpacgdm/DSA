def max_profit(prices: list[int]) -> int:
    best = 0
    lo = prices[0] if prices else 0
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best
