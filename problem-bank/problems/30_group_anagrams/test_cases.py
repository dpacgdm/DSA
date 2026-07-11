PRIMARY = "group_anagrams"

def _norm(got, expected_groups):
    # compare as frozenset of frozensets
    g = frozenset(frozenset(x) for x in got)
    e = frozenset(frozenset(x) for x in expected_groups)
    return g == e

CASES = [
    ((["eat","tea","tan","ate","nat","bat"],), [["eat","tea","ate"],["tan","nat"],["bat"]]),
    (([""],), [[""]]),
    ((["a"],), [["a"]]),
]

# harness uses equality — override with TESTS
TESTS = [
    lambda sol: (_ for _ in ()).throw(AssertionError("use CASES via custom")) if False else None,
]
# Actually harness compares with == which fails on order. Use TESTS only.
TESTS = []
def t1(sol):
    got = sol.group_anagrams(["eat","tea","tan","ate","nat","bat"])
    assert frozenset(frozenset(g) for g in got) == frozenset([frozenset(["eat","tea","ate"]), frozenset(["tan","nat"]), frozenset(["bat"])])
def t2(sol):
    assert sol.group_anagrams([""]) == [[""]] or list(sol.group_anagrams([""])) == [[""]]
def t3(sol):
    assert frozenset(frozenset(g) for g in sol.group_anagrams(["a"])) == frozenset([frozenset(["a"])])
TESTS = [t1, t2, t3]
CASES = []
PRIMARY = "group_anagrams"
