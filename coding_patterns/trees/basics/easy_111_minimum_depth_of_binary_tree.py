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
