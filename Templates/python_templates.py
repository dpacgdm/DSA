"""
Interview-ready Python templates — copy into a scratch file and fill the TODOs.
Conventions: clear names, early returns, one-line invariant comments.
"""

from __future__ import annotations

import heapq
from collections import Counter, defaultdict, deque
from typing import Callable, Hashable, Optional


# =============================================================================
# Clean coding conventions (mini)
# =============================================================================
# - Name by role: lo/hi, left/right, indeg, dist, path, best
# - Early-return empties / impossibles
# - One invariant comment above the hot loop
# - Prefer not mutating caller inputs unless allowed
# - Say time/space before coding


# =============================================================================
# Binary search — exact find (closed interval)
# =============================================================================
def binary_search_exact(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    # invariant: target in nums[lo..hi] if present
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# =============================================================================
# Binary search — lower / upper bound (half-open [lo, hi))
# =============================================================================
def lower_bound(nums: list[int], target: int) -> int:
    """First index i with nums[i] >= target (or len(nums))."""
    lo, hi = 0, len(nums)
    # invariant: answer in [lo, hi]
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums: list[int], target: int) -> int:
    """First index i with nums[i] > target (or len(nums))."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search_answer(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with ok(x) True. Assumes ok monotonic False→True.
    hi should be an inclusive upper candidate that is feasible, or adjust.
    """
    # search in half-open [lo, hi+1) style: pass hi_exclusive = hi + 1
    left, right = lo, hi + 1
    while left < right:
        mid = (left + right) // 2
        if ok(mid):
            right = mid
        else:
            left = mid + 1
    return left


# =============================================================================
# Sliding window skeleton
# =============================================================================
def sliding_window_template(s: str) -> int:
    """Longest / best window under a constraint — fill `invalid` / `add` / `remove`."""
    left = 0
    best = 0
    # state = ...
    for right, _ch in enumerate(s):
        # add s[right] into state
        while False:  # while window invalid:
            # remove s[left] from state
            left += 1
        # invariant: [left, right] is valid
        best = max(best, right - left + 1)
    return best


def fixed_window_sum(nums: list[int], k: int) -> int:
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


# =============================================================================
# BFS / DFS graph
# =============================================================================
def bfs_shortest(graph: dict[int, list[int]], start: int) -> dict[int, int]:
    """Unit-weight shortest distances from start."""
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def dfs_recursive(graph: dict[int, list[int]], start: int) -> set[int]:
    seen: set[int] = set()

    def dfs(u: int) -> None:
        seen.add(u)
        for v in graph[u]:
            if v not in seen:
                dfs(v)

    dfs(start)
    return seen


def dfs_iterative(graph: dict[int, list[int]], start: int) -> set[int]:
    seen: set[int] = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(graph[u])
    return seen


# =============================================================================
# Union-Find
# =============================================================================
class UnionFind:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        self.components -= 1
        return True


# =============================================================================
# Dijkstra (non-negative weights)
# =============================================================================
def dijkstra(graph: dict[int, list[tuple[int, int]]], src: int) -> dict[int, int]:
    """graph[u] = [(v, weight), ...]. Returns dist map for reachable nodes."""
    dist = {src: 0}
    pq = [(0, src)]  # (dist, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        # invariant: d is final for u when first popped (non-neg weights)
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


# =============================================================================
# DP — memo (top-down) and tab (bottom-up)
# =============================================================================
def dp_memo_template(n: int) -> int:
    memo: dict[int, int] = {}

    def dp(i: int) -> int:
        if i in memo:
            return memo[i]
        if i <= 1:
            return i
        # dp[i] meaning: ___
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    return dp(n)


def dp_tab_template(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    # dp[i] = ways / best to reach i
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def coin_change_tab(coins: list[int], amount: int) -> int:
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < INF else -1


# =============================================================================
# Backtracking skeleton
# =============================================================================
def subsets_template(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        out.append(path.copy())
        for i in range(start, len(nums)):
            path.append(nums[i])      # choose
            dfs(i + 1)                # explore
            path.pop()                # unchoose

    dfs(0)
    return out


def permutations_template(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def dfs() -> None:
        if len(path) == len(nums):
            out.append(path.copy())
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return out


# =============================================================================
# Trie
# =============================================================================
class TrieNode:
    __slots__ = ("children", "end")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.end = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return bool(node and node.end)

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


# =============================================================================
# Linked list helpers
# =============================================================================
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    cur = head
    # invariant: prev = reversed prefix head; cur = remaining head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def merge_two_sorted(
    a: Optional[ListNode], b: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next
    return slow


# =============================================================================
# Heap patterns
# =============================================================================
def top_k_largest(nums: list[int], k: int) -> list[int]:
    """Min-heap of size k → k largest (unordered)."""
    if k <= 0:
        return []
    heap = nums[:k]
    heapq.heapify(heap)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])]


