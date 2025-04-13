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
        Check if two binary trees are the same using recursive DFS (pre-order).

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        # Base cases
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False

        # Recursive checks (pre-order: root, left, right)
        return (self.isSameTree(p.left, q.left) and 
                self.isSameTree(p.right, q.right))


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Check if two binary trees are the same using iterative DFS (pre-order).

        Time Complexity: O(n) - we visit each node once
        Space Complexity: 
            - O(log n) for balanced trees
            - O(n) worst case for skewed trees
        """
        # Initialize stack with root pair
        stack = [(p, q)]

        while stack:
            node1, node2 = stack.pop()

            # Check current pair of nodes
            if not node1 and not node2:
                continue
            if not node1 or not node2 or node1.val != node2.val:
                return False

            # Pre-order: Push right then left (so left is processed first)
            stack.append((node1.right, node2.right))
            stack.append((node1.left, node2.left))

        return True


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Check if two binary trees are the same using BFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(w) where w is the maximum width of the tree
            - O(n/2) ≈ O(n) worst case for a perfect tree's bottom level
        """
        # Initialize queue with root pair
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            # Check current pair of nodes
            if not node1 and not node2:
                continue
            if not node1 or not node2 or node1.val != node2.val:
                return False

            # Add children to queue
            queue.append((node1.left, node2.left))
            queue.append((node1.right, node2.right))

        return True
