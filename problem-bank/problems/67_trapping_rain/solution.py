def trap(height: list[int]) -> int:
    lo, hi = 0, len(height)-1
    left_max = right_max = 0
    ans = 0
    while lo <= hi:
        if height[lo] <= height[hi]:
            left_max = max(left_max, height[lo])
            ans += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            ans += right_max - height[hi]
            hi -= 1
    return ans
