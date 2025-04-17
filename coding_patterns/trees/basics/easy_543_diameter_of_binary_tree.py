from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Find the diameter of a binary tree using recursive DFS (post-order).
        Diameter is the length of the longest path between any two nodes.
        
        Time Complexity: O(n) - we visit each node once
        Space Complexity: O(h) where h is the height of the tree (recursion stack)
        """
        # Track the maximum diameter found
        max_diameter = 0
        
        def dfs(node):
            nonlocal max_diameter
            
            # Base case: empty node
            if not node:
                return 0
            
            # Get depths of left and right subtrees
            left_depth = dfs(node.left)
            right_depth = dfs(node.right)
            
            # Update max diameter (path through current node)
            current_diameter = left_depth + right_depth
            max_diameter = max(max_diameter, current_diameter)
            
            # Return the depth of current subtree
            return max(left_depth, right_depth) + 1
        
        # Start DFS and return the result
        dfs(root)
        return max_diameter
