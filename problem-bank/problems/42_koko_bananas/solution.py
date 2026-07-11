def min_eating_speed(piles: list[int], h: int) -> int:
    def ok(k):
        return sum((p + k - 1)//k for p in piles) <= h
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo+hi)//2
        if ok(mid):
            hi = mid
        else:
            lo = mid+1
    return lo
