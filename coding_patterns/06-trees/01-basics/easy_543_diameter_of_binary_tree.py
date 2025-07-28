"""
LeetCode 543. Diameter of Binary Tree
Problem: Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two nodes 
in a tree. This path may or may not pass through the root.
The length of a path between two nodes is represented by the number of edges between them.

Example:
Input: root = [1,2,3,4,5]
       1
      / \
     2   3
    / \
   4   5
Output: 3
Explanation: The diameter is the path [4,2,1,3] or [5,2,1,3] with length 3.

Key Insights:
1. The diameter passes through some node as the "highest" point
2. For any node, diameter = left_height + right_height
3. We need to check every node as a potential "center" of the diameter
4. Can optimize by calculating height and diameter in single traversal
"""

from typing import Optional

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Approach 1: Optimized DFS - Single Pass (BEST SOLUTION)
        Time: O(N) where N is number of nodes
        Space: O(H) where H is height of tree (recursion stack)
        
        This is the optimal solution that most interviewers expect.
        """
        self.diameter = 0
        
        def height(node):
            """
            Returns height of subtree rooted at node.
            Also updates global diameter during traversal.
            """
            if not node:
                return 0
            
            # Get height of left and right subtrees
            left_height = height(node.left)
            right_height = height(node.right)
            
            # Update diameter if path through current node is longer
            # Diameter through current node = left_height + right_height
            self.diameter = max(self.diameter, left_height + right_height)
            
            # Return height of current subtree
            return 1 + max(left_height, right_height)
        
        height(root)
        return self.diameter

    def diameterOfBinaryTree_v2(self, root: Optional[TreeNode]) -> int:
        """
        Approach 2: Naive DFS - Two Pass (INEFFICIENT)
        Time: O(N²) in worst case (skewed tree)
        Space: O(H)
        
        This approach calculates height separately for each node.
        Don't use this in interviews, but good to understand why it's inefficient.
        """
        if not root:
            return 0
        
        def height(node):
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))
        
        def diameter(node):
            if not node:
                return 0
            
            # Diameter through current node
            left_height = height(node.left)
            right_height = height(node.right)
            current_diameter = left_height + right_height
            
            # Check diameters of subtrees
            left_diameter = diameter(node.left)
            right_diameter = diameter(node.right)
            
            # Return maximum of all three
            return max(current_diameter, left_diameter, right_diameter)
        
        return diameter(root)

    def diameterOfBinaryTree_v3(self, root: Optional[TreeNode]) -> int:
        """
        Approach 3: Using Return Tuple (Clean Alternative)
        Time: O(N)
        Space: O(H)
        
        Returns (height, diameter) tuple to avoid global variable.
        """
        def helper(node):
            """Returns (height, diameter) of subtree rooted at node"""
            if not node:
                return 0, 0
            
            left_height, left_diameter = helper(node.left)
            right_height, right_diameter = helper(node.right)
            
            # Current node's height
            current_height = 1 + max(left_height, right_height)
            
            # Diameter through current node
            current_diameter = left_height + right_height
            
            # Maximum diameter in this subtree
            max_diameter = max(current_diameter, left_diameter, right_diameter)
            
            return current_height, max_diameter
        
        if not root:
            return 0
        
        _, diameter = helper(root)
        return diameter

    def diameterOfBinaryTree_v4(self, root: Optional[TreeNode]) -> int:
        """
        Approach 4: Using Nonlocal Variable (Python-specific)
        Time: O(N)
        Space: O(H)
        
        Uses nonlocal instead of self.diameter to avoid class variable.
        """
        if not root:
            return 0
        
        max_diameter = 0
        
        def height(node):
            nonlocal max_diameter
            
            if not node:
                return 0
            
            left_height = height(node.left)
            right_height = height(node.right)
            
            # Update diameter
            max_diameter = max(max_diameter, left_height + right_height)
            
            return 1 + max(left_height, right_height)
        
        height(root)
        return max_diameter

    def diameterOfBinaryTree_iterative(self, root: Optional[TreeNode]) -> int:
        """
        Approach 5: Iterative using Stack (Advanced)
        Time: O(N)
        Space: O(N)
        
        More complex iterative approach. Generally not expected in interviews.
        """
        if not root:
            return 0
        
        # Stack for post-order traversal
        stack = [(root, False)]
        heights = {}  # node -> height
        max_diameter = 0
        
        while stack:
            node, visited = stack.pop()
            
            if visited:
                # Process node (post-order)
                left_height = heights.get(node.left, 0)
                right_height = heights.get(node.right, 0)
                
                heights[node] = 1 + max(left_height, right_height)
                max_diameter = max(max_diameter, left_height + right_height)
            else:
                # Visit node later
                stack.append((node, True))
                
                # Add children to stack
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))
        
        return max_diameter

# Helper function to build tree from list
def build_tree(values):
    """Build tree from leetcode array representation"""
    if not values:
        return None
    
    from collections import deque
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

# Test the solutions
def test_solutions():
    solution = Solution()
    
    # Test case 1: [1,2,3,4,5]
    root1 = build_tree([1, 2, 3, 4, 5])
    print("Test case 1: [1,2,3,4,5]")
    print("Expected: 3")
    print("Optimized DFS:", solution.diameterOfBinaryTree(root1))
    print("Tuple approach:", solution.diameterOfBinaryTree_v3(root1))
    print()
    
    # Test case 2: [1,2]
    root2 = build_tree([1, 2])
    print("Test case 2: [1,2]")
    print("Expected: 1")
    print("Result:", solution.diameterOfBinaryTree(root2))
    print()
    
    # Test case 3: Single node [1]
    root3 = build_tree([1])
    print("Test case 3: [1]")
    print("Expected: 0")
    print("Result:", solution.diameterOfBinaryTree(root3))
    print()
    
    # Test case 4: Empty tree
    root4 = None
    print("Test case 4: Empty tree")
    print("Expected: 0")
    print("Result:", solution.diameterOfBinaryTree(root4))
    print()
    
    # Test case 5: Skewed tree [1,null,2,null,3,null,4]
    root5 = TreeNode(1)
    root5.right = TreeNode(2)
    root5.right.right = TreeNode(3)
    root5.right.right.right = TreeNode(4)
    print("Test case 5: Skewed tree [1,null,2,null,3,null,4]")
    print("Expected: 3")
    print("Result:", solution.diameterOfBinaryTree(root5))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - Diameter = longest path between ANY two nodes (not necessarily through root)
   - Path length = number of edges (not nodes)
   - The longest path must pass through some node as the "highest" point

2. Key Insight:
   - For any node, the longest path through it = left_height + right_height
   - We need to check every node as a potential center of the longest path
   - Can combine height calculation with diameter calculation in single pass

3. Why Approach 1 is Optimal:
   - Single traversal: O(N) time instead of O(N²)
   - For each node, we calculate its height AND update global diameter
   - This avoids recalculating heights multiple times

4. Edge Cases:
   - Empty tree → diameter = 0
   - Single node → diameter = 0 (no edges)
   - Two nodes → diameter = 1
   - Skewed tree (linked list) → diameter = number of nodes - 1

5. Common Mistakes:
   - Confusing diameter (edges) with number of nodes in path
   - Thinking diameter must pass through root
   - Not updating diameter for every node during traversal
   - Forgetting to handle empty tree case

6. Time/Space Complexity:
   - Optimal: O(N) time, O(H) space where H is height
   - Naive: O(N²) time in worst case (recalculating heights)

7. Alternative Approaches:
   - Return tuple (height, diameter) to avoid global variable
   - Use nonlocal variable instead of self.diameter
   - Iterative approach using stack (more complex)

8. Follow-up Questions:
   - What if we want the actual path, not just length?
   - What about diameter of N-ary tree?
   - How to find diameter if edge weights are different?

RECOMMENDED APPROACH FOR INTERVIEW:
- Start with Approach 1 (optimized single-pass DFS)
- Explain the key insight: diameter through any node = left_height + right_height  
- Walk through example showing how diameter is calculated for each node
- Emphasize that we update diameter during height calculation to avoid O(N²)
- Handle edge cases properly
- Mention alternative approaches if time permits

CRITICAL INSIGHT TO COMMUNICATE:
"The diameter of a tree is the maximum value of (left_height + right_height) 
across all nodes in the tree. We can calculate this efficiently by computing 
heights and updating diameter in a single DFS traversal."
"""