def merge_k_sorted_lists(lists: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []  # (val, list_id, idx)
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    out: list[int] = []
    while heap:
        val, i, idx = heapq.heappop(heap)
        out.append(val)
        if idx + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][idx + 1], i, idx + 1))
    return out


# =============================================================================
# Monotonic stack — next greater element
# =============================================================================
def next_greater(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [-1] * n
    stack: list[int] = []  # indices; values decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        stack.append(i)
    return ans


def daily_temperatures(temps: list[int]) -> list[int]:
    """Days until a warmer temperature (monotonic stack of indices)."""
    n = len(temps)
    ans = [0] * n
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


# =============================================================================
# Misc helpers often needed in interviews
# =============================================================================
def build_adj_undirected(n: int, edges: list[list[int]]) -> dict[int, list[int]]:
    g: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g


def build_adj_weighted(
    edges: list[tuple[Hashable, Hashable, int]]
) -> dict[Hashable, list[tuple[Hashable, int]]]:
    g: dict[Hashable, list[tuple[Hashable, int]]] = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    return g



# =============================================================================
# 0-1 BFS (weights in {0, 1}) — Graphs II
# =============================================================================
def zero_one_bfs(
    n: int, graph: dict[int, list[tuple[int, int]]], src: int
) -> list[int]:
    """graph[u] = [(v, w), ...] with w in {0, 1}. Returns dist from src."""
    INF = 10**18
    dist = [INF] * n
    dist[src] = 0
    dq: deque[int] = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist


# =============================================================================
# LRU Cache — hash map + doubly linked list
# =============================================================================
class _LRUNode:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _LRUNode] = {}
        self.head, self.tail = _LRUNode(), _LRUNode()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: _LRUNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_mru(self, node: _LRUNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if not node:
            return -1
        self._remove(node)
        self._add_mru(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_mru(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = _LRUNode(key, value)
        self.map[key] = node
        self._add_mru(node)


# =============================================================================
# Serialize / deserialize binary tree — preorder with '#' nulls
# =============================================================================
class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        vals: list[str] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                vals.append("#")
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = iter(data.split(","))

        def dfs() -> Optional[TreeNode]:
            val = next(tokens)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


# =============================================================================
# KMP — prefix function (LPS) + search
# =============================================================================
def prefix_function(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> list[int]:
    """Return start indices of pattern in text."""
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    out: list[int] = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            out.append(i - j + 1)
            j = pi[j - 1]
    return out


# =============================================================================
# Tree DP — House Robber III style (rob, skip)
# =============================================================================
def tree_rob(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
        if not node:
            return 0, 0
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob = node.val + ls + rs
        skip = max(lr, ls) + max(rr, rs)
        return rob, skip

    return max(dfs(root))



# =============================================================================
# Simplify Path (LC 71)
# =============================================================================
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for tok in path.split("/"):
        if tok == "" or tok == ".":
            continue
        if tok == "..":
            if stack:
                stack.pop()
        else:
            stack.append(tok)
    return "/" + "/".join(stack)


# =============================================================================
# Interval intersection (LC 986)
# =============================================================================
def interval_intersection(
    first: list[list[int]], second: list[list[int]]
) -> list[list[int]]:
    i = j = 0
    out: list[list[int]] = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return out


# =============================================================================
# Longest Increasing Path in matrix (LC 329)
# =============================================================================
def longest_increasing_path(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    R, C = len(matrix), len(matrix[0])
    memo: dict[tuple[int, int], int] = {}

    def dfs(r: int, c: int) -> int:
        if (r, c) in memo:
            return memo[(r, c)]
        best = 1
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[(r, c)] = best
        return best

    return max(dfs(r, c) for r in range(R) for c in range(C))
