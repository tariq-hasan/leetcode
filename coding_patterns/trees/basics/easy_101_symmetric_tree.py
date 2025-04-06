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


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Initialize stack with the left and right subtrees as a pair
        stack = [(root.left, root.right)]

        while stack:
            left, right = stack.pop()

            # Both nodes are None, continue checking other nodes
            if not left and not right:
                continue

            # One node is None or values don't match
            if not left or not right or left.val != right.val:
                return False

            # Push the pairs to compare (outer and inner subtrees)
            stack.append((left.left, right.right))
            stack.append((left.right, right.left))

        return True


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative BFS
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(1) if tree is null or root-only
            - Average: O(w) where w = max width of the tree
            - Worst: O(n) if all nodes are at one level
        """
        # Helper function to check if two nodes are mirrors
        def check(left: TreeNode, right: TreeNode) -> bool:
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            return True

        # Initialize queue with the left and right subtrees as a pair
        queue = deque([(root.left, root.right)])

        while queue:
            left, right = queue.popleft()

            # Check current pair of nodes
            if not check(left, right):
                return False

            # If nodes are valid, add their children to queue
            if left and right:  # Both nodes exist due to check function
                # Add outer pair (left.left, right.right)
                queue.append((left.left, right.right))
                # Add inner pair (left.right, right.left)
                queue.append((left.right, right.left))

        return True
