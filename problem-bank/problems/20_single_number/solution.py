def single_number(nums: list[int]) -> int:
    x = 0
    for n in nums:
        x ^= n
    return x
