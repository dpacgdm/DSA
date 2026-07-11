# Phase A — MVP Problem Spines

Ruthless minimum viable sets for timed / blind practice. **Not** a completionist list.

**Legend**

| Column | Meaning |
|---|---|
| Diff | E / M / H (interview weight, not ego) |
| LC | LeetCode id when standard; `—` if classic variant / bank-only |
| Bank | `Y` = present under `problem-bank/problems/`; else study on LC / notebook |

**How to use:** For each module, clear the spine before declaring `timed-verified`. Prefer bank problems for local red/green loops; use LC for UI timing.

---

## Module 1 — Complexity + Arrays & Strings (18)

| Problem | Why it earns M1 | Diff | LC | Bank |
|---|---|---|---|---|
| Two Sum | Hash complement; O(n) vs nested | E | 1 | Y `01_two_sum` |
| Contains Duplicate | Set membership / complexity talk | E | 217 | Y `02_contains_duplicate` |
| Valid Anagram | Frequency maps | E | 242 | Y `23_valid_anagram` |
| Best Time to Buy/Sell Stock | One-pass running min | E | 121 | — |
| Maximum Subarray (Kadane) | Linear scan invariant | M | 53 | — |
| Move Zeroes | Two pointers in-place | E | 283 | — |
| Container With Most Water | Two pointers maximize | M | 11 | — |
| 3Sum | Sort + two pointers; dedupe | M | 15 | — |
| Longest Substring No Repeat | Variable sliding window | M | 3 | Y `03_longest_substr_no_repeat` |
| Max Sum Subarray Size K | Fixed window | E | — | Y `04_max_sum_subarray_k` |
| Minimum Size Subarray Sum | Window shrink for target | M | 209 | — |
| Product Except Self | Prefix/suffix products | M | 238 | Y `24_product_except_self` |
| Rotate Array | Index mapping / reverse trick | M | 189 | — |
| Longest Common Prefix | Vertical scan / edge empty | E | 14 | — |
| Valid Palindrome | Two pointers + filter | E | 125 | — |
| Merge Sorted Array | Two pointers from end | E | 88 | — |
| Majority Element | Boyer-Moore or hash | E | 169 | — |
| Big-O teach-back (custom) | Explain nested vs hash on Two Sum | E | — | — |

---

## Module 2 — Hashing + Recursion (16)

| Problem | Why it earns M2 | Diff | LC | Bank |
|---|---|---|---|---|
| Group Anagrams | Hash by signature | M | 49 | — |
| Two Sum (revisit timed) | Hash under time | E | 1 | Y |
| Longest Consecutive Sequence | Set jumps O(n) | M | 128 | — |
| Subarray Sum Equals K | Prefix + hash counts | M | 560 | — |
| 4Sum II | Meet-in-middle hash | M | 454 | — |
| Design HashMap (lite) | Collision mental model | E | 706 | — |
| Fibonacci (memo) | Recursion + memo | E | 509 | — |
| Climb Stairs | Recurrence → DP bridge | E | 70 | Y `16_climb_stairs` |
| Pow(x, n) | Divide & conquer recursion | M | 50 | — |
| Generate Parentheses | Recursion tree / constraints | M | 22 | — |
| Reverse String (recur) | Base + recurse | E | 344 | — |
| Merge Two Lists (recur) | Recursion on structure | E | 21 | — |
| Sort / permute warm-up | Recursion call tree | M | 46 | — |
| Letter Combinations Phone | Recursion branching | M | 17 | — |
| Valid Anagram (timed) | Hash speed | E | 242 | Y |
| Single Number | XOR / bit as hash cousin | E | 136 | Y `20_single_number` |

---

## Module 3 — Searching & Sorting (18)

