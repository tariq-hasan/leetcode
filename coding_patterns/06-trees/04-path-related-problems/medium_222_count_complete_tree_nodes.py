# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional
import math

class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        """
        Optimal Solution - Exploiting Complete Binary Tree Property
        
        Key insight: In complete binary tree, if left and right subtree heights are equal,
        left subtree is perfect. If not, right subtree is perfect.
        
        Time Complexity: O(log²n) where n is number of nodes
        Space Complexity: O(log n) due to recursion depth
        """
        if not root:
            return 0
        
        # Get heights of leftmost and rightmost paths
        left_height = self.get_left_height(root)
        right_height = self.get_right_height(root)
        
        # If heights are equal, tree is perfect binary tree
        if left_height == right_height:
            return (1 << left_height) - 1  # 2^height - 1
        
        # Otherwise, recursively count left and right subtrees
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)
    
    def get_left_height(self, node):
        """Get height by going only left"""
        height = 0
        while node:
            height += 1
            node = node.left
        return height
    
    def get_right_height(self, node):
        """Get height by going only right"""
        height = 0
        while node:
            height += 1
            node = node.right
        return height

    def countNodesSimple(self, root: Optional[TreeNode]) -> int:
        """
        Simple Recursive Solution (Not optimal but easy to understand)
        
        Standard tree traversal counting all nodes
        Time Complexity: O(n)
        Space Complexity: O(log n)
        """
        if not root:
            return 0
        return 1 + self.countNodesSimple(root.left) + self.countNodesSimple(root.right)

    def countNodesIterative(self, root: Optional[TreeNode]) -> int:
        """
        Iterative Solution with Stack (O(n) but shows iterative thinking)
        
        Standard iterative tree traversal
        Time Complexity: O(n)
        Space Complexity: O(log n) average case
        """
        if not root:
            return 0
        
        stack = [root]
        count = 0
        
        while stack:
            node = stack.pop()
            count += 1
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return count

    def countNodesBinarySearch(self, root: Optional[TreeNode]) -> int:
        """
        Alternative Optimal Solution - Binary Search on Last Level
        
        Use binary search to find how many nodes exist in the last level
        Time Complexity: O(log²n)
        Space Complexity: O(log n)
        """
        if not root:
            return 0
        
        # Get the height of the tree
        height = 0
        node = root
        while node.left:
            height += 1
            node = node.left
        
        # If height is 0, only root exists
        if height == 0:
            return 1
        
        # Binary search on the last level
        # Last level can have 1 to 2^height nodes
        left, right = 1, 1 << height  # 2^height
        
        while left <= right:
            mid = (left + right) // 2
            if self.node_exists(root, height, mid):
                left = mid + 1
            else:
                right = mid - 1
        
        # Total nodes = nodes in complete levels + nodes in last level
        return (1 << height) - 1 + right
    
    def node_exists(self, root, height, index):
        """Check if node at given index exists in last level"""
        left, right = 1, 1 << height
        node = root
        
        for _ in range(height):
            mid = (left + right) // 2
            if index <= mid:
                node = node.left
                right = mid
            else:
                node = node.right
                left = mid + 1
        
        return node is not None

    def countNodesFormula(self, root: Optional[TreeNode]) -> int:
        """
        Enhanced Optimal Solution with Better Constant Factors
        
        More efficient implementation of the complete tree property exploitation
        Time Complexity: O(log²n)
        Space Complexity: O(log n)
        """
        def compute_depth(node):
            """Compute depth of leftmost path"""
            depth = 0
            while node.left:
                node = node.left
                depth += 1
            return depth
        
        if not root:
            return 0
        
        left_depth = compute_depth(root.left) if root.left else -1
        right_depth = compute_depth(root.right) if root.right else -1
        
        if left_depth == right_depth:
            # Left subtree is perfect, count it with formula + recurse right
            return (1 << (left_depth + 1)) + self.countNodesFormula(root.right)
        else:
            # Right subtree is perfect, count it with formula + recurse left  
            return (1 << (right_depth + 1)) + self.countNodesFormula(root.left)

# Test cases and utility functions
def build_complete_tree1():
    """
    Build complete tree:     1
                           /   \
                          2     3
                         / \   /
                        4   5 6
    
    Expected count: 6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    return root

def build_complete_tree2():
    """
    Build perfect tree:      1
                           /   \
                          2     3
                         / \   / \
                        4   5 6   7
    
    Expected count: 7
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    return root

def build_single_node():
    """Single node tree: 1"""
    return TreeNode(1)

