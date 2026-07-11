# Problem Bank

Local executable practice for Phase A DSA. Stdlib only — no pytest required.

## Layout

```
problem-bank/
  harness.py          # loader + equality helpers
  run_all.py          # discover + run everything
  problems/
    <id>_<slug>/
      prompt.md       # problem statement + API
      solution.py     # reference solution
      test_cases.py   # CASES and/or TESTS
```

## Run all tests

From the `problem-bank/` directory:

```bash
python run_all.py
```

Filter by name substring:

```bash
python run_all.py two_sum
python run_all.py 07
```

Quiet mode (failures + summary only):

```bash
python run_all.py -q
```

## Run one problem (optional pytest)

If you have pytest installed:

```bash
# from problem-bank/
python -c "from harness import run_problem; from pathlib import Path; print(run_problem(Path('problems/01_two_sum')))"
```

Or write a thin pytest wrapper that imports `harness.run_problem`.

## Student workflow

1. Read `prompt.md`.
2. Copy `solution.py` to a scratch file (or edit in place — git can restore).
3. Implement your version with the same function/class names.
4. Run `python run_all.py <slug>` until green.
5. Compare against the reference only after a real attempt.

## Adding a problem

1. Create `problems/<nn>_<slug>/` with `prompt.md`, `solution.py`, `test_cases.py`.
2. In `test_cases.py` set either:
   - `PRIMARY = "fn_name"` and `CASES = [((arg1, arg2), expected), ...]`
   - and/or `TESTS = [callable(sol_module), ...]` that assert
3. Run `python run_all.py <slug>`.

## Coverage map (26 problems)

| ID | Slug | Pattern |
|---|---|---|
| 01 | two_sum | Hash map |
| 02 | contains_duplicate | Hash set |
| 03 | longest_substr_no_repeat | Sliding window |
| 04 | max_sum_subarray_k | Fixed window |
| 05 | binary_search | Binary search |
| 06 | search_insert | Lower bound |
| 07 | merge_intervals | Intervals |
| 08 | reverse_linked_list | Linked list |
| 09 | next_greater_element | Monotonic stack |
| 10 | max_depth_tree | Tree DFS |
| 11 | lca_bst | BST LCA |
| 12 | top_k_frequent | Heap |
| 13 | course_schedule | Graph / topo |
| 14 | word_ladder | BFS |
| 15 | network_delay | Dijkstra |
| 16 | climb_stairs | DP |
| 17 | coin_change | DP unbounded |
| 18 | subsets | Backtracking |
| 19 | implement_trie | Trie |
| 20 | single_number | Bits / XOR |
| 21 | num_islands | Matrix DFS |
| 22 | randomized_set | Design O(1) |
| 23 | valid_anagram | Hashing |
| 24 | product_except_self | Prefix products |
| 25 | zero_one_bfs | 0-1 BFS |
| 26 | lru_cache | Design LRU |

