"""
LeetCode 110: Balanced Binary Tree

Problem: Given a binary tree, determine if it is height-balanced.
A height-balanced binary tree is one in which the depth of the two subtrees 
of every node never differ by more than 1.

Key Insight: For every node, |left_height - right_height| <= 1
AND both left and right subtrees must also be balanced.

Time Complexity: O(n) for optimal solution
Space Complexity: O(h) where h is height of tree
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        """
        OPTIMAL SOLUTION - Single pass with height calculation
        
        Key insight: Calculate height and check balance in single traversal
        Return -1 if subtree is unbalanced, otherwise return actual height
        
        Time: O(n), Space: O(h)
        """
        def getHeight(node):
            # Base case: empty node has height 0
            if not node:
                return 0
            
            # Get heights of subtrees
            left_height = getHeight(node.left)
            right_height = getHeight(node.right)
            
            # If any subtree is unbalanced, propagate the failure
            if left_height == -1 or right_height == -1:
                return -1
            
            # Check if current node violates balance condition
            if abs(left_height - right_height) > 1:
                return -1
            
            # Return actual height if balanced
            return 1 + max(left_height, right_height)
        
        return getHeight(root) != -1
    
    def isBalancedNaive(self, root: TreeNode) -> bool:
        """
        NAIVE SOLUTION - Recalculates height multiple times
        
        For each node, calculate heights of subtrees separately
        This leads to O(n²) time complexity due to repeated calculations
        
        Time: O(n²), Space: O(h)
        Good to mention but NOT recommended for interviews
        """
        def getHeight(node):
            if not node:
                return 0
            return 1 + max(getHeight(node.left), getHeight(node.right))
        
        def isBalancedHelper(node):
            if not node:
                return True
            
            # Calculate heights (expensive!)
            left_height = getHeight(node.left)
            right_height = getHeight(node.right)
            
            # Check balance conditions
            return (abs(left_height - right_height) <= 1 and
                    isBalancedHelper(node.left) and
                    isBalancedHelper(node.right))
        
        return isBalancedHelper(root)
    
    def isBalancedIterative(self, root: TreeNode) -> bool:
        """
        ITERATIVE SOLUTION - Using stack with postorder traversal
        
        Use stack to simulate recursion
        Calculate heights bottom-up using postorder traversal
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return True
        
        stack = []
        heights = {}  # node -> height
        node = root
        last_visited = None
        
        while stack or node:
            # Go to leftmost node
            if node:
                stack.append(node)
                node = node.left
            else:
                peek_node = stack[-1]
                
                # If right child exists and hasn't been processed
                if peek_node.right and last_visited != peek_node.right:
                    node = peek_node.right
                else:
                    # Process current node (postorder)
                    stack.pop()
                    
                    # Calculate height
                    left_height = heights.get(peek_node.left, 0)
                    right_height = heights.get(peek_node.right, 0)
                    
                    # Check balance
                    if abs(left_height - right_height) > 1:
                        return False
                    
                    # Store height
                    heights[peek_node] = 1 + max(left_height, right_height)
                    last_visited = peek_node
        
        return True
    
    def isBalancedWithInfo(self, root: TreeNode) -> bool:
        """
        SOLUTION WITH DETAILED INFO - Returns both balance and height
        
        More explicit version that returns tuple (is_balanced, height)
        Good for explaining the logic step by step
        
        Time: O(n), Space: O(h)
        """
        def checkBalance(node):
            # Base case: empty tree is balanced with height 0
            if not node:
                return True, 0
            
            # Check left subtree
            left_balanced, left_height = checkBalance(node.left)
            if not left_balanced:
                return False, 0  # Early termination
            
            # Check right subtree
            right_balanced, right_height = checkBalance(node.right)
            if not right_balanced:
                return False, 0  # Early termination
            
            # Check current node's balance
            height_diff = abs(left_height - right_height)
            is_balanced = height_diff <= 1
            current_height = 1 + max(left_height, right_height)
            
            return is_balanced, current_height
        
        balanced, _ = checkBalance(root)
        return balanced


# Helper function to build test trees
def build_tree(values):
    """Build tree from level-order list (None for missing nodes)"""
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while queue and i < len(values):
        node = queue.pop(0)
        
        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

def print_tree(root, level=0, prefix="Root: "):
    """Helper to visualize tree structure"""
    if root:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")

def get_tree_heights(root):
    """Helper to show height of each subtree"""
    if not root:
        return 0
    left_h = get_tree_heights(root.left)
    right_h = get_tree_heights(root.right)
    print(f"Node {root.val}: left_height={left_h}, right_height={right_h}, diff={abs(left_h - right_h)}")
    return 1 + max(left_h, right_h)

# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        # (tree_values, expected, description)
        ([3, 9, 20, None, None, 15, 7], True, "Balanced tree from problem"),
        ([1, 2, 2, 3, 3, None, None, 4, 4], False, "Unbalanced tree from problem"),
        ([1, 2, 2, 3, None, None, 3, 4, None, None, 4], False, "Deep unbalanced"),
        ([1], True, "Single node"),
        ([], True, "Empty tree"),
        ([1, 2, 3], True, "Simple balanced"),
        ([1, 2, None, 3], False, "Left skewed (unbalanced)"),
        ([1, None, 2, None, 3], False, "Right skewed (unbalanced)"),
        ([1, 2, 3, 4, 5, 6, 7], True, "Perfect binary tree"),
        ([1, 2, 3, 4, 5, 6, None, 7, 8], True, "Nearly complete balanced"),
    ]
    
    print("Testing Balanced Binary Tree Solutions:")
    print("=" * 70)
    
    for i, (vals, expected, desc) in enumerate(test_cases):
        tree = build_tree(vals) if vals else None
        
        # Test main solutions
        result_opt = sol.isBalanced(tree)
        result_info = sol.isBalancedWithInfo(tree)
        result_iter = sol.isBalancedIterative(tree)
        
        # Check all results match
        all_correct = all(r == expected for r in [result_opt, result_info, result_iter])
        status = "✓" if all_correct else "✗"
        
        print(f"Test {i+1}: {desc}")
        print(f"  Tree: {vals}")
        
        if vals and len(vals) <= 10:  # Show structure for smaller trees
            print("  Structure:")
            print_tree(tree)
            if tree:
                print("  Height analysis:")
                get_tree_heights(tree)
        
        print(f"  Results: {status}")
        print(f"    Optimal: {result_opt}")
        print(f"    With Info: {result_info}")
        print(f"    Iterative: {result_iter}")
        print(f"    Expected: {expected}")
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Balanced = |left_height - right_height| ≤ 1 for EVERY node
   - Not just checking the root - must check all nodes
   - Both subtrees must also be balanced (recursive property)

2. KEY INSIGHT - AVOID O(n²) SOLUTION:
   - Naive approach: For each node, calculate heights separately
   - Optimal approach: Calculate height and check balance in single pass
   - Use -1 as sentinel value to indicate unbalanced subtree

3. APPROACH COMPARISON:
   - Optimal recursive: O(n) time, single traversal
   - Naive recursive: O(n²) time, recalculates heights
   - Iterative: O(n) time, uses explicit stack
   - With info: More explicit, returns tuple

4. COMPLEXITY ANALYSIS:
   - Optimal time: O(n) - visit each node once
   - Space: O(h) - recursion stack depth
   - Naive time: O(n²) - recalculates heights repeatedly

5. ALGORITHM WALKTHROUGH:
   - For each node, get heights of left and right subtrees
   - If either subtree is unbalanced, return -1 immediately
   - Check if current node violates balance (height diff > 1)
   - If balanced, return actual height; if not, return -1

6. EDGE CASES:
   - Empty tree (balanced by definition)
   - Single node (balanced)
   - Skewed trees (unbalanced)
   - Perfect binary trees (balanced)

7. COMMON MISTAKES:
   - Only checking balance at root (must check all nodes)
   - Recalculating heights multiple times (O(n²) trap)
   - Forgetting to check if subtrees are balanced
   - Off-by-one errors in height calculation

8. OPTIMIZATION TECHNIQUES:
   - Early termination when unbalanced subtree found
   - Single-pass height calculation with balance checking
   - Using sentinel values (-1) to propagate failures

9. FOLLOW-UP QUESTIONS:
   - "What if we wanted to return the unbalanced node?" → Modify return type
   - "Can you do this iteratively?" → Show stack-based solution
   - "What's the time complexity of naive approach?" → Explain O(n²)
   - "How to make a tree balanced?" → Tree rotation/reconstruction

10. RELATED PROBLEMS:
    - Maximum Depth of Binary Tree (104) - foundation
    - Validate Binary Search Tree (98) - similar pattern
    - Diameter of Binary Tree (543) - uses similar technique
    - Convert Sorted Array to BST (108) - creates balanced tree

INTERVIEW STRATEGY:
1. Explain the naive O(n²) approach first to show understanding
2. Then optimize to O(n) single-pass solution
3. Emphasize the key insight of using -1 as failure indicator
4. Walk through example showing height calculations
5. Code the optimal solution cleanly
"""