def build_complete_tree3():
    """
    Larger complete tree:        1
                              /     \
                             2       3
                           /   \   /   \
                          4     5 6     7
                         / \   /
                        8   9 10
    
    Expected count: 10
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    root.left.left.left = TreeNode(8)
    root.left.left.right = TreeNode(9)
    root.left.right.left = TreeNode(10)
    return root

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Complete but not perfect
    tree1 = build_complete_tree1()
    print("Test 1 - Complete tree (6 nodes):")
    print("     1")
    print("   /   \\")
    print("  2     3")
    print(" / \\   /")
    print("4   5 6")
    print(f"  Optimal: {solution.countNodes(tree1)}")
    print(f"  Simple: {solution.countNodesSimple(tree1)}")
    print(f"  Binary Search: {solution.countNodesBinarySearch(tree1)}")
    print(f"  Expected: 6")
    print()
    
    # Test case 2 - Perfect tree
    tree2 = build_complete_tree2()
    print("Test 2 - Perfect tree (7 nodes):")
    print(f"  Optimal: {solution.countNodes(tree2)}")
    print(f"  Expected: 7")
    print()
    
    # Test case 3 - Single node
    tree3 = build_single_node()
    print("Test 3 - Single node:")
    print(f"  Optimal: {solution.countNodes(tree3)}")
    print(f"  Expected: 1")
    print()
    
    # Test case 4 - Larger complete tree
    tree4 = build_complete_tree3()
    print("Test 4 - Larger complete tree (10 nodes):")
    print(f"  Optimal: {solution.countNodes(tree4)}")
    print(f"  Binary Search: {solution.countNodesBinarySearch(tree4)}")
    print(f"  Expected: 10")
    print()
    
    # Edge case - Empty tree
    print("Test 5 - Empty tree:")
    print(f"  Result: {solution.countNodes(None)}")
    print(f"  Expected: 0")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Complete binary tree: all levels filled except possibly last, which fills left-to-right
   - Could have up to 2^h - 1 nodes (perfect) or fewer
   - Need to count ALL nodes efficiently

2. NAIVE APPROACH (mention but don't implement as primary):
   - Simple DFS/BFS traversal: O(n) time
   - "While this works, I can do better by using the complete tree property"

3. OPTIMAL APPROACH - KEY INSIGHTS:

   INSIGHT 1: Complete Tree Property
   - Left subtree or right subtree is always perfect
   - If left height == right height → left subtree is perfect
   - If left height != right height → right subtree is perfect

   INSIGHT 2: Perfect Tree Formula
   - Perfect binary tree with height h has exactly 2^h - 1 nodes
   - Can count perfect subtrees in O(1) using this formula

   INSIGHT 3: Logarithmic Recursion
   - At each level, one subtree is perfect (count with formula)
   - Recursively count the other subtree
   - Only recurse on one side → O(log n) levels
   - Height computation takes O(log n) → Total O(log²n)

4. SOLUTION WALKTHROUGH:
   - Compute left height (going only left)
   - Compute right height (going only right)
   - If equal: left subtree perfect, use formula + recurse right
   - If not equal: right subtree perfect, use formula + recurse left

5. WHY THIS IS BRILLIANT:
   - Reduces O(n) problem to O(log²n) by exploiting structure
   - Perfect subtrees can be counted instantly with formula
   - Only need to "explore" the incomplete subtree

6. IMPLEMENTATION DETAILS:
   - Use bit shifting for 2^h: (1 << h)
   - Height calculation: keep going left/right until null
   - Recursive structure matches the tree property

7. COMPLEXITY ANALYSIS:
   - Time: O(log²n) - O(log n) recursive calls, each with O(log n) height computation
   - Space: O(log n) - recursion depth
   - Much better than naive O(n) approach!

8. ALTERNATIVE APPROACHES:
   - Binary search on last level (also O(log²n))
   - Simple traversal (O(n) but easier to code)

9. EDGE CASES:
   - Empty tree → 0
   - Single node → 1  
   - Perfect tree → formula gives exact answer immediately
   - Complete but not perfect → algorithm handles correctly

10. INTERVIEW PRESENTATION:
    - Start with: "I can use the complete binary tree property to do better than O(n)"
    - Explain the perfect subtree insight
    - Code the optimal solution
    - Walk through example showing perfect subtree identification
    - Emphasize the O(log²n) complexity achievement

11. FOLLOW-UP QUESTIONS:
    - "What if it's not complete?" → Need O(n) traversal
    - "Can you do better than O(log²n)?" → This is optimal for this problem
    - "Explain why one subtree is always perfect" → Complete tree definition
    - "What's the space complexity?" → O(log n) due to recursion

12. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests if you can exploit problem constraints
    - Shows understanding of tree properties
    - Demonstrates optimization thinking
    - Clear distinction between naive and optimal solutions

13. RED FLAGS TO AVOID:
    - Just implementing O(n) traversal without mentioning optimization
    - Not explaining WHY the complete tree property helps
    - Incorrect complexity analysis
    - Not handling edge cases properly
"""
