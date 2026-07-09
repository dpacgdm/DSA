from __future__ import annotations
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_from_list(vals: list) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def lowest_common_ancestor(root: TreeNode, p_val: int, q_val: int) -> int:
    cur = root
    while cur:
        if p_val < cur.val and q_val < cur.val:
            cur = cur.left
        elif p_val > cur.val and q_val > cur.val:
            cur = cur.right
        else:
            return cur.val
    raise ValueError("not found")
