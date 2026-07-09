PRIMARY = "length_of_longest_substring"
CASES = [
    (("abcabcbb",), 3),
    (("bbbbb",), 1),
    (("pwwkew",), 3),
    (("",), 0),
    ((" ",), 1),
    (("au",), 2),
    (("dvdf",), 3),  # classic off-by-one / stale left bug
    (("abba",), 2),  # stale index trap
]
