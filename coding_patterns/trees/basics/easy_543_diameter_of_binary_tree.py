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


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Find the diameter of a binary tree using iterative DFS with post-order traversal.
        
        Time Complexity: O(n)
        Space Complexity: O(h) where h is the height of the tree
        """
        if not root:
            return 0
        
        max_diameter = 0
        # Map to store heights of subtrees
        heights = {None: 0}
        # Stack for post-order traversal
        stack = []
        node = root
        last_visited = None
        
        while stack or node:
            # Traverse to leftmost node
            if node:
                stack.append(node)
                node = node.left
            else:
                # Peek at the top node
                peek = stack[-1]
                
                # If right child exists and not visited yet
                if peek.right and peek.right != last_visited:
                    node = peek.right
                else:
                    # Process the node (post-order)
                    node = stack.pop()
                    
                    # Calculate heights of children
                    left_height = heights.get(node.left, 0)
                    right_height = heights.get(node.right, 0)
                    
                    # Update max diameter
                    max_diameter = max(max_diameter, left_height + right_height)
                    
                    # Store height of current subtree
                    heights[node] = max(left_height, right_height) + 1
                    
                    # Mark as visited
                    last_visited = node
                    node = None
        
        return max_diameter
