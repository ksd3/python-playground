"""R20 - Trees

Trees usually arrive in level order with None for a missing child: [1, None, 2, 3]
is 1 with right child 2, whose left child is 3. Nearly every tree problem is one
of five shapes: a traversal variant; information passed up (return what the
parent needs and record the overall answer at each node); information passed
down (running sums, (lo, hi) bounds, the current path); a BST property (inorder
visits values in sorted order); or building a tree. Recursion depth equals the
tree's height, so a 3000-node chain needs the iterative versions. A node can
hold 0, so test `is None`, never truthiness.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).
The snippets write a tree as nested tuples (value, left, right).

Part 2 - Drills. Implement every function until `python check.py 20` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: the tree family: traversals, heights and paths, balance checks, BST
validation and edits, lowest common ancestors, and rebuilding trees.
"""

PREDICT = r"""
>>> t = (1, (2, (4, None, None), None), (3, None, (5, None, None)))
>>> def pre(n):
...     return [] if n is None else [n[0]] + pre(n[1]) + pre(n[2])
>>> def ino(n):
...     return [] if n is None else ino(n[1]) + [n[0]] + ino(n[2])
>>> def post(n):
...     return [] if n is None else post(n[1]) + post(n[2]) + [n[0]]
>>> pre(t), ino(t), post(t)
???

>>> t = (1, (2, (4, None, None), None), (3, None, None))
>>> def height(n):
...     return 0 if n is None else 1 + max(height(n[1]), height(n[2]))
>>> height(t), height(None)
???

>>> t = (1, (2, (4, None, None), (5, None, None)), (3, None, None))
>>> best = 0
>>> def h(n):
...     global best
...     if n is None:
...         return 0
...     l, r = h(n[1]), h(n[2])
...     best = max(best, l + r)
...     return 1 + max(l, r)
>>> h(t), best
???

>>> t = (1, (2, (4, None, None), None), (3, None, (5, None, None)))
>>> q, levels = deque([t]), []
>>> while q:
...     level = []
...     for _ in range(len(q)):
...         n = q.popleft()
...         level.append(n[0])
...         q.extend(c for c in (n[1], n[2]) if c)
...     levels.append(level)
>>> levels
???

>>> q, order = deque([1]), []
>>> while q:
...     x = q.popleft()
...     order.append(x)
...     if x < 4:
...         q.extend([2 * x, 2 * x + 1])
>>> order
???

>>> level = [1, 0, None, 2]
>>> [v for v in level if v], [v for v in level if v is not None]
???

>>> vals = [1, None, 2, 3]
>>> i = vals.index(2)
>>> vals[2 * i + 1] if 2 * i + 1 < len(vals) else 'out of range'
???

>>> t = (1, (2, None, None), (3, None, None))
>>> st, out = [t], []
>>> while st:
...     n = st.pop()
...     out.append(n[0])
...     st.extend(c for c in (n[1], n[2]) if c)
>>> out
???

>>> def ino(n):
...     if n:
...         yield from ino(n[1])
...         yield n[0]
...         yield from ino(n[2])
>>> g = ino((4, (2, (1, None, None), (3, None, None)), (6, None, None)))
>>> next(g), next(g), list(g)
???

>>> def insert(n, v):
...     if n is None:
...         return (v, None, None)
...     if v < n[0]:
...         return (n[0], insert(n[1], v), n[2])
...     return (n[0], n[1], insert(n[2], v))
>>> def ino(n):
...     return [] if n is None else ino(n[1]) + [n[0]] + ino(n[2])
>>> root = None
>>> for v in [5, 2, 8, 1, 9, 3]:
...     root = insert(root, v)
>>> ino(root), root[0], root[1][0]
???

>>> t = (5, (1, None, None), (6, (3, None, None), None))
>>> def local_ok(n):
...     if n is None:
...         return True
...     if n[1] and n[1][0] >= n[0]:
...         return False
...     if n[2] and n[2][0] <= n[0]:
...         return False
...     return local_ok(n[1]) and local_ok(n[2])
>>> def bounded_ok(n, lo=-math.inf, hi=math.inf):
...     return n is None or (lo < n[0] < hi and bounded_ok(n[1], lo, n[0]) and bounded_ok(n[2], n[0], hi))
>>> local_ok(t), bounded_ok(t)
???

>>> t = (1, (2, None, None), (3, None, None))
>>> paths, path = [], []
>>> def dfs(n):
...     if n is None:
...         return
...     path.append(n[0])
...     if not n[1] and not n[2]:
...         paths.append(path)
...     dfs(n[1]); dfs(n[2])
...     path.pop()
>>> dfs(t)
>>> paths
???

>>> def best_down(n):
...     if n is None:
...         return 0
...     return n[0] + max(0, best_down(n[1]), best_down(n[2]))
>>> best_down((-3, (5, None, None), (-1, None, None)))
???

>>> def take_or_skip(n):
...     if n is None:
...         return (0, 0)
...     l, r = take_or_skip(n[1]), take_or_skip(n[2])
...     return (n[0] + l[1] + r[1], max(l) + max(r))
>>> take_or_skip((3, (2, None, (3, None, None)), (3, None, (1, None, None))))
???

>>> def lca(n, a, b):
...     if n is None or n[0] in (a, b):
...         return n
...     l, r = lca(n[1], a, b), lca(n[2], a, b)
...     return n if l and r else l or r
>>> t = (3, (5, (6, None, None), (2, None, None)), (1, None, None))
>>> lca(t, 6, 2)[0], lca(t, 6, 1)[0], lca(t, 5, 6)[0]
???
"""