| Problem | Why it earns M3 | Diff | LC | Bank |
|---|---|---|---|---|
| Binary Search | Closed-interval template | E | 704 | Y `05_binary_search` |
| Search Insert Position | Lower bound | E | 35 | Y `06_search_insert` |
| First Bad Version | Monotonic predicate | E | 278 | — |
| Find Peak Element | BS on answer slope | M | 162 | — |
| Search Rotated Sorted Array | BS + pivot logic | M | 33 | — |
| Find Min Rotated | BS variant | M | 153 | — |
| Time-Based Key-Value | BS on timestamps | M | 981 | — |
| Koko Eating Bananas | BS on capacity | M | 875 | — |
| Capacity To Ship Packages | BS on answer | M | 1011 | — |
| Merge Intervals | Sort + sweep | M | 56 | Y `07_merge_intervals` |
| Sort Colors | Dutch partition | M | 75 | — |
| Kth Largest (sort/heap) | Order stats | M | 215 | — |
| Merge Sorted Arrays | Merge step of mergesort | E | 88 | — |
| Sort List (merge sort) | Linked mergesort | M | 148 | — |
| Count of Range Sum | Merge-sort on prefixes — **optional / gauntlet only** | H | 327 | — |
| Meeting Rooms II | Sort + heap/sweep | M | 253 | — |
| Insertion / quick mental | Complexity + Master Theorem talk | — | — | — |
| Search 2D Matrix | BS on virtual index | M | 74 | — |

---

## Module 4 — Linked Lists + Stacks & Queues (18)

| Problem | Why it earns M4 | Diff | LC | Bank |
|---|---|---|---|---|
| Reverse Linked List | 3-pointer mastery | E | 206 | Y `08_reverse_linked_list` |
| Middle of Linked List | Slow/fast | E | 876 | — |
| Linked List Cycle | Floyd | E | 141 | — |
| Merge Two Sorted Lists | Dummy head | E | 21 | — |
| Remove Nth From End | Two pointers gap | M | 19 | — |
| Add Two Numbers | Digits + carry | M | 2 | — |
| Reorder List | Split + reverse + merge | M | 143 | — |
| LRU Cache | Hash + DLL design | M | 146 | — |
| Valid Parentheses | Stack matching | E | 20 | — |
| Min Stack | Aux stack invariant | M | 155 | — |
| Daily Temperatures | Monotonic stack | M | 739 | — |
| Next Greater Element | Mono stack | M | 496/503 | Y `09_next_greater_element` |
| Evaluate RPN | Stack eval | M | 150 | — |
| Implement Queue using Stacks | Amortized O(1) | E | 232 | — |
| Implement Stack using Queues | API discipline | E | 225 | — |
| Sliding Window Maximum | Deque mono | H | 239 | — |
| Decode String | Stack parse | M | 394 | — |
| Asteroid Collision | Stack simulation | M | 735 | — |

---

## Module 5 — Trees (20)

| Problem | Why it earns M5 | Diff | LC | Bank |
|---|---|---|---|---|
| Max Depth | Recurrence on tree | E | 104 | Y `10_max_depth_tree` |
| Invert Binary Tree | Swap recurse | E | 226 | — |
| Same Tree | Structural equality | E | 100 | — |
| Symmetric Tree | Mirror recurse/BFS | E | 101 | — |
| Diameter of Binary Tree | Postorder heights | M | 543 | — |
| Path Sum | DFS carry | E | 112 | — |
| Binary Tree Level Order | BFS queue | M | 102 | — |
| Validate BST | Bounds DFS | M | 98 | — |
| LCA of BST | Walk by value | M | 235 | Y `11_lca_bst` |
| LCA of Binary Tree | Postorder report | M | 236 | — |
| Kth Smallest BST | Inorder count | M | 230 | — |
| Construct from Pre+In | Divide indices | M | 105 | — |
| Serialize/Deserialize | BFS protocol | H | 297 | — |
| Balanced Binary Tree | Height + flag | E | 110 | — |
| Lowest Common Ancestor III* | Parent pointers (if seen) | M | 1650 | — |
| BST Iterator | Controlled inorder | M | 173 | — |
| Right Side View | BFS last / DFS depth | M | 199 | — |
| Flatten to Linked List | Morris/rethread | M | 114 | — |
| Binary Tree Max Path Sum | Tree DP bend | H | 124 | — |
| House Robber III | Tree DP rob/skip | M | 337 | — |

