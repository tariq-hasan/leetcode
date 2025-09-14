# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def inorderTraversal(self, root):
        """
        RECURSIVE SOLUTION (MOST INTUITIVE FOR INTERVIEWS)
        
        Inorder traversal: Left -> Root -> Right
        - Recursively traverse left subtree
        - Visit root node (add to result)
        - Recursively traverse right subtree
        
        This is the natural recursive definition of inorder traversal.
        
        Time: O(n) - visit each node exactly once
        Space: O(h) where h is height of tree (recursion stack)
               O(log n) for balanced tree, O(n) for skewed tree
        """
        result = []
        
        def helper(node):
            if not node:
                return
            
            # Left -> Root -> Right
            helper(node.left)   # Traverse left subtree
            result.append(node.val)  # Visit root
            helper(node.right)  # Traverse right subtree
        
        helper(root)
        return result

class SolutionIterative:
    def inorderTraversal(self, root):
        """
        ITERATIVE SOLUTION WITH STACK (OPTIMAL SPACE IN SOME CASES)
        
        Use explicit stack to simulate recursion:
        1. Go as far left as possible, pushing nodes onto stack
        2. When can't go left, pop node, add to result
        3. Move to right subtree and repeat
        
        Key insight: Stack holds the "path" to current node
        
        Time: O(n) - visit each node exactly once
        Space: O(h) - stack can contain at most h nodes
        """
        result = []
        stack = []
        current = root
        
        while stack or current:
            # Go as far left as possible
            while current:
                stack.append(current)
                current = current.left
            
            # Current is None, so we backtrack
            current = stack.pop()
            result.append(current.val)  # Visit node
            
            # Move to right subtree
            current = current.right
        
        return result

class SolutionMorris:
    def inorderTraversal(self, root):
        """
        MORRIS TRAVERSAL (ADVANCED - O(1) SPACE)
        
        Uses threading to eliminate recursion/stack:
        - Create temporary links to enable traversal
        - Restore original tree structure
        - Achieves O(1) space complexity
        
        Algorithm:
        1. If no left child, visit node and go right
        2. If left child exists, find inorder predecessor
        3. If predecessor's right is null, create thread and go left
        4. If thread exists, remove it, visit node, go right
        
        Time: O(n) - each edge traversed at most 3 times
        Space: O(1) - no recursion or stack needed
        """
        result = []
        current = root
        
        while current:
            if not current.left:
                # No left subtree, visit current and go right
                result.append(current.val)
                current = current.right
            else:
                # Find inorder predecessor (rightmost node in left subtree)
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right
                
                if not predecessor.right:
                    # Create thread (temporary link)
                    predecessor.right = current
                    current = current.left
                else:
                    # Thread exists, remove it and visit current
                    predecessor.right = None
                    result.append(current.val)
                    current = current.right
        
        return result

class SolutionUnified:
    """
    UNIFIED SOLUTION SHOWING ALL THREE APPROACHES
    Useful for demonstrating understanding of different techniques
    """
    
    def inorderRecursive(self, root):
        """Recursive approach"""
        result = []
        
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.val)
                inorder(node.right)
        
        inorder(root)
        return result
    
    def inorderIterative(self, root):
        """Iterative approach with stack"""
        result = []
        stack = []
        current = root
        
        while stack or current:
            # Push all left nodes
            while current:
                stack.append(current)
                current = current.left
            
            # Pop and visit
            current = stack.pop()
            result.append(current.val)
            current = current.right
        
        return result
    
    def inorderMorris(self, root):
        """Morris traversal - O(1) space"""
        result = []
        current = root
        
        while current:
            if not current.left:
                result.append(current.val)
                current = current.right
            else:
                # Find predecessor
                pred = current.left
                while pred.right and pred.right != current:
                    pred = pred.right
                
                if not pred.right:
                    # Make thread
                    pred.right = current
                    current = current.left
                else:
                    # Remove thread
                    pred.right = None
                    result.append(current.val)
                    current = current.right
        
        return result