# ---------------------------------------------------------------- given

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


# ---------------------------------------------------------------- drills

def build_tree(vals):
    """Build a tree from level-order values with None for missing children and
    return the root (None for [] or [None]). Only real nodes get children in the
    list. build_tree([1, None, 2, 3]): 1's right child is 2, and 2's left is 3."""
    raise NotImplementedError


def tree_vals(root):
    """The inverse of build_tree: level-order values with None for missing
    children, trailing Nones removed. tree_vals(build_tree([1, None, 2, 3])) ==
    [1, None, 2, 3]; tree_vals(None) == []."""
    raise NotImplementedError


def preorder_iter(root):
    """Values in preorder (node, left, right) using an explicit stack."""
    raise NotImplementedError


def inorder_iter(root):
    """Values in inorder (left, node, right) using an explicit stack: push the
    whole left spine, pop a node, then move to its right child."""
    raise NotImplementedError


def postorder_iter(root):
    """Values in postorder (left, right, node) using an explicit stack."""
    raise NotImplementedError


def level_order(root):
    """Values level by level: [[3], [9, 20], [15, 7]]. [] for an empty tree."""
    raise NotImplementedError


def subtree_sizes(parents):
    """A tree on nodes 0..n-1 given as a parent array (parents[root] == -1; the
    root needn't be node 0). Return size[v] = the number of nodes in v's subtree,
    v included. subtree_sizes([-1, 0, 0, 1]) == [4, 2, 1, 1]. Iterative, because
    the tree can be a 5000-node path."""
    raise NotImplementedError


def is_balanced(root):
    """True if at every node the heights of the two subtrees differ by at most 1.
    O(n): return heights upward and stop at the first imbalance."""
    raise NotImplementedError


def max_path_sum(root):
    """The largest sum of node values along any path (a chain of parent-child
    links, with at least one node, that needn't pass through the root) in a
    non-empty tree. max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42."""
    raise NotImplementedError


def root_to_leaf_paths(root, target):
    """Every root-to-leaf path whose values sum to target, as lists of values,
    ordered by leaf from left to right."""
    raise NotImplementedError


def is_bst(root):
    """True if the tree is a binary search tree with no duplicates: every value
    in a node's left subtree is smaller than it and every value in its right
    subtree is bigger. Pass (lo, hi) bounds down, not just parent checks."""
    raise NotImplementedError


