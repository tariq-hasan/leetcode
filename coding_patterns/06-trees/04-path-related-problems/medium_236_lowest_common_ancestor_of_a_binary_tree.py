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
        Optimal Recursive Solution (Most Elegant and Common)
        
        Key insight: The LCA is the first node where p and q diverge, or one of p/q if 
        one is ancestor of the other.
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        # Base case: if we reach null or find one of the target nodes
        if not root or root == p or root == q:
            return root
        
        # Recursively search in left and right subtrees
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        
        # If both left and right return non-null, current node is LCA
        if left and right:
            return root
        
        # Otherwise, return whichever is non-null (or null if both are null)
        return left if left else right

    def lowestCommonAncestorIterative(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Iterative Solution with Parent Pointers (Alternative Approach)
        
        Build parent mapping, then trace paths from both nodes to root
        Time Complexity: O(n)
        Space Complexity: O(n) for parent mapping
        """
        if not root:
            return None
        
        # Build parent mapping using BFS
        parent = {root: None}
        stack = [root]
        
        # Continue until we've found both p and q
        while p not in parent or q not in parent:
            node = stack.pop()
            
            if node.left:
                parent[node.left] = node
                stack.append(node.left)
            if node.right:
                parent[node.right] = node
                stack.append(node.right)
        
        # Get all ancestors of p
        ancestors = set()
        while p:
            ancestors.add(p)
            p = parent[p]
        
        # Walk up from q until we find common ancestor
        while q not in ancestors:
            q = parent[q]
        
        return q

    def lowestCommonAncestorWithPaths(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Solution with Path Finding (Good for Understanding)
        
        Find paths to both nodes, then compare to find divergence point
        Time Complexity: O(n)
        Space Complexity: O(h) for paths + O(h) for recursion = O(h)
        """
        def find_path(node, target, path):
            """Find path from root to target node"""
            if not node:
                return False
            
            # Add current node to path
            path.append(node)
            
            # If we found the target, return True
            if node == target:
                return True
            
            # Search in left and right subtrees
            if (find_path(node.left, target, path) or 
                find_path(node.right, target, path)):
                return True
            
            # Backtrack if not found
            path.pop()
            return False
        
        # Find paths to both nodes
        path_p, path_q = [], []
        find_path(root, p, path_p)
        find_path(root, q, path_q)
        
        # Find the last common node in both paths
        lca = None
        for i in range(min(len(path_p), len(path_q))):
            if path_p[i] == path_q[i]:
                lca = path_p[i]
            else:
                break
        
        return lca

    def lowestCommonAncestorFunctional(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Functional Programming Style (Clean but less efficient)
        
        More explicit about what each recursive call returns
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def lca_helper(node):
            """Returns (found_p, found_q, lca_node)"""
            if not node:
                return False, False, None
            
            # Check current node
            is_p = node == p
            is_q = node == q
            
            # Search subtrees
            left_p, left_q, left_lca = lca_helper(node.left)
            right_p, right_q, right_lca = lca_helper(node.right)
            
            # If LCA already found in subtree, return it
            if left_lca:
                return True, True, left_lca
            if right_lca:
                return True, True, right_lca
            
            # Check if current node is LCA
            found_p = is_p or left_p or right_p
            found_q = is_q or left_q or right_q
            
            if found_p and found_q:
                return True, True, node
            
            return found_p, found_q, None
        
        _, _, lca = lca_helper(root)
        return lca

    def lowestCommonAncestorCounts(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Alternative Recursive with Count Tracking
        
        Track how many target nodes found in each subtree
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def lca_helper(node):
            """Returns (count_of_targets_found, lca_if_found)"""
            if not node:
                return 0, None
            
            # Count for current node
            count = 0
            if node == p or node == q:
                count = 1
            
            # Get counts from subtrees
            left_count, left_lca = lca_helper(node.left)
            right_count, right_lca = lca_helper(node.right)
            
            # If LCA already found, return it
            if left_lca:
                return 2, left_lca
            if right_lca:
                return 2, right_lca
            
            # Total count including current node
            total_count = count + left_count + right_count
            
            # If we found both targets, current node is LCA
            if total_count == 2:
                return 2, node
            
            return total_count, None
        
        _, lca = lca_helper(root)
        return lca

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:        3
                     /   \
                    5     1
                   / \   / \
                  6   2 0   8
                     / \
                    7   4
    
    Various test cases:
    - LCA(5,1) = 3 (root)
    - LCA(5,4) = 5 (one is ancestor of other)
    - LCA(6,4) = 5 (common subtree root)
    """
    nodes = {}
    for val in [3,5,1,6,2,0,8,7,4]:
        nodes[val] = TreeNode(val)
    
    nodes[3].left = nodes[5]
    nodes[3].right = nodes[1]
    nodes[5].left = nodes[6]
    nodes[5].right = nodes[2]
    nodes[1].left = nodes[0]
    nodes[1].right = nodes[8]
    nodes[2].left = nodes[7]
    nodes[2].right = nodes[4]
    
    return nodes[3], nodes

def build_simple_tree():
    """
    Simple tree:  1
                 / \
                2   3
    """
    nodes = {}
    for val in [1,2,3]:
        nodes[val] = TreeNode(val)
    
    nodes[1].left = nodes[2]
    nodes[1].right = nodes[3]
    
    return nodes[1], nodes

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Complex tree
    root1, nodes1 = build_test_tree1()
    print("Test 1 - Complex tree:")
    print("       3")
    print("     /   \\")
    print("    5     1")
    print("   / \\   / \\")
    print("  6   2 0   8")
    print("     / \\")
    print("    7   4")
    print()
    
    # Test LCA(5,1) = 3
    lca1 = solution.lowestCommonAncestor(root1, nodes1[5], nodes1[1])
    print(f"LCA(5,1) = {lca1.val} (Expected: 3)")
    
    # Test LCA(5,4) = 5  
    lca2 = solution.lowestCommonAncestor(root1, nodes1[5], nodes1[4])
    print(f"LCA(5,4) = {lca2.val} (Expected: 5)")
    
    # Test LCA(6,4) = 5
    lca3 = solution.lowestCommonAncestor(root1, nodes1[6], nodes1[4])
    print(f"LCA(6,4) = {lca3.val} (Expected: 5)")
    
    # Test LCA(6,7) = 5
    lca4 = solution.lowestCommonAncestor(root1, nodes1[6], nodes1[7])
    print(f"LCA(6,7) = {lca4.val} (Expected: 5)")
    print()
    
    # Test case 2 - Simple tree
    root2, nodes2 = build_simple_tree()
    print("Test 2 - Simple tree [1,2,3]:")
    lca5 = solution.lowestCommonAncestor(root2, nodes2[2], nodes2[3])
    print(f"LCA(2,3) = {lca5.val} (Expected: 1)")
    print()
    
    # Test iterative solution
    print("Testing iterative solution:")
    lca6 = solution.lowestCommonAncestorIterative(root1, nodes1[6], nodes1[4])
    print(f"Iterative LCA(6,4) = {lca6.val} (Expected: 5)")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Find the deepest node that is ancestor of both p and q
   - Both p and q are guaranteed to exist in the tree
   - All node values are unique
   - Nodes can be ancestors of themselves

2. KEY INSIGHTS FOR OPTIMAL SOLUTION:

   INSIGHT 1: Bottom-up approach
   - Use post-order traversal (process children before parent)
   - Information flows up from leaves to root
   
   INSIGHT 2: Three cases at each node:
   - Found both p and q in different subtrees → current node is LCA
   - Found both in same subtree → LCA is deeper, pass it up
   - Found neither or only one → pass up what we found

   INSIGHT 3: Early termination
   - If we find p or q, we can return immediately
   - This handles the case where one node is ancestor of the other

3. SOLUTION WALKTHROUGH:
   - Base case: null or found target → return node
   - Recursive case: search both subtrees
   - Decision logic: if found in both subtrees → current is LCA
   - Otherwise: return whichever subtree found something

4. WHY THIS SOLUTION IS ELEGANT:
   - Single pass through tree
   - Minimal state tracking
   - Natural recursive structure
   - Handles all edge cases automatically

5. ALTERNATIVE APPROACHES:
   - Parent pointers: Build parent map, trace upward
   - Path finding: Find paths to both nodes, compare
   - Both are correct but less elegant than recursive

6. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node at most once
   - Space: O(h) - recursion depth equals tree height
   - Optimal for this problem

7. EDGE CASES:
   - One node is ancestor of the other
   - Nodes are in different subtrees
   - Nodes are at different depths
   - Root is one of the target nodes

8. INTERVIEW PRESENTATION:
   - Start with problem clarification
   - Explain the bottom-up insight
   - Code the recursive solution
   - Walk through example with tree diagram
   - Discuss complexity and alternatives

9. FOLLOW-UP QUESTIONS:
   - "What if nodes might not exist?" → Need to verify existence first
   - "What about BST version?" → Can use BST property for O(h) solution
   - "Multiple nodes to find LCA of?" → Generalize the counting approach
   - "What if tree is very large?" → Discuss iterative vs recursive trade-offs

10. COMMON MISTAKES:
    - Trying to search top-down instead of bottom-up
    - Not handling the case where one node is ancestor of other
    - Overcomplicating with unnecessary state tracking
    - Forgetting base cases

11. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests recursive thinking
    - Multiple valid approaches (shows problem-solving flexibility)
    - Clean vs complex implementations
    - Understanding of tree traversal patterns

12. IMPLEMENTATION TIPS:
    - The recursive solution is most elegant - lead with this
    - Explain the "return early on finding target" insight
    - Show how the solution naturally handles all edge cases
    - Mention alternatives if they ask for different approaches

13. KEY INSIGHT TO ARTICULATE:
    "The LCA is the first node where our search paths diverge, or one of the 
    target nodes if one is an ancestor of the other. By searching bottom-up 
    and returning early when we find targets, the algorithm naturally finds 
    this divergence point."
"""
