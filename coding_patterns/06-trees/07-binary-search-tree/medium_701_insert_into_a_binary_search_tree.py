# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Optimal Recursive Solution (Most Common and Clean)
        
        Key insight: BST insertion always happens at leaf level.
        Use BST property to navigate to correct position, then insert.
        
        Time Complexity: O(h) where h is height of tree
        Space Complexity: O(h) due to recursion stack
        """
        # Base case: found insertion point (empty spot)
        if not root:
            return TreeNode(val)
        
        # Navigate based on BST property
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:  # val > root.val (problem guarantees no duplicates)
            root.right = self.insertIntoBST(root.right, val)
        
        return root

    def insertIntoBSTIterative(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Iterative Solution (Space Optimal)
        
        Uses explicit parent tracking to avoid recursion
        Time Complexity: O(h)
        Space Complexity: O(1)
        """
        # Handle empty tree
        if not root:
            return TreeNode(val)
        
        current = root
        
        while True:
            if val < current.val:
                if current.left is None:
                    current.left = TreeNode(val)
                    break
                current = current.left
            else:  # val > current.val
                if current.right is None:
                    current.right = TreeNode(val)
                    break
                current = current.right
        
        return root

    def insertIntoBSTIterativeWithParent(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Alternative Iterative with Explicit Parent Tracking
        
        More explicit parent management for clarity
        Time Complexity: O(h)
        Space Complexity: O(1)
        """
        if not root:
            return TreeNode(val)
        
        parent = None
        current = root
        
        # Find the insertion point
        while current:
            parent = current
            if val < current.val:
                current = current.left
            else:
                current = current.right
        
        # Insert the new node
        new_node = TreeNode(val)
        if val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
        
        return root

    def insertIntoBSTBalanced(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Insertion with Basic Balancing Consideration
        
        Standard insertion but shows awareness of balancing issues
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        def insert(node, value):
            if not node:
                return TreeNode(value)
            
            if value < node.val:
                node.left = insert(node.left, value)
            else:
                node.right = insert(node.right, value)
            
            # In a self-balancing BST, we would rebalance here
            # For standard BST, just return the node
            return node
        
        return insert(root, val)

    def insertIntoBSTWithHeight(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Insertion with Height Tracking (Educational Version)
        
        Shows how to track tree height during insertion
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        def insert_with_info(node, value):
            """Returns (new_node, height_increased)"""
            if not node:
                return TreeNode(value), True
            
            height_increased = False
            
            if value < node.val:
                node.left, left_increased = insert_with_info(node.left, value)
                # Height increases if left subtree grew and was previously shorter
                height_increased = left_increased
            else:
                node.right, right_increased = insert_with_info(node.right, value)
                # Height increases if right subtree grew and was previously shorter
                height_increased = right_increased
            
            return node, height_increased
        
        result, _ = insert_with_info(root, val)
        return result

    def insertIntoBSTMultiple(self, root: Optional[TreeNode], values: list) -> Optional[TreeNode]:
        """
        Insert Multiple Values (Extension for Bulk Operations)
        
        Efficiently insert multiple values maintaining BST property
        Time Complexity: O(n * h) where n is number of values
        Space Complexity: O(h) for each insertion
        """
        for val in values:
            root = self.insertIntoBST(root, val)
        return root

    def insertIntoBSTWithValidation(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Insertion with Validation (Production-Ready Version)
        
        Includes validation and error handling
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        def is_valid_insertion(node, value, min_val, max_val):
            """Check if insertion would maintain BST property"""
            if not node:
                return min_val < value < max_val
            
            if value < node.val:
                return is_valid_insertion(node.left, value, min_val, node.val)
            elif value > node.val:
                return is_valid_insertion(node.right, value, node.val, max_val)
            else:
                return False  # Duplicate value
        
        def insert(node, value):
            if not node:
                return TreeNode(value)
            
            if value < node.val:
                node.left = insert(node.left, value)
            elif value > node.val:
                node.right = insert(node.right, value)
            # Note: ignoring duplicates in this version
            
            return node
        
        # Validate before insertion (in practice, problem guarantees validity)
        if root and not is_valid_insertion(root, val, float('-inf'), float('inf')):
            raise ValueError(f"Invalid insertion: {val}")
        
        return insert(root, val)

# Test cases and utility functions
def build_test_bst():
    """
    Build initial BST:    4
                        /   \
                       2     7
                      / \   /
                     1   3 6
    """
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(6)
    return root

def build_empty_tree():
    """Empty tree for testing"""
    return None

def build_single_node():
    """Single node tree"""
    return TreeNode(5)

def build_linear_bst():
    """
    Linear BST:  1
                  \
                   3
                    \
                     5
                      \
                       7
    """
    root = TreeNode(1)
    root.right = TreeNode(3)
    root.right.right = TreeNode(5)
    root.right.right.right = TreeNode(7)
    return root

def inorder_traversal(root):
    """Helper to verify BST property"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def tree_height(root):
    """Calculate tree height"""
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))

