# python-playground

Drills for Python mechanics and algorithm patterns. Each routine is one file: REPL sessions where you predict the output, then small functions to implement against tests. Reference solutions live separately so you can compare after trying.

Requires Python 3.10+ (outputs were checked on 3.12). No dependencies.

## Using it

```bash
git clone https://github.com/ksd3/python-playground.git
cd python-playground
python new.py            # list the routines
python new.py 1          # fresh copy of routine 1 -> work/r01_objects.py
# edit work/r01_objects.py: replace every ??? with your prediction, implement the functions
python check.py 1        # see what's right
python check.py all      # progress across everything you've started
git pull                 # get updates
```

- Everything you type lives in `work/`, which git ignores, so `git pull` never conflicts with your attempts.
- Running `python new.py N` again archives the old attempt to `work/archive/` and gives you a blank copy. That's the point: templates get rewritten from scratch on a schedule.
- `python check.py N -s` runs the reference solution; `solutions/` is for comparing after you've tried.
- `new.py` also creates `work/gotchas.md` and `work/triggers.md`, the two logs described below.

### Predictions

Each `PREDICT` block is a REPL session. Replace every `???` with exactly what Python would print:

```
>>> t = ([1],)
>>> t[0] += [2]
TypeError
>>> t
([1, 2],)
```

Expression values are echoed the way the REPL echoes them. A line that raises shows just the exception name, and the session continues. Common modules (`math`, `collections`, `heapq`, `bisect`, `itertools`, `functools`, `copy`, ...) are already imported.

## How to practice

1. **Predict, then run.** Every wrong prediction goes into `gotchas.md` with a one-line reason.
2. **Write from a blank file.** A template counts as known when you can write it with no references and it passes the tests on the first run.
3. **Spaced rewrites.** Redo each routine on day 1, 3, 7, 14 and 30 (`python new.py N` gives a fresh copy).
4. **Two logs.** `gotchas.md` holds language traps. `triggers.md` maps "what the problem says" to "which pattern fits". The second one is the real output of all this.

**Daily session, about 90 minutes:**

| Minutes | What |
|---|---|
| 10 | Rewrite two earlier templates from a blank file |
| 10 | Re-predict 5 entries from `gotchas.md` |
| 55 | Today's routine |
| 10 | One timing experiment or stress test |
| 5 | Update both logs |

## Routines

| # | Routine | Unlocks |
|---|---|---|
| **Phase 0: lab** | | |
| 00 | Your own test harness | stress testing, list/tree builders, call-sequence replay |
| **Phase 1: how Python runs** | | |
| 01 | Names, objects, mutability, identity | collecting results safely, in-place edits, grid setup |
| 02 | Functions, scope, closures, recursion | nested helpers, `nonlocal`, memoization, iterative rewrites |
| **Phase 2: built-in types** | | |
| 03 | Integers, floats, math | modular arithmetic, combinatorics, exact geometry, digits |
| 04 | Bit manipulation | XOR tricks, subset enumeration, bitmask states |
| 05 | Strings | parsing, anagram/palindrome checks, string building |
| 06 | Lists, tuples, 2D grids | matrix walks and rotations, in-place array work |
| 07 | dict, set, Counter, defaultdict, OrderedDict | the whole hashing family, frequency windows, caches |
| 08 | deque, heapq, bisect | BFS, top-k, scheduling, sorted lookups |
| **Phase 3: iteration and idioms** | | |
| 09 | Iterators and generators | lazy streams, custom iterators, tree walkers |
| 10 | itertools, functools, operator | brute-force generators, prefix sums, comparators |
| 11 | Pythonic idioms and assignment order | fewer index bugs, safe swaps, pointer rewiring |
| 12 | Sorting | sort-first greedy, custom orders, inversions, quickselect |
| **Phase 4: classes** | | |
| 13 | Class mechanics | clean classes, alternative constructors, reusable graph code |
| 14 | Special methods and protocols | custom heap order, hashable states, matrix power |
| 15 | dataclasses, namedtuples, slots, inheritance | compact state objects, memory-light nodes |
| 16 | Design builds | min-stack, LRU cache, O(1) random set, versioned store, running median |
| **Phase 5: data structures by hand** | | |
| 17 | Linked lists | dummy heads, reversal, fast/slow pointers, merge-k |
| 18 | Stacks, queues, monotonic structures | brackets, expression evaluation, next-greater, window max |
| 19 | Internals: hash map, heap, dynamic array | trustworthy complexity reasoning |
| 20 | Trees | traversals, passing info up/down, BST operations, construction |
| 21 | Graphs | BFS/DFS, topological sort, Dijkstra, 0-1 BFS, MST, bipartite |
| 22 | Union-Find, Trie, Fenwick tree | connectivity, prefix lookups, range queries |
| **Phase 6: algorithm templates** | | |
| 23 | Two pointers | sorted pairs, in-place compaction, partitioning |
| 24 | Sliding window | longest/shortest windows, "at most k", counts |
| 25 | Prefix sums and difference arrays | subarray sums with negatives, range updates |
| 26 | Binary search | boundaries, rotated arrays, search on the answer |
| 27 | Recursion and backtracking | subsets, permutations, combinations, pruning |
| 28 | Dynamic programming | knapsack, LIS, LCS/edit distance, interval and bitmask DP |
| 29 | Greedy, intervals, sweep line | merging, rooms, scheduling, exchange arguments |
| **Phase 7: performance and contest mechanics** | | |
| 30 | Complexity lab | knowing what each operation costs |
| 31 | Contest I/O, deep recursion, stress testing | fast input, iterative DFS, finding counterexamples |
| **Phase 8: recognition** | | |
| 32 | Pattern recognition | constraints to complexity, signals to patterns, mixed review |

