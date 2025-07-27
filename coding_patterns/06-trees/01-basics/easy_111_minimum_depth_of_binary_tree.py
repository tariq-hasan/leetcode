"""
LeetCode 111: Minimum Depth of Binary Tree

Problem: Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path 
from the root node down to the nearest leaf node.

KEY INSIGHT: A leaf is a node with no children. 
If a node has only one child, we CANNOT stop there - we must continue to find a leaf.

Time Complexity: O(n) worst case, but BFS can be much faster in practice
Space Complexity: O(h) for DFS, O(w) for BFS where w is max width
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def minDepth(self, root: TreeNode) -> int:
        """
        OPTIMAL BFS SOLUTION - Most efficient in practice
        
        Key insight: BFS finds shortest path first!
        Stop as soon as we find the first leaf node
        Much faster than DFS for trees where min depth << max depth
        
        Time: O(n) worst case, O(min_depth * width) best case
        Space: O(w) where w is maximum width
        """
        if not root:
            return 0
        
        from collections import deque
        queue = deque([(root, 1)])  # (node, depth)
        
        while queue:
            node, depth = queue.popleft()
            
            # Found first leaf - this is minimum depth!
            if not node.left and not node.right:
                return depth
            
            # Add children to queue
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        
        return 0  # Should never reach here for valid input
    
    def minDepthDFS(self, root: TreeNode) -> int:
        """
        RECURSIVE DFS SOLUTION - Good alternative
        
        Key insight: Handle the case where node has only one child
        - Both children exist: min(left, right) + 1
        - Only one child exists: take the existing child + 1
        - No children: leaf node, return 1
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return 0
        
        # Leaf node
        if not root.left and not root.right:
            return 1
        
        # Only right child exists
        if not root.left:
            return 1 + self.minDepthDFS(root.right)
        
        # Only left child exists
        if not root.right:
            return 1 + self.minDepthDFS(root.left)
        
        # Both children exist - take minimum
        return 1 + min(self.minDepthDFS(root.left), self.minDepthDFS(root.right))
    
    def minDepthDFSConcise(self, root: TreeNode) -> int:
        """
        CONCISE DFS SOLUTION - More compact version
        
        Same logic but using conditional expressions
        """
        if not root:
            return 0
        
        if not root.left and not root.right:
            return 1
        
        left_depth = self.minDepthDFSConcise(root.left) if root.left else float('inf')
        right_depth = self.minDepthDFSConcise(root.right) if root.right else float('inf')
        
        return 1 + min(left_depth, right_depth)
    
    def minDepthIterativeDFS(self, root: TreeNode) -> int:
        """
        ITERATIVE DFS SOLUTION - Stack-based approach
        
        Use stack to track (node, depth) pairs
        Keep track of minimum depth found so far
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return 0
        
        stack = [(root, 1)]
        min_depth = float('inf')
        
        while stack:
            node, depth = stack.pop()
            
            # Found a leaf - update minimum
            if not node.left and not node.right:
                min_depth = min(min_depth, depth)
                continue
            
            # Add children to stack
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        
        return min_depth
    
    def minDepthWrong(self, root: TreeNode) -> int:
        """
        WRONG SOLUTION - Common mistake to avoid!
        
        This treats nodes with one child as potential stopping points
        which violates the definition of "leaf node"
        
        DON'T use this approach!
        """
        if not root:
            return 0
        
        # WRONG: This would return 1 for a node with only one child
        # That node is NOT a leaf!
        left_depth = self.minDepthWrong(root.left) if root.left else 0
        right_depth = self.minDepthWrong(root.right) if root.right else 0
        
        return 1 + min(left_depth, right_depth)  # INCORRECT!
    
    def minDepthLevelOrder(self, root: TreeNode) -> int:
        """
        LEVEL-ORDER TRAVERSAL - Alternative BFS implementation
        
        Process tree level by level until we find first leaf
        More explicit about level processing
        
        Time: O(n), Space: O(w)
        """
        if not root:
            return 0
        
        from collections import deque
        queue = deque([root])
        depth = 1
        
        while queue:
            level_size = len(queue)
            
            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                
                # Found first leaf at this level
                if not node.left and not node.right:
                    return depth
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            depth += 1
        
        return depth


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
        if root.left or right.right:
            if root.left:
                print_tree(root.left, level + 1, "L--- ")
            if root.right:
                print_tree(root.right, level + 1, "R--- ")

def find_leaves(root, depth=1):
    """Helper to show all leaf nodes and their depths"""
    if not root:
        return []
    
    if not root.left and not root.right:
        return [(root.val, depth)]
    
    leaves = []
    if root.left:
        leaves.extend(find_leaves(root.left, depth + 1))
    if root.right:
        leaves.extend(find_leaves(root.right, depth + 1))
    
    return leaves

# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        # (tree_values, expected, description)
        ([3, 9, 20, None, None, 15, 7], 2, "Example from problem"),
        ([2, None, 3, None, 4, None, 5, None, 6], 5, "Right skewed tree"),
        ([1, 2], 2, "Simple two-node tree"),
        ([1], 1, "Single node"),
        ([], 0, "Empty tree"),
        ([1, 2, 3, 4, 5], 3, "Balanced tree"),
        ([1, 2, None, 4, None, 8], 4, "Left skewed subtree"),
        ([1, 2, 3, None, None, 4, 5], 3, "Min depth at level 3"),
        ([1, 2, 3, 4, None, None, 5, 8], 3, "Mixed structure"),
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 3, "Complex tree"),
    ]
    
    print("Testing Minimum Depth Solutions:")
    print("=" * 70)
    
    for i, (vals, expected, desc) in enumerate(test_cases):
        tree = build_tree(vals) if vals else None
        
        # Test main solutions
        result_bfs = sol.minDepth(tree)
        result_dfs = sol.minDepthDFS(tree)
        result_concise = sol.minDepthDFSConcise(tree)
        result_iter = sol.minDepthIterativeDFS(tree)
        result_level = sol.minDepthLevelOrder(tree)
        
        # Check all results match
        results = [result_bfs, result_dfs, result_concise, result_iter, result_level]
        all_correct = all(r == expected for r in results)
        status = "✓" if all_correct else "✗"
        
        print(f"Test {i+1}: {desc}")
        print(f"  Tree: {vals}")
        
        if tree and len(vals) <= 10:  # Show analysis for smaller trees
            leaves = find_leaves(tree)
            print(f"  Leaf nodes: {leaves}")
            min_leaf_depth = min(depth for _, depth in leaves) if leaves else 0
            print(f"  Minimum leaf depth: {min_leaf_depth}")
        
        print(f"  Results: {status}")
        print(f"    BFS: {result_bfs}")
        print(f"    DFS: {result_dfs}")
        print(f"    Concise: {result_concise}")
        print(f"    Iterative: {result_iter}")
        print(f"    Level-order: {result_level}")
        print(f"    Expected: {expected}")
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING - CRITICAL:
   - Minimum depth = shortest path to ANY leaf node
   - Leaf = node with NO children (both left and right are None)
   - Node with only one child is NOT a leaf!

2. KEY INSIGHT - BFS vs DFS:
   - BFS: Finds shortest path first, can terminate early
   - DFS: Must explore all paths, but simpler to implement
   - BFS is often more efficient in practice for this problem

3. COMMON MISTAKE TO AVOID:
   - DON'T use min(left_depth, right_depth) when one is 0
   - A node with one missing child is NOT a stopping point
   - Must continue until you find actual leaf nodes

4. APPROACH COMPARISON:
   - BFS: Best for early termination, efficient for wide trees
   - DFS Recursive: Clean and intuitive, good for interviews
   - DFS Iterative: Shows stack understanding
   - Level-order: Explicit level processing

5. WHEN TO USE WHICH:
   - BFS: When minimum depth likely much smaller than maximum
   - DFS: When tree is deep and narrow, or for simplicity
   - Choose BFS for optimal performance, DFS for clean code

6. COMPLEXITY ANALYSIS:
   - Time: O(n) worst case, but BFS can be much faster
   - Space: O(w) for BFS, O(h) for DFS
   - Best case BFS: O(minimum_depth * width_at_min_level)

7. EDGE CASES:
   - Empty tree (return 0)
   - Single node (return 1)
   - Skewed trees (all nodes have at most one child)
   - Balanced trees (multiple leaves at same level)

8. ALGORITHM WALKTHROUGH (DFS):
   - If no children: return 1 (leaf)
   - If only left child: return 1 + minDepth(left)
   - If only right child: return 1 + minDepth(right)
   - If both children: return 1 + min(minDepth(left), minDepth(right))

9. FOLLOW-UP QUESTIONS:
   - "Which is more efficient, BFS or DFS?" → Depends on tree shape
   - "What if we wanted all minimum depth paths?" → Modify to collect paths
   - "Memory constraints?" → Compare BFS vs DFS space usage
   - "What about n-ary trees?" → Extend to multiple children

10. RELATED PROBLEMS:
    - Maximum Depth (104) - similar but simpler
    - Binary Tree Paths (257) - finding all root-to-leaf paths
    - Sum Root to Leaf Numbers (129) - processing all paths
    - Path Sum (112) - checking specific path sums

INTERVIEW STRATEGY:
1. Clarify what constitutes a "leaf" - very important!
2. Explain why naive min() approach fails
3. Choose BFS for efficiency or DFS for simplicity
4. Walk through example showing why one-child nodes aren't leaves
5. Code your chosen solution cleanly
6. Mention the alternative approach exists
"""