---

## Module 6 — Heaps + Advanced Array Patterns (16)

| Problem | Why it earns M6 | Diff | LC | Bank |
|---|---|---|---|---|
| Kth Largest in Stream | Size-k heap | E | 703 | — |
| Top K Frequent | Heap / bucket | M | 347 | Y `12_top_k_frequent` |
| Merge K Sorted Lists | Heap of heads | H | 23 | — |
| Find Median from Data Stream | Two heaps | H | 295 | — |
| Task Scheduler | Greedy + heap/count | M | 621 | — |
| K Closest Points | Heap / select | M | 973 | — |
| Last Stone Weight | Max-heap sim | E | 1046 | — |
| Meeting Rooms II | Min-heap ends | M | 253 | — |
| Product Except Self | Prefix pattern | M | 238 | Y |
| Merge Intervals (revisit) | Sort sweep under time | M | 56 | Y |
| Insert Interval | Edge merge cases | M | 57 | — |
| Non-overlapping Intervals | Greedy sort end | M | 435 | — |
| Jump Game | Greedy reach | M | 55 | — |
| Jump Game II | Greedy levels | M | 45 | — |
| Gas Station | Circular greedy | M | 134 | — |
| Randomized Set | O(1) design | M | 380 | Y `22_randomized_set` |

---

## Module 7 — Graphs I (17)

| Problem | Why it earns M7 | Diff | LC | Bank |
|---|---|---|---|---|
| Number of Islands | Grid DFS/BFS | M | 200 | Y `21_num_islands` |
| Clone Graph | BFS/DFS map | M | 133 | — |
| Course Schedule | Cycle / topo | M | 207 | Y `13_course_schedule` |
| Course Schedule II | Kahn order | M | 210 | — |
| Word Ladder | Implicit BFS | H | 127 | Y `14_word_ladder` |
| Alien Dictionary | Topo on chars | H | 269 | — |
| Pacific Atlantic Water Flow | Multi-source DFS | M | 417 | — |
| Graph Valid Tree | n-1 edges + connected | M | 261 | — |
| Number of Connected Components | UF or DFS | M | 323 | — |
| Redundant Connection | UF cycle | M | 684 | — |
| Rotting Oranges | Multi-source BFS | M | 994 | — |
| 01 Matrix | Multi-source BFS | M | 542 | — |
| Surrounded Regions | Border DFS | M | 130 | — |
| Keys and Rooms | Reachability | M | 841 | — |
| Shortest Path Binary Matrix | Grid BFS | M | 1091 | — |
| Accounts Merge | UF + strings | M | 721 | — |
| Is Graph Bipartite? | 2-color BFS/DFS | M | 785 | — |

---

## Module 8 — Graphs II + DP I (18)

| Problem | Why it earns M8 | Diff | LC | Bank |
|---|---|---|---|---|
| Network Delay Time | Dijkstra | M | 743 | Y `15_network_delay` |
| 0-1 BFS shortest path | Deque 0/1 weights | M | — | Y `25_zero_one_bfs` |
| Cheapest Flights K Stops | Bounded BF/DP (awareness) | M | 787 | — |
| Path With Minimum Effort | BS + BFS or Dijkstra | M | 1631 | — |
| Min Cost to Connect All Points | MST (Prim/Kruskal) | M | 1584 | — |
| Critical Connections | Tarjan bridges — **exposure only, not gate** | H | 1192 | — |
| Climbing Stairs | 1D DP base | E | 70 | Y |
| House Robber | Choose/skip DP | M | 198 | — |
| House Robber II | Circular casework | M | 213 | — |
| Coin Change | Unbounded knapsack | M | 322 | Y `17_coin_change` |
| Coin Change II | Combo count loops | M | 518 | — |
| Longest Increasing Subsequence | DP / patience | M | 300 | — |
| Word Break | Prefix DP | M | 139 | — |
| Unique Paths | Grid DP | M | 62 | — |
| Min Path Sum | Grid DP | M | 64 | — |
| Decode Ways | String DP | M | 91 | — |
| Partition Equal Subset Sum | 0/1 knapsack | M | 416 | — |
| Target Sum | +/- knapsack | M | 494 | — |
| Maximal Square | 2D DP | M | 221 | — |