# Helper function for testing - creates sample trees
def create_sample_trees():
    """Create various sample trees for testing"""
    
    # Tree 1: [1,null,2,3]
    #   1
    #    \
    #     2
    #    /
    #   3
    tree1 = TreeNode(1)
    tree1.right = TreeNode(2)
    tree1.right.left = TreeNode(3)
    
    # Tree 2: Empty tree
    tree2 = None
    
    # Tree 3: Single node
    tree3 = TreeNode(1)
    
    # Tree 4: Balanced tree [4,2,6,1,3,5,7]
    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    tree4 = TreeNode(4)
    tree4.left = TreeNode(2)
    tree4.right = TreeNode(6)
    tree4.left.left = TreeNode(1)
    tree4.left.right = TreeNode(3)
    tree4.right.left = TreeNode(5)
    tree4.right.right = TreeNode(7)
    
    # Tree 5: Left skewed tree
    tree5 = TreeNode(3)
    tree5.left = TreeNode(2)
    tree5.left.left = TreeNode(1)
    
    return [
        ("Tree 1: [1,null,2,3]", tree1),
        ("Tree 2: Empty", tree2),
        ("Tree 3: Single node", tree3),
        ("Tree 4: Balanced", tree4),
        ("Tree 5: Left skewed", tree5)
    ]

# Test all solutions
if __name__ == "__main__":
    solution = Solution()
    iterative_solution = SolutionIterative()
    morris_solution = SolutionMorris()
    unified_solution = SolutionUnified()
    
    test_trees = create_sample_trees()
    
    for tree_name, tree_root in test_trees:
        print(f"=== {tree_name} ===")
        
        # Test recursive solution
        result_rec = solution.inorderTraversal(tree_root)
        print(f"Recursive:  {result_rec}")
        
        # Test iterative solution
        result_iter = iterative_solution.inorderTraversal(tree_root)
        print(f"Iterative:  {result_iter}")
        
        # Test Morris traversal
        result_morris = morris_solution.inorderTraversal(tree_root)
        print(f"Morris:     {result_morris}")
        
        # Verify all solutions give same result
        if result_rec == result_iter == result_morris:
            print("✅ All solutions match!")
        else:
            print("❌ Solutions don't match!")
        
        print()

"""
INTERVIEW TALKING POINTS:

1. TRAVERSAL UNDERSTANDING:
   "Inorder traversal visits nodes in Left -> Root -> Right order"
   "For BST, this gives nodes in sorted ascending order"
   "One of three fundamental tree traversals (in, pre, post)"

2. RECURSIVE APPROACH (MOST COMMON):
   - Natural and intuitive implementation
   - Follows the definition directly
   - Easy to understand and code
   - Space: O(h) due to call stack

3. ITERATIVE APPROACH (SHOWS ADVANCED UNDERSTANDING):
   - Uses explicit stack to simulate recursion
   - Same time/space complexity as recursive
   - Shows deeper understanding of how recursion works
   - Useful when recursion depth might be an issue

4. MORRIS TRAVERSAL (ADVANCED TECHNIQUE):
   - Achieves O(1) space complexity
   - Uses threading technique
   - More complex but shows algorithmic sophistication
   - Temporarily modifies tree structure (then restores)

5. WHEN TO USE EACH APPROACH:
   - Recursive: Default choice, most readable
   - Iterative: When recursion depth is a concern
   - Morris: When space is extremely limited

6. COMPLEXITY ANALYSIS:
   All approaches: O(n) time
   - Recursive: O(h) space (call stack)
   - Iterative: O(h) space (explicit stack)
   - Morris: O(1) space (threading technique)

7. EDGE CASES TO CONSIDER:
   - Empty tree → return []
   - Single node → return [node.val]
   - Left/right skewed trees → test stack depth
   - Balanced tree → optimal case

8. COMMON MISTAKES:
   - Forgetting base case in recursion
   - Wrong order of operations (should be L->Root->R)
   - Stack management errors in iterative approach
   - Not restoring tree in Morris (though not required here)

9. FOLLOW-UP QUESTIONS:
   - "Implement preorder/postorder?" → Change order of operations
   - "What if tree has parent pointers?" → Can simplify traversal
   - "Iterative version?" → Shows deeper understanding
   - "O(1) space solution?" → Morris traversal

10. REAL-WORLD APPLICATIONS:
    - Binary Search Tree validation
    - Expression tree evaluation
    - Serialization/deserialization
    - Tree structure analysis

11. INTERVIEW STRATEGY:
    - Start with recursive (most natural)
    - Mention iterative alternative
    - If asked for O(1) space, explain Morris
    - Always test with edge cases
    - Explain the Left->Root->Right pattern clearly
"""
