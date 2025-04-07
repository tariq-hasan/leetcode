from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Strategy: Recursive DFS (post-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Base case
        if root is None:
            return 0

        # Recursive case: max depth is max of left and right subtrees + 1 for current node
        left_height = self.maxDepth(root.left)
        right_height = self.maxDepth(root.right)
        return max(left_height, right_height) + 1


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Strategy: Iterative DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Base case
        if root is None:
            return 0

        max_depth = 0
        stack = [(root, 1)]  # (node, depth) pairs
        
        while stack:
            node, depth = stack.pop()
            
            if node:
                # Update max depth if current depth is greater
                max_depth = max(depth, max_depth)
                
                # Pre-order: Push right then left (so left is processed first when popped)
                stack.append((node.right, depth + 1))
                stack.append((node.left, depth + 1))

        return max_depth
