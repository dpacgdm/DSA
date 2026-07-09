PRIMARY = "contains_duplicate"
CASES = [
    (([1, 2, 3, 1],), True),
    (([1, 2, 3, 4],), False),
    (([],), False),
    (([1],), False),
    (([1, 1],), True),
    (([0, 0, 0],), True),
]
