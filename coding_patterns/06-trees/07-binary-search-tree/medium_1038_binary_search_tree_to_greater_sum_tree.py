# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def bstToGst(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Optimal Solution - Reverse Inorder Traversal (Single Pass)
        
        Key insight: Use reverse inorder (right-root-left) to process nodes
        from largest to smallest. Maintain running sum of all larger values.
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        self.running_sum = 0
        
        def reverse_inorder(node):
            if not node:
                return
            
            # Process right subtree first (larger values)
            reverse_inorder(node.right)
            
            # Update current node with running sum
            self.running_sum += node.val
            node.val = self.running_sum
            
            # Process left subtree (smaller values)
            reverse_inorder(node.left)
        
        reverse_inorder(root)
        return root

    def bstToGstIterative(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Iterative Solution using Stack
        
        Same logic as recursive but uses explicit stack
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return None
        
        stack = []
        current = root
        running_sum = 0
        
        while stack or current:
            # Go to rightmost node (largest values first)
            while current:
                stack.append(current)
                current = current.right
            
            # Process current node
            current = stack.pop()
            running_sum += current.val
            current.val = running_sum
            
            # Move to left subtree
            current = current.left
        
        return root

    def bstToGstTwoPass(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Two-Pass Solution (Less Optimal but Intuitive)
        
        First pass: collect all values in sorted order
        Second pass: update each node with sum of larger values
        Time Complexity: O(n)
        Space Complexity: O(n) for storing values
        """
        # First pass: collect all values
        values = []
        
        def inorder_collect(node):
            if node:
                inorder_collect(node.left)
                values.append(node.val)
                inorder_collect(node.right)
        
        inorder_collect(root)
        
        # Compute suffix sums (sum of all values >= current)
        suffix_sums = {}
        total = sum(values)
        current_sum = 0
        
        for val in values:
            suffix_sums[val] = total - current_sum
            current_sum += val
        
        # Second pass: update nodes
        def update_nodes(node):
            if node:
                node.val = suffix_sums[node.val]
                update_nodes(node.left)
                update_nodes(node.right)
        
        update_nodes(root)
        return root

    def bstToGstMorris(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Morris Traversal Solution (O(1) Space - Advanced)
        
        Uses threading technique for O(1) space reverse inorder traversal
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        running_sum = 0
        current = root
        
        while current:
            if not current.right:
                # Process current node
                running_sum += current.val
                current.val = running_sum
                current = current.left
            else:
                # Find inorder predecessor in right subtree
                predecessor = current.right
                while predecessor.left and predecessor.left != current:
                    predecessor = predecessor.left
                
                if not predecessor.left:
                    # Create thread
                    predecessor.left = current
                    current = current.right
                else:
                    # Remove thread and process current
                    predecessor.left = None
                    running_sum += current.val
                    current.val = running_sum
                    current = current.left
        
        return root

    def bstToGstExplicitSum(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Explicit Sum Calculation (Educational Version)
        
        More explicit about what sum is being calculated at each node
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def calculate_greater_sum(node, accumulated_sum):
            """
            Returns the sum of all nodes in this subtree
            Updates node values with sum of all greater values
            """
            if not node:
                return 0
            
            # Get sum from right subtree (all values > current)
            right_sum = calculate_greater_sum(node.right, accumulated_sum)
            
            # Update current node: accumulated_sum + right_subtree_sum
            original_val = node.val
            node.val = accumulated_sum + right_sum + original_val
            
            # Process left subtree with updated accumulated sum
            left_sum = calculate_greater_sum(node.left, node.val)
            
            # Return total sum of this subtree
            return left_sum + right_sum + original_val
        
        calculate_greater_sum(root, 0)
        return root

    def bstToGstWithPath(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Solution with Path Tracking (For Debugging)
        
        Tracks the path during traversal for educational purposes
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.running_sum = 0
        
        def reverse_inorder_with_path(node, path):
            if not node:
                return
            
            # Add current node to path
            path.append(node.val)
            
            # Process right subtree
            reverse_inorder_with_path(node.right, path)
            
            # Process current node
            self.running_sum += node.val
            original_val = node.val
            node.val = self.running_sum
            
            # Debug output (remove in actual solution)
            # print(f"Node {original_val} -> {node.val}, Path: {path}")
            
            # Process left subtree
            reverse_inorder_with_path(node.left, path)
            
            # Remove current node from path
            path.pop()
        
        reverse_inorder_with_path(root, [])
        return root

# Test cases and utility functions
def build_test_bst1():
    """
    Build BST:     4
                  / \
                 1   6
                  \ / \
                  2 5  7
                   \    \
                    3    8
    
    Expected GST: Each node = original + sum of all larger values
    """
    root = TreeNode(4)
    root.left = TreeNode(1)
    root.right = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    root.left.right.right = TreeNode(3)
    root.right.right.right = TreeNode(8)
    return root

def build_test_bst2():
    """
    Simple BST:   0
                   \
                    1
    
    Expected: [1, 1] (0 becomes 0+1=1, 1 stays 1)
    """
    root = TreeNode(0)
    root.right = TreeNode(1)
    return root

def build_test_bst3():
    """
    Balanced BST:    3
                    / \
                   2   4
                  /     \
                 1       5
    
    Values: [1,2,3,4,5]
    Expected: [15,14,12,9,5]
    """
    root = TreeNode(3)
    root.left = TreeNode(2)
    root.right = TreeNode(4)
    root.left.left = TreeNode(1)
    root.right.right = TreeNode(5)
    return root

def build_single_node():
    """Single node BST"""
    return TreeNode(1)

def inorder_traversal(root):
    """Get inorder traversal to verify transformation"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def reverse_inorder_traversal(root):
    """Get reverse inorder traversal"""
    result = []
    def reverse_inorder(node):
        if node:
            reverse_inorder(node.right)
            result.append(node.val)
            reverse_inorder(node.left)
    reverse_inorder(root)
    return result

def calculate_expected_gst(original_values):
    """Calculate what the GST values should be"""
    n = len(original_values)
    gst_values = []
    
    for i in range(n):
        # For each value, sum itself + all larger values
        current_sum = sum(val for val in original_values if val >= original_values[i])
        gst_values.append(current_sum)
    
    return gst_values

def print_tree_comparison(original_root, gst_root, level=0, prefix="Root: "):
    """Print both trees side by side for comparison"""
    if original_root or gst_root:
        orig_val = original_root.val if original_root else "None"
        gst_val = gst_root.val if gst_root else "None"
        print(" " * (level * 4) + prefix + f"{orig_val} -> {gst_val}")
        
        # Recurse on children
        if (original_root and (original_root.left or original_root.right)) or \
           (gst_root and (gst_root.left or gst_root.right)):
            
            orig_left = original_root.left if original_root else None
            orig_right = original_root.right if original_root else None
            gst_left = gst_root.left if gst_root else None  
            gst_right = gst_root.right if gst_root else None
            
            print_tree_comparison(orig_left, gst_left, level + 1, "L--- ")
            print_tree_comparison(orig_right, gst_right, level + 1, "R--- ")

def test_transformation(tree_builder, test_name):
    """Test BST to GST transformation"""
    solution = Solution()
    
    print(f"\n{test_name}:")
    
    # Get original values
    original = tree_builder()
    original_inorder = inorder_traversal(original)
    print(f"Original BST inorder: {original_inorder}")
    
    # Calculate expected GST values
    expected_gst = calculate_expected_gst(original_inorder)
    print(f"Expected GST values: {expected_gst}")
    
    # Test different methods
    tree1 = tree_builder()  # Recursive
    tree2 = tree_builder()  # Iterative
    tree3 = tree_builder()  # Two-pass
    
    result1 = solution.bstToGst(tree1)
    result2 = solution.bstToGstIterative(tree2)  
    result3 = solution.bstToGstTwoPass(tree3)
    
    result1_inorder = inorder_traversal(result1)
    result2_inorder = inorder_traversal(result2)
    result3_inorder = inorder_traversal(result3)
    
    print(f"Recursive result:  {result1_inorder}")
    print(f"Iterative result:  {result2_inorder}")
    print(f"Two-pass result:   {result3_inorder}")
    
    # Verify correctness
    all_correct = (result1_inorder == expected_gst and 
                   result2_inorder == expected_gst and
                   result3_inorder == expected_gst)
    print(f"All methods correct: {all_correct}")
    
    # Show tree transformation
    original_copy = tree_builder()
    print(f"\nTree transformation visualization:")
    print_tree_comparison(original_copy, result1)

def demonstrate_reverse_inorder():
    """Demonstrate why reverse inorder works"""
    print("\nDEMONSTRATING REVERSE INORDER APPROACH:")
    
    tree = build_test_bst3()
    original_inorder = inorder_traversal(tree)
    original_reverse = reverse_inorder_traversal(tree)
    
    print(f"Original inorder:         {original_inorder}")
    print(f"Original reverse inorder: {original_reverse}")
    
    print("\nProcessing in reverse inorder:")
    running_sum = 0
    for i, val in enumerate(original_reverse):
        running_sum += val
        print(f"Step {i+1}: Process {val}, running_sum = {running_sum}")
    
    print("\nThis gives us the greater sum for each node!")

def comprehensive_test():
    """Run comprehensive tests"""
    
    # Test different tree structures
    test_transformation(build_test_bst1, "Test 1: Complex BST")
    test_transformation(build_test_bst2, "Test 2: Simple BST [0,null,1]")  
    test_transformation(build_test_bst3, "Test 3: Balanced BST")
    test_transformation(build_single_node, "Test 4: Single node")
    
    # Demonstrate the algorithm
    demonstrate_reverse_inorder()

if __name__ == "__main__":
    comprehensive_test()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Transform BST where each node becomes sum of itself + all larger values
   - Must maintain tree structure, only values change
   - BST property is lost after transformation (becomes Greater Sum Tree)
   - Example: node with value 4 becomes 4 + sum(all values ≥ 4)

2. KEY INSIGHT - REVERSE INORDER TRAVERSAL:
   - Regular inorder: left-root-right (ascending order)
   - Reverse inorder: right-root-left (descending order)  
   - Process nodes from largest to smallest
   - Maintain running sum of all processed (larger) values

3. ALGORITHM WALKTHROUGH:
   - Use reverse inorder to visit nodes largest to smallest
   - Maintain running_sum of all nodes processed so far
   - For each node: add its value to running_sum, update node with running_sum
   - This automatically gives each node the sum of itself + all larger values

4. WHY REVERSE INORDER WORKS:
   - When we process a node, we've already processed all larger nodes
   - running_sum contains sum of all nodes with values > current node
   - Adding current node value gives us the desired greater sum

5. SOLUTION APPROACHES:

   APPROACH 1 - Reverse Inorder Recursive (RECOMMENDED):
   - Most elegant and intuitive
   - Single pass through tree
   - O(n) time, O(h) space

   APPROACH 2 - Reverse Inorder Iterative:
   - Same logic but with explicit stack
   - Good alternative to show iterative thinking

   APPROACH 3 - Two-Pass Solution:
   - First pass: collect all values
   - Second pass: calculate and update sums
   - Less optimal but more obvious approach

6. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node exactly once
   - Space: O(h) - recursion stack depth
   - Optimal for this problem

7. EDGE CASES:
   - Empty tree → return None
   - Single node → value stays same (sum of itself)
   - All nodes in right chain → linear processing
   - Balanced tree → logarithmic depth

8. INTERVIEW PRESENTATION:
   - Start with problem clarification: "each node becomes sum of itself + larger values"
   - Key insight: "I'll use reverse inorder to process largest values first"
   - Explain running sum technique
   - Code the recursive solution
   - Walk through example showing the traversal order

9. FOLLOW-UP QUESTIONS:
   - "Can you do it iteratively?" → Show stack-based solution
   - "What about O(1) space?" → Morris traversal (advanced)
   - "Two-pass approach?" → Show collect-then-update method
   - "What's the time complexity?" → O(n) single pass

10. WHY THIS PROBLEM IS CLEVER:
    - Tests understanding of tree traversal variations
    - Requires recognizing reverse inorder pattern
    - Shows how traversal order affects algorithm efficiency
    - Demonstrates running sum technique on trees

11. COMMON MISTAKES:
    - Using regular inorder instead of reverse inorder
    - Not maintaining running sum correctly
    - Trying to calculate sums from scratch for each node
    - Forgetting that tree structure is preserved

12. OPTIMIZATION INSIGHTS:
    - Single pass is optimal (can't do better than O(n))
    - Reverse inorder is key insight for efficiency
    - Running sum avoids recalculation
    - Recursive approach is cleanest

13. RELATED PROBLEMS:
    - Convert BST to sorted doubly linked list
    - Sum of all nodes greater than X
    - Binary tree right side view
    - Inorder traversal variations

14. KEY INSIGHT TO ARTICULATE:
    "The brilliant insight is using reverse inorder traversal (right-root-left)
    to process nodes from largest to smallest. By maintaining a running sum 
    of all processed nodes, each node automatically gets updated with the sum 
    of itself plus all larger values. This eliminates the need for multiple 
    passes or complex calculations."

15. PATTERN RECOGNITION:
    - This demonstrates the "accumulator during traversal" pattern
    - Shows how traversal order affects algorithm efficiency
    - Example of transforming tree values while preserving structure
    - Foundation for more complex tree transformation problems

16. INTERVIEW TIPS:
    - Emphasize the reverse inorder insight early
    - Draw tree showing traversal order
    - Show running sum evolution step by step
    - Mention that regular inorder would require different approach
    - Discuss why single pass is optimal
"""
