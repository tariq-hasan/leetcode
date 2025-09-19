# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import defaultdict
from typing import Optional

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        """
        Optimal Solution - Prefix Sum with HashMap (Single Pass)
        
        Key insight: Use prefix sums to find paths ending at current node.
        If prefix_sum - targetSum exists in map, we found a valid path.
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (for hashmap and recursion)
        """
        def dfs(node, current_sum, prefix_count):
            if not node:
                return 0
            
            # Update current prefix sum
            current_sum += node.val
            
            # Check how many paths end at current node with target sum
            # If current_sum - target exists, those prefix positions to current form target
            paths = prefix_count[current_sum - targetSum]
            
            # Add current prefix sum to map
            prefix_count[current_sum] += 1
            
            # Recursively count paths in left and right subtrees
            paths += dfs(node.left, current_sum, prefix_count)
            paths += dfs(node.right, current_sum, prefix_count)
            
            # Backtrack - remove current prefix sum when done with this subtree
            prefix_count[current_sum] -= 1
            
            return paths
        
        # Initialize with prefix sum 0 (for paths starting from root)
        prefix_count = defaultdict(int)
        prefix_count[0] = 1
        
        return dfs(root, 0, prefix_count)

    def pathSumBruteForce(self, root: Optional[TreeNode], targetSum: int) -> int:
        """
        Brute Force Solution - Try Every Node as Starting Point
        
        For each node, try all paths starting from that node
        Time Complexity: O(n²) in worst case (skewed tree)
        Space Complexity: O(h) for recursion
        """
        def count_paths_from(node, target):
            """Count paths starting from given node with target sum"""
            if not node:
                return 0
            
            paths = 0
            # If current node equals target, we found one path
            if node.val == target:
                paths += 1
            
            # Continue searching with updated target
            remaining_target = target - node.val
            paths += count_paths_from(node.left, remaining_target)
            paths += count_paths_from(node.right, remaining_target)
            
            return paths
        
        if not root:
            return 0
        
        # Count paths starting from current node
        total_paths = count_paths_from(root, targetSum)
        
        # Count paths in left and right subtrees (starting from their nodes)
        total_paths += self.pathSumBruteForce(root.left, targetSum)
        total_paths += self.pathSumBruteForce(root.right, targetSum)
        
        return total_paths

    def pathSumWithPaths(self, root: Optional[TreeNode], targetSum: int) -> int:
        """
        Enhanced Solution - Also Collect Actual Paths (for debugging)
        
        Similar to optimal but also tracks the actual paths found
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.all_paths = []  # Store actual paths for debugging
        
        def dfs(node, current_sum, prefix_count, path):
            if not node:
                return 0
            
            current_sum += node.val
            path.append(node.val)
            
            # Find paths ending at current node
            paths = 0
            complement = current_sum - targetSum
            
            if complement in prefix_count:
                paths = prefix_count[complement]
                # Find the actual paths (for debugging)
                if paths > 0:
                    # This is simplified - in real implementation would track exact path segments
                    self.all_paths.append(path.copy())
            
            # Add current sum to prefix count
            prefix_count[current_sum] += 1
            
            # Recurse on children
            paths += dfs(node.left, current_sum, prefix_count, path)
            paths += dfs(node.right, current_sum, prefix_count, path)
            
            # Backtrack
            prefix_count[current_sum] -= 1
            path.pop()
            
            return paths
        
        prefix_count = defaultdict(int)
        prefix_count[0] = 1
        
        result = dfs(root, 0, prefix_count, [])
        return result

    def pathSumIterative(self, root: Optional[TreeNode], targetSum: int) -> int:
        """
        Iterative Solution using Stack (More Complex)
        
        Simulates the recursive DFS with explicit stack
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return 0
        
        result = 0
        prefix_count = defaultdict(int)
        prefix_count[0] = 1
        
        # Stack stores (node, current_sum, going_down)
        stack = [(root, 0, True)]
        
        while stack:
            node, current_sum, going_down = stack.pop()
            
            if going_down:
                # Process node on the way down
                current_sum += node.val
                result += prefix_count[current_sum - targetSum]
                prefix_count[current_sum] += 1
                
                # Add return path (for backtracking)
                stack.append((node, current_sum, False))
                
                # Add children
                if node.right:
                    stack.append((node.right, current_sum, True))
                if node.left:
                    stack.append((node.left, current_sum, True))
            else:
                # Backtrack - remove current sum
                prefix_count[current_sum] -= 1
        
        return result

    def pathSumAlternativeRecursive(self, root: Optional[TreeNode], targetSum: int) -> int:
        """
        Alternative Recursive - Different Style (Less Optimal)
        
        Maintains path explicitly instead of just prefix sums
        Time Complexity: O(n)
        Space Complexity: O(h) for recursion + O(h) for path = O(h)
        """
        def dfs(node, path, target):
            if not node:
                return 0
            
            # Add current node to path
            path.append(node.val)
            
            # Count paths ending at current node
            paths = 0
            current_sum = 0
            
            # Check all possible starting points in current path
            for i in range(len(path) - 1, -1, -1):
                current_sum += path[i]
                if current_sum == target:
                    paths += 1
            
            # Recurse on children
            paths += dfs(node.left, path, target)
            paths += dfs(node.right, path, target)
            
            # Backtrack
            path.pop()
            
            return paths
        
        return dfs(root, [], targetSum)

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:        10
                     /    \
                    5      -3
                   / \      \
                  3   2      11
                 / \   \
                3  -2   1
    
    Target: 8
    Paths: [5,3], [5,2,1], [-3,11], [10,-3,11] (but not [10,-3,1] - not connected)
    Expected: Multiple paths sum to 8
    """
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(-3)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(2)
    root.right.right = TreeNode(11)
    root.left.left.left = TreeNode(3)
    root.left.left.right = TreeNode(-2)
    root.left.right.right = TreeNode(1)
    return root

def build_test_tree2():
    """
    Build tree:    5
                  / \
                 4   8
                /   / \
               11  13  4
              /  \    / \
             7    2  5   1
    
    Target: 22
    Expected: 3 paths
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

