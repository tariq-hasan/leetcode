# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, inorder, postorder):
        """
        Construct Binary Tree from Inorder and Postorder Traversal
        
        Key Insights:
        - Last element in postorder is always the root
        - In inorder, elements left of root are left subtree, right are right subtree
        - Postorder: left -> right -> root, so we process from RIGHT to LEFT
        - Build RIGHT subtree first, then LEFT subtree
        
        Time: O(n) - each node processed once
        Space: O(n) - hashmap + recursion stack
        """
        if not inorder or not postorder:
            return None
        
        # Create hashmap for O(1) inorder lookups
        inorder_map = {val: i for i, val in enumerate(inorder)}
        self.postorder_idx = len(postorder) - 1
        
        def build(left, right):
            if left > right:
                return None
            
            # Root is current element in postorder (from end)
            root_val = postorder[self.postorder_idx]
            root = TreeNode(root_val)
            self.postorder_idx -= 1
            
            # Find root position in inorder
            root_idx = inorder_map[root_val]
            
            # CRITICAL: Build RIGHT subtree first!
            # Postorder is left->right->root, so when going backwards: root->right->left
            root.right = build(root_idx + 1, right)
            root.left = build(left, root_idx - 1)
            
            return root
        
        return build(0, len(inorder) - 1)

# Alternative Solution: Using array slicing (less efficient but more intuitive)
class SolutionSlicing:
    def buildTree(self, inorder, postorder):
        if not inorder or not postorder:
            return None
        
        # Last element in postorder is root
        root = TreeNode(postorder[-1])
        
        # Find root in inorder to split left/right subtrees
        mid = inorder.index(postorder[-1])
        
        # Recursively build subtrees
        # Left subtree: inorder[:mid], postorder[:mid]
        # Right subtree: inorder[mid+1:], postorder[mid:-1]
        root.left = self.buildTree(inorder[:mid], postorder[:mid])
        root.right = self.buildTree(inorder[mid+1:], postorder[mid:-1])
        
        return root

# Iterative Solution (Advanced - shows deep understanding)
class SolutionIterative:
    def buildTree(self, inorder, postorder):
        if not inorder or not postorder:
            return None
        
        stack = []
        root = TreeNode(postorder[-1])
        stack.append(root)
        
        inorder_idx = len(inorder) - 1
        
        for i in range(len(postorder) - 2, -1, -1):
            node = TreeNode(postorder[i])
            parent = None
            
            # Find the parent for current node
            while stack and stack[-1].val == inorder[inorder_idx]:
                parent = stack.pop()
                inorder_idx -= 1
            
            if parent:
                parent.left = node
            else:
                stack[-1].right = node
            
            stack.append(node)
        
        return root

# Test cases and utility functions
def inorder_traversal(root):
    """Helper to verify solution"""
    if not root:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)

def postorder_traversal(root):
    """Helper to verify solution"""
    if not root:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.val]

# Test the solution
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1: [9,3,15,20,7]
    inorder1 = [9, 3, 15, 20, 7]
    postorder1 = [9, 15, 7, 20, 3]
    
    root1 = solution.buildTree(inorder1, postorder1)
    print(f"Test 1 - Inorder: {inorder_traversal(root1)}")      # [9, 3, 15, 20, 7]
    print(f"Test 1 - Postorder: {postorder_traversal(root1)}")  # [9, 15, 7, 20, 3]
    
    # Test case 2: Single node
    inorder2 = [-1]
    postorder2 = [-1]
    
    root2 = solution.buildTree(inorder2, postorder2)
    print(f"Test 2 - Inorder: {inorder_traversal(root2)}")      # [-1]
    print(f"Test 2 - Postorder: {postorder_traversal(root2)}")  # [-1]
    
    # Test case 3: Left skewed tree
    inorder3 = [3, 2, 1]
    postorder3 = [3, 2, 1]
    
    root3 = solution.buildTree(inorder3, postorder3)
    print(f"Test 3 - Inorder: {inorder_traversal(root3)}")      # [3, 2, 1]
    print(f"Test 3 - Postorder: {postorder_traversal(root3)}")  # [3, 2, 1]

"""
INTERVIEW TALKING POINTS:

1. KEY DIFFERENCE FROM PROBLEM 105:
   - Postorder: left -> right -> root (vs preorder: root -> left -> right)
   - Process postorder from RIGHT to LEFT (backwards)
   - Build RIGHT subtree BEFORE left subtree

2. CRITICAL INSIGHT:
   - When going backwards through postorder: root -> right -> left
   - This is why we build right subtree first, then left

3. ALGORITHM STEPS:
   - Take last element from postorder as root
   - Find root in inorder to split left/right subtrees
   - Recursively build right subtree, then left subtree
   - Decrement postorder index after processing each node

4. EDGE CASES:
   - Empty arrays
   - Single node
   - Left/right skewed trees

5. OPTIMIZATIONS:
   - HashMap for O(1) inorder lookups
   - Single index tracking instead of array slicing
   - Iterative solution possible (advanced)

6. TIME/SPACE COMPLEXITY:
   - Time: O(n) - each node processed once
   - Space: O(n) - hashmap + O(h) recursion stack

7. COMMON MISTAKES:
   - Building left subtree first (wrong!)
   - Incrementing instead of decrementing postorder index
   - Forgetting that postorder is processed backwards
"""
