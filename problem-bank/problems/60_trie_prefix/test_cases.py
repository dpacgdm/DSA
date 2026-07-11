PRIMARY = "exist"
CASES = [
    (([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"), True),
    (([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"), True),
    (([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"), False),
]
