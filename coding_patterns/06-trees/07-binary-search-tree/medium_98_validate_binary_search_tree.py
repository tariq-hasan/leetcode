# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        Optimal Solution - Range Validation (Most Efficient)
        
        Key insight: Each node must be within a valid range determined by ancestors.
        Pass down min/max bounds and validate at each node.
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        def validate(node, min_val, max_val):
            # Empty tree is valid BST
            if not node:
                return True
            
            # Current node must be within valid range
            if node.val <= min_val or node.val >= max_val:
                return False
            
            # Recursively validate subtrees with updated bounds
            # Left subtree: all values < current node value
            # Right subtree: all values > current node value
            return (validate(node.left, min_val, node.val) and 
                    validate(node.right, node.val, max_val))
        
        return validate(root, float('-inf'), float('inf'))

    def isValidBSTInorder(self, root: Optional[TreeNode]) -> bool:
        """
        Inorder Traversal Solution (Very Intuitive)
        
        Key insight: Inorder traversal of BST produces sorted sequence.
        If sequence is strictly increasing, tree is valid BST.
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.prev = float('-inf')
        
        def inorder(node):
            if not node:
                return True
            
            # Traverse left subtree
            if not inorder(node.left):
                return False
            
            # Check current node
            if node.val <= self.prev:
                return False
            self.prev = node.val
            
            # Traverse right subtree
            return inorder(node.right)
        
        return inorder(root)

    def isValidBSTInorderList(self, root: Optional[TreeNode]) -> bool:
        """
        Inorder to List Solution (Easy to Understand)
        
        Generate complete inorder traversal, then check if sorted
        Time Complexity: O(n)
        Space Complexity: O(n) for storing all values
        """
        def inorder(node, result):
            if node:
                inorder(node.left, result)
                result.append(node.val)
                inorder(node.right, result)
        
        values = []
        inorder(root, values)
        
        # Check if strictly increasing
        for i in range(1, len(values)):
            if values[i] <= values[i-1]:
                return False
        
        return True

    def isValidBSTIterative(self, root: Optional[TreeNode]) -> bool:
        """
        Iterative Inorder Solution (Non-Recursive)
        
        Uses stack to simulate inorder traversal
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return True
        
        stack = []
        current = root
        prev = float('-inf')
        
        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            
            # Check BST property
            if current.val <= prev:
                return False
            prev = current.val
            
            # Move to right subtree
            current = current.right
        
        return True

    def isValidBSTMorris(self, root: Optional[TreeNode]) -> bool:
        """
        Morris Traversal Solution (O(1) Space - Advanced)
        
        Uses threading to achieve O(1) space inorder traversal
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        current = root
        prev = float('-inf')
        
        while current:
            if not current.left:
                # Process current node
                if current.val <= prev:
                    return False
                prev = current.val
                current = current.right
            else:
                # Find inorder predecessor
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right
                
                if not predecessor.right:
                    # Create thread
                    predecessor.right = current
                    current = current.left
                else:
                    # Remove thread and process current
                    predecessor.right = None
                    if current.val <= prev:
                        return False
                    prev = current.val
                    current = current.right
        
        return True

    def isValidBSTRangeAlternative(self, root: Optional[TreeNode]) -> bool:
        """
        Alternative Range Implementation (More Explicit)
        
        Same logic as optimal solution but with clearer structure
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def is_valid_bst_helper(node, lower_bound, upper_bound):
            # Base case: empty tree is valid
            if not node:
                return True
            
            val = node.val
            
            # Check bounds
            if val <= lower_bound or val >= upper_bound:
                return False
            
            # Check left subtree: all values must be < val
            if not is_valid_bst_helper(node.left, lower_bound, val):
                return False
            
            # Check right subtree: all values must be > val
            if not is_valid_bst_helper(node.right, val, upper_bound):
                return False
            
            return True
        
        return is_valid_bst_helper(root, float('-inf'), float('inf'))

    def isValidBSTWithNulls(self, root: Optional[TreeNode]) -> bool:
        """
        Range Solution with Null Bounds (Handle Edge Cases)
        
        Uses None instead of infinity for cleaner edge case handling
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def validate(node, min_val, max_val):
            if not node:
                return True
            
            # Check lower bound
            if min_val is not None and node.val <= min_val:
                return False
            
            # Check upper bound
            if max_val is not None and node.val >= max_val:
                return False
            
            # Validate subtrees
            return (validate(node.left, min_val, node.val) and 
                    validate(node.right, node.val, max_val))
        
        return validate(root, None, None)

# Test cases and utility functions
def build_valid_bst1():
    """
    Valid BST:     2
                  / \
                 1   3
    
    Inorder: [1, 2, 3] - strictly increasing ✓
    """
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    return root

def build_invalid_bst1():
    """
    Invalid BST:   5
                  / \
                 1   4
                    / \
                   3   6
    
    Inorder: [1, 5, 3, 4, 6] - not strictly increasing ✗
    Node 3 is in right subtree but < 5
    """
    root = TreeNode(5)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(6)
    return root

def build_invalid_bst2():
    """
    Invalid BST:   10
                  /  \
                 5   15
                    /  \
                   6   20
    
    Node 6 is in right subtree but < 10
    """
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(20)
    return root

def build_edge_case_bst():
    """
    Edge case: duplicate values
    Tree:      2
              / \
             2   2
    
    Invalid because BST requires strict inequality
    """
    root = TreeNode(2)
    root.left = TreeNode(2)
    root.right = TreeNode(2)
    return root

def build_single_node():
    """Single node - always valid BST"""
    return TreeNode(1)

def build_complex_valid_bst():
    """
    Complex valid BST:    8
                        /   \
                       3    10
                      / \     \
                     1   6    14
                        / \   /
                       4   7 13
    """
    root = TreeNode(8)
    root.left = TreeNode(3)
    root.right = TreeNode(10)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(6)
    root.right.right = TreeNode(14)
    root.left.right.left = TreeNode(4)
    root.left.right.right = TreeNode(7)
    root.right.right.left = TreeNode(13)
    return root

def inorder_traversal(root):
    """Helper to see inorder sequence"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def test_solution(solution_method, tree, test_name, expected):
    """Test a solution method"""
    result = solution_method(tree)
    status = "✓" if result == expected else "✗"
    inorder_seq = inorder_traversal(tree)
    print(f"  {test_name}: {result} {status} (inorder: {inorder_seq})")

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Valid BST
    tree1 = build_valid_bst1()
    print("Test 1 - Valid BST [2,1,3]:")
    test_solution(solution.isValidBST, tree1, "Range validation", True)
    test_solution(solution.isValidBSTInorder, tree1, "Inorder traversal", True)
    test_solution(solution.isValidBSTIterative, tree1, "Iterative inorder", True)
    print()
    
    # Test case 2 - Invalid BST (classic case)
    tree2 = build_invalid_bst1()
    print("Test 2 - Invalid BST [5,1,4,null,null,3,6]:")
    test_solution(solution.isValidBST, tree2, "Range validation", False)
    test_solution(solution.isValidBSTInorder, tree2, "Inorder traversal", False)
    test_solution(solution.isValidBSTInorderList, tree2, "Inorder to list", False)
    print()
    
    # Test case 3 - Another invalid BST
    tree3 = build_invalid_bst2()
    print("Test 3 - Invalid BST [10,5,15,null,null,6,20]:")
    test_solution(solution.isValidBST, tree3, "Range validation", False)
    print()
    
    # Test case 4 - Duplicate values
    tree4 = build_edge_case_bst()
    print("Test 4 - Duplicate values [2,2,2]:")
    test_solution(solution.isValidBST, tree4, "Range validation", False)
    test_solution(solution.isValidBSTInorder, tree4, "Inorder traversal", False)
    print()
    
    # Test case 5 - Single node
    tree5 = build_single_node()
    print("Test 5 - Single node [1]:")
    test_solution(solution.isValidBST, tree5, "Range validation", True)
    print()
    
    # Test case 6 - Complex valid BST
    tree6 = build_complex_valid_bst()
    print("Test 6 - Complex valid BST:")
    test_solution(solution.isValidBST, tree6, "Range validation", True)
    test_solution(solution.isValidBSTMorris, tree6, "Morris traversal", True)
    print()
    
    # Test case 7 - Empty tree
    print("Test 7 - Empty tree:")
    test_solution(solution.isValidBST, None, "Range validation", True)

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - BST property: left < root < right for ALL nodes
   - This must hold for entire tree, not just immediate children
   - Values must be strictly less/greater (no duplicates)
   - Empty tree is considered valid BST