def build_simple_tree():
    """
    Simple tree:  1
                 / \
                2   3
    
    Target: 3, Expected: 2 paths (just node 3, and path 1->2)
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    return root

def build_negative_tree():
    """
    Tree with negative values:  1
                               /
                             -2
                               \
                                1
                               /
                              -1
    
    Target: 0, Expected: paths that sum to 0
    """
    root = TreeNode(1)
    root.left = TreeNode(-2)
    root.left.right = TreeNode(1)
    root.left.right.left = TreeNode(-1)
    return root

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Complex tree
    tree1 = build_test_tree1()
    target1 = 8
    print("Test 1 - Complex tree, target = 8:")
    print("       10")
    print("     /    \\")
    print("    5      -3")
    print("   / \\      \\")
    print("  3   2      11")
    print(" / \\   \\")
    print("3  -2   1")
    print(f"  Optimal: {solution.pathSum(tree1, target1)}")
    print(f"  Brute Force: {solution.pathSumBruteForce(tree1, target1)}")
    print(f"  Some paths: [5,3], [5,2,1], [-3,11]")
    print()
    
    # Test case 2 - Tree from problem description
    tree2 = build_test_tree2()
    target2 = 22
    print("Test 2 - Standard tree, target = 22:")
    print(f"  Optimal: {solution.pathSum(tree2, target2)}")
    print(f"  Expected: 3")
    print()
    
    # Test case 3 - Simple tree
    tree3 = build_simple_tree()
    target3 = 3
    print("Test 3 - Simple tree [1,2,3], target = 3:")
    print(f"  Optimal: {solution.pathSum(tree3, target3)}")
    print(f"  Expected: 2 (node 3 alone, and path 1->2)")
    print()
    
    # Test case 4 - Tree with negative values
    tree4 = build_negative_tree()
    target4 = 0
    print("Test 4 - Tree with negatives, target = 0:")
    print(f"  Optimal: {solution.pathSum(tree4, target4)}")
    print()
    
    # Edge cases
    print("Test 5 - Empty tree:")
    print(f"  Result: {solution.pathSum(None, 0)}")
    print(f"  Expected: 0")
    print()
    
    # Single node
    single_node = TreeNode(1)
    print("Test 6 - Single node [1], target = 1:")
    print(f"  Result: {solution.pathSum(single_node, 1)}")
    print(f"  Expected: 1")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Find number of paths that sum to targetSum
   - Paths can start and end at ANY nodes (not just root to leaf)
   - Path must go downward (parent to child direction)
   - Can include negative numbers
   - Multiple paths can have same sum

2. NAIVE APPROACH (mention but don't implement as primary):
   - For each node, try all paths starting from that node: O(n²)
   - "While this works, I can do much better with prefix sum technique"

3. OPTIMAL APPROACH - KEY INSIGHTS:

   INSIGHT 1: Prefix Sum Pattern
   - Track cumulative sum from root to current node
   - If (current_sum - target) exists in our history, we found valid path(s)
   - This is similar to "Two Sum" but for tree paths

   INSIGHT 2: HashMap for O(1) Lookups
   - Store frequency of each prefix sum seen so far
   - Multiple paths can have same prefix sum (hence frequency count)

   INSIGHT 3: Backtracking Pattern
   - Add current sum when entering subtree
   - Remove current sum when leaving subtree (backtrack)
   - This ensures we don't count cross-subtree paths

4. ALGORITHM WALKTHROUGH:
   - Maintain running sum from root to current node
   - Check if (current_sum - target) exists in prefix sum map
   - Add current_sum to map before recursing
   - Recurse on children
   - Remove current_sum from map (backtrack)

5. WHY PREFIX SUM WORKS:
   - If we have prefix_sum[i] and prefix_sum[j] where j > i
   - Then sum from i+1 to j = prefix_sum[j] - prefix_sum[i]
   - We want this to equal target, so prefix_sum[i] = prefix_sum[j] - target

6. CRITICAL IMPLEMENTATION DETAILS:
   - Initialize map with {0: 1} for paths starting from root
   - Use defaultdict or handle missing keys carefully
   - Backtrack by decrementing count (not deleting) to handle duplicates
   - Handle negative numbers correctly

7. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node once, O(1) hashmap operations
   - Space: O(h) for recursion stack + O(h) for hashmap = O(h)
   - Much better than O(n²) brute force!

8. EDGE CASES:
   - Empty tree → 0
   - Single node matching target → 1
   - All negative numbers
   - Target is 0 (tricky with prefix sum logic)
   - Multiple paths with same sum

9. COMPARISON TO RELATED PROBLEMS:
   - Path Sum I (112): boolean, root to leaf only
   - Path Sum II (113): all paths, root to leaf only  
   - Path Sum III (437): count paths, any start/end but downward only
   - Path Sum IV (666): different tree representation

10. INTERVIEW PRESENTATION:
    - Start with: "I'll use prefix sum technique like in subarray problems"
    - Explain the key insight: current_sum - target lookup
    - Emphasize the backtracking for tree traversal
    - Code the optimal solution
    - Walk through example showing prefix sum evolution

11. FOLLOW-UP QUESTIONS:
    - "What if paths can go upward too?" → Much harder, need different approach
    - "What if we want actual paths?" → Need to track path segments
    - "What about very wide trees?" → Discuss space complexity of hashmap
    - "Can you do it iteratively?" → Yes, but more complex

12. WHY THIS IS BRILLIANT:
    - Reduces O(n²) problem to O(n) using auxiliary space
    - Leverages well-known prefix sum pattern
    - Clean recursive structure with backtracking
    - Handles all edge cases naturally

13. COMMON MISTAKES:
    - Forgetting to initialize prefix_sum[0] = 1
    - Not backtracking properly (affects sibling subtrees)
    - Using wrong data structure (need frequency count, not just set)
    - Misunderstanding the prefix sum math

14. KEY INSIGHT TO ARTICULATE:
    "This problem is essentially finding subarrays with target sum, but on 
    tree paths instead of arrays. I can use the same prefix sum technique: 
    if I've seen prefix_sum - target before, then there's a valid path 
    ending at the current node. The key difference is backtracking when 
    leaving subtrees to ensure I don't count invalid cross-subtree paths."

15. IMPLEMENTATION CHOICE:
    - Lead with the clean recursive solution with defaultdict
    - It's elegant and shows mastery of both tree traversal and prefix sum
    - Mention brute force for comparison but don't implement as primary
    - Show iterative version only if specifically requested
"""
