PRIMARY = "ladder_length"
CASES = [
    (("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
    (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
    (("a", "c", ["a", "b", "c"]), 2),
    (("hot", "dog", ["hot", "dog"]), 0),  # no intermediate path of length>1? hot->dog needs 2 letter change unless mid
    (("hot", "dog", ["hot", "dot", "dog"]), 3),
]
