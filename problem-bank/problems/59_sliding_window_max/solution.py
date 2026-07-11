from collections import deque
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()  # indices decreasing values
    out = []
    for i,x in enumerate(nums):
        while dq and dq[0] <= i-k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k-1:
            out.append(nums[dq[0]])
    return out
