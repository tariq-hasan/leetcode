"""
LeetCode 572. Subtree of Another Tree
Problem: Given the roots of two binary trees root and subRoot, return true if there 
is a subtree of root with the same structure and node values of subRoot and false otherwise.
A subtree of a binary tree tree is a tree that consists of a node in tree and all 
of this node's descendants. The tree tree could also be considered as a subtree of itself.

Example:
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
       3              4
      / \            / \
     4   5          1   2
    / \
   1   2
Output: true

Key Insights:
1. Need to check if subRoot matches any subtree starting from each node in root
2. Two parts: traverse root tree + compare trees for equality
3. A subtree must match EXACTLY (structure and values)
4. Multiple approaches: DFS + comparison, serialization, hashing
"""

from typing import Optional

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 1: DFS + Tree Comparison (MOST COMMON INTERVIEW SOLUTION)
        Time: O(M * N) where M = nodes in root, N = nodes in subRoot
        Space: O(max(H1, H2)) where H1, H2 are heights of trees
        
        This is the most intuitive and commonly expected approach.
        """
        if not subRoot:
            return True
        if not root:
            return False
        
        # Check if trees starting from current root are same
        if self.isSameTree(root, subRoot):
            return True
        
        # Check left and right subtrees
        return (self.isSubtree(root.left, subRoot) or 
                self.isSubtree(root.right, subRoot))
    
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """Helper function to check if two trees are identical"""
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        
        return (self.isSameTree(p.left, q.left) and 
                self.isSameTree(p.right, q.right))

    def isSubtree_v2(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 2: Serialization + String Matching
        Time: O(M + N) where M = nodes in root, N = nodes in subRoot
        Space: O(M + N) for string storage
        
        Convert trees to strings and use string matching.
        """
        def serialize(node):
            """Serialize tree to string with null markers"""
            if not node:
                return "#"
            return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"
        
        root_str = serialize(root)
        subroot_str = serialize(subRoot)
        
        return subroot_str in root_str

    def isSubtree_v3(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 3: Hash-based Comparison (Advanced)
        Time: O(M + N) average case, O(M * N) worst case
        Space: O(M + N)
        
        Use tree hashing to quickly identify potential matches.
        """
        def get_hash(node, hashes):
            """Get hash of subtree rooted at node"""
            if not node:
                return hash(None)
            
            left_hash = get_hash(node.left, hashes)
            right_hash = get_hash(node.right, hashes)
            
            # Create unique hash for this subtree
            subtree_hash = hash((node.val, left_hash, right_hash))
            hashes[subtree_hash] = node
            return subtree_hash
        
        # Get target hash
        target_hashes = {}
        target_hash = get_hash(subRoot, target_hashes)
        
        # Check if any subtree in root has same hash
        root_hashes = {}
        get_hash(root, root_hashes)
        
        if target_hash in root_hashes:
            # Verify with actual tree comparison (handle hash collisions)
            return self.isSameTree(root_hashes[target_hash], subRoot)
        
        return False

    def isSubtree_v4(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 4: DFS with Early Termination (Optimized)
        Time: O(M * N) worst case, better average case
        Space: O(max(H1, H2))
        
        Same as approach 1 but with optimizations.
        """
        if not subRoot:
            return True
        if not root:
            return False
        
        def dfs(node):
            if not node:
                return False
            
            # If values match, check if trees are same
            if node.val == subRoot.val and self.isSameTree(node, subRoot):
                return True
            
            # Continue searching in subtrees
            return dfs(node.left) or dfs(node.right)
        
        return dfs(root)

    def isSubtree_iterative(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 5: Iterative DFS using Stack
        Time: O(M * N)
        Space: O(M)
        
        Iterative version of the main algorithm.
        """
        if not subRoot:
            return True
        if not root:
            return False
        
        stack = [root]
        
        while stack:
            node = stack.pop()
            
            if self.isSameTree(node, subRoot):
                return True
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return False

    def isSubtree_v6(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 6: Level-by-Level BFS Comparison
        Time: O(M * N)
        Space: O(M)
        
        Use BFS to traverse root tree and check each node.
        """
        if not subRoot:
            return True
        if not root:
            return False
        
        from collections import deque
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            if self.isSameTree(node, subRoot):
                return True
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return False

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
    
    # Test case 1: [3,4,5,1,2], [4,1,2]
    root1 = build_tree([3, 4, 5, 1, 2])
    subRoot1 = build_tree([4, 1, 2])
    print("Test case 1:")
    print("root = [3,4,5,1,2], subRoot = [4,1,2]")
    print("Expected: True")
    print("DFS + Comparison:", solution.isSubtree(root1, subRoot1))
    print("Serialization:", solution.isSubtree_v2(root1, subRoot1))
    print()
    
    # Test case 2: [3,4,5,1,2,null,null,null,null,0], [4,1,2]
    root2 = build_tree([3, 4, 5, 1, 2, None, None, None, None, 0])
    subRoot2 = build_tree([4, 1, 2])
    print("Test case 2:")
    print("root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]")
    print("Expected: False")
    print("Result:", solution.isSubtree(root2, subRoot2))
    print()
    
    # Test case 3: Single nodes
    root3 = build_tree([1])
    subRoot3 = build_tree([1])
    print("Test case 3:")
    print("root = [1], subRoot = [1]")
    print("Expected: True")
    print("Result:", solution.isSubtree(root3, subRoot3))
    print()
    
    # Test case 4: subRoot is null
    root4 = build_tree([1, 2, 3])
    subRoot4 = None
    print("Test case 4:")
    print("root = [1,2,3], subRoot = null")
    print("Expected: True")
    print("Result:", solution.isSubtree(root4, subRoot4))
    print()
    
    # Test case 5: root is null, subRoot is not null
    root5 = None
    subRoot5 = build_tree([1])
    print("Test case 5:")
    print("root = null, subRoot = [1]")
    print("Expected: False")
    print("Result:", solution.isSubtree(root5, subRoot5))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - Need to find if subRoot appears as a subtree anywhere in root
   - Subtree must match EXACTLY (structure and values)
   - A tree is considered a subtree of itself
   - Empty subRoot should return True (empty set is subset of any set)

2. Key Insights:
   - Two-step process: traverse root + compare trees
   - For each node in root, check if subtree starting there matches subRoot
   - Need helper function to compare two trees for equality
   - Multiple ways to optimize: serialization, hashing, early termination

3. Approach 1 (DFS + Comparison) - Most Common:
   - Traverse every node in root tree
   - At each node, check if subtree matches subRoot using isSameTree
   - Time: O(M * N), Space: O(max(H1, H2))
   - Most intuitive and commonly expected by interviewers

4. Approach 2 (Serialization) - Clever Optimization:
   - Convert both trees to strings with unique encoding
   - Use string matching to find subRoot pattern in root
   - Time: O(M + N), Space: O(M + N)
   - Need careful serialization to avoid false positives

5. Edge Cases:
   - Empty trees (root = null, subRoot = null)
   - subRoot is null (should return True)
   - root is null but subRoot is not (should return False)
   - Single node trees
   - Identical trees
   - subRoot larger than root

6. Common Mistakes:
   - Not handling null cases correctly
   - Incorrect serialization leading to false matches
   - Forgetting that exact structure match is required
   - Not considering that tree can be subtree of itself

7. Time/Space Complexity Analysis:
   - DFS approach: O(M * N) time, O(H) space
   - Serialization: O(M + N) time, O(M + N) space
   - Hash-based: O(M + N) average, O(M * N) worst case

8. Follow-up Questions:
   - What if values can be negative? (affects serialization)
   - What if we want to find all occurrences?
   - How to handle very large trees efficiently?
   - What about subtree with different structure but same inorder?

9. Optimization Techniques:
   - Early termination when values don't match
   - Memoization for repeated subtree comparisons
   - KMP algorithm for string matching in serialization approach

RECOMMENDED APPROACH FOR INTERVIEW:
1. Start with Approach 1 (DFS + Tree Comparison) - most intuitive
2. Explain the two-step process clearly
3. Implement isSameTree helper function first
4. Walk through example showing how each node is checked
5. Discuss edge cases thoroughly
6. Mention serialization approach as optimization if time permits
7. Always test with edge cases

CRITICAL POINTS TO EMPHASIZE:
- "We need to check every node in root as a potential starting point"
- "Subtree must match exactly - both structure and values"
- "This is essentially 'find pattern in tree' problem"
- "The isSameTree helper is crucial for exact matching"

The key insight is recognizing this as a pattern matching problem where we need 
to check every possible starting position in the main tree.
"""
