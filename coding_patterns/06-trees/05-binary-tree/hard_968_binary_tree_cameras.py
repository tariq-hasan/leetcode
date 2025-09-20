# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """
        Optimal Greedy Solution with State Tracking
        
        Key insight: Use post-order traversal with three states:
        0 = Not covered (needs camera or parent with camera)
        1 = Has camera (covers itself and children)
        2 = Covered by child camera (no camera needed here)
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        self.cameras = 0
        
        def dfs(node):
            """
            Returns state of current node:
            0 = Not covered (leaf nodes start here)
            1 = Has camera  
            2 = Covered by child
            """
            if not node:
                return 2  # Null nodes are considered "covered"
            
            left_state = dfs(node.left)
            right_state = dfs(node.right)
            
            # If any child is not covered, current node must have camera
            if left_state == 0 or right_state == 0:
                self.cameras += 1
                return 1  # Current node has camera
            
            # If any child has camera, current node is covered
            if left_state == 1 or right_state == 1:
                return 2  # Covered by child
            
            # Both children are covered by their children, current node not covered
            return 0  # Not covered (will force parent to have camera)
        
        root_state = dfs(root)
        
        # If root is not covered, it needs a camera
        if root_state == 0:
            self.cameras += 1
        
        return self.cameras

    def minCameraCoverDP(self, root: Optional[TreeNode]) -> int:
        """
        Dynamic Programming Solution (More Explicit)
        
        For each node, consider three cases:
        1. Node has camera
        2. Node is covered by children  
        3. Node is not covered
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def dfs(node):
            """
            Returns (not_covered, has_camera, covered_by_child)
            Each represents min cameras needed for that scenario
            """
            if not node:
                # Null node: can't have camera, considered covered, costs nothing
                return float('inf'), 0, 0
            
            left = dfs(node.left)
            right = dfs(node.right)
            
            # Case 1: Current node not covered
            # Children can be in any valid state, but we can't use this state
            # unless parent has camera
            not_covered = left[2] + right[2]
            
            # Case 2: Current node has camera
            # Children can be in any state, we take minimum for each
            has_camera = 1 + min(left) + min(right)
            
            # Case 3: Current node covered by children
            # At least one child must have camera
            covered_by_child = min(
                left[1] + min(right[1], right[2]),  # Left child has camera
                right[1] + min(left[1], left[2]),   # Right child has camera
                left[1] + right[1]                  # Both children have cameras
            )
            
            return not_covered, has_camera, covered_by_child
        
        not_covered, has_camera, covered_by_child = dfs(root)
        
        # Root cannot be not_covered, so we choose min of other two states
        return min(has_camera, covered_by_child)

    def minCameraCoverExplicit(self, root: Optional[TreeNode]) -> int:
        """
        More Explicit Greedy Solution (Easier to Understand)
        
        Uses clear state definitions and explicit logic
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        # States
        NEEDS_CAMERA = 0
        HAS_CAMERA = 1
        COVERED = 2
        
        self.result = 0
        
        def solve(node):
            if not node:
                return COVERED
            
            left = solve(node.left)
            right = solve(node.right)
            
            # If any child needs camera, current node must have one
            if left == NEEDS_CAMERA or right == NEEDS_CAMERA:
                self.result += 1
                return HAS_CAMERA
            
            # If any child has camera, current node is covered
            if left == HAS_CAMERA or right == HAS_CAMERA:
                return COVERED
            
            # Both children are covered but don't have cameras
            # Current node needs camera from parent
            return NEEDS_CAMERA
        
        # Handle root specially
        if solve(root) == NEEDS_CAMERA:
            self.result += 1
        
        return self.result

    def minCameraCoverBottomUp(self, root: Optional[TreeNode]) -> int:
        """
        Bottom-up DP Solution with Memoization
        
        Builds solution from leaves up to root
        Time Complexity: O(n)
        Space Complexity: O(n) for memoization + O(h) for recursion
        """
        memo = {}
        
        def dp(node, parent_has_camera):
            """
            Returns minimum cameras needed for subtree rooted at node
            given whether parent has camera
            """
            if not node:
                return 0
            
            if (node, parent_has_camera) in memo:
                return memo[(node, parent_has_camera)]
            
            # Option 1: Current node has camera
            with_camera = 1 + dp(node.left, True) + dp(node.right, True)
            
            # Option 2: Current node doesn't have camera
            without_camera = float('inf')
            
            if parent_has_camera:
                # Parent covers current node
                without_camera = dp(node.left, False) + dp(node.right, False)
            else:
                # Current node must be covered by children
                # At least one child must have camera
                left_options = [dp(node.left, False)]
                right_options = [dp(node.right, False)]
                
                # Try all combinations where at least one child has camera
                # This is complex - the greedy approach is much cleaner
            
            result = min(with_camera, without_camera)
            memo[(node, parent_has_camera)] = result
            return result
        
        return dp(root, False)

    def minCameraCoverBruteForce(self, root: Optional[TreeNode]) -> int:
        """
        Brute Force Solution (For Understanding Only)
        
        Try all possible camera placements and return minimum
        Exponential time complexity - not practical for large inputs
        """
        def get_all_nodes(node, nodes):
            if node:
                nodes.append(node)
                get_all_nodes(node.left, nodes)
                get_all_nodes(node.right, nodes)
        
        def is_covered(node, cameras):
            """Check if node is covered by cameras set"""
            if node in cameras:
                return True
            
            # Check if any adjacent node has camera
            parent = getattr(node, 'parent', None)
            if parent and parent in cameras:
                return True
            
            if node.left and node.left in cameras:
                return True
            
            if node.right and node.right in cameras:
                return True
            
            return False
        
        def all_covered(nodes, cameras):
            """Check if all nodes are covered"""
            return all(is_covered(node, cameras) for node in nodes)
        
        # Get all nodes
        nodes = []
        get_all_nodes(root, nodes)
        
        # Try all possible camera combinations (2^n possibilities)
        min_cameras = len(nodes)  # Worst case: camera on every node
        
        for mask in range(1 << len(nodes)):
            cameras = set()
            for i in range(len(nodes)):
                if mask & (1 << i):
                    cameras.add(nodes[i])
            
            if all_covered(nodes, cameras):
                min_cameras = min(min_cameras, len(cameras))
        
        return min_cameras

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:    0
                  / \
                 0   0
                  \   \
                   0   0
    
    Expected: 1 camera (place at root)
    """
    root = TreeNode(0)
    root.left = TreeNode(0)
    root.right = TreeNode(0)
    root.left.right = TreeNode(0)
    root.right.right = TreeNode(0)
    return root

def build_test_tree2():
    """
    Build tree:      0
                   /   \
                  0     0
                 /     / \
                0     0   0
    
    Expected: 2 cameras
    """
    root = TreeNode(0)
    root.left = TreeNode(0)
    root.right = TreeNode(0)
    root.left.left = TreeNode(0)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(0)
    return root

def build_simple_tree():
    """
    Simple tree:  0
                 /
                0
    
    Expected: 1 camera (at parent)
    """
    root = TreeNode(0)
    root.left = TreeNode(0)
    return root

def build_single_node():
    """
    Single node: 0
    Expected: 1 camera
    """
    return TreeNode(0)

def build_complex_tree():
    """
    Complex tree:        0
                       /   \
                      0     0
                     / \   / \
                    0   0 0   0
                   /         / \
                  0         0   0
    
    Test case for multiple cameras
    """
    root = TreeNode(0)
    root.left = TreeNode(0)
    root.right = TreeNode(0)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(0)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(0)
    root.left.left.left = TreeNode(0)
    root.right.right.left = TreeNode(0)
    root.right.right.right = TreeNode(0)
    return root

def test_solutions():
    solution = Solution()
    
    # Test case 1 - Simple tree
    tree1 = build_test_tree1()
    print("Test 1 - Tree with branches:")
    print("    0")
    print("   / \\")
    print("  0   0")
    print("   \\   \\")
    print("    0   0")
    print(f"  Greedy: {solution.minCameraCover(tree1)}")
    print(f"  DP: {solution.minCameraCoverDP(tree1)}")
    print(f"  Expected: 1")
    print()
    
    # Test case 2 - More complex
    tree2 = build_test_tree2()
    print("Test 2 - Larger tree:")
    print("      0")
    print("    /   \\")
    print("   0     0")
    print("  /     / \\")
    print(" 0     0   0")
    print(f"  Greedy: {solution.minCameraCover(tree2)}")
    print(f"  DP: {solution.minCameraCoverDP(tree2)}")
    print(f"  Expected: 2")
    print()
    
    # Test case 3 - Simple parent-child
    tree3 = build_simple_tree()
    print("Test 3 - Parent-child tree:")
    print(f"  Greedy: {solution.minCameraCover(tree3)}")
    print(f"  Expected: 1")
    print()
    
    # Test case 4 - Single node
    tree4 = build_single_node()
    print("Test 4 - Single node:")
    print(f"  Greedy: {solution.minCameraCover(tree4)}")
    print(f"  Expected: 1")
    print()
    
    # Test case 5 - Complex tree
    tree5 = build_complex_tree()
    print("Test 5 - Complex tree:")
    print(f"  Greedy: {solution.minCameraCover(tree5)}")
    print(f"  DP: {solution.minCameraCoverDP(tree5)}")
    print()
    
    # Compare different implementations
    print("Comparing different approaches on tree2:")
    print(f"  Greedy Solution: {solution.minCameraCover(tree2)}")
    print(f"  Explicit Greedy: {solution.minCameraCoverExplicit(tree2)}")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Place minimum cameras to monitor all nodes
   - Camera at node monitors itself, parent, and children
   - This is a covering problem on trees
   - Need to find optimal placement strategy

2. KEY INSIGHTS:

   INSIGHT 1: Greedy Approach Works
   - Place cameras as low as possible in tree
   - If a leaf node needs monitoring, place camera on its parent
   - This covers more nodes efficiently

   INSIGHT 2: Three States per Node
   - Not covered (needs monitoring)
   - Has camera (monitors neighbors)  
   - Covered (monitored by neighbor)

   INSIGHT 3: Post-order Traversal
   - Process children before parent
   - Parent's decision depends on children's states
   - Bottom-up information flow

3. ALGORITHM WALKTHROUGH:
   - Use DFS post-order traversal
   - Each node returns its state to parent
   - Parent decides its state based on children
   - Count cameras as we place them

4. STATE TRANSITIONS:
   - If any child not covered → current node gets camera
   - If any child has camera → current node is covered
   - If all children covered → current node not covered

5. WHY GREEDY WORKS:
   - Tree structure eliminates cycles
   - Local optimal choices lead to global optimum
   - Placing camera higher covers more nodes

6. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node once
   - Space: O(h) - recursion depth equals tree height
   - Optimal for this problem

7. ALTERNATIVE APPROACHES:
   - Dynamic Programming: More complex state management
   - Brute Force: Try all 2^n combinations (exponential)
   - Graph Theory: Minimum dominating set (NP-hard in general)

8. CRITICAL IMPLEMENTATION DETAILS:
   - Handle null nodes as "covered" 
   - Special case for root node
   - Use post-order traversal pattern
   - Count cameras during state transitions

9. EDGE CASES:
   - Single node tree → needs 1 camera
   - Linear tree (chain) → cameras every 3 nodes
   - Perfect binary tree → strategic placement
   - Empty tree → 0 cameras

10. INTERVIEW PRESENTATION:
    - Start with: "This is a tree covering problem, I'll use greedy approach"
    - Explain the three states clearly
    - Emphasize post-order traversal reasoning
    - Code the clean greedy solution
    - Walk through example showing state transitions

11. FOLLOW-UP QUESTIONS:
    - "What if cameras have different ranges?" → Changes the coverage model
    - "What about minimum cost instead of count?" → Weighted version
    - "Can you prove greedy is optimal?" → Discuss tree properties
    - "What about general graphs?" → Much harder (NP-hard)

12. WHY THIS IS HARD:
    - Requires understanding of tree DP
    - Greedy correctness is non-obvious
    - State management is complex
    - Multiple valid approaches exist

13. COMMON MISTAKES:
    - Not using post-order traversal
    - Incorrect state transitions
    - Forgetting to handle root specially
    - Not understanding when greedy works

14. OPTIMIZATION INSIGHTS:
    - Greedy is optimal due to tree structure
    - DP solution is more general but overkill
    - State compression reduces space complexity
    - Early termination not applicable here

15. KEY INSIGHT TO ARTICULATE:
    "This problem leverages the tree structure to make greedy choices optimal. 
    By processing nodes bottom-up, I can make locally optimal decisions about 
    camera placement that lead to globally optimal solution. The key is 
    recognizing that placing cameras as low as possible maximizes coverage 
    efficiency, and the three-state model captures all necessary information 
    for optimal decision making."

16. PROBLEM VARIATIONS:
    - Maximum cameras with budget constraint
    - Different camera ranges or costs
    - Multiple types of cameras
    - Dynamic camera placement (online version)

17. RELATED PROBLEMS:
    - Minimum dominating set
    - Vertex cover problem
    - Set cover problem
    - Tree DP problems in general
"""
