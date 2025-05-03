from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find the minimum depth of a binary tree using recursive DFS (post-order).
        Minimum depth is the number of nodes along the shortest path from root to leaf.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        # Base case: empty tree
        if not root:
            return 0

        # Leaf node
        if not root.left and not root.right:
            return 1

        # If missing left or right child, we can only go down the existing path
        if not root.left:
            return self.minDepth(root.right) + 1
        if not root.right:
            return self.minDepth(root.left) + 1

        # If both children exist, take the minimum depth path
        return min(self.minDepth(root.left), self.minDepth(root.right)) + 1


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find the minimum depth of a binary tree using iterative DFS.

        Time Complexity: O(n) - we might still need to visit all nodes
        Space Complexity:
            - O(log n) for balanced trees
            - O(n) worst case for skewed trees
        """
        # Base case
        if not root:
            return 0

        # Stack stores (node, depth) pairs
        stack = [(root, 1)]
        min_depth = float('inf')

        while stack:
            node, depth = stack.pop()

            # Check if it's a leaf node
            if not node.left and not node.right:
                min_depth = min(min_depth, depth)
                # Optimization: if we found a leaf at depth 1, we can return immediately
                if depth == 1:
                    return 1

            # Push children with incremented depth
            # We push right first so that left is processed first (though order doesn't matter much here)
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))

        return min_depth


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find the minimum depth of a binary tree using BFS (level-order traversal).
        This is often the most efficient approach for finding minimum depth.

        Time Complexity: O(n) in worst case, but often better as we can terminate early
        Space Complexity:
            - O(w) where w is the maximum width of the tree
            - O(n/2) ≈ O(n) worst case for a perfect tree's bottom level
        """
        # Base case
        if not root:
            return 0

        # Queue for BFS, storing (node, depth) pairs
        queue = deque([(root, 1)])

        while queue:
            node, depth = queue.popleft()

            # If we found a leaf node, we can return immediately
            # This is the key advantage of BFS for this problem
            if not node.left and not node.right:
                return depth

            # Add children to queue
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))

        # This line shouldn't be reached if the tree has at least one node
        return 0
