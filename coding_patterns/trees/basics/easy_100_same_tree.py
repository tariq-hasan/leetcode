from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        if not p and not q:
            return True

        if not p or not q:
            return False

        if p.val != q.val:
            return False

        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        def check(p: TreeNode, q: TreeNode) -> bool:
            if not p and not q:
                return True

            if not p or not q:
                return False

            if p.val != q.val:
                return False

            return True

        deq = deque(
            [
                (p, q),
            ]
        )
        while deq:
            p, q = deq.popleft()
            if not check(p, q):
                return False

            if p:
                deq.append((p.left, q.left))
                deq.append((p.right, q.right))

        return True
