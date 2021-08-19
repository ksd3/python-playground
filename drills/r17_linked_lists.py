"""R17 - Linked lists

A linked list is nodes pointing at nodes, so every bug is a pointer rewired in
the wrong order or a reference you lost. Draw the boxes and arrows before you
code each change. A dummy node in front of the head removes every "what if it's
the head" special case. Fast/slow pointers find the middle, the k-th node from
the end and cycles (Floyd's algorithm) with O(1) extra space. Python's default
recursion limit is 1000, so anything that must handle long lists is iterative.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 17` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.
ListNode, build, to_list and RandomNode are given; use them while you experiment.

Unlocks: the linked-list family, LRU caches, merging k sorted streams, and
Floyd's cycle trick on arrays where index i points to nums[i].
"""

PREDICT = r"""
>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2))
>>> cur = head
>>> cur = cur.next
>>> head.val, cur.val
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2))
>>> cur = head
>>> cur.next = None
>>> head.next is None
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3)))
>>> out = []
>>> while head:
...     out.append(head.val)
...     head = head.next
>>> out, head
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> Node(1) == Node(1), Node(1) is Node(1)
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> def vals(h):
...     out = []
...     while h:
...         out.append(h.val)
...         h = h.next
...     return out
>>> prev, curr = None, Node(1, Node(2, Node(3)))
>>> while curr:
...     prev, curr.next, curr = curr, prev, curr.next
>>> vals(prev)
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> prev, curr = None, Node(1, Node(2, Node(3)))
>>> while curr:
...     curr, curr.next, prev = curr.next, prev, curr
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> def rev(h):
...     if not h or not h.next:
...         return h
...     new_head = rev(h.next)
...     h.next.next = h
...     h.next = None
...     return new_head
>>> head = Node(1, Node(2, Node(3)))
>>> new = rev(head)
>>> new.val, head.next, new.next.next.val
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(7, Node(7, Node(3)))
>>> dummy = Node(0, head)
>>> cur = dummy
>>> while cur.next:
...     if cur.next.val == 7:
...         cur.next = cur.next.next
...     else:
...         cur = cur.next
>>> dummy.next.val, head.val
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3, Node(4))))
>>> slow = fast = head
>>> while fast and fast.next:
...     slow, fast = slow.next, fast.next.next
>>> slow.val
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3, Node(4))))
>>> slow, fast = head, head.next
>>> while fast and fast.next:
...     slow, fast = slow.next, fast.next.next
>>> slow.val
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> a, b, c = Node(1), Node(2), Node(3)
>>> a.next, b.next, c.next = b, c, b
>>> seen, cur = set(), a
>>> while cur and cur not in seen:
...     seen.add(cur)
...     cur = cur.next
>>> cur.val, len(seen)
???

>>> nums = [1, 3, 4, 2, 2]
>>> slow = fast = 0
>>> while True:
...     slow, fast = nums[slow], nums[nums[fast]]
...     if slow == fast:
...         break
>>> slow = 0
>>> while slow != fast:
...     slow, fast = nums[slow], nums[fast]
>>> slow
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> h = []
>>> heappush(h, (1, Node(1)))
>>> heappush(h, (1, Node(1)))
???

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> h = []
>>> for i, v in enumerate([5, 1, 5, 1]):
...     heappush(h, (v, i, Node(v)))
>>> [heappop(h)[:2] for _ in range(4)]
???

>>> class DNode:
...     def __init__(self, val):
...         self.val, self.prev, self.next = val, None, None
>>> head, tail = DNode(None), DNode(None)
>>> head.next, tail.prev = tail, head
>>> def add_front(node):
...     node.prev, node.next = head, head.next
...     head.next.prev = node
...     head.next = node
>>> for v in (1, 2, 3):
...     add_front(DNode(v))
>>> out, cur = [], head.next
>>> while cur is not tail:
...     out.append(cur.val)
...     cur = cur.next
>>> out
???

>>> d = deque([1, 2, 3])
>>> d.appendleft(0); d.pop()
???
>>> d
???
"""


# ---------------------------------------------------------------- given

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def build(vals):
    """Linked list from an iterable of values; returns the head (None if empty)."""
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head, limit=100_000):
    """Values front to back. Stops after `limit` nodes so a cycle can't hang you."""
    out = []
    while head is not None and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


