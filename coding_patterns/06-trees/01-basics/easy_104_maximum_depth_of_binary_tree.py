"""
LeetCode 104: Maximum Depth of Binary Tree

Problem: Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path 
from the root node down to the farthest leaf node.

Time Complexity: O(n) where n is number of nodes
Space Complexity: O(h) where h is height of tree
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        """
        OPTIMAL RECURSIVE SOLUTION - Most important for interviews
        
        Classic divide-and-conquer approach:
        - Base case: empty node has depth 0
        - Recursive case: 1 + max(left_depth, right_depth)
        
        Time: O(n), Space: O(h) for recursion stack
        """
        # Base case: empty tree has depth 0
        if not root:
            return 0
        
        # Recursive case: 1 + maximum of left and right subtree depths
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)
    
    def maxDepthOneLiner(self, root: TreeNode) -> int:
        """
        CONCISE RECURSIVE - One-liner version
        
        Same logic but more compact
        """
        return 0 if not root else 1 + max(self.maxDepthOneLiner(root.left), 
                                          self.maxDepthOneLiner(root.right))
    
    def maxDepthIterativeBFS(self, root: TreeNode) -> int:
        """
        ITERATIVE BFS SOLUTION - Level-order traversal
        
        Process tree level by level, counting levels
        Uses queue to maintain current level nodes
        
        Time: O(n), Space: O(w) where w is maximum width
        """
        if not root:
            return 0
        
        from collections import deque
        queue = deque([root])
        depth = 0
        
        while queue:
            depth += 1
            # Process all nodes at current level
            level_size = len(queue)
            
            for _ in range(level_size):
                node = queue.popleft()
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return depth
    
    def maxDepthIterativeDFS(self, root: TreeNode) -> int:
        """
        ITERATIVE DFS SOLUTION - Using stack with depth tracking
        
        Use stack to store (node, current_depth) pairs
        Track maximum depth seen so far
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return 0
        
        stack = [(root, 1)]  # (node, current_depth)
        max_depth = 0
        
        while stack:
            node, current_depth = stack.pop()
            
            # Update maximum depth
            max_depth = max(max_depth, current_depth)
            
            # Add children with incremented depth
            if node.left:
                stack.append((node.left, current_depth + 1))
            if node.right:
                stack.append((node.right, current_depth + 1))
        
        return max_depth
    
    def maxDepthPreorder(self, root: TreeNode) -> int:
        """
        PREORDER TRAVERSAL APPROACH - Explicit traversal
        
        Manually traverse using preorder and track depth
        Good to show understanding of traversal patterns
        
        Time: O(n), Space: O(h)
        """
        self.max_depth = 0
        
        def preorder(node, depth):
            if not node:
                return
            
            # Update global maximum
            self.max_depth = max(self.max_depth, depth)
            
            # Traverse children with increased depth
            preorder(node.left, depth + 1)
            preorder(node.right, depth + 1)
        
        if root:
            preorder(root, 1)
        
        return self.max_depth
    
    def maxDepthPostorder(self, root: TreeNode) -> int:
        """
        POSTORDER TRAVERSAL APPROACH - Bottom-up
        
        Process children first, then determine current node's contribution
        More natural for this problem (similar to main recursive solution)
        
        Time: O(n), Space: O(h)
        """
        def postorder(node):
            if not node:
                return 0
            
            # Get depths of subtrees first
            left_depth = postorder(node.left)
            right_depth = postorder(node.right)
            
            # Return depth including current node
            return 1 + max(left_depth, right_depth)
        
        return postorder(root)


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

# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        # (tree_values, expected, description)
        ([3, 9, 20, None, None, 15, 7], 3, "Example from problem"),
        ([1, None, 2], 2, "Right skewed tree"),
        ([1, 2], 2, "Simple two-node tree"),
        ([1], 1, "Single node"),
        ([], 0, "Empty tree"),
        ([1, 2, 3, 4, 5], 3, "Balanced tree"),
        ([1, 2, None, 3, None, 4], 4, "Left skewed tree"),
        ([1, 2, 3, 4, 5, 6, 7, 8], 4, "Nearly complete tree"),
    ]
    
    print("Testing Maximum Depth Solutions:")
    print("=" * 60)
    
    for i, (vals, expected, desc) in enumerate(test_cases):
        tree = build_tree(vals) if vals else None
        
        # Test all solutions
        result_rec = sol.maxDepth(tree)
        result_one = sol.maxDepthOneLiner(tree)
        result_bfs = sol.maxDepthIterativeBFS(tree)
        result_dfs = sol.maxDepthIterativeDFS(tree)
        result_post = sol.maxDepthPostorder(tree)
        
        # Check all results match
        all_correct = all(r == expected for r in [result_rec, result_one, result_bfs, result_dfs, result_post])
        status = "✓" if all_correct else "✗"
        
        print(f"Test {i+1}: {desc}")
        print(f"  Tree: {vals}")
        if vals and len(vals) <= 8:  # Only print structure for smaller trees
            print("  Structure:")
            print_tree(tree)
        print(f"  Results: {status}")
        print(f"    Recursive: {result_rec}")
        print(f"    One-liner: {result_one}")
        print(f"    BFS: {result_bfs}")
        print(f"    DFS: {result_dfs}")
        print(f"    Postorder: {result_post}")
        print(f"    Expected: {expected}")
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Depth = number of nodes from root to deepest leaf
   - NOT the number of edges (that would be height)
   - Single node has depth 1, empty tree has depth 0

2. APPROACH COMPARISON:
   - Recursive: Most natural, divide-and-conquer
   - BFS: Level-by-level, intuitive for "depth" concept
   - DFS: Stack-based, good alternative to recursion
   - Traversal variants: Show understanding of tree traversal patterns

3. COMPLEXITY ANALYSIS:
   - Time: O(n) - must visit every node
   - Space: O(h) for recursion/stack, O(w) for BFS queue
   - Best case: O(log n) for balanced tree
   - Worst case: O(n) for skewed tree

4. WHICH APPROACH TO CHOOSE:
   - Recursive: Most preferred, clean and intuitive
   - BFS: Good if interviewer asks about level-order processing
   - DFS iterative: Shows understanding of recursion-to-iteration conversion

5. EDGE CASES:
   - Empty tree (return 0)
   - Single node (return 1)
   - Skewed tree (linear chain)
   - Balanced tree

6. FOLLOW-UP QUESTIONS:
   - "Can you do this iteratively?" → Show BFS or DFS stack
   - "What if we wanted minimum depth?" → Similar but use min()
   - "Memory constraints?" → Discuss recursive vs iterative trade-offs
   - "What about n-ary trees?" → Extend to multiple children

7. COMMON MISTAKES:
   - Confusing depth with height (off-by-one errors)
   - Not handling empty tree case
   - In BFS, not processing level by level correctly

8. OPTIMIZATION NOTES:
   - Could add early termination if we know max possible depth
   - For very wide trees, DFS might be more memory efficient than BFS
   - Tail recursion optimization possible in some languages

9. RELATED PROBLEMS:
   - Minimum Depth of Binary Tree (111)
   - Balanced Binary Tree (110)
   - Diameter of Binary Tree (543)
   - Path Sum problems
"""
