from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    g = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        g[key].append(s)
    return list(g.values())
