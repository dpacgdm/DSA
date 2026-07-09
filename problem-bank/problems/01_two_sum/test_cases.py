PRIMARY = "two_sum"

CASES = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([3, 2, 4], 6), [1, 2]),
    (([3, 3], 6), [0, 1]),
    (([-1, -2, -3, -4, -5], -8), [2, 4]),
    (([0, 4, 3, 0], 0), [0, 3]),
]

def test_order_independent(sol):
    got = sorted(sol.two_sum([2, 7, 11, 15], 9))
    assert got == [0, 1]

def test_negative(sol):
    got = sol.two_sum([-3, 4, 3, 90], 0)
    assert sorted(got) == [0, 2]

def test_sum_property(sol):
    nums, target = [1, 5, 3, 7], 8
    i, j = sol.two_sum(nums, target)
    assert i != j and nums[i] + nums[j] == target

TESTS = [test_order_independent, test_negative, test_sum_property]
