from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Strategy: Recursive DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Helper function to check if two subtrees are mirror images
        def isMirror(left: TreeNode, right: TreeNode) -> bool:
            # Base cases
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False

            # Recursive checks - compare outer and inner subtrees
            # (left.left with right.right and left.right with right.left)
            return (isMirror(left.left, right.right) and 
                    isMirror(left.right, right.left))

        return isMirror(root.left, root.right)
