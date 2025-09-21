# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from typing import Optional

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Optimal BST Solution - Leveraging BST Property (Recursive)
        
        Key insight: Use BST ordering to determine direction without full traversal.
        LCA is the first node where p and q are on different sides.
        
        Time Complexity: O(h) where h is height of tree
        Space Complexity: O(h) due to recursion stack
        """
        # Both p and q are in left subtree
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        
        # Both p and q are in right subtree  
        elif p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        
        # p and q are on different sides, or one of them is root
        # This means root is the LCA
        else:
            return root

    def lowestCommonAncestorIterative(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Optimal BST Solution - Iterative (Most Efficient)
        
        Same logic as recursive but without recursion stack overhead
        Time Complexity: O(h)
        Space Complexity: O(1)
        """
        current = root
        
        while current:
            # Both nodes in left subtree
            if p.val < current.val and q.val < current.val:
                current = current.left
            # Both nodes in right subtree
            elif p.val > current.val and q.val > current.val:
                current = current.right
            # Found LCA: nodes are on different sides or one equals current
            else:
                return current
        
        return None  # Should never reach here given problem constraints

    def lowestCommonAncestorExplicit(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        More Explicit BST Solution (Clearer Logic)
        
        Makes the conditions more explicit for better understanding
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        # Ensure p has smaller value for consistent logic
        if p.val > q.val:
            p, q = q, p
        
        def find_lca(node):
            if not node:
                return None
            
            # Case 1: Both nodes are smaller - go left
            if q.val < node.val:
                return find_lca(node.left)
            
            # Case 2: Both nodes are larger - go right
            elif p.val > node.val:
                return find_lca(node.right)
            
            # Case 3: Nodes are on different sides or one equals current
            else:
                return node
        
        return find_lca(root)

    def lowestCommonAncestorGeneral(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        General Binary Tree Solution (Not Optimal for BST)
        
        This is the solution from problem 236, works but doesn't leverage BST property
        Time Complexity: O(n) - visits all nodes potentially
        Space Complexity: O(h)
        """
        # Base case
        if not root or root == p or root == q:
            return root
        
        # Search in subtrees
        left = self.lowestCommonAncestorGeneral(root.left, p, q)
        right = self.lowestCommonAncestorGeneral(root.right, p, q)
        
        # If found in both subtrees, current node is LCA
        if left and right:
            return root
        
        # Return whichever subtree found the nodes
        return left if left else right

    def lowestCommonAncestorWithPath(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Path-Based Solution (Good for Understanding)
        
        Find paths to both nodes, then find divergence point
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        def find_path(node, target):
            """Find path from root to target in BST"""
            path = []
            current = node
            
            while current:
                path.append(current)
                if target.val == current.val:
                    break
                elif target.val < current.val:
                    current = current.left
                else:
                    current = current.right
            
            return path
        
        # Get paths to both nodes
        path_p = find_path(root, p)
        path_q = find_path(root, q)
        
        # Find last common node in both paths
        lca = None
        min_len = min(len(path_p), len(path_q))
        
        for i in range(min_len):
            if path_p[i] == path_q[i]:
                lca = path_p[i]
            else:
                break
        
        return lca

    def lowestCommonAncestorRange(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Range-Based Solution (Alternative Perspective)
        
        Think of LCA as the node whose value is between p and q
        Time Complexity: O(h)
        Space Complexity: O(1)
        """
        # Ensure p.val <= q.val for simpler logic
        if p.val > q.val:
            p, q = q, p
        
        current = root
        
        while current:
            # If current value is in range [p.val, q.val], it's the LCA
            if p.val <= current.val <= q.val:
                return current
            # If current is too large, go left
            elif current.val > q.val:
                current = current.left
            # If current is too small, go right
            else:
                current = current.right
        
        return None

    def lowestCommonAncestorRecursiveClean(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Clean Recursive Implementation (Interview Favorite)
        
        Most concise and elegant solution
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        if (p.val <= root.val <= q.val) or (q.val <= root.val <= p.val):
            return root
        elif p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestorRecursiveClean(root.left, p, q)
        else:
            return self.lowestCommonAncestorRecursiveClean(root.right, p, q)

# Test cases and utility functions
def build_test_bst1():
    """
    Build BST:        6
                    /   \
                   2     8
                  / \   / \
                 0   4 7   9
                    / \
                   3   5
    
    Test cases:
    - LCA(2, 8) = 6 (root)
    - LCA(2, 4) = 2 (one is ancestor of other)
    - LCA(3, 5) = 4 (common ancestor)
    """
    nodes = {}
    for val in [6, 2, 8, 0, 4, 7, 9, 3, 5]:
        nodes[val] = TreeNode(val)
    
    nodes[6].left = nodes[2]
    nodes[6].right = nodes[8]
    nodes[2].left = nodes[0]
    nodes[2].right = nodes[4]
    nodes[8].left = nodes[7]
    nodes[8].right = nodes[9]
    nodes[4].left = nodes[3]
    nodes[4].right = nodes[5]
    
    return nodes[6], nodes

def build_simple_bst():
    """
    Simple BST:   2
                 / \
                1   3
    """
    nodes = {}
    for val in [2, 1, 3]:
        nodes[val] = TreeNode(val)
    
    nodes[2].left = nodes[1]
    nodes[2].right = nodes[3]
    
    return nodes[2], nodes

def build_linear_bst():
    """
    Linear BST:  1
                  \
                   2
                    \
                     3
                      \
                       4
    """
    nodes = {}
    for val in [1, 2, 3, 4]:
        nodes[val] = TreeNode(val)
    
    nodes[1].right = nodes[2]
    nodes[2].right = nodes[3]
    nodes[3].right = nodes[4]
    
    return nodes[1], nodes

def print_path_to_node(root, target):
    """Helper to visualize path to target node"""
    path = []
    current = root
    
    while current:
        path.append(current.val)
        if target.val == current.val:
            break
        elif target.val < current.val:
            current = current.left
        else:
            current = current.right
    
    return path

def test_lca_method(method, root, nodes, p_val, q_val, expected_val, method_name):
    """Test an LCA method"""
    p, q = nodes[p_val], nodes[q_val]
    result = method(root, p, q)
    
    path_p = print_path_to_node(root, p)
    path_q = print_path_to_node(root, q)
    
    print(f"  {method_name}:")
    print(f"    LCA({p_val}, {q_val}) = {result.val} (Expected: {expected_val})")
    print(f"    Path to {p_val}: {path_p}")
    print(f"    Path to {q_val}: {path_q}")
    print(f"    Correct: {result.val == expected_val}")
    print()

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Complex BST
    root1, nodes1 = build_test_bst1()
    print("Test 1 - Complex BST:")
    print("       6")
    print("     /   \\")
    print("    2     8")
    print("   / \\   / \\")
    print("  0   4 7   9")
    print("     / \\")
    print("    3   5")
    print()
    
    # Test LCA(2, 8) = 6
    test_lca_method(solution.lowestCommonAncestor, root1, nodes1, 2, 8, 6, "BST Recursive")
    test_lca_method(solution.lowestCommonAncestorIterative, root1, nodes1, 2, 8, 6, "BST Iterative")
    
    # Test LCA(2, 4) = 2 (ancestor case)
    test_lca_method(solution.lowestCommonAncestor, root1, nodes1, 2, 4, 2, "BST Recursive")
    
    # Test LCA(3, 5) = 4
    test_lca_method(solution.lowestCommonAncestor, root1, nodes1, 3, 5, 4, "BST Recursive")
    
    # Test case 2 - Simple BST
    root2, nodes2 = build_simple_bst()
    print("Test 2 - Simple BST [2,1,3]:")
    test_lca_method(solution.lowestCommonAncestor, root2, nodes2, 1, 3, 2, "BST Recursive")
    
    # Test case 3 - Linear BST
    root3, nodes3 = build_linear_bst()
    print("Test 3 - Linear BST:")
    test_lca_method(solution.lowestCommonAncestorIterative, root3, nodes3, 1, 4, 1, "BST Iterative")
    
    # Compare BST vs General solution performance
    print("Performance Comparison (conceptual):")
    print("  BST Solution: O(h) - follows single path")
    print("  General Solution: O(n) - may visit all nodes")
    print("  For balanced BST: BST is O(log n) vs General O(n)")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - This is BST-specific version of problem 236
   - Can leverage BST ordering property for efficiency
   - LCA is first node where p and q are on different sides
   - Much more efficient than general binary tree approach

2. KEY INSIGHT - BST PROPERTY OPTIMIZATION:
   - Don't need to search entire tree like general case
   - Use BST ordering to determine which direction to go
   - If both nodes smaller than current → go left
   - If both nodes larger than current → go right
   - Otherwise → current node is LCA

3. ALGORITHM LOGIC:
   - Start from root
   - If both p and q are less than current → go left
   - If both p and q are greater than current → go right  
   - Otherwise → current node is LCA (split point)

4. WHY BST VERSION IS BETTER:
   - Time: O(h) instead of O(n) for general case
   - Space: Can be O(1) with iterative approach
   - More direct - doesn't need to explore both subtrees

5. SOLUTION APPROACHES:

   APPROACH 1 - BST Recursive (RECOMMENDED):
   - Clean and intuitive
   - Leverages BST property optimally
   - O(h) time, O(h) space

   APPROACH 2 - BST Iterative:
   - Same logic but iterative
   - O(h) time, O(1) space
   - Most space-efficient

   APPROACH 3 - General Tree Solution:
   - Works but doesn't leverage BST property
   - Less efficient: O(n) time vs O(h)

6. IMPLEMENTATION DETAILS:
   - Compare node values, not references
   - Handle edge cases (one node is ancestor of other)
   - BST property: left < root < right

7. COMPLEXITY ANALYSIS:
   - Time: O(h) where h is height of tree
   - Best case: O(log n) for balanced BST
   - Worst case: O(n) for skewed BST (but still better than general O(n))
   - Space: O(h) recursive, O(1) iterative

8. EDGE CASES:
   - One node is ancestor of the other
   - Both nodes are the same
   - Nodes at different depths
   - Skewed BST (essentially a linked list)

9. INTERVIEW PRESENTATION:
   - Start with: "Since this is BST, I can use ordering property for efficiency"
   - Explain the key insight: "LCA is where paths diverge"
   - Code the BST-optimized solution
   - Mention general tree approach but emphasize BST optimization
   - Walk through example showing path decisions

10. FOLLOW-UP QUESTIONS:
    - "How is this different from general binary tree LCA?" → Explain BST optimization
    - "What if it's not BST?" → Need general tree approach (problem 236)
    - "Can you do it iteratively?" → Show iterative version
    - "What's the time complexity?" → O(h) vs O(n) comparison

11. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests BST property understanding
    - Shows optimization thinking (BST vs general)
    - Multiple implementation approaches
    - Clear complexity improvement demonstration

12. COMPARISON WITH PROBLEM 236:
    - Problem 236: General binary tree, O(n) time
    - Problem 235: BST-specific, O(h) time
    - Same problem but different constraints allow optimization

13. IMPLEMENTATION VARIATIONS:
    - Recursive vs iterative
    - Value comparison vs reference comparison
    - Explicit vs implicit range checking

14. OPTIMIZATION INSIGHTS:
    - BST property eliminates need to search both subtrees
    - Single path traversal instead of full tree exploration
    - Early termination when split point found

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is that in a BST, I don't need to explore the entire tree 
    like in the general case. The BST ordering property tells me exactly which 
    direction to go. The LCA is simply the first node where the two target 
    nodes would be placed on different sides of the tree."

16. MISTAKE TO AVOID:
    - Using general binary tree approach without leveraging BST property
    - Not explaining why BST version is more efficient
    - Forgetting to handle ancestor case properly

17. PERFORMANCE DEMONSTRATION:
    - For balanced BST: O(log n) vs O(n) - significant improvement
    - For skewed BST: still O(n) but with better constant factors
    - Space: O(1) possible with iterative vs always O(h) for general
"""
