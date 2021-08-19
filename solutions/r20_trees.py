"""R20 - Trees (reference solutions)

Compare after you've made your own attempt. Run: python check.py 20 -s
"""
import math
from collections import deque

PREDICT = r"""
>>> t = (1, (2, (4, None, None), None), (3, None, (5, None, None)))
>>> def pre(n):
...     return [] if n is None else [n[0]] + pre(n[1]) + pre(n[2])
>>> def ino(n):
...     return [] if n is None else ino(n[1]) + [n[0]] + ino(n[2])
>>> def post(n):
...     return [] if n is None else post(n[1]) + post(n[2]) + [n[0]]
>>> pre(t), ino(t), post(t)
([1, 2, 4, 3, 5], [4, 2, 1, 3, 5], [4, 2, 5, 3, 1])

>>> t = (1, (2, (4, None, None), None), (3, None, None))
>>> def height(n):
...     return 0 if n is None else 1 + max(height(n[1]), height(n[2]))
>>> height(t), height(None)
(3, 0)

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
(3, 3)

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
[[1], [2, 3], [4, 5]]

>>> q, order = deque([1]), []
>>> while q:
...     x = q.popleft()
...     order.append(x)
...     if x < 4:
...         q.extend([2 * x, 2 * x + 1])
>>> order
[1, 2, 3, 4, 5, 6, 7]

>>> level = [1, 0, None, 2]
>>> [v for v in level if v], [v for v in level if v is not None]
([1, 2], [1, 0, 2])

>>> vals = [1, None, 2, 3]
>>> i = vals.index(2)
>>> vals[2 * i + 1] if 2 * i + 1 < len(vals) else 'out of range'
'out of range'

>>> t = (1, (2, None, None), (3, None, None))
>>> st, out = [t], []
>>> while st:
...     n = st.pop()
...     out.append(n[0])
...     st.extend(c for c in (n[1], n[2]) if c)
>>> out
[1, 3, 2]

>>> def ino(n):
...     if n:
...         yield from ino(n[1])
...         yield n[0]
...         yield from ino(n[2])
>>> g = ino((4, (2, (1, None, None), (3, None, None)), (6, None, None)))
>>> next(g), next(g), list(g)
(1, 2, [3, 4, 6])

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
([1, 2, 3, 5, 8, 9], 5, 2)

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
(True, False)

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
[[], []]

>>> def best_down(n):
...     if n is None:
...         return 0
...     return n[0] + max(0, best_down(n[1]), best_down(n[2]))
>>> best_down((-3, (5, None, None), (-1, None, None)))
2

>>> def take_or_skip(n):
...     if n is None:
...         return (0, 0)
...     l, r = take_or_skip(n[1]), take_or_skip(n[2])
...     return (n[0] + l[1] + r[1], max(l) + max(r))
>>> take_or_skip((3, (2, None, (3, None, None)), (3, None, (1, None, None))))
(7, 6)

>>> def lca(n, a, b):
...     if n is None or n[0] in (a, b):
...         return n
...     l, r = lca(n[1], a, b), lca(n[2], a, b)
...     return n if l and r else l or r
>>> t = (3, (5, (6, None, None), (2, None, None)), (1, None, None))
>>> lca(t, 6, 2)[0], lca(t, 6, 1)[0], lca(t, 5, 6)[0]
(5, 3, 5)
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


def tree_vals(root):
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def preorder_iter(root):
    out, st = [], [root] if root is not None else []
    while st:
        node = st.pop()
        out.append(node.val)
        if node.right is not None:      # pushed first, so popped after the left subtree
            st.append(node.right)
        if node.left is not None:
            st.append(node.left)
    return out


def inorder_iter(root):
    out, st, node = [], [], root
    while st or node is not None:
        while node is not None:         # push the whole left spine
            st.append(node)
            node = node.left
        node = st.pop()
        out.append(node.val)
        node = node.right
    return out


def postorder_iter(root):
    out, st = [], [root] if root is not None else []
    while st:
        node = st.pop()
        out.append(node.val)
        if node.left is not None:
            st.append(node.left)
        if node.right is not None:
            st.append(node.right)
    return out[::-1]                    # node-right-left, reversed, is left-right-node


def level_order(root):
    if root is None:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):         # len(q) is read once: exactly this level
            node = q.popleft()
            level.append(node.val)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        out.append(level)
    return out


def subtree_sizes(parents):
    n = len(parents)
    children = [[] for _ in range(n)]
    root = -1
    for v, p in enumerate(parents):
        if p == -1:
            root = v
        else:
            children[p].append(v)
    order, st = [], [root]
    while st:                           # iterative preorder: parents before children
        v = st.pop()
        order.append(v)
        st.extend(children[v])
    size = [1] * n
    for v in reversed(order):           # children are finished before their parents
        if parents[v] != -1:
            size[parents[v]] += size[v]
    return size


def is_balanced(root):
    def height(node):                   # -1 means "unbalanced somewhere below"
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        if left < 0 or right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) >= 0


def max_path_sum(root):
    best = -math.inf

    def gain(node):                     # best downward path that starts at node
        nonlocal best
        if node is None:
            return 0
        left, right = max(0, gain(node.left)), max(0, gain(node.right))
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return best


def root_to_leaf_paths(root, target):
    out, path = [], []

    def walk(node, remaining):
        if node is None:
            return
        path.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                out.append(path[:])
        else:
            walk(node.left, remaining)
            walk(node.right, remaining)
        path.pop()

    walk(root, target)
    return out


def is_bst(root):
    st = [(root, -math.inf, math.inf)]
    while st:
        node, lo, hi = st.pop()
        if node is None:
            continue
        if not lo < node.val < hi:
            return False
        st.append((node.left, lo, node.val))
        st.append((node.right, node.val, hi))
    return True


def bst_delete(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    elif root.left is None:
        return root.right
    elif root.right is None:
        return root.left
    else:
        succ = root.right
        while succ.left is not None:
            succ = succ.left
        root.val = succ.val
        root.right = bst_delete(root.right, succ.val)
    return root


def lowest_common_ancestor(root, a, b):
    if root is None or root.val in (a, b):
        return root
    left = lowest_common_ancestor(root.left, a, b)
    right = lowest_common_ancestor(root.right, a, b)
    if left is not None and right is not None:
        return root                     # a and b sit on different sides
    return left if left is not None else right


def from_preorder_inorder(preorder, inorder):
    index = {v: i for i, v in enumerate(inorder)}
    nxt = 0

    def build(lo, hi):                  # the subtree whose inorder values are inorder[lo:hi]
        nonlocal nxt
        if lo >= hi:
            return None
        node = TreeNode(preorder[nxt])
        nxt += 1
        mid = index[node.val]
        node.left = build(lo, mid)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