class RandomNode:
    """A node with one extra pointer that can point at any node of the list, or None."""

    def __init__(self, val, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


# ---------------------------------------------------------------- drills

def delete_all(head, val):
    """Remove every node whose value equals val and return the new head.
    delete_all(build([7, 7, 3, 7]), 7) -> the list [3]. Use a dummy node instead
    of special-casing the head."""
    raise NotImplementedError


def reverse(head):
    """Reverse the list by rewiring next pointers (no new nodes, O(1) extra space)
    and return the new head. [1, 2, 3] -> [3, 2, 1]."""
    raise NotImplementedError


def reverse_recursive(head):
    """Same contract as reverse(), written recursively."""
    raise NotImplementedError


def reverse_between(head, left, right):
    """Reverse the nodes at positions left..right (1-based, inclusive) and return
    the head. reverse_between(build([1, 2, 3, 4, 5]), 2, 4) -> [1, 4, 3, 2, 5]."""
    raise NotImplementedError


def reverse_in_groups(head, k):
    """Reverse every consecutive group of k nodes; a final group shorter than k
    stays as it is. k=2: [1, 2, 3, 4, 5] -> [2, 1, 4, 3, 5]. Rewire, don't copy."""
    raise NotImplementedError


def middle(head):
    """Return the middle NODE using fast/slow pointers. For an even length return
    the second of the two middles ([1, 2, 3, 4] -> the node holding 3); None for
    an empty list."""
    raise NotImplementedError


def has_cycle(head):
    """Return True if following next pointers ever revisits a node, else False.
    O(1) extra space, and don't modify the list."""
    raise NotImplementedError


def cycle_start(head):
    """Return the node where the cycle begins, or None if there's no cycle.
    O(1) extra space (Floyd: meet inside the loop, then walk one pointer from the
    head and one from the meeting point until they meet). Don't modify the list."""
    raise NotImplementedError


def kth_from_end(head, k):
    """Return the k-th node from the end (k=1 is the last node) in one pass, using
    two pointers k nodes apart. Return None if the list has fewer than k nodes."""
    raise NotImplementedError


def merge_two(a, b):
    """Merge two sorted lists by splicing their nodes (no new value nodes) and
    return the head. On equal values a's node comes first. Iterative, because the
    lists can be long."""
    raise NotImplementedError


def merge_k(lists):
    """Merge a list of sorted linked lists (some may be None) into one sorted list
    and return the head. Use a heap of (value, index, node) so ties never compare
    nodes. O(N log k) for N nodes in k lists."""
    raise NotImplementedError


def sort_list(head):
    """Sort the list in O(n log n) with merge sort: split at the middle, sort both
    halves, merge them. Reuse the nodes. Must handle 2000 nodes."""
    raise NotImplementedError


class DoublyLinkedList:
    """Doubly linked list with sentinel head and tail nodes, so no operation needs
    an empty-list special case. Everything is O(1) except to_list().

    add_front(val)      -> the new node (it has .val, .prev and .next)
    remove(node)        -> unlinks a node that's in this list
    move_to_front(node) -> moves a node that's in this list to the front
    pop_back()          -> removes the last node and returns its value
                           (IndexError if the list is empty)
    len(dll)            -> number of nodes
    dll.to_list()       -> values front to back
    """

    def __init__(self):
        raise NotImplementedError

    def add_front(self, val):
        raise NotImplementedError

    def remove(self, node):
        raise NotImplementedError

    def move_to_front(self, node):
        raise NotImplementedError

    def pop_back(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def to_list(self):
        raise NotImplementedError


def copy_with_random(head):
    """Deep-copy a list of RandomNode (next and random pointers) and return the new
    head. The copy must share no nodes with the original, and the original must be
    left exactly as it was."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random


def _nodes(head, limit=100_000):
    out = []
    while head is not None and len(out) < limit:
        out.append(head)
        head = head.next
    return out


def _same(xs, ys):
    return len(xs) == len(ys) and all(x is y for x, y in zip(xs, ys))


def _cyclic(n, pos):
    """n nodes valued 0..n-1 whose last node points back at node pos."""
    nodes = _nodes(build(range(n)))
    nodes[-1].next = nodes[pos]
    return nodes


def test_delete_all():
    assert to_list(delete_all(build([7, 7, 3, 7]), 7)) == [3], "after unlinking a node, don't advance: the new next may match too"
    assert delete_all(build([7, 7]), 7) is None, "deleting every node should leave None"
    assert delete_all(None, 1) is None
    assert to_list(delete_all(build([1, 2, 3]), 9)) == [1, 2, 3]
    rng = random.Random(17)
    for _ in range(300):
        vals = [rng.randint(0, 3) for _ in range(rng.randint(0, 8))]
        target = rng.randint(0, 3)
        head = build(vals)
        keep = [n for n in _nodes(head) if n.val != target]
        assert _same(_nodes(delete_all(head, target)), keep), (vals, target)


def test_reverse():
    assert reverse(None) is None
    rng = random.Random(17)
    for n in range(12):
        head = build(rng.randint(0, 9) for _ in range(n))
        nodes = _nodes(head)
        assert _same(_nodes(reverse(head)), nodes[::-1]), "rewire the original nodes; the old head must end with next = None"
    head = build(range(5000))
    assert to_list(reverse(head))[:3] == [4999, 4998, 4997]


def test_reverse_recursive():
    assert reverse_recursive(None) is None
    rng = random.Random(17)
    for n in list(range(12)) + [300]:
        head = build(rng.randint(0, 9) for _ in range(n))
        nodes = _nodes(head)
        assert _same(_nodes(reverse_recursive(head)), nodes[::-1]), "the old head must end with next = None"


def test_reverse_between():
    assert to_list(reverse_between(build([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
    assert to_list(reverse_between(build([1, 2]), 1, 2)) == [2, 1], "left == 1 changes the head: use a dummy node"
    assert to_list(reverse_between(build([5]), 1, 1)) == [5]
    rng = random.Random(17)
    for _ in range(300):
        n = rng.randint(1, 9)
        left = rng.randint(1, n)
        right = rng.randint(left, n)
        head = build(range(n))
        nodes = _nodes(head)
        want = nodes[:left - 1] + nodes[left - 1:right][::-1] + nodes[right:]
        assert _same(_nodes(reverse_between(head, left, right)), want), (n, left, right)


def test_reverse_in_groups():
    assert to_list(reverse_in_groups(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(reverse_in_groups(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5], "a short last group stays as it is"
    assert to_list(reverse_in_groups(build([1, 2, 3]), 1)) == [1, 2, 3]
    assert reverse_in_groups(None, 2) is None
    rng = random.Random(17)
    for _ in range(300):
        n, k = rng.randint(0, 10), rng.randint(1, 4)
        head = build(range(n))
        nodes = _nodes(head)
        want = []
        for i in range(0, n, k):
            chunk = nodes[i:i + k]
            want += chunk[::-1] if len(chunk) == k else chunk
        assert _same(_nodes(reverse_in_groups(head, k)), want), (n, k)


def test_middle():
    assert middle(None) is None
    for n in range(1, 11):
        head = build(range(n))
        assert middle(head) is _nodes(head)[n // 2], f"length {n}: expected the node holding {n // 2}"


def test_has_cycle():
    assert has_cycle(None) is False
    for n in range(1, 7):
        assert has_cycle(build(range(n))) is False
        for pos in range(n):
            nodes = _cyclic(n, pos)
            assert has_cycle(nodes[0]) is True, (n, pos)
            assert nodes[-1].next is nodes[pos], "don't modify the list"


def test_cycle_start():
    assert cycle_start(None) is None
    for n in range(1, 8):
        assert cycle_start(build(range(n))) is None
        for pos in range(n):
            nodes = _cyclic(n, pos)
            assert cycle_start(nodes[0]) is nodes[pos], (n, pos)
            assert all(a.next is b for a, b in zip(nodes, nodes[1:])), "don't modify the list"
            assert nodes[-1].next is nodes[pos], "don't modify the list"


def test_kth_from_end():
    assert kth_from_end(None, 1) is None
    head = build([10, 20, 30, 40, 50])
    nodes = _nodes(head)
    for k in range(1, 6):
        assert kth_from_end(head, k) is nodes[-k], k
    assert kth_from_end(head, 6) is None, "fewer than k nodes -> None"


def test_merge_two():
    assert merge_two(None, None) is None
    assert to_list(merge_two(build([1, 4]), None)) == [1, 4]
    rng = random.Random(17)
    for _ in range(300):
        a_vals = sorted(rng.randint(0, 5) for _ in range(rng.randint(0, 6)))
        b_vals = sorted(rng.randint(0, 5) for _ in range(rng.randint(0, 6)))
        a, b = build(a_vals), build(b_vals)
        from_a = {id(n) for n in _nodes(a)}
        every = {id(n) for n in _nodes(a) + _nodes(b)}
        out = _nodes(merge_two(a, b))
        assert [n.val for n in out] == sorted(a_vals + b_vals)
        assert {id(n) for n in out} == every and len(out) == len(every), "splice the existing nodes"
        for x, y in zip(out, out[1:]):
            assert not (x.val == y.val and id(x) not in from_a and id(y) in from_a), "on ties, a's node goes first"
    long_a, long_b = build(range(0, 6000, 2)), build(range(1, 6000, 2))
    assert to_list(merge_two(long_a, long_b)) == list(range(6000))


def test_merge_k():
    assert merge_k([]) is None
    assert merge_k([None, None]) is None
    rng = random.Random(17)
    for _ in range(200):
        lists = [sorted(rng.randint(0, 4) for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 6))]
        heads = [build(vals) for vals in lists]
        assert to_list(merge_k(heads)) == sorted(v for vals in lists for v in vals), lists


def test_sort_list():
    assert sort_list(None) is None
    rng = random.Random(17)
    for n in list(range(30)) + [2000]:
        vals = [rng.randint(-50, 50) for _ in range(n)]
        head = build(vals)
        ids = {id(node) for node in _nodes(head)}
        out = _nodes(sort_list(head))
        assert [node.val for node in out] == sorted(vals), n
        assert {id(node) for node in out} == ids, "reuse the original nodes"


def test_doubly_linked_list():
    d = DoublyLinkedList()
    assert len(d) == 0 and d.to_list() == []
    try:
        d.pop_back()
    except IndexError:
        pass
    else:
        raise AssertionError("pop_back() on an empty list should raise IndexError")
    n1, n2, n3 = d.add_front(1), d.add_front(2), d.add_front(3)
    assert d.to_list() == [3, 2, 1] and len(d) == 3
    d.move_to_front(n1)
    assert d.to_list() == [1, 3, 2]
    d.move_to_front(n1)
    assert d.to_list() == [1, 3, 2], "moving the front node to the front changes nothing"
    d.remove(n3)
    assert d.to_list() == [1, 2] and len(d) == 2
    assert d.pop_back() == 2 and d.to_list() == [1] and len(d) == 1
    rng = random.Random(17)
    d, model = DoublyLinkedList(), []          # model holds the nodes, front first
    for step in range(400):
        op = rng.choice(["add", "add", "remove", "move", "pop"])
        if op == "add":
            model.insert(0, d.add_front(step))
        elif op == "remove" and model:
            node = model.pop(rng.randrange(len(model)))
            d.remove(node)
        elif op == "move" and model:
            node = model.pop(rng.randrange(len(model)))
            model.insert(0, node)
            d.move_to_front(node)
        elif op == "pop" and model:
            assert d.pop_back() == model.pop().val
        assert d.to_list() == [n.val for n in model] and len(d) == len(model), op
        assert all(a.next is b and b.prev is a for a, b in zip(model, model[1:])), "prev/next links disagree"


def _random_list(rng, n):
    nodes = [RandomNode(rng.randint(0, 9)) for _ in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    for node in nodes:
        node.random = rng.choice(nodes + [None])
    return nodes


def _shape(head):
    nodes = _nodes(head)
    index = {id(n): i for i, n in enumerate(nodes)}
    return [(n.val, None if n.random is None else index.get(id(n.random), "outside the list")) for n in nodes]


def test_copy_with_random():
    assert copy_with_random(None) is None
    rng = random.Random(17)
    for _ in range(200):
        nodes = _random_list(rng, rng.randint(1, 8))
        before = _shape(nodes[0])
        links = [(n.next, n.random) for n in nodes]
        copy = copy_with_random(nodes[0])
        assert _shape(copy) == before, "values, next order or random targets differ"
        assert not ({id(n) for n in _nodes(copy)} & {id(n) for n in nodes}), "the copy must not reuse original nodes"
        assert [(n.next, n.random) for n in nodes] == links, "the original list was modified"