def print_tree_structure(root, level=0, prefix="Root: "):
    """Visualize tree structure"""
    if root:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            if root.left:
                print_tree_structure(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_structure(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

def test_insertion(tree_builder, insert_val, test_name):
    """Test insertion on a tree"""
    solution = Solution()
    
    print(f"\n{test_name} - Inserting {insert_val}:")
    
    # Original tree
    original = tree_builder()
    original_inorder = inorder_traversal(original)
    original_height = tree_height(original)
    print(f"Original inorder: {original_inorder}")
    print(f"Original height: {original_height}")
    
    # Insert with different methods
    tree1 = tree_builder()  # For recursive
    tree2 = tree_builder()  # For iterative
    
    result1 = solution.insertIntoBST(tree1, insert_val)
    result2 = solution.insertIntoBSTIterative(tree2, insert_val)
    
    result1_inorder = inorder_traversal(result1)
    result2_inorder = inorder_traversal(result2)
    new_height = tree_height(result1)
    
    print(f"After insertion (recursive): {result1_inorder}")
    print(f"After insertion (iterative): {result2_inorder}")
    print(f"New height: {new_height}")
    print(f"Both methods agree: {result1_inorder == result2_inorder}")
    
    # Verify BST property
    is_sorted = result1_inorder == sorted(result1_inorder)
    print(f"BST property maintained: {is_sorted}")
    
    # Show final structure
    print("Final tree structure (recursive method):")
    print_tree_structure(result1)

def performance_comparison():
    """Compare recursive vs iterative performance"""
    solution = Solution()
    
    # Build test tree
    root = build_test_bst()
    
    print("\nPERFORMANCE COMPARISON:")
    print("Recursive approach:")
    print("  - Time: O(h), Space: O(h)")
    print("  - Clean and intuitive")
    print("  - Natural BST navigation")
    
    print("\nIterative approach:")  
    print("  - Time: O(h), Space: O(1)")
    print("  - More space efficient")
    print("  - Explicit navigation logic")
    
    # Test both methods
    tree1 = build_test_bst()
    tree2 = build_test_bst()
    
    result1 = solution.insertIntoBST(tree1, 5)
    result2 = solution.insertIntoBSTIterative(tree2, 5)
    
    print(f"\nBoth methods produce same result: {inorder_traversal(result1) == inorder_traversal(result2)}")

def comprehensive_test():
    """Run comprehensive tests"""
    
    # Test Case 1: Insert into balanced tree
    test_insertion(build_test_bst, 5, "Test 1: Insert into balanced BST")
    
    # Test Case 2: Insert into empty tree
    test_insertion(build_empty_tree, 10, "Test 2: Insert into empty tree")
    
    # Test Case 3: Insert into single node
    test_insertion(build_single_node, 3, "Test 3: Insert into single node")
    
    # Test Case 4: Insert into linear tree (worst case)
    test_insertion(build_linear_bst, 4, "Test 4: Insert into linear BST")
    
    # Test Case 5: Insert at leftmost position
    test_insertion(build_test_bst, 0, "Test 5: Insert leftmost")
    
    # Test Case 6: Insert at rightmost position
    test_insertion(build_test_bst, 8, "Test 6: Insert rightmost")

def bulk_insertion_test():
    """Test multiple insertions"""
    solution = Solution()
    
    print("\nBULK INSERTION TEST:")
    
    # Start with empty tree
    root = None
    values = [5, 3, 7, 2, 4, 6, 8, 1, 9]
    
    print(f"Inserting values: {values}")
    
    for val in values:
        root = solution.insertIntoBST(root, val)
        current_inorder = inorder_traversal(root)
        print(f"After inserting {val}: {current_inorder}")
    
    final_height = tree_height(root)
    print(f"Final height: {final_height}")
    print("Final tree structure:")
    print_tree_structure(root)

if __name__ == "__main__":
    comprehensive_test()
    performance_comparison()
    bulk_insertion_test()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Insert value into BST while maintaining BST property
   - BST property: left < root < right for all nodes
   - No duplicates guaranteed by problem statement
   - Return root of modified tree

2. KEY INSIGHT - LEAF INSERTION:
   - BST insertion always happens at leaf level
   - Use BST property to navigate to correct empty position
   - Create new node and attach to appropriate parent
   - Much simpler than deletion (no complex cases)

3. ALGORITHM STRATEGY:
   - Start from root
   - Compare value with current node
   - Go left if smaller, right if larger
   - When reach null position, insert new node
   - Recursively rebuild path back to root

4. TWO MAIN APPROACHES:

   APPROACH 1 - Recursive (RECOMMENDED):
   - Natural BST navigation pattern
   - Clean and intuitive code
   - Automatically rebuilds tree structure
   - O(h) time, O(h) space

   APPROACH 2 - Iterative:
   - Explicit parent tracking
   - More space efficient: O(1) space
   - Slightly more complex logic
   - O(h) time, O(1) space

5. WHY RECURSIVE IS PREFERRED:
   - Matches natural tree structure
   - Cleaner, more readable code
   - Less error-prone than parent tracking
   - Standard approach for tree problems

6. COMPLEXITY ANALYSIS:
   - Time: O(h) where h is height of tree
   - Best case: O(log n) for balanced BST
   - Worst case: O(n) for skewed BST
   - Space: O(h) recursive, O(1) iterative

7. EDGE CASES:
   - Empty tree (create root)
   - Single node tree
   - Insert at leftmost position
   - Insert at rightmost position
   - Skewed tree (linear chain)

8. INTERVIEW PRESENTATION:
   - Explain BST property and leaf insertion
   - Show recursive solution first
   - Walk through example with tree diagram
   - Mention iterative alternative for space optimization
   - Discuss complexity trade-offs

9. FOLLOW-UP QUESTIONS:
   - "Can you do it iteratively?" → Show iterative version
   - "What about duplicates?" → Explain problem assumes no duplicates
   - "How to keep tree balanced?" → Mention AVL/Red-Black trees
   - "Bulk insertion optimization?" → Discuss sorted array to BST

10. WHY THIS PROBLEM IS FUNDAMENTAL:
    - Basic BST operation (along with search and delete)
    - Foundation for more complex tree operations
    - Tests understanding of recursive tree navigation
    - Building block for BST construction

11. COMMON MISTAKES:
    - Trying to insert at non-leaf positions
    - Incorrect BST property application
    - Not handling empty tree case
    - Forgetting to return modified root

12. OPTIMIZATION INSIGHTS:
    - Insertion is always O(h) - can't do better
    - Iterative saves space but adds complexity
    - For multiple insertions, consider building from sorted array
    - Self-balancing trees prevent worst-case O(n) height

13. PRODUCTION CONSIDERATIONS:
    - Duplicate handling strategy
    - Tree balancing after insertions
    - Memory management
    - Concurrent access patterns

14. RELATED PROBLEMS:
    - Search in BST
    - Delete from BST
    - Validate BST
    - Convert sorted array to BST
    - BST to sorted array

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is that BST insertion always happens at the leaf level. 
    I use the BST property to navigate to the correct empty position, then 
    create a new node there. The recursive approach naturally rebuilds the 
    tree structure as the call stack unwinds, maintaining all BST properties."

16. ALGORITHMIC PATTERN:
    - This demonstrates the "search and insert" pattern
    - Similar to binary search but with tree modification
    - Foundation for understanding more complex tree operations

17. INTERVIEW TIPS:
    - Start with recursive approach (cleaner to explain)
    - Draw tree diagram showing insertion process  
    - Explain why insertion is always at leaf level
    - Mention space optimization with iterative approach
    - Discuss balancing considerations for follow-up
"""