---

## Module 9 — DP II + Backtracking + Greedy (18)

| Problem | Why it earns M9 | Diff | LC | Bank |
|---|---|---|---|---|
| Longest Common Subsequence | 2-string DP | M | 1143 | — |
| Edit Distance | Classic DP | M | 72 | — |
| Distinct Subsequences | Count DP | H | 115 | — |
| Burst Balloons | Interval DP (select) | H | 312 | — |
| Subsets | Backtrack power set | M | 78 | Y `18_subsets` |
| Subsets II | Dedupe backtrack | M | 90 | — |
| Combination Sum | Unlimited choose | M | 39 | — |
| Combination Sum II | Dedupe + limit | M | 40 | — |
| Permutations | Used[] backtrack | M | 46 | — |
| Palindrome Partitioning | DFS + check | M | 131 | — |
| Word Search | Board DFS backtrack | M | 79 | — |
| N-Queens | Constraint backtrack | H | 51 | — |
| Jump Game (greedy) | Reach invariant | M | 55 | — |
| Gas Station | Tank reset greedy | M | 134 | — |
| Partition Labels | Greedy last index | M | 763 | — |
| Non-overlapping Intervals | End-sort greedy | M | 435 | — |
| Remove Invalid Parentheses | BFS/backtrack hard | H | 301 | — |
| Regular Expression Matching | DP hard (optional) | H | 10 | — |

---

## Module 10 — Advanced Structures (15)

| Problem | Why it earns M10 | Diff | LC | Bank |
|---|---|---|---|---|
| Implement Trie | Prefix tree API | M | 208 | Y `19_implement_trie` |
| Design Add/Search Words | Trie + DFS `.` | M | 211 | — |
| Word Search II | Trie + board prune | H | 212 | — |
| Maximum XOR Two Numbers | Bit trie (select) | M | 421 | — |
| Next Greater Element | Mono stack revisit | M | 503 | Y |
| Largest Rectangle Histogram | Mono stack | H | 84 | — |
| Sliding Window Maximum | Mono deque | H | 239 | — |
| Sum of Subarray Minimums | Mono stack contrib | M | 907 | — |
| Range Sum Query Immutable | Prefix (seg preview) | E | 303 | — |
| Range Sum Query Mutable | Fenwick/Seg exposure | M | 307 | — |
| Count of Smaller After Self | Merge/BIT exposure | H | 315 | — |
| Online Majority / seg lite | Exposure only | H | — | — |
| Single Number | Bits | E | 136 | Y |
| Number of 1 Bits | Bit ops | E | 191 | — |
| Sum of Two Integers | Bit add (optional) | M | 371 | — |

---

## Module 11 — Gauntlet / Integration (15)

Mixed patterns; no new theory. Prefer timed blocks from `Gauntlet/Phase A Gauntlet.md`.

