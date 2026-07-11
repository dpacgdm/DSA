def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    out = []
    for i in range(n):
        if i and nums[i] == nums[i-1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo-1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi+1]:
                    hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return out
