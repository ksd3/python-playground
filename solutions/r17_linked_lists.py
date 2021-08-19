"""R17 - Linked lists (reference solutions)

Compare after you've made your own attempt. Run: python check.py 17 -s
"""
from heapq import heapify, heappop, heappush

PREDICT = r"""
>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2))
>>> cur = head
>>> cur = cur.next
>>> head.val, cur.val
(1, 2)

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2))
>>> cur = head
>>> cur.next = None
>>> head.next is None
True

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3)))
>>> out = []
>>> while head:
...     out.append(head.val)
...     head = head.next
>>> out, head
([1, 2, 3], None)

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> Node(1) == Node(1), Node(1) is Node(1)
(False, False)

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
[3, 2, 1]

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> prev, curr = None, Node(1, Node(2, Node(3)))
>>> while curr:
...     curr, curr.next, prev = curr.next, prev, curr
AttributeError

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
(3, None, 1)

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
(3, 7)

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3, Node(4))))
>>> slow = fast = head
>>> while fast and fast.next:
...     slow, fast = slow.next, fast.next.next
>>> slow.val
3

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> head = Node(1, Node(2, Node(3, Node(4))))
>>> slow, fast = head, head.next
>>> while fast and fast.next:
...     slow, fast = slow.next, fast.next.next
>>> slow.val
2

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
(2, 3)

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
2

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> h = []
>>> heappush(h, (1, Node(1)))
>>> heappush(h, (1, Node(1)))
TypeError

>>> class Node:
...     def __init__(self, val, next=None):
...         self.val, self.next = val, next
>>> h = []
>>> for i, v in enumerate([5, 1, 5, 1]):
...     heappush(h, (v, i, Node(v)))
>>> [heappop(h)[:2] for _ in range(4)]
[(1, 1), (1, 3), (5, 0), (5, 2)]

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
[3, 2, 1]

>>> d = deque([1, 2, 3])
>>> d.appendleft(0); d.pop()
3
>>> d
deque([0, 1, 2])
"""


# ---------------------------------------------------------------- given

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def build(vals):
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head, limit=100_000):
    out = []
    while head is not None and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


class RandomNode:
    def __init__(self, val, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


# ---------------------------------------------------------------- drills

def delete_all(head, val):
    dummy = cur = ListNode(0, head)
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next


def reverse(head):
    prev, curr = None, head
    while curr:
        prev, curr.next, curr = curr, prev, curr.next
    return prev


def reverse_recursive(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


def reverse_between(head, left, right):
    dummy = before = ListNode(0, head)
    for _ in range(left - 1):
        before = before.next
    prev, curr = None, before.next
    for _ in range(right - left + 1):
        prev, curr.next, curr = curr, prev, curr.next
    before.next.next = curr      # the segment's old first node is now its last
    before.next = prev
    return dummy.next


def reverse_in_groups(head, k):
    dummy = group_prev = ListNode(0, head)
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        prev, curr = group_next, group_prev.next   # starting prev at group_next links the reversed tail onward
        while curr is not group_next:
            prev, curr.next, curr = curr, prev, curr.next
        first = group_prev.next
        group_prev.next = kth
        group_prev = first


def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            # head -> start equals meeting point -> start (mod the cycle length)
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None


def kth_from_end(head, k):
    lead = head
    for _ in range(k):
        if lead is None:
            return None
        lead = lead.next
    trail = head
    while lead:
        lead, trail = lead.next, trail.next
    return trail


def merge_two(a, b):
    dummy = tail = ListNode()
    while a and b:
        if b.val < a.val:
            tail.next, b = b, b.next
        else:
            tail.next, a = a, a.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k(lists):
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heappush(heap, (node.next.val, i, node.next))
    return dummy.next


def sort_list(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next          # slow stops at the end of the first half
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    return merge_two(sort_list(head), sort_list(second))


class _DNode:
    __slots__ = ("val", "prev", "next")

    def __init__(self, val=None):
        self.val, self.prev, self.next = val, None, None


class DoublyLinkedList:
    def __init__(self):
        self.head, self.tail = _DNode(), _DNode()
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def _link_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def add_front(self, val):
        node = _DNode(val)
        self._link_front(node)
        self.size += 1
        return node

    def remove(self, node):
        self._unlink(node)
        self.size -= 1

    def move_to_front(self, node):
        self._unlink(node)
        self._link_front(node)

    def pop_back(self):
        if self.size == 0:
            raise IndexError("pop_back from an empty list")
        node = self.tail.prev
        self.remove(node)
        return node.val

    def __len__(self):
        return self.size

    def to_list(self):
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur.val)
            cur = cur.next
        return out


def copy_with_random(head):
    clone = {None: None}          # maps original node -> its copy; None maps to None
    node = head
    while node:
        clone[node] = RandomNode(node.val)
        node = node.next
    node = head
    while node:
        clone[node].next = clone[node.next]
        clone[node].random = clone[node.random]
        node = node.next
    return clone[head]
