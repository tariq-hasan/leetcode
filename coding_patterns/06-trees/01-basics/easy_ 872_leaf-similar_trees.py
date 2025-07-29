"""
LeetCode 872. Leaf-Similar Trees
Problem: Consider all the leaves of a binary tree, from left to right, 
are the values of those leaves form a leaf value sequence.
Two binary trees are considered leaf-similar if their leaf value sequence is the same.
Return true if and only if the two given trees are leaf-similar.

Example:
Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true
Explanation: Both trees have leaf sequence [6,7,4,9,8]

Key Insights:
1. Need to extract leaf nodes in left-to-right order (inorder-like traversal)
2. A leaf node has no left and no right children
3. Compare leaf sequences of both trees
4. Multiple approaches: collect all leaves first, or use generators for space efficiency
"""

from typing import List, Optional, Generator

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 1: Collect All Leaves (MOST COMMON INTERVIEW SOLUTION)
        Time: O(N1 + N2) where N1, N2 are number of nodes in each tree
        Space: O(H1 + H2 + L1 + L2) where H is height, L is number of leaves
        
        This is the most straightforward and commonly expected approach.
        """
        def get_leaves(root):
            """Get all leaf values in left-to-right order using DFS"""
            if not root:
                return []
            
            # If it's a leaf node, return its value
            if not root.left and not root.right:
                return [root.val]
            
            # Collect leaves from left subtree, then right subtree
            leaves = []
            leaves.extend(get_leaves(root.left))
            leaves.extend(get_leaves(root.right))
            return leaves
        
        return get_leaves(root1) == get_leaves(root2)

    def leafSimilar_v2(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 2: DFS with Helper Function (Alternative Implementation)
        Time: O(N1 + N2)
        Space: O(H1 + H2 + L1 + L2)
        
        Same logic but with explicit helper function and result list.
        """
        def dfs(node, leaves):
            """DFS to collect leaves in left-to-right order"""
            if not node:
                return
            
            if not node.left and not node.right:
                leaves.append(node.val)
                return
            
            dfs(node.left, leaves)
            dfs(node.right, leaves)
        
        leaves1, leaves2 = [], []
        dfs(root1, leaves1)
        dfs(root2, leaves2)
        
        return leaves1 == leaves2

    def leafSimilar_v3(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 3: Using Generators (SPACE OPTIMIZED)
        Time: O(N1 + N2)
        Space: O(H1 + H2) - only recursion stack, no leaf storage
        
        More memory efficient - generates leaves on demand.
        """
        def get_leaves(root):
            """Generator that yields leaf values in left-to-right order"""
            if not root:
                return
            
            if not root.left and not root.right:
                yield root.val
            else:
                yield from get_leaves(root.left)
                yield from get_leaves(root.right)
        
        # Compare leaf sequences using generators
        leaves1 = get_leaves(root1)
        leaves2 = get_leaves(root2)
        
        # Compare generators element by element
        for leaf1, leaf2 in zip(leaves1, leaves2):
            if leaf1 != leaf2:
                return False
        
        # Check if both generators are exhausted
        try:
            next(leaves1)
            return False  # root1 has more leaves
        except StopIteration:
            pass
        
        try:
            next(leaves2)
            return False  # root2 has more leaves
        except StopIteration:
            pass
        
        return True

    def leafSimilar_v4(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 4: Iterative DFS using Stack
        Time: O(N1 + N2)
        Space: O(H1 + H2 + L1 + L2)
        
        Iterative version using explicit stack for DFS.
        """
        def get_leaves_iterative(root):
            """Get leaves using iterative DFS with stack"""
            if not root:
                return []
            
            leaves = []
            stack = [root]
            
            while stack:
                node = stack.pop()
                
                if not node.left and not node.right:
                    leaves.append(node.val)
                else:
                    # Add right first, then left (for left-to-right order)
                    if node.right:
                        stack.append(node.right)
                    if node.left:
                        stack.append(node.left)
            
            return leaves
        
        return get_leaves_iterative(root1) == get_leaves_iterative(root2)

    def leafSimilar_v5(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 5: Early Termination with Generators (MOST OPTIMIZED)
        Time: O(min(N1, N2)) best case, O(N1 + N2) worst case
        Space: O(H1 + H2)
        
        Combines generators with early termination for maximum efficiency.
        """
        def get_leaves(root):
            """Generator for leaf values"""
            if not root:
                return
            
            if not root.left and not root.right:
                yield root.val
            else:
                yield from get_leaves(root.left)
                yield from get_leaves(root.right)
        
        # Use itertools.zip_longest for proper comparison
        from itertools import zip_longest
        
        leaves1 = get_leaves(root1)
        leaves2 = get_leaves(root2)
        
        # Compare with sentinel value to detect length differences
        sentinel = object()
        for leaf1, leaf2 in zip_longest(leaves1, leaves2, fillvalue=sentinel):
            if leaf1 != leaf2:
                return False
        
        return True

    def leafSimilar_v6(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """
        Approach 6: Morris Traversal (ADVANCED - Constant Space)
        Time: O(N1 + N2)
        Space: O(L1 + L2) - only for storing leaves, O(1) for traversal
        
        Advanced approach using Morris traversal for constant space tree traversal.
        """
        def get_leaves_morris(root):
            """Get leaves using Morris traversal (threaded binary tree)"""
            leaves = []
            current = root
            
            while current:
                if not current.left:
                    # Check if it's a leaf
                    if not current.right:
                        leaves.append(current.val)
                    current = current.right
                else:
                    # Find inorder predecessor
                    predecessor = current.left
                    while predecessor.right and predecessor.right != current:
                        predecessor = predecessor.right
                    
                    if not predecessor.right:
                        # Make threading
                        predecessor.right = current
                        current = current.left
                    else:
                        # Remove threading and check if current is leaf
                        predecessor.right = None
                        if not current.left and not current.right:
                            leaves.append(current.val)
                        current = current.right
            
            return leaves
        
        return get_leaves_morris(root1) == get_leaves_morris(root2)

# Helper function to build tree from list
def build_tree(values):
    """Build tree from leetcode array representation"""
    if not values:
        return None
    
    from collections import deque
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

# Test the solutions
def test_solutions():
    solution = Solution()
    
    # Test case 1: Example from problem
    root1 = build_tree([3,5,1,6,2,9,8,None,None,7,4])
    root2 = build_tree([3,5,1,6,7,4,2,None,None,None,None,None,None,9,8])
    print("Test case 1:")
    print("root1 = [3,5,1,6,2,9,8,null,null,7,4]")
    print("root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]")
    print("Expected: True (both have leaf sequence [6,7,4,9,8])")
    print("Collect All:", solution.leafSimilar(root1, root2))
    print("Generators:", solution.leafSimilar_v3(root1, root2))
    print("Iterative:", solution.leafSimilar_v4(root1, root2))
    print()
    
    # Test case 2: Different leaf sequences
    root3 = build_tree([1,2,3])
    root4 = build_tree([1,3,2])
    print("Test case 2:")
    print("root1 = [1,2,3], root2 = [1,3,2]")
    print("Expected: False (leaf sequences [2,3] vs [3,2])")
    print("Result:", solution.leafSimilar(root3, root4))
    print()
    
    # Test case 3: Single node trees
    root5 = build_tree([1])
    root6 = build_tree([1])
    print("Test case 3:")
    print("root1 = [1], root2 = [1]")
    print("Expected: True")
    print("Result:", solution.leafSimilar(root5, root6))
    print()
    
    # Test case 4: Different single nodes
    root7 = build_tree([1])
    root8 = build_tree([2])
    print("Test case 4:")
    print("root1 = [1], root2 = [2]")
    print("Expected: False")
    print("Result:", solution.leafSimilar(root7, root8))
    print()
    
    # Test case 5: Different number of leaves
    root9 = build_tree([1,2])
    root10 = build_tree([2,1,3])
    print("Test case 5:")
    print("root1 = [1,2] (leaf: [2]), root2 = [2,1,3] (leaves: [1,3])")
    print("Expected: False")
    print("Result:", solution.leafSimilar(root9, root10))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - Need to compare leaf sequences of two trees in left-to-right order
   - A leaf node has no left and no right children
   - Trees are leaf-similar if their leaf sequences are identical
   - Order matters: [1,2,3] ≠ [1,3,2]

2. Key Insights:
   - This is a tree traversal problem with specific ordering requirement
   - Need DFS traversal that visits left subtree before right subtree
   - Can collect all leaves first, or use generators for space efficiency
   - Leaf identification: node.left is None AND node.right is None

3. Approach 1 (Collect All Leaves) - Most Common:
   - Use DFS to collect all leaves from both trees
   - Compare the resulting lists for equality
   - Simple, intuitive, and easy to implement
   - Most commonly expected in interviews

4. Approach 3 (Generators) - Space Optimized:
   - Generate leaves on-demand without storing all at once
   - More memory efficient for large trees
   - Shows advanced Python knowledge
   - Good follow-up if interviewer asks about optimization

5. Edge Cases:
   - Empty trees (both null) → should return True
   - Single-node trees → node itself is a leaf
   - Trees with different structures but same leaf sequence
   - Trees with different number of leaves
   - Trees where one is null and other is not

6. Common Mistakes:
   - Incorrect leaf identification (forgetting to check both left AND right are null)
   - Wrong traversal order (not maintaining left-to-right sequence)
   - Not handling empty tree cases
   - Comparing tree structures instead of leaf sequences

7. Time/Space Complexity:
   - Time: O(N1 + N2) for all approaches (must visit all nodes to find leaves)
   - Space: Collect approach - O(H + L), Generator approach - O(H)
   - Where H = height, L = number of leaves

8. Traversal Order Importance:
   - Must use DFS that processes left subtree before right subtree
   - This ensures left-to-right leaf ordering
   - Inorder, preorder, or postorder all work as long as left comes before right

9. Follow-up Questions:
   - How to optimize for space? (Use generators)
   - What if trees are very large? (Streaming comparison)
   - How to modify for right-to-left comparison?
   - What about comparing leaf sums instead of sequences?

10. Alternative Optimizations:
    - Early termination when sequences don't match
    - Morris traversal for constant space tree traversal
    - Parallel traversal of both trees simultaneously

RECOMMENDED APPROACH FOR INTERVIEW:
1. Start with Approach 1 (Collect All Leaves) - most intuitive
2. Explain leaf identification clearly: both left and right must be null
3. Show DFS traversal that maintains left-to-right order
4. Walk through example showing how leaf sequences are built
5. Handle edge cases (empty trees, single nodes)
6. Mention generator approach as space optimization if time permits

CRITICAL INSIGHT TO COMMUNICATE:
"The key insight is that we need to extract leaves in left-to-right order from 
both trees and compare the sequences. A leaf is identified as a node with no 
left AND no right children. We use DFS traversal that processes left subtree 
before right subtree to maintain the correct ordering."

PATTERN RECOGNITION:
This problem combines several important patterns:
- Tree traversal (DFS)
- Leaf node identification
- Sequence comparison
- Generator/iterator usage (for optimization)

The skills learned here apply to many tree problems involving leaf operations.
"""