2. COMMON MISTAKE TO AVOID:
   - Only checking immediate children (local property)
   - Need to check global BST property
   - Example: [10,5,15,null,null,6,20] - node 6 violates BST even though 6<15

3. KEY INSIGHTS:

   INSIGHT 1: Range Validation
   - Each node has valid range based on ancestors
   - Pass down min/max bounds during traversal
   - Most efficient approach

   INSIGHT 2: Inorder Property
   - BST inorder traversal produces sorted sequence
   - If sequence is strictly increasing, tree is valid BST
   - Intuitive but requires tracking previous value

4. SOLUTION APPROACHES:

   APPROACH 1 - Range Validation (RECOMMENDED):
   - Pass min/max bounds down the tree
   - Each node must be within valid range
   - Most efficient: O(n) time, O(h) space

   APPROACH 2 - Inorder Traversal:
   - Generate inorder sequence, check if sorted
   - Intuitive and easy to understand
   - Can be optimized to avoid storing all values

   APPROACH 3 - Iterative Solutions:
   - Stack-based inorder traversal
   - Avoids recursion if required

5. SOLUTION CHOICE FOR INTERVIEW:
   - Lead with range validation (most efficient)
   - Mention inorder approach as alternative
   - Show understanding of BST properties

6. IMPLEMENTATION DETAILS - RANGE VALIDATION:
   - Start with range (-∞, +∞)
   - For left child: update upper bound to parent value
   - For right child: update lower bound to parent value
   - Check if current node violates bounds

