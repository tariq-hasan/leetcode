from typing import Optional, Tuple


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Check if a binary tree is height-balanced using recursive DFS (post-order).
        A height-balanced tree is a tree where the depth of the two subtrees of every
        node never differs by more than one.

        Time Complexity: O(n) - We visit each node exactly once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        # Helper function that returns (isBalanced, height)
        def check_balance(node: Optional[TreeNode]) -> Tuple[bool, int]:
            # Base case
            if not node:
                return True, 0

            # Check left subtree
            left_balanced, left_height = check_balance(node.left)
            if not left_balanced:
                return False, 0  # Early termination

            # Check right subtree
            right_balanced, right_height = check_balance(node.right)
            if not right_balanced:
                return False, 0  # Early termination

            # Check if current node is balanced
            is_balanced = abs(left_height - right_height) <= 1
            height = max(left_height, right_height) + 1

            return is_balanced, height

        # Get result from helper function
        is_balanced, _ = check_balance(root)
        return is_balanced
