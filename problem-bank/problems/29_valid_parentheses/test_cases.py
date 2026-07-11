PRIMARY = "is_valid"
CASES = [
    (("()",), True),
    (("()[]{}",), True),
    (("(]",), False),
    (("([)]",), False),
    (("{[]}",), True),
    (("",), True),
]