7. COMPLEXITY ANALYSIS:
   - Time: O(n) - must visit each node once
   - Space: O(h) - recursion depth equals tree height
   - Optimal for this problem

8. EDGE CASES:
   - Empty tree → True (by definition)
   - Single node → True
   - Duplicate values → False (strict inequality required)
   - Integer overflow → use float('inf') for bounds

9. INTERVIEW PRESENTATION:
   - Clarify: "BST property must hold globally, not just locally"
   - Explain range validation insight
   - Code the recursive range solution
   - Walk through example showing bound propagation
   - Mention inorder alternative

10. FOLLOW-UP QUESTIONS:
    - "What if duplicates are allowed?" → Change strict inequality to ≤/≥
    - "What about very deep trees?" → Discuss iterative vs recursive
    - "O(1) space solution?" → Morris traversal (advanced)
    - "What if tree can be modified?" → Different problem (repair BST)

11. WHY RANGE VALIDATION IS OPTIMAL:
    - Single pass through tree
    - Early termination when invalid node found
    - Minimal space usage (just recursion stack)
    - Direct validation without auxiliary data structures

12. COMMON IMPLEMENTATION MISTAKES:
    - Using <= or >= instead of < and > for bounds checking
    - Not handling integer overflow with proper infinity values
    - Forgetting that empty tree is valid
    - Only checking immediate parent-child relationships

13. VARIATIONS TO BE AWARE OF:
    - Recover BST (fix swapped nodes)
    - Closest BST value
    - BST iterator
    - Convert sorted array to BST

14. OPTIMIZATION INSIGHTS:
    - Range validation is most efficient
    - Inorder can terminate early on first violation
    - Morris traversal achieves O(1) space but complex
    - Choose based on constraints and clarity needs

15. KEY INSIGHT TO ARTICULATE:
    "The crucial insight is that BST property must hold globally, not just 
    locally. Each node constrains the valid range for all nodes in its 
    subtrees. By passing down these range constraints during traversal, 
    I can validate the entire tree efficiently in a single pass."

16. PROBLEM PATTERN RECOGNITION:
    - Tree validation problems
    - Range constraint propagation
    - Property checking vs property maintaining
    - Global vs local invariants

17. REAL-WORLD APPLICATIONS:
    - Database index validation
    - Tree data structure integrity checks
    - Algorithm correctness verification
    - Data structure testing and debugging
"""
