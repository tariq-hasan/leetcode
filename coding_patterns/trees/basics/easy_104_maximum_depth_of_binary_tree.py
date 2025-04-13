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
        Find the maximum depth of a binary tree using recursive DFS (post-order).

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        # Base case
        if not root:
            return 0

        # Recursive case: max depth is max of left and right subtrees + 1
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return max(left_depth, right_depth) + 1


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find the maximum depth of a binary tree using iterative DFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees
            - O(n) worst case for skewed trees
        """
        # Base case
        if not root:
            return 0

        max_depth = 0
        stack = [(root, 1)]  # (node, depth) pairs

        while stack:
            node, depth = stack.pop()

            # Update max depth if necessary
            if node:
                max_depth = max(max_depth, depth)

                # Push children with incremented depth
                stack.append((node.right, depth + 1))
                stack.append((node.left, depth + 1))

        return max_depth


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find the maximum depth of a binary tree using BFS (level-order traversal).

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(w) where w is the maximum width of the tree
            - O(n/2) ≈ O(n) worst case for a perfect tree's bottom level
        """
        # Base case
        if not root:
            return 0

        max_depth = 0
        queue = deque([(root, 1)])  # (node, depth) pairs

        while queue:
            node, depth = queue.popleft()

            # Update max depth if necessary
            if node:
                max_depth = max(max_depth, depth)

                # Add children to the queue with incremented depth
                if node.left:
                    queue.append((node.left, depth + 1))
                if node.right:
                    queue.append((node.right, depth + 1))

        return max_depth
