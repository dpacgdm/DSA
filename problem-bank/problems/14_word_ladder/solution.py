from collections import defaultdict, deque


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    patterns: dict[str, list[str]] = defaultdict(list)
    for w in words:
        for i in range(len(w)):
            patterns[w[:i] + "*" + w[i + 1 :]].append(w)

    q = deque([(begin_word, 1)])
    seen = {begin_word}
    while q:
        word, dist = q.popleft()
        if word == end_word:
            return dist
        for i in range(len(word)):
            pat = word[:i] + "*" + word[i + 1 :]
            for nei in patterns.get(pat, []):
                if nei not in seen:
                    seen.add(nei)
                    q.append((nei, dist + 1))
    return 0
