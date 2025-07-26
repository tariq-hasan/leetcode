"""
LeetCode 101: Symmetric Tree

Problem: Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

Key Insight: A tree is symmetric if left subtree is mirror image of right subtree.
This means: left.left should equal right.right AND left.right should equal right.left

Time Complexity: O(n) where n is number of nodes
Space Complexity: O(h) where h is height of tree (recursion stack)
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        """
        OPTIMAL RECURSIVE SOLUTION - Most important for interviews
        
        Key insight: Check if left subtree is mirror of right subtree
        Mirror means: left.left == right.right AND left.right == right.left
        
        Time: O(n), Space: O(h) for recursion stack
        """
        if not root:
            return True
        
        def isMirror(left: TreeNode, right: TreeNode) -> bool:
            # Both None - symmetric
            if not left and not right:
                return True
            
            # One None, other not - not symmetric
            if not left or not right:
                return False
            
            # Values must match and children must be mirrored
            return (left.val == right.val and 
                    isMirror(left.left, right.right) and 
                    isMirror(left.right, right.left))
        
        return isMirror(root.left, root.right)
    
    def isSymmetricIterative(self, root: TreeNode) -> bool:
        """
        ITERATIVE SOLUTION - Good alternative using queue/stack
        
        Use queue to store pairs of nodes that should be mirrors
        Process pairs level by level (BFS-like approach)
        
        Time: O(n), Space: O(w) where w is max width of tree
        """
        if not root:
            return True
        
        from collections import deque
        queue = deque([(root.left, root.right)])
        
        while queue:
            left, right = queue.popleft()
            
            # Both None - continue
            if not left and not right:
                continue
            
            # One None or values don't match - not symmetric
            if not left or not right or left.val != right.val:
                return False
            
            # Add mirror pairs to queue
            queue.append((left.left, right.right))   # Outer pair
            queue.append((left.right, right.left))   # Inner pair
        
        return True
    
    def isSymmetricStack(self, root: TreeNode) -> bool:
        """
        ITERATIVE WITH STACK - DFS-like approach
        
        Similar to queue version but uses stack (LIFO)
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return True
        
        stack = [(root.left, root.right)]
        
        while stack:
            left, right = stack.pop()
            
            if not left and not right:
                continue
            
            if not left or not right or left.val != right.val:
                return False
            
            # Add mirror pairs to stack
            stack.append((left.left, right.right))
            stack.append((left.right, right.left))
        
        return True
    
    def isSymmetricInorder(self, root: TreeNode) -> bool:
        """
        INORDER TRAVERSAL APPROACH - Less optimal but shows different thinking
        
        Compare inorder traversal of left subtree with reversed inorder of right subtree
        Need to handle None values carefully
        
        Time: O(n), Space: O(n)
        """
        if not root:
            return True
        
        def inorder(node, result):
            if not node:
                result.append(None)
                return
            inorder(node.left, result)
            result.append(node.val)
            inorder(node.right, result)
        
        def reverse_inorder(node, result):
            if not node:
                result.append(None)
                return
            reverse_inorder(node.right, result)
            result.append(node.val)
            reverse_inorder(node.left, result)
        
        left_traversal = []
        right_traversal = []
        
        inorder(root.left, left_traversal)
        reverse_inorder(root.right, right_traversal)
        
        return left_traversal == right_traversal


# Helper function to build test trees
def build_tree(values):
    """Build tree from level-order list (None for missing nodes)"""
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while queue and i < len(values):
        node = queue.pop(0)
        
        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

def print_tree(root, level=0, prefix="Root: "):
    """Helper to visualize tree structure"""
    if root:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")

# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        # (tree_values, expected, description)
        ([1, 2, 2, 3, 4, 4, 3], True, "Perfect symmetric tree"),
        ([1, 2, 2, None, 3, None, 3], False, "Asymmetric structure"),
        ([1, 2, 2, 3, None, None, 3], True, "Symmetric with None nodes"),
        ([1], True, "Single node"),
        ([], True, "Empty tree"),
        ([1, 2, 3], False, "Simple asymmetric"),
        ([1, 2, 2], True, "Simple symmetric"),
        ([1, 2, 2, 2, None, 2], False, "Asymmetric values"),
        ([1, 2, 2, None, 3, 3, None], True, "Mirror structure"),
    ]
    
    print("Testing Symmetric Tree Solutions:")
    print("=" * 60)
    
    for i, (vals, expected, desc) in enumerate(test_cases):
        tree = build_tree(vals) if vals else None
        
        # Test all solutions
        result_rec = sol.isSymmetric(tree)
        result_iter = sol.isSymmetricIterative(tree)
        result_stack = sol.isSymmetricStack(tree)
        
        status_rec = "✓" if result_rec == expected else "✗"
        status_iter = "✓" if result_iter == expected else "✗"
        status_stack = "✓" if result_stack == expected else "✗"
        
        print(f"Test {i+1}: {desc}")
        print(f"  Tree: {vals}")
        if vals:
            print("  Structure:")
            print_tree(tree)
        print(f"  Recursive: {status_rec} {result_rec}")
        print(f"  Iterative (Queue): {status_iter} {result_iter}")
        print(f"  Iterative (Stack): {status_stack} {result_stack}")
        print(f"  Expected: {expected}")
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Symmetric = left subtree is mirror image of right subtree
   - Mirror means: left.left == right.right AND left.right == right.left
   - Not just checking if left subtree == right subtree!

2. KEY INSIGHT:
   - Convert to "Same Tree" problem but with mirrored comparison
   - Compare root.left with root.right in a special way
   - Recursive helper function compares two nodes as mirrors

3. APPROACH COMPARISON:
   - Recursive: Most natural and preferred
   - Iterative with Queue: BFS-like, good for showing queue usage
   - Iterative with Stack: DFS-like, shows stack understanding
   - Inorder: Less optimal but shows creative thinking

4. COMPLEXITY ANALYSIS:
   - Time: O(n) - must visit each node once
   - Space: O(h) recursive stack or O(w) for queue where w is max width
   - Best case: O(1) if root has no children or values differ at top
   - Worst case: O(n) for skewed tree or when tree is actually symmetric

5. EDGE CASES:
   - Empty tree (symmetric by definition)
   - Single node (symmetric)
   - Tree with all same values (check structure)
   - Tree with None nodes in different positions

6. CODING MISTAKES TO AVOID:
   - Don't compare left subtree with right subtree directly
   - Remember to swap the children in recursive calls
   - Handle None cases properly in iterative solutions

7. FOLLOW-UP QUESTIONS:
   - "Can you do this iteratively?" → Show queue/stack solution
   - "What if we had n-ary trees?" → Extend the mirror logic
   - "How to find the axis of symmetry?" → Different problem
   - "Memory constraints?" → Discuss iterative vs recursive trade-offs

8. RELATED PROBLEMS:
   - Same Tree (100) - foundation for this problem
   - Invert Binary Tree (226) - related tree manipulation
   - Maximum Depth (104) - tree traversal practice
"""