## Schedule

About 1.5 to 2 hours a day. The exam below decides when you're done, not the calendar.

| Week | Routines |
|---|---|
| 1 | 00-02 |
| 2 | 03-05 |
| 3 | 06-08 |
| 4 | 09-12 |
| 5 | 13-16 |
| 6 | 17-20 |
| 7 | 21-22 |
| 8 | 23-26 |
| 9 | 27-28 |
| 10 | 29-32, then the exam |

## Final exam

From a blank file, no references, each one in 10 minutes or less and passing its tests on the first run:

- grid BFS, Dijkstra, Union-Find, topological sort with cycle detection
- a boundary binary search, plus one search-on-the-answer problem
- a variable-size sliding window, a monotonic stack, a monotonic deque
- subsets, permutations and combinations with duplicates
- a trie, an LRU cache (both versions), a Fenwick tree
- building and serializing a binary tree
- linked-list reversal (iterative and recursive) and merge-k
- 0/1 knapsack in 1D, LIS in O(n log n), edit distance
- interval merge and minimum meeting rooms

Also: 95% or better on 40 random entries from `gotchas.md`, the complexity table below from memory, and for any set of constraints, the target complexity plus two candidate patterns in under 10 seconds.

Once you move on to full problems, log each one: did you name the pattern within 5 minutes, was it right, how long did it take, and was the bug a Python mechanic or the idea itself? That log shows whether the patterns paid off, and which routine to revisit when one doesn't.

## Reference tables

### What operations cost

| Operation | Cost |
|---|---|
| list `a[i]`, `append`, `pop()`, `len` | O(1) (append amortized) |
| list `pop(0)`, `insert(0, x)`, `x in a`, `index`, `remove`, `del a[i]` | O(n) |
| slice `a[i:j]`, `a[:]`, `list(x)`, `a == b` | O(k) / O(n), easy to miss inside loops |
| `sort` / `sorted` | O(n log n) |
| dict/set get, set, `in`, delete | O(1) average |
| deque at either end | O(1); `dq[i]` is O(n) |
| `heappush` / `heappop` | O(log n); `heapify` O(n); `h[0]` O(1) |
| bisect search | O(log n); `insort` O(n) |
| `s + t` on strings | O(len(s) + len(t)), so build strings with `''.join` |

Passing `nums[1:]` into every recursive call costs O(n²) in total. Pass indices instead.

### Constraints to target complexity

| n | Target | Usually means |
|---|---|---|
| ≤ 10 | O(n!) | permutations |
| ≤ 20 | O(2ⁿ·n) | subsets, bitmask DP |
| ≤ 40 | O(2^(n/2)) | meet in the middle |
| ≤ 500 | O(n³) | interval DP, Floyd-Warshall |
| ≤ 5·10³ | O(n²) | 2D DP, all pairs |
| ≤ 10⁶ | O(n log n) / O(n) | sorting, heap, binary search, two pointers, hashing |
| ≥ 10⁹ | O(√n) / O(log n) / O(1) | math, binary search on the answer, matrix power |

These limits assume a fast compiled language. Plain Python loops run tens of times slower, so near the upper edge you need tight code, built-ins, or PyPy.

### Signal to pattern

| Signal | Reach for |
|---|---|
| sorted input; pair/triple with a target; in-place | two pointers |
| contiguous subarray/substring; longest/shortest/at most k | sliding window |
| subarray sum = k with negatives; many range-sum queries | prefix sums + hashmap |
| many range updates, then reads | difference array |
| "minimum X such that…", "maximize the minimum" | binary search on the answer |
| O(log n) required; sorted or rotated array | binary search |
| next greater/smaller, spans, histogram | monotonic stack |
| window max/min | monotonic deque |
| top k, k-th largest, k closest, merge k sorted | heap |
| running median | two heaps |
| nesting, matching, undo | stack |
| fewest steps, unweighted | BFS |
| weighted, non-negative | Dijkstra |
| weights are 0 or 1 | 0-1 BFS |
| islands, regions, flood fill | grid DFS/BFS |
| connections arriving over time, equivalences | Union-Find |
| prerequisites, ordering, cycles in a directed graph | topological sort |
| "all combinations/permutations/ways to build" | backtracking |
| count ways / min cost / max value with overlapping choices | DP |
| two strings being aligned or compared | 2D DP (LCS, edit distance) |
| prefixes, a dictionary of words | trie |
| overlapping intervals, meeting rooms | sort + sweep, or heap |
| cycle, middle, or k-th from end in a linked list | fast/slow pointers |
| tree height/path/balance | postorder returning values |
| tree levels | BFS by level |
| BST | inorder = sorted; pass bounds down |
| numbers in 1..n, find the missing/duplicate | cyclic sort / XOR / marking indices |
| every number appears twice except one | XOR |
| range queries with point updates | Fenwick / segment tree |
| group equivalent items | canonical key → dict of lists |
| answer mod 10⁹+7 | DP or combinatorics with modular arithmetic |

For every template, also know its false trigger: a sliding window with negative numbers, Dijkstra with negative edges, BFS on a weighted graph, binary search on a condition that isn't monotone, a greedy with no exchange argument.
