PRIMARY = "is_anagram"
CASES = [
    (("anagram", "nagaram"), True),
    (("rat", "car"), False),
    (("", ""), True),
    (("a", "ab"), False),
    (("ab", "ba"), True),
]
