"""
LeetCode 100: Same Tree

Problem: Given the roots of two binary trees p and q, write a function to check if they are the same or not.
Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

Time Complexity: O(min(m,n)) where m,n are number of nodes
Space Complexity: O(min(m,n)) for recursion stack in worst case
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        """
        OPTIMAL RECURSIVE SOLUTION - Most elegant for interviews
        
        Base cases:
        1. Both nodes are None -> True
        2. One is None, other isn't -> False
        3. Values don't match -> False
        
        Recursive case: Both subtrees must be same
        
        Time: O(min(m,n)), Space: O(min(m,n)) for recursion
        """
        # Base case: both are None
        if not p and not q:
            return True
        
        # Base case: one is None, other isn't
        if not p or not q:
            return False
        
        # Base case: values don't match
        if p.val != q.val:
            return False
        
        # Recursive case: check both subtrees
        return (self.isSameTree(p.left, q.left) and 
                self.isSameTree(p.right, q.right))
    
    def isSameTreeIterative(self, p: TreeNode, q: TreeNode) -> bool:
        """
        ITERATIVE SOLUTION - Good alternative to show different approaches
        
        Use a stack/queue to simulate the recursion
        Process pairs of nodes simultaneously
        
        Time: O(min(m,n)), Space: O(min(m,n)) for stack
        """
        # Use a stack to store pairs of nodes to compare
        stack = [(p, q)]
        
        while stack:
            node1, node2 = stack.pop()
            
            # Both None - continue
            if not node1 and not node2:
                continue
            
            # One None, other not - different
            if not node1 or not node2:
                return False
            
            # Different values - different
            if node1.val != node2.val:
                return False
            
            # Add children to stack for comparison
            stack.append((node1.left, node2.left))
            stack.append((node1.right, node2.right))
        
        return True
    
    def isSameTreePreorder(self, p: TreeNode, q: TreeNode) -> bool:
        """
        PREORDER TRAVERSAL SOLUTION - Alternative approach
        
        Serialize both trees using preorder traversal with null markers
        Compare the serialized strings
        
        Time: O(m + n), Space: O(m + n)
        """
        def serialize(node):
            if not node:
                return ["null"]
            return [str(node.val)] + serialize(node.left) + serialize(node.right)
        
        return serialize(p) == serialize(q)
    
    def isSameTreeOnePass(self, p: TreeNode, q: TreeNode) -> bool:
        """
        ONE-LINER RECURSIVE - Concise version
        
        Very compact but less readable - good to mention you could write it this way
        """
        return (not p and not q) or \
               (p and q and p.val == q.val and 
                self.isSameTreeOnePass(p.left, q.left) and 
                self.isSameTreeOnePass(p.right, q.right))


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
        # (tree1_values, tree2_values, expected)
        ([1, 2, 3], [1, 2, 3], True),           # Same trees
        ([1, 2], [1, None, 2], False),          # Different structure
        ([1, 2, 1], [1, 1, 2], False),          # Different values
        ([], [], True),                         # Both empty
        ([1], [], False),                       # One empty
        ([1], [1], True),                       # Single nodes same
        ([1], [2], False),                      # Single nodes different
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], True),  # Larger same trees
        ([1, 2, 3, 4], [1, 2, 3, None, 4], False), # Different structure
    ]
    
    print("Testing Same Tree Solutions:")
    print("=" * 50)
    
    for i, (vals1, vals2, expected) in enumerate(test_cases):
        tree1 = build_tree(vals1) if vals1 else None
        tree2 = build_tree(vals2) if vals2 else None
        
        # Test recursive solution
        result_rec = sol.isSameTree(tree1, tree2)
        # Test iterative solution  
        result_iter = sol.isSameTreeIterative(tree1, tree2)
        
        status_rec = "✓" if result_rec == expected else "✗"
        status_iter = "✓" if result_iter == expected else "✗"
        
        print(f"Test {i+1}:")
        print(f"  Tree1: {vals1}")
        print(f"  Tree2: {vals2}")
        print(f"  Recursive: {status_rec} {result_rec} (expected {expected})")
        print(f"  Iterative: {status_iter} {result_iter} (expected {expected})")
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM ANALYSIS:
   - Need to check both structure AND values
   - Tree traversal problem - multiple approaches possible
   - Early termination opportunities for efficiency

2. APPROACH COMPARISON:
   - Recursive: Most natural and clean
   - Iterative: Shows understanding of stack-based traversal
   - Serialization: Alternative thinking (but less efficient)

3. COMPLEXITY ANALYSIS:
   - Time: O(min(m,n)) - we stop as soon as we find difference
   - Space: O(min(m,n)) - recursion depth or stack size
   - Best case: O(1) if root values differ
   - Worst case: O(n) if trees are identical

4. EDGE CASES TO DISCUSS:
   - Both trees are None (empty)
   - One tree is None, other isn't
   - Single node trees
   - Trees with same structure but different values
   - Trees with same values but different structure

5. OPTIMIZATION NOTES:
   - Early termination when values differ
   - No need to traverse entire trees if difference found
   - Could optimize further with iterative level-order if needed

6. FOLLOW-UP QUESTIONS:
   - What if we wanted to find the first differing node?
   - How to handle very large trees (memory constraints)?
   - What if trees had additional properties to compare?
   - How to make it work for n-ary trees?

7. CODE VARIATIONS:
   - One-liner version (less readable but shows Python skills)
   - Different traversal orders (inorder, postorder)
   - Using deque instead of list for better performance
"""
