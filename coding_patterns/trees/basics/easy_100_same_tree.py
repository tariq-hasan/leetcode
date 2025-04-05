from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution1:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative BFS
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(1) if both trees are null or root-only
            - Average: O(w) where w = max width of the tree
            - Worst: O(n) if all nodes are at one level
        """
        # Helper function to compare two nodes
        def check(node1: TreeNode, node2: TreeNode) -> bool:
            if not node1 and not node2:
                return True
            if not node1 or not node2:
                return False
            if node1.val != node2.val:
                return False
            return True

        # Initialize queue with root pair
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            # Check current pair of nodes
            if not check(node1, node2):
                return False

            # If nodes are valid, add their children to queue
            if node1:  # (and thus node2 as well due to check function)
                queue.append((node1.left, node2.left))
                queue.append((node1.right, node2.right))

        return True


class Solution2:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Recursive DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
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
