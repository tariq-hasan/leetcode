# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder, inorder):
        """
        Construct Binary Tree from Preorder and Inorder Traversal
        
        Key Insights:
        - First element in preorder is always the root
        - In inorder, elements left of root are left subtree, right are right subtree
        - Recursively build left and right subtrees
        
        Time: O(n) - each node processed once
        Space: O(n) - hashmap + recursion stack
        """
        if not preorder or not inorder:
            return None
        
        # Create hashmap for O(1) inorder lookups
        inorder_map = {val: i for i, val in enumerate(inorder)}
        self.preorder_idx = 0
        
        def build(left, right):
            if left > right:
                return None
            
            # Root is current element in preorder
            root_val = preorder[self.preorder_idx]
            root = TreeNode(root_val)
            self.preorder_idx += 1
            
            # Find root position in inorder
            root_idx = inorder_map[root_val]
            
            # Build left subtree first (preorder: root -> left -> right)
            root.left = build(left, root_idx - 1)
            root.right = build(root_idx + 1, right)
            
            return root
        
        return build(0, len(inorder) - 1)

# Alternative Solution: Using array slicing (less efficient but more intuitive)
class SolutionSlicing:
    def buildTree(self, preorder, inorder):
        if not preorder or not inorder:
            return None
        
        # First element in preorder is root
        root = TreeNode(preorder[0])
        
        # Find root in inorder to split left/right subtrees
        mid = inorder.index(preorder[0])
        
        # Recursively build subtrees
        # Left subtree: preorder[1:mid+1], inorder[:mid]
        # Right subtree: preorder[mid+1:], inorder[mid+1:]
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        
        return root

# Test cases and utility functions
def inorder_traversal(root):
    """Helper to verify solution"""
    if not root:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)

def preorder_traversal(root):
    """Helper to verify solution"""
    if not root:
        return []
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)

# Test the solution
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1: [3,9,20,15,7]
    preorder1 = [3, 9, 20, 15, 7]
    inorder1 = [9, 3, 15, 20, 7]
    
    root1 = solution.buildTree(preorder1, inorder1)
    print(f"Test 1 - Preorder: {preorder_traversal(root1)}")  # [3, 9, 20, 15, 7]
    print(f"Test 1 - Inorder: {inorder_traversal(root1)}")    # [9, 3, 15, 20, 7]
    
    # Test case 2: Single node
    preorder2 = [-1]
    inorder2 = [-1]
    
    root2 = solution.buildTree(preorder2, inorder2)
    print(f"Test 2 - Preorder: {preorder_traversal(root2)}")  # [-1]
    print(f"Test 2 - Inorder: {inorder_traversal(root2)}")    # [-1]

"""
INTERVIEW TALKING POINTS:

1. APPROACH EXPLANATION:
   - Preorder gives us root first, then left subtree, then right subtree
   - Inorder gives us left subtree, then root, then right subtree
   - Use preorder to identify roots, inorder to split subtrees

2. OPTIMIZATION:
   - HashMap for O(1) inorder lookups instead of O(n) linear search
   - Single preorder index instead of array slicing to avoid O(n) space per call

3. EDGE CASES:
   - Empty arrays
   - Single node
   - All left/right skewed trees

4. TIME/SPACE COMPLEXITY:
   - Time: O(n) - visit each node once
   - Space: O(n) - hashmap + recursion stack (O(log n) best case, O(n) worst case)

5. FOLLOW-UP VARIATIONS:
   - Postorder + Inorder
   - Preorder + Postorder (only works if no duplicates)
   - Level order + Inorder
"""
