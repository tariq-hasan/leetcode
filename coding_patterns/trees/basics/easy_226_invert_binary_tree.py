from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert a binary tree using recursive DFS (pre-order).

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        # Base case
        if not root:
            return None

        # Swap the children (pre-order: process current node first)
        root.left, root.right = root.right, root.left

        # Recursively invert left and right subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert a binary tree using iterative DFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees
            - O(n) worst case for skewed trees
        """
        # Base case
        if not root:
            return None

        # Stack for DFS
        stack = [root]

        while stack:
            # Pop a node to process
            node = stack.pop()

            # Swap its children
            node.left, node.right = node.right, node.left

            # Push non-null children to continue DFS
            # Push right first so left is processed first (though order doesn't matter much here)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return root
