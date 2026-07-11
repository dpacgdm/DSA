from collections import defaultdict
def subarray_sum(nums: list[int], k: int) -> int:
    pref = 0
    cnt = defaultdict(int)
    cnt[0] = 1
    ans = 0
    for x in nums:
        pref += x
        ans += cnt[pref - k]
        cnt[pref] += 1
    return ans
