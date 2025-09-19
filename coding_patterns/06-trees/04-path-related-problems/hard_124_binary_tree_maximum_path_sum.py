# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional
import math

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Optimal DFS Solution with Global Maximum
        
        Key insight: At each node, consider two things:
        1. Max path that passes through this node (for global answer)
        2. Max path starting from this node (for parent's calculation)
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        self.max_sum = float('-inf')
        
        def max_gain(node):
            """
            Returns the maximum gain from a path starting at this node.
            Updates global maximum for paths passing through this node.
            """
            if not node:
                return 0
            
            # Get maximum gain from left and right subtrees
            # Use max(0, gain) to ignore negative paths
            left_gain = max(0, max_gain(node.left))
            right_gain = max(0, max_gain(node.right))
            
            # Maximum path sum passing through current node
            current_path_sum = node.val + left_gain + right_gain
            
            # Update global maximum
            self.max_sum = max(self.max_sum, current_path_sum)
            
            # Return maximum gain from this node (can only use one side)
            return node.val + max(left_gain, right_gain)
        
        max_gain(root)
        return self.max_sum

    def maxPathSumClean(self, root: Optional[TreeNode]) -> int:
        """
        Clean Version without Instance Variable
        
        Uses nested function to avoid instance variable
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def dfs(node):
            """Returns (max_gain_from_node, max_path_through_subtree)"""
            if not node:
                return 0, float('-inf')
            
            # Get values from children
            left_gain, left_max = dfs(node.left)
            right_gain, right_max = dfs(node.right)
            
            # Only consider positive gains
            left_gain = max(0, left_gain)
            right_gain = max(0, right_gain)
            
            # Max gain continuing from this node (for parent)
            max_gain = node.val + max(left_gain, right_gain)
            
            # Max path sum through this node (for answer)
            max_through_node = node.val + left_gain + right_gain
            
            # Max in entire subtree
            max_in_subtree = max(max_through_node, left_max, right_max)
            
            return max_gain, max_in_subtree
        
        _, result = dfs(root)
        return result

    def maxPathSumExplicit(self, root: Optional[TreeNode]) -> int:
        """
        More Explicit Version for Understanding
        
        Separates the two concerns more clearly
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.global_max = float('-inf')
        
        def get_max_single_path(node):
            """
            Returns max sum of single path starting from node.
            Also updates global_max with paths passing through node.
            """
            if not node:
                return 0
            
            # Get max single paths from children
            left_max = get_max_single_path(node.left)
            right_max = get_max_single_path(node.right)
            
            # For paths through current node, consider all possibilities:
            # 1. Just current node
            current_only = node.val
            # 2. Current + left path (if positive)
            current_left = node.val + max(0, left_max)
            # 3. Current + right path (if positive) 
            current_right = node.val + max(0, right_max)
            # 4. Current + both paths (bridge path)
            current_bridge = node.val + max(0, left_max) + max(0, right_max)
            
            # Update global maximum with best path through current node
            self.global_max = max(self.global_max, current_only, 
                                current_left, current_right, current_bridge)
            
            # Return best single path starting from current node
            return max(current_only, current_left, current_right)
        
        get_max_single_path(root)
        return self.global_max

    def maxPathSumIterative(self, root: Optional[TreeNode]) -> int:
        """
        Iterative Solution using Stack and Post-order
        
        More complex but shows non-recursive approach
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return 0
        
        stack = []
        node = root
        last_visited = None
        node_gains = {}  # Store computed gains
        max_sum = float('-inf')
        
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                peek_node = stack[-1]
                
                # If right child exists and hasn't been processed
                if peek_node.right and last_visited != peek_node.right:
                    node = peek_node.right
                else:
                    # Process current node (post-order)
                    visited_node = stack.pop()
                    last_visited = visited_node
                    
                    # Calculate gains
                    left_gain = node_gains.get(visited_node.left, 0)
                    right_gain = node_gains.get(visited_node.right, 0)
                    
                    left_gain = max(0, left_gain)
                    right_gain = max(0, right_gain)
                    
                    # Update global max with path through current node
                    current_max = visited_node.val + left_gain + right_gain
                    max_sum = max(max_sum, current_max)
                    
                    # Store gain from this node for parent
                    node_gains[visited_node] = visited_node.val + max(left_gain, right_gain)
        
        return max_sum

    def maxPathSumWithPaths(self, root: Optional[TreeNode]) -> int:
        """
        Version that also tracks the actual maximum path (for debugging)
        
        Useful for understanding and follow-up questions
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.max_sum = float('-inf')
        self.max_path = []
        
        def dfs(node, path):
            if not node:
                return 0
            
            # Get gains from children
            left_path = path + [node]
            right_path = path + [node]
            
            left_gain = dfs(node.left, left_path)
            right_gain = dfs(node.right, right_path)
            
            left_gain = max(0, left_gain)
            right_gain = max(0, right_gain)
            
            # Check if path through current node is better
            current_sum = node.val + left_gain + right_gain
            if current_sum > self.max_sum:
                self.max_sum = current_sum
                # Construct the actual path (simplified)
                self.max_path = [node.val]  # In real implementation, would track full path
            
            return node.val + max(left_gain, right_gain)
        
        dfs(root, [])
        return self.max_sum

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:      1
                   /   \
                  2     3
    
    Max path: 2 -> 1 -> 3 = 6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    return root

def build_test_tree2():
    """
    Build tree:     -10
                   /    \
                  9      20
                        /  \
                       15   7
    
    Max path: 15 -> 20 -> 7 = 42
    """
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    return root

def build_test_tree3():
    """
    Build tree:     -3
    
    Max path: -3 (single node)
    """
    return TreeNode(-3)

def build_test_tree4():
    """
    Build tree:      5
                   /   \
                  4     8
                 /     / \
                11    13  4
               /  \      / \
              7    2    5   1
    
    Max path through various nodes
    """
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.right.left = TreeNode(5)
    root.right.right.right = TreeNode(1)
    return root

def build_negative_tree():
    """
    Build tree with all negative values:  -1
                                         /  \
                                       -2   -3
    
    Max path: -1 (choose least negative single node)
    """
    root = TreeNode(-1)
    root.left = TreeNode(-2)
    root.right = TreeNode(-3)
    return root

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Simple positive tree
    tree1 = build_test_tree1()
    print("Test 1 - Simple tree [1,2,3]:")
    print("   1")
    print("  / \\")
    print(" 2   3")
    print(f"  Result: {solution.maxPathSum(tree1)}")
    print(f"  Expected: 6 (path: 2->1->3)")
    print()
    
    # Test case 2 - Tree with negative root
    tree2 = build_test_tree2()
    print("Test 2 - Tree with negative root [-10,9,20,null,null,15,7]:")
    print("     -10")
    print("    /   \\")
    print("   9     20")
    print("        /  \\")
    print("      15    7")
    print(f"  Result: {solution.maxPathSum(tree2)}")
    print(f"  Expected: 42 (path: 15->20->7)")
    print()
    
    # Test case 3 - Single negative node
    tree3 = build_test_tree3()
    print("Test 3 - Single negative node [-3]:")
    print(f"  Result: {solution.maxPathSum(tree3)}")
    print(f"  Expected: -3")
    print()
    
    # Test case 4 - Complex tree
    tree4 = build_test_tree4()
    print("Test 4 - Complex tree:")
    print(f"  Result: {solution.maxPathSum(tree4)}")
    print()
    
    # Test case 5 - All negative values
    tree5 = build_negative_tree()
    print("Test 5 - All negative values [-1,-2,-3]:")
    print(f"  Result: {solution.maxPathSum(tree5)}")
    print(f"  Expected: -1 (single node)")
    print()
    
    # Test different implementations
    print("Testing different implementations on tree2:")
    print(f"  Clean version: {solution.maxPathSumClean(tree2)}")
    print(f"  Explicit version: {solution.maxPathSumExplicit(tree2)}")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Path can start and end at ANY nodes (not necessarily root to leaf)
   - Path must be connected (no jumping between disconnected nodes)
   - Path can go through a node (using both children) or start/end at a node
   - Need to handle negative values correctly

2. KEY INSIGHTS:

   INSIGHT 1: Two Different Concepts
   - Max gain FROM a node (for parent's calculation) - single path
   - Max path SUM THROUGH a node (for global answer) - can use both sides

   INSIGHT 2: Negative Path Handling
   - If a subtree path sum is negative, ignore it (use 0 instead)
   - This naturally handles the "don't use negative paths" logic

   INSIGHT 3: Global vs Local Optimization
   - At each node, update global maximum with best path through current node
   - Return to parent only the best single-direction path

3. ALGORITHM WALKTHROUGH:
   - For each node, calculate max gain from left and right children
   - Use max(0, child_gain) to ignore negative contributions
   - Global max = node.val + left_gain + right_gain (path through node)
   - Return to parent = node.val + max(left_gain, right_gain) (single path)

4. WHY THIS SOLUTION WORKS:
   - Post-order traversal ensures we have child information before processing
   - Global variable tracks best answer found so far
   - Return value serves parent's calculation needs
   - Negative path handling is automatic

5. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node exactly once
   - Space: O(h) - recursion depth equals tree height
   - Optimal for this problem

6. CRITICAL IMPLEMENTATION DETAILS:
   - Initialize global max to negative infinity (handle all-negative trees)
   - Use max(0, child_gain) to ignore negative paths
   - Update global max before returning to parent
   - Return single-direction path sum to parent

7. EDGE CASES:
   - Single node (positive or negative)
   - All negative values → return least negative single node
   - Empty tree (though problem states tree is non-empty)
   - Linear tree (chain of nodes)

8. COMMON MISTAKES:
   - Forgetting to handle negative paths correctly
   - Not distinguishing between "path through node" and "path from node"
   - Incorrect initialization of global maximum
   - Not using post-order traversal

9. INTERVIEW PRESENTATION:
   - Clarify: "Path can start and end anywhere, not just root to leaf"
   - Explain the two concepts: "through node" vs "from node"
   - Emphasize negative path handling
   - Code the clean recursive solution
   - Walk through example showing both calculations

10. FOLLOW-UP QUESTIONS:
    - "What if we want the actual path?" → Need to track path during traversal
    - "What about very deep trees?" → Discuss iterative vs recursive trade-offs
    - "Can you do it without global variable?" → Show the clean version
    - "What if empty tree is allowed?" → Handle null root case

11. WHY THIS IS HARD:
    - Requires understanding two different optimization problems
    - Global vs local optimization pattern
    - Proper handling of negative values
    - Post-order traversal insight

12. VARIATIONS TO BE AWARE OF:
    - Path sum equals target (different problem)
    - Path sum from root to leaf only (easier version)
    - K paths with maximum sum (much harder)

13. KEY INSIGHT TO ARTICULATE:
    "At each node, I need to solve two problems: what's the maximum path sum 
    that passes through this node (for the global answer), and what's the 
    maximum gain I can provide to my parent (single direction only). The key 
    is that these are different values - I can use both children for the global 
    answer but only one child when contributing to my parent."

14. IMPLEMENTATION STYLE:
    - Most candidates should use the version with instance variable
    - It's cleaner and easier to understand under pressure
    - Mention the no-instance-variable version if they ask for alternatives
"""
