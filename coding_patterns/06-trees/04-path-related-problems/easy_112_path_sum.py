# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import Optional

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        Optimal Recursive DFS Solution (Most Common Interview Choice)
        
        Key insight: Subtract current node value and recurse with remaining sum
        Base case: leaf node with remaining sum equals node value
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        # Base case: empty tree
        if not root:
            return False
        
        # Base case: leaf node
        if not root.left and not root.right:
            return root.val == targetSum
        
        # Recursive case: check left and right subtrees with updated target
        remaining_sum = targetSum - root.val
        return (self.hasPathSum(root.left, remaining_sum) or 
                self.hasPathSum(root.right, remaining_sum))

    def hasPathSumIterativeDFS(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        Iterative DFS with Stack (Good alternative to show iterative thinking)
        
        Use stack to simulate recursion, storing (node, remaining_sum) pairs
        Time Complexity: O(n)
        Space Complexity: O(h) in average case, O(n) worst case
        """
        if not root:
            return False
        
        stack = [(root, targetSum)]
        
        while stack:
            node, remaining = stack.pop()
            
            # Check if this is a leaf with matching sum
            if not node.left and not node.right:
                if node.val == remaining:
                    return True
            
            # Add children to stack with updated remaining sum
            new_remaining = remaining - node.val
            if node.right:
                stack.append((node.right, new_remaining))
            if node.left:
                stack.append((node.left, new_remaining))
        
        return False

    def hasPathSumBFS(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        BFS Solution with Queue (Less common but shows breadth-first thinking)
        
        Level-order traversal storing (node, current_sum) pairs
        Time Complexity: O(n)
        Space Complexity: O(w) where w is maximum width of tree
        """
        if not root:
            return False
        
        queue = deque([(root, targetSum)])
        
        while queue:
            node, remaining = queue.popleft()
            
            # Check if leaf node matches target
            if not node.left and not node.right:
                if node.val == remaining:
                    return True
                continue
            
            # Add children with updated sum
            new_remaining = remaining - node.val
            if node.left:
                queue.append((node.left, new_remaining))
            if node.right:
                queue.append((node.right, new_remaining))
        
        return False

    def hasPathSumTrackingPath(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        DFS with Path Tracking (Useful for follow-up questions)
        
        Keeps track of the actual path for debugging/follow-up questions
        Time Complexity: O(n)
        Space Complexity: O(h) for recursion + O(h) for path = O(h)
        """
        def dfs(node, remaining, path):
            if not node:
                return False
            
            # Add current node to path
            path.append(node.val)
            
            # Check if leaf with correct sum
            if not node.left and not node.right:
                if node.val == remaining:
                    # Uncomment next line to see the path
                    # print(f"Found path: {path}")
                    return True
            
            # Try left and right subtrees
            new_remaining = remaining - node.val
            if (dfs(node.left, new_remaining, path) or 
                dfs(node.right, new_remaining, path)):
                return True
            
            # Backtrack
            path.pop()
            return False
        
        return dfs(root, targetSum, [])

    def hasPathSumAlternative(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        Alternative Recursive - Building Sum Upward
        
        Instead of subtracting, build sum from root to leaf
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def dfs(node, current_sum):
            if not node:
                return False
            
            current_sum += node.val
            
            # If leaf, check if sum matches target
            if not node.left and not node.right:
                return current_sum == targetSum
            
            # Check subtrees
            return dfs(node.left, current_sum) or dfs(node.right, current_sum)
        
        return dfs(root, 0)

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:      5
                   /   \
                  4     8
                 /     / \
                11    13  4
               /  \        \
              7    2        1
    Target: 22, Expected: True (5->4->11->2)
    """
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.right.right = TreeNode(1)
    return root

def build_test_tree2():
    """
    Build tree:    1
                  / \
                 2   3
    Target: 5, Expected: False
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    return root

def build_test_tree3():
    """
    Single node tree: 1
    Target: 1, Expected: True
    """
    return TreeNode(1)

def test_solutions():
    solution = Solution()
    
    # Test case 1
    tree1 = build_test_tree1()
    target1 = 22
    print(f"Test 1 - Target {target1}:")
    print(f"  Recursive DFS: {solution.hasPathSum(tree1, target1)}")
    print(f"  Iterative DFS: {solution.hasPathSumIterativeDFS(tree1, target1)}")
    print(f"  BFS: {solution.hasPathSumBFS(tree1, target1)}")
    print()
    
    # Test case 2
    tree2 = build_test_tree2()
    target2 = 5
    print(f"Test 2 - Target {target2}:")
    print(f"  Recursive DFS: {solution.hasPathSum(tree2, target2)}")
    print(f"  Should be False")
    print()
    
    # Test case 3
    tree3 = build_test_tree3()
    target3 = 1
    print(f"Test 3 - Single node, Target {target3}:")
    print(f"  Recursive DFS: {solution.hasPathSum(tree3, target3)}")
    print(f"  Should be True")
    print()
    
    # Edge case: empty tree
    print("Test 4 - Empty tree:")
    print(f"  Result: {solution.hasPathSum(None, 0)}")
    print(f"  Should be False")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Find if ANY root-to-leaf path sums to target
   - Must reach a LEAF node (both children are None)
   - Path must start from root

2. KEY INSIGHTS:
   - This is a classic DFS problem
   - Two approaches: subtract going down OR add going down
   - Base case: leaf node - check if remaining sum equals node value
   - Early termination: return True as soon as we find one valid path

3. SOLUTION CHOICE FOR INTERVIEW:
   
   PRIMARY: Recursive DFS (subtracting approach)
   - Most intuitive and clean
   - Easy to explain and implement
   - Shows solid recursion understanding
   
   ALTERNATIVE: Iterative DFS with stack
   - Good if they ask for non-recursive solution
   - Shows you understand stack simulation of recursion

4. IMPLEMENTATION DETAILS:
   - Handle empty tree edge case first
   - Leaf check: not node.left and not node.right
   - Short-circuit evaluation: use OR to return early
   - Subtract current value before recursive calls

5. COMMON MISTAKES TO AVOID:
   - Forgetting to check for leaf nodes (counting internal nodes)
   - Not handling empty tree case
   - Adding instead of subtracting (both work but subtract is cleaner)
   - Forgetting that path must end at leaf

6. EDGE CASES TO DISCUSS:
   - Empty tree → False
   - Single node matching target → True
   - Single node not matching target → False
   - No valid paths → False
   - Multiple paths but only one matches → True

7. TIME/SPACE COMPLEXITY:
   - Time: O(n) - must potentially visit all nodes
   - Space: O(h) - recursion depth equals tree height
   - Worst case space: O(n) for skewed tree

8. FOLLOW-UP QUESTIONS:
   - "Find all paths that sum to target" → Need to collect paths, not just boolean
   - "What if we want root-to-any-node, not just leaf?" → Remove leaf check
   - "Can you do it iteratively?" → Show stack-based solution
   - "What about negative numbers?" → Algorithm works the same

9. WHY THIS SOLUTION IS OPTIMAL:
   - Clean recursive structure matches tree structure
   - Early termination when path found
   - Minimal space usage (just recursion stack)
   - Easy to understand and debug

10. INTERVIEW PRESENTATION:
    - Start with problem clarification (must reach leaf)
    - Explain the recursive insight
    - Code the clean recursive solution
    - Walk through with an example
    - Discuss time/space complexity
    - Mention iterative alternative if asked
"""
