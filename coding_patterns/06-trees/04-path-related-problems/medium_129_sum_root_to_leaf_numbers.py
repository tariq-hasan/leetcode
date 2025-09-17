# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import Optional

class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        """
        Optimal Recursive DFS Solution (Most Common Interview Choice)
        
        Key insight: Build the number as we traverse down, sum when we reach leaves
        Pass the accumulated number down the recursion
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        def dfs(node, current_number):
            if not node:
                return 0
            
            # Build the current number by appending this digit
            current_number = current_number * 10 + node.val
            
            # If leaf node, return this complete number
            if not node.left and not node.right:
                return current_number
            
            # Sum the results from left and right subtrees
            return dfs(node.left, current_number) + dfs(node.right, current_number)
        
        return dfs(root, 0)

    def sumNumbersIterativeDFS(self, root: Optional[TreeNode]) -> int:
        """
        Iterative DFS with Stack (Good alternative for non-recursive preference)
        
        Use stack to store (node, accumulated_number) pairs
        Time Complexity: O(n)
        Space Complexity: O(h) average case, O(n) worst case
        """
        if not root:
            return 0
        
        total_sum = 0
        stack = [(root, 0)]
        
        while stack:
            node, current_number = stack.pop()
            current_number = current_number * 10 + node.val
            
            # If leaf, add to total sum
            if not node.left and not node.right:
                total_sum += current_number
            else:
                # Add children to stack
                if node.right:
                    stack.append((node.right, current_number))
                if node.left:
                    stack.append((node.left, current_number))
        
        return total_sum

    def sumNumbersBFS(self, root: Optional[TreeNode]) -> int:
        """
        BFS Solution with Queue (Shows breadth-first thinking)
        
        Process level by level, maintaining running numbers
        Time Complexity: O(n)
        Space Complexity: O(w) where w is maximum width
        """
        if not root:
            return 0
        
        total_sum = 0
        queue = deque([(root, 0)])
        
        while queue:
            node, current_number = queue.popleft()
            current_number = current_number * 10 + node.val
            
            # If leaf, add to sum
            if not node.left and not node.right:
                total_sum += current_number
            else:
                # Add children to queue
                if node.left:
                    queue.append((node.left, current_number))
                if node.right:
                    queue.append((node.right, current_number))
        
        return total_sum

    def sumNumbersWithBacktracking(self, root: Optional[TreeNode]) -> int:
        """
        DFS with Backtracking (Shows path manipulation technique)
        
        Maintains explicit path, useful for debugging and path-related follow-ups
        Time Complexity: O(n)
        Space Complexity: O(h) for recursion + O(h) for path = O(h)
        """
        def path_to_number(path):
            """Convert digit path to number"""
            number = 0
            for digit in path:
                number = number * 10 + digit
            return number
        
        def dfs(node, path):
            if not node:
                return 0
            
            # Add current digit to path
            path.append(node.val)
            
            # If leaf, convert path to number
            if not node.left and not node.right:
                result = path_to_number(path)
                path.pop()  # Backtrack
                return result
            
            # Recurse on children
            total = dfs(node.left, path) + dfs(node.right, path)
            
            # Backtrack
            path.pop()
            return total
        
        return dfs(root, [])

    def sumNumbersGlobalSum(self, root: Optional[TreeNode]) -> int:
        """
        Alternative with Global Variable (Less preferred but shows different style)
        
        Uses instance variable to accumulate sum
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.total = 0
        
        def dfs(node, current_number):
            if not node:
                return
            
            current_number = current_number * 10 + node.val
            
            # If leaf, add to global total
            if not node.left and not node.right:
                self.total += current_number
                return
            
            # Continue DFS
            dfs(node.left, current_number)
            dfs(node.right, current_number)
        
        dfs(root, 0)
        return self.total

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:    1
                  / \
                 2   3
    
    Paths: 1->2 (12), 1->3 (13)
    Expected: 12 + 13 = 25
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    return root

def build_test_tree2():
    """
    Build tree:      4
                   /   \
                  9     0
                 / \
                5   1
    
    Paths: 4->9->5 (495), 4->9->1 (491), 4->0 (40)
    Expected: 495 + 491 + 40 = 1026
    """
    root = TreeNode(4)
    root.left = TreeNode(9)
    root.right = TreeNode(0)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(1)
    return root

def build_test_tree3():
    """
    Single node: 5
    Expected: 5
    """
    return TreeNode(5)