| Problem | Why it earns M11 | Diff | LC | Bank |
|---|---|---|---|---|
| LRU Cache | Design under pressure | M | 146 | — |
| Randomized Set | Design O(1) | M | 380 | Y |
| Word Ladder | Graph BFS transfer | H | 127 | Y |
| Coin Change | DP transfer | M | 322 | Y |
| Course Schedule | Topo transfer | M | 207 | Y |
| Merge Intervals | Sort sweep transfer | M | 56 | Y |
| LCA (BST or BT) | Tree transfer | M | 235/236 | Y / — |
| Top K Frequent | Heap transfer | M | 347 | Y |
| Number of Islands | Grid graph transfer | M | 200 | Y |
| Subsets + timed | Backtrack speed | M | 78 | Y |
| Network Delay | Dijkstra transfer | M | 743 | Y |
| Trapping Rain Water | Two ptr / stack | H | 42 | — |
| Serialize Tree | Protocol design | H | 297 | — |
| Find Median Stream | Two heaps | H | 295 | — |
| Mini-mock set (custom) | Rubric G5 | — | — | Gauntlet |

---

## Coverage modules MVP (24)

Full lessons live under `Intervals/`, `Bitwise/`, `Strings/`, `Math/`, `Matrix/`, `Design/`. Retention: `Retention Questions/Coverage Gaps Retention.md`.

### Intervals & Sweep (4)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Merge Intervals | Sort + sweep core | M | 56 | Y `07_merge_intervals` |
| Insert Interval | Edge splice | M | 57 | — |
| Meeting Rooms II | Sweep / heap | M | 253 | — |
| Non-overlapping Intervals | Greedy end-sort | M | 435 | — |

### Bit Manipulation (4)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Single Number | XOR identity | E | 136 | Y `20_single_number` |
| Number of 1 Bits | `n & (n-1)` | E | 191 | — |
| Counting Bits | DP on bits | E | 338 | — |
| Subsets (bit mask) | Mask enumeration | M | 78 | Y `18_subsets` |

### String Algorithms (5)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Implement strStr / needle | KMP or rolling hash | M | 28 | — |
| Repeated Substring Pattern | Prefix / KMP border | E | 459 | — |
| Longest Happy Prefix | Prefix function | H | 1392 | — |
| Find Duplicate Substring | Rolling hash / binary search | M | 1044 | — |
| Valid Anagram | Freq bridge | E | 242 | Y `23_valid_anagram` |

### Math for Interviews (5)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Pow(x, n) | Fast pow | M | 50 | — |
| Sqrt(x) | Integer root / BS | E | 69 | — |
| GCD / LCM pair ops | Euclidean + overflow care | E | — | — |
| Count Primes | Sieve mental model | M | 204 | — |
| Super Pow / mod exponent | Mod arithmetic | M | 372 | — |

### Matrix & Grid (6)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Number of Islands | Grid graph | M | 200 | Y `21_num_islands` |
| Spiral Matrix | Layer sim | M | 54 | — |
| Set Matrix Zeroes | In-place markers | M | 73 | — |
| Rotate Image | Transpose + reverse | M | 48 | — |
| Search a 2D Matrix II | Staircase search | M | 240 | — |
| Walls and Gates | Multi-source BFS | M | 286 | — |

### Design Data Structures (4)
| Problem | Why | Diff | LC | Bank |
|---|---|---|---|---|
| Insert Delete GetRandom O(1) | Hash + list | M | 380 | Y `22_randomized_set` |
| Min Stack | Aux stack | M | 155 | — |
| Time Based Key-Value | Hash + BS | M | 981 | — |
| LRU Cache | Design + DLL/hash (full in Design Part 15) | M | 146 | Y `26_lru_cache` |

---

## Counts

| Spine | Problems listed |
|---|---|
| M1 | 18 |
| M2 | 16 |
| M3 | 18 |
| M4 | 18 |
| M5 | 20 |
| M6 | 16 |
| M7 | 17 |
| M8 | 18 |
| M9 | 18 |
| M10 | 15 |
| M11 | 15 |
| Coverage modules | 27 |
| **Total spine rows** | **~217** |
| **In problem-bank** | **26 unique packages** (many spines point at the same bank ids) |

Bank ids: `01`–`26` under `problem-bank/problems/`. Run: `py -3 problem-bank/run_all.py`.
