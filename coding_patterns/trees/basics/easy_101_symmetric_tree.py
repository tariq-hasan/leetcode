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
        Check if a binary tree is symmetric using recursive DFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(log n) for balanced trees (height of the tree)
            - O(n) worst case for skewed trees
        """
        if not root:
            return True

        def isMirror(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
            # Base cases
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False

            # Recursive checks - compare outer and inner pairs
            return (isMirror(left.left, right.right) and
                    isMirror(left.right, right.left))

        return isMirror(root.left, root.right)


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Check if a binary tree is symmetric using iterative DFS.
        
        Time Complexity: O(n) - we visit each node once
        Space Complexity: 
            - O(log n) for balanced trees
            - O(n) worst case for skewed trees
        """
        if not root:
            return True
            
        # Initialize stack with the left and right subtrees as a pair
        stack = [(root.left, root.right)]

        while stack:
            left, right = stack.pop()

            # Check current pair of nodes
            if not left and not right:
                continue
            if not left or not right or left.val != right.val:
                return False

            # Push the pairs to compare (outer and inner pairs)
            stack.append((left.left, right.right))
            stack.append((left.right, right.left))

        return True


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Check if a binary tree is symmetric using BFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(w) where w is the maximum width of the tree
            - O(n/2) ≈ O(n) worst case for a perfect tree's bottom level
        """
        if not root:
            return True

        # Initialize queue with the left and right subtrees as a pair
        queue = deque([(root.left, root.right)])

        while queue:
            left, right = queue.popleft()

            # Check current pair of nodes
            if not left and not right:
                continue
            if not left or not right or left.val != right.val:
                return False

            # Add mirror pairs to queue
            queue.append((left.left, right.right))
            queue.append((left.right, right.left))

        return True