def build_test_tree4():
    """
    Linear tree:  1
                   \
                    2
                     \
                      3
    Path: 1->2->3 (123)
    Expected: 123
    """
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.right = TreeNode(3)
    return root

def test_solutions():
    solution = Solution()
    
    # Test case 1
    tree1 = build_test_tree1()
    print("Test 1 - Simple tree [1,2,3]:")
    print(f"  Recursive DFS: {solution.sumNumbers(tree1)}")
    print(f"  Expected: 25")
    print()
    
    # Test case 2  
    tree2 = build_test_tree2()
    print("Test 2 - Tree [4,9,0,5,1]:")
    print(f"  Recursive DFS: {solution.sumNumbers(tree2)}")
    print(f"  Iterative DFS: {solution.sumNumbersIterativeDFS(tree2)}")
    print(f"  BFS: {solution.sumNumbersBFS(tree2)}")
    print(f"  Expected: 1026")
    print()
    
    # Test case 3
    tree3 = build_test_tree3()
    print("Test 3 - Single node [5]:")
    print(f"  Recursive DFS: {solution.sumNumbers(tree3)}")
    print(f"  Expected: 5")
    print()
    
    # Test case 4
    tree4 = build_test_tree4()
    print("Test 4 - Linear tree [1,null,2,null,3]:")
    print(f"  Recursive DFS: {solution.sumNumbers(tree4)}")
    print(f"  Expected: 123")
    print()
    
    # Edge case
    print("Test 5 - Empty tree:")
    print(f"  Result: {solution.sumNumbers(None)}")
    print(f"  Expected: 0")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Each root-to-leaf path represents a number (digits concatenated)
   - Need to find SUM of ALL such numbers
   - Must visit every leaf to get complete answer
   - Example: paths 12 and 13 → sum is 25

2. KEY INSIGHTS:
   - This is DFS problem - need to explore all paths
   - Build number incrementally: current_num = current_num * 10 + digit
   - At leaf: add complete number to result
   - At internal node: sum results from left and right subtrees

3. SOLUTION CHOICE FOR INTERVIEW:
   
   PRIMARY: Recursive DFS (clean and intuitive)
   - Pass accumulated number down through recursion
   - Most elegant and easy to explain
   - Shows solid recursive thinking
   
   ALTERNATIVE: Iterative DFS with stack
   - Good if they prefer iterative solutions
   - Same logic, just using explicit stack

4. CRITICAL IMPLEMENTATION DETAILS:
   - Handle empty tree (return 0)
   - Build number: current_number * 10 + node.val
   - Leaf detection: not node.left and not node.right
   - Sum all leaf values, don't just find one

5. MATHEMATICAL INSIGHT:
   - Building number left-to-right: multiply by 10 then add digit
   - Example: 0 → 1 → 12 → 123 (0*10+1, 1*10+2, 12*10+3)
   - This is more efficient than string concatenation + conversion

6. EDGE CASES TO DISCUSS:
   - Empty tree → 0
   - Single node → that node's value
   - Linear tree (all left or all right)
   - Tree with zeros (they're still valid digits)

7. TIME/SPACE COMPLEXITY:
   - Time: O(n) - visit each node exactly once
   - Space: O(h) - recursion depth equals tree height
   - Note: even though we might have many paths, we process incrementally

8. COMPARISON TO PROBLEM 112 (Path Sum):
   - Path Sum: boolean check, can return early
   - This problem: must visit ALL leaves, accumulate ALL paths
   - Similar DFS structure but different aggregation logic

9. FOLLOW-UP QUESTIONS:
   - "What if digits could be multi-digit?" → Would need different parsing
   - "What if we want the actual paths, not just sum?" → Track paths explicitly
   - "What about very large numbers?" → Discuss integer overflow concerns
   - "Can you do it iteratively?" → Show stack-based solution

10. WHY RECURSIVE IS OPTIMAL:
    - Clean separation of concerns (build vs sum)
    - Natural tree traversal pattern
    - Easy to reason about and debug
    - Minimal code with maximum clarity

11. INTERVIEW PRESENTATION:
    - Clarify: "I need to sum ALL root-to-leaf numbers"
    - Explain building numbers incrementally
    - Code the recursive solution
    - Walk through example showing number building
    - Discuss complexity and alternatives

12. COMMON MISTAKES TO AVOID:
    - Forgetting to multiply by 10 when building numbers
    - Not handling single node case properly  
    - Trying to convert to strings (inefficient)
    - Missing the leaf node check
"""