def bst_delete(root, key):
    """Delete key from a BST (if present) and return the new root. A node with
    two children takes its inorder successor's value, then the successor is
    deleted from the right subtree."""
    raise NotImplementedError


def lowest_common_ancestor(root, a, b):
    """Return the deepest NODE that has both values a and b in its subtree (a node
    counts as its own ancestor). Values are unique and both are in the tree; the
    tree is a plain binary tree, not a BST."""
    raise NotImplementedError


def from_preorder_inorder(preorder, inorder):
    """Rebuild a tree with unique values from its preorder and inorder value
    lists and return the root. O(n): look up inorder positions in a dict instead
    of calling list.index or slicing."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import math
import random
from collections import deque


def _build(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q, i = deque([root]), 1
    while q and i < len(vals):
        node = q.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def _vals(root):
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def _random_tree(rng, n, values=None):
    """A random shape with n nodes; values default to random ints from -5 to 9."""
    if n == 0:
        return None
    nodes = [TreeNode(values[i] if values else rng.randint(-5, 9)) for i in range(n)]
    for i in range(1, n):
        while True:
            parent, side = nodes[rng.randrange(i)], rng.choice(('left', 'right'))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return nodes[0]


def _chain(n, side):
    root = node = TreeNode(0)
    for v in range(1, n):
        setattr(node, side, TreeNode(v))
        node = getattr(node, side)
    return root


def _pre(n):
    return [] if n is None else [n.val] + _pre(n.left) + _pre(n.right)


def _in(n):
    return [] if n is None else _in(n.left) + [n.val] + _in(n.right)


def _post(n):
    return [] if n is None else _post(n.left) + _post(n.right) + [n.val]


def _height(n):
    return 0 if n is None else 1 + max(_height(n.left), _height(n.right))


def _nodes(n):
    return [] if n is None else [n] + _nodes(n.left) + _nodes(n.right)


def _deep(fn, *args):
    try:
        return fn(*args)
    except RecursionError:
        raise AssertionError("a few thousand levels is too deep for recursion: use an explicit stack")


def _insert(root, v):
    node = TreeNode(v)
    if root is None:
        return node
    cur = root
    while True:
        side = 'left' if v < cur.val else 'right'
        if getattr(cur, side) is None:
            setattr(cur, side, node)
            return root
        cur = getattr(cur, side)


def _bst_from(values):
    root = None
    for v in values:
        root = _insert(root, v)
    return root


def _strictly_sorted(xs):
    return all(a < b for a, b in zip(xs, xs[1:]))


def test_build_tree():
    assert build_tree([]) is None and build_tree([None]) is None
    assert _vals(build_tree([1, None, 2, 3])) == [1, None, 2, 3], \
        "only real nodes get children, so 2i+1 indexing breaks once there's a gap"
    root = build_tree([1, None, 2, 3])
    assert root.val == 1 and root.left is None and root.right.left.val == 3 and root.right.right is None
    assert _vals(build_tree([0, 0, None, 0])) == [0, 0, None, 0], "0 is a value, not a gap: test `is None`"
    for vals in ([1], [1, 2, 3, 4, 5, None, 7], [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]):
        assert _vals(build_tree(vals)) == vals, vals
    rng = random.Random(20)
    for _ in range(200):
        vals = _vals(_random_tree(rng, rng.randint(0, 12)))
        assert _vals(build_tree(vals)) == vals, vals


def test_tree_vals():
    assert tree_vals(None) == [], "an empty tree is [] (drop trailing Nones)"
    assert tree_vals(_build([1, None, 2, 3])) == [1, None, 2, 3], "drop the trailing Nones"
    assert tree_vals(_build([0, None, 0])) == [0, None, 0]
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(0, 12))
        assert tree_vals(root) == _vals(root), _vals(root)


def test_preorder_iter():
    assert preorder_iter(None) == []
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(0, 12))
        assert preorder_iter(root) == _pre(root), _vals(root)
    assert _deep(preorder_iter, _chain(3000, 'left')) == list(range(3000))


def test_inorder_iter():
    assert inorder_iter(None) == []
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(0, 12))
        assert inorder_iter(root) == _in(root), _vals(root)
    assert _deep(inorder_iter, _chain(3000, 'left')) == list(range(2999, -1, -1))
    assert _deep(inorder_iter, _chain(3000, 'right')) == list(range(3000))


def test_postorder_iter():
    assert postorder_iter(None) == []
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(0, 12))
        assert postorder_iter(root) == _post(root), _vals(root)
    assert _deep(postorder_iter, _chain(3000, 'right')) == list(range(2999, -1, -1))


def test_level_order():
    assert level_order(None) == []
    assert level_order(_build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]], "one list per level"
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(1, 12))
        want, level = [], [root]
        while level:
            want.append([n.val for n in level])
            level = [c for n in level for c in (n.left, n.right) if c is not None]
        assert level_order(root) == want, _vals(root)


def test_subtree_sizes():
    assert subtree_sizes([-1]) == [1]
    assert subtree_sizes([-1, 0, 0, 1]) == [4, 2, 1, 1]
    assert subtree_sizes([2, 2, -1]) == [1, 1, 3], "the root isn't always node 0"
    rng = random.Random(20)
    for _ in range(200):
        n = rng.randint(1, 12)
        order = list(range(n))
        rng.shuffle(order)
        parents = [-1] * n
        for i in range(1, n):
            parents[order[i]] = order[rng.randrange(i)]
        want = [0] * n
        for u in range(n):
            v = u
            while v != -1:
                want[v] += 1
                v = parents[v]
        assert subtree_sizes(parents) == want, parents
    path = [-1] + list(range(4999))
    assert _deep(subtree_sizes, path) == list(range(5000, 0, -1))


def test_is_balanced():
    assert is_balanced(None) is True
    assert is_balanced(_build([3, 9, 20, None, None, 15, 7])) is True
    assert is_balanced(_build([1, 2, 2, 3, 3, None, None, 4, 4])) is False
    assert is_balanced(_build([1, 2, 2, 3, None, None, 3, 4, None, None, 4])) is False, \
        "equal heights at the root aren't enough: every node must be balanced"
    rng = random.Random(20)

    def balanced(n):
        return n is None or (abs(_height(n.left) - _height(n.right)) <= 1 and balanced(n.left) and balanced(n.right))

    for _ in range(300):
        root = _random_tree(rng, rng.randint(0, 10))
        assert is_balanced(root) == balanced(root), _vals(root)


def test_max_path_sum():
    assert max_path_sum(_build([1, 2, 3])) == 6
    assert max_path_sum(_build([-10, 9, 20, None, None, 15, 7])) == 42
    assert max_path_sum(_build([-3])) == -3, "a path has at least one node, even when every value is negative"
    assert max_path_sum(_build([-2, -1])) == -1
    assert max_path_sum(_build([2, -1])) == 2, "drop a branch whose best sum is negative"
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(1, 9))
        nodes = _nodes(root)
        adj = {id(n): [c for c in (n.left, n.right) if c is not None] for n in nodes}
        for n in nodes:
            for c in (n.left, n.right):
                if c is not None:
                    adj[id(c)].append(n)
        want = -math.inf
        for start in nodes:
            st = [(start, None, start.val)]
            while st:
                node, came_from, total = st.pop()
                want = max(want, total)
                st += [(nxt, node, total + nxt.val) for nxt in adj[id(node)] if nxt is not came_from]
        assert max_path_sum(root) == want, _vals(root)


def test_root_to_leaf_paths():
    root = _build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    assert root_to_leaf_paths(root, 22) == [[5, 4, 11, 2], [5, 8, 4, 5]], \
        "store a copy of the path (path[:]), not the list you keep changing"
    assert root_to_leaf_paths(None, 0) == []
    assert root_to_leaf_paths(_build([1, 2]), 1) == [], "a path must end at a leaf, and 1 has a child"
    rng = random.Random(20)
    for _ in range(200):
        root = _random_tree(rng, rng.randint(1, 10))
        target = rng.randint(-3, 12)
        want = []

        def walk(n, path):
            path = path + [n.val]
            if n.left is None and n.right is None:
                if sum(path) == target:
                    want.append(path)
            for c in (n.left, n.right):
                if c is not None:
                    walk(c, path)

        walk(root, [])
        assert root_to_leaf_paths(root, target) == want, (_vals(root), target)


def test_is_bst():
    assert is_bst(None) is True
    assert is_bst(_build([2, 1, 3])) is True
    assert is_bst(_build([0, -1])) is True
    assert is_bst(_build([5, 1, 4, None, None, 3, 6])) is False
    assert is_bst(_build([5, 1, 6, None, None, 3, 7])) is False, \
        "3 sits in 5's right subtree: check against bounds, not just the parent"
    assert is_bst(_build([2, 2])) is False and is_bst(_build([2, None, 2])) is False, "no duplicates"
    rng = random.Random(20)
    for _ in range(300):
        if rng.random() < 0.5:
            root = _bst_from(rng.sample(range(-20, 20), rng.randint(1, 12)))
            if rng.random() < 0.5:
                rng.choice(_nodes(root)).val = rng.randint(-20, 20)
        else:
            root = _random_tree(rng, rng.randint(1, 8))
        assert is_bst(root) == _strictly_sorted(_in(root)), _vals(root)


def test_bst_delete():
    root = bst_delete(_bst_from([5, 3, 6, 2, 4, 7]), 3)
    assert _in(root) == [2, 4, 5, 6, 7], "deleting a node with two children must keep both subtrees"
    assert bst_delete(_bst_from([1]), 1) is None
    assert _in(bst_delete(_bst_from([5, 3, 6]), 9)) == [3, 5, 6], "deleting a missing key changes nothing"
    root = bst_delete(_bst_from([5, 3, 8, 7, 9]), 5)
    assert _in(root) == [3, 7, 8, 9] and root.val == 7, "two children: the inorder successor takes the node's place"
    rng = random.Random(20)
    for _ in range(200):
        keys = rng.sample(range(30), rng.randint(1, 15))
        root, alive = _bst_from(keys), set(keys)
        for key in rng.sample(range(30), 8):
            root = bst_delete(root, key)
            alive.discard(key)
            assert _in(root) == sorted(alive), (keys, key)


def test_lowest_common_ancestor():
    root = _build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    assert lowest_common_ancestor(root, 5, 1).val == 3, "when a and b turn up on different sides, this node is the answer"
    assert lowest_common_ancestor(root, 5, 4).val == 5, "a node counts as its own ancestor"
    assert lowest_common_ancestor(root, 7, 8).val == 3
    assert lowest_common_ancestor(root, 0, 8).val == 1, "0 is a real value"
    rng = random.Random(20)
    for _ in range(200):
        n = rng.randint(1, 12)
        root = _random_tree(rng, n, values=rng.sample(range(n), n))
        a, b = rng.randrange(n), rng.randrange(n)
        paths = {}
        st = [(root, [root])]
        while st:
            node, path = st.pop()
            paths[node.val] = path
            st += [(c, path + [c]) for c in (node.left, node.right) if c is not None]
        want = None
        for x, y in zip(paths[a], paths[b]):
            if x is not y:
                break
            want = x
        assert lowest_common_ancestor(root, a, b) is want, (_vals(root), a, b)


def test_from_preorder_inorder():
    assert from_preorder_inorder([], []) is None
    root = from_preorder_inorder([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert _vals(root) == [3, 9, 20, None, None, 15, 7]
    rng = random.Random(20)
    for _ in range(200):
        n = rng.randint(1, 30)
        tree = _random_tree(rng, n, values=rng.sample(range(-50, 50), n))
        pre, ino = _pre(tree), _in(tree)
        assert _vals(from_preorder_inorder(pre[:], ino[:])) == _vals(tree), (pre, ino)
