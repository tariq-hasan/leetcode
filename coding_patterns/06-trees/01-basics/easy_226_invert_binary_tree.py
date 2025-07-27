"""
LeetCode 226: Invert Binary Tree

Problem: Given the root of a binary tree, invert the tree, and return its root.
Invert means to swap the left and right children of every node in the tree.

This is the famous problem that caused controversy when asked at Google interviews.
Max Howell (creator of Homebrew) was rejected for not solving this on a whiteboard.

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
    def invertTree(self, root: TreeNode) -> TreeNode:
        """
        OPTIMAL RECURSIVE SOLUTION - Most elegant and preferred
        
        Simple divide-and-conquer approach:
        1. Base case: if node is None, return None
        2. Recursively invert left and right subtrees
        3. Swap the (now inverted) subtrees
        4. Return the root
        
        Time: O(n), Space: O(h)
        """
        # Base case: empty tree
        if not root:
            return None
        
        # Recursively invert both subtrees
        left_inverted = self.invertTree(root.left)
        right_inverted = self.invertTree(root.right)
        
        # Swap the children
        root.left = right_inverted
        root.right = left_inverted
        
        return root
    
    def invertTreeConcise(self, root: TreeNode) -> TreeNode:
        """
        CONCISE RECURSIVE - One-liner approach
        
        Same logic but more compact using tuple assignment
        """
        if not root:
            return None
        
        # Swap and recursively invert in one line
        root.left, root.right = self.invertTreeConcise(root.right), self.invertTreeConcise(root.left)
        
        return root
    
    def invertTreeIterativeBFS(self, root: TreeNode) -> TreeNode:
        """
        ITERATIVE BFS SOLUTION - Level-by-level inversion
        
        Use queue to process nodes level by level
        For each node, swap its children and add them to queue
        
        Time: O(n), Space: O(w) where w is max width
        """
        if not root:
            return None
        
        from collections import deque
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            # Swap children
            node.left, node.right = node.right, node.left
            
            # Add children to queue for processing
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return root
    
    def invertTreeIterativeDFS(self, root: TreeNode) -> TreeNode:
        """
        ITERATIVE DFS SOLUTION - Stack-based approach
        
        Use stack to simulate recursion
        For each node, swap children and add to stack
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return None
        
        stack = [root]
        
        while stack:
            node = stack.pop()
            
            # Swap children
            node.left, node.right = node.right, node.left
            
            # Add children to stack for processing
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        
        return root
    
    def invertTreePostorder(self, root: TreeNode) -> TreeNode:
        """
        POSTORDER TRAVERSAL - Bottom-up approach
        
        Invert children first, then swap at current node
        More explicit about traversal order
        
        Time: O(n), Space: O(h)
        """
        def postorder(node):
            if not node:
                return None
            
            # First, invert the subtrees
            left = postorder(node.left)
            right = postorder(node.right)
            
            # Then swap them at current node
            node.left = right
            node.right = left
            
            return node
        
        return postorder(root)
    
    def invertTreePreorder(self, root: TreeNode) -> TreeNode:
        """
        PREORDER TRAVERSAL - Top-down approach
        
        Swap children first, then recursively invert
        
        Time: O(n), Space: O(h)
        """
        if not root:
            return None
        
        # Swap children at current node first
        root.left, root.right = root.right, root.left
        
        # Then recursively invert the subtrees
        self.invertTreePreorder(root.left)
        self.invertTreePreorder(root.right)
        
        return root


# Helper functions for testing
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

def tree_to_list(root):
    """Convert tree back to level-order list for comparison"""
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result

def print_tree(root, level=0, prefix="Root: "):
    """Helper to visualize tree structure"""
    if root:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")

def copy_tree(root):
    """Create a deep copy of the tree"""
    if not root:
        return None
    
    new_root = TreeNode(root.val)
    new_root.left = copy_tree(root.left)
    new_root.right = copy_tree(root.right)
    return new_root

# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        # (original_tree, expected_inverted, description)
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1], "Example from problem"),
        ([2, 1, 3], [2, 3, 1], "Simple three-node tree"),
        ([1], [1], "Single node"),
        ([], [], "Empty tree"),
        ([1, 2], [1, None, 2], "Left child only"),
        ([1, None, 2], [1, 2], "Right child only"),
        ([1, 2, 3, 4, 5, 6, 7], [1, 3, 2, 7, 6, 5, 4], "Perfect binary tree"),
        ([1, 2, None, 3, None, 4], [1, None, 2, None, 3, None, 4], "Left skewed becomes right skewed"),
    ]
    
    print("Testing Invert Binary Tree Solutions:")
    print("=" * 70)
    
    for i, (original_vals, expected_vals, desc) in enumerate(test_cases):
        print(f"Test {i+1}: {desc}")
        print(f"  Original: {original_vals}")
        print(f"  Expected: {expected_vals}")
        
        # Test different approaches on copies of the tree
        trees = {
            "Recursive": build_tree(original_vals),
            "Concise": build_tree(original_vals),
            "BFS": build_tree(original_vals),
            "DFS": build_tree(original_vals),
            "Postorder": build_tree(original_vals)
        }
        
        if original_vals:
            print("  Original structure:")
            print_tree(trees["Recursive"])
        
        # Apply different inversion methods
        results = {}
        results["Recursive"] = sol.invertTree(trees["Recursive"])
        results["Concise"] = sol.invertTreeConcise(trees["Concise"])
        results["BFS"] = sol.invertTreeIterativeBFS(trees["BFS"])
        results["DFS"] = sol.invertTreeIterativeDFS(trees["DFS"])
        results["Postorder"] = sol.invertTreePostorder(trees["Postorder"])
        
        # Convert results to lists for comparison
        result_lists = {name: tree_to_list(tree) for name, tree in results.items()}
        
        # Check if all methods produce expected result
        all_correct = all(result == expected_vals for result in result_lists.values())
        status = "✓" if all_correct else "✗"
        
        print(f"  Results: {status}")
        for method, result_list in result_lists.items():
            method_status = "✓" if result_list == expected_vals else "✗"
            print(f"    {method}: {method_status} {result_list}")
        
        if results["Recursive"] and original_vals:
            print("  Inverted structure:")
            print_tree(results["Recursive"])
        
        print()

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Invert = swap left and right children of EVERY node
   - Also called "mirror" the binary tree
   - The operation should be applied recursively to all nodes

2. APPROACH COMPARISON:
   - Recursive: Most elegant and natural
   - Iterative BFS: Level-by-level processing
   - Iterative DFS: Stack-based simulation of recursion
   - Different traversal orders: Pre/post-order variations

3. KEY INSIGHT:
   - Simple operation: just swap left and right for each node
   - Can be done top-down (preorder) or bottom-up (postorder)
   - Order doesn't matter since we're swapping at each node

4. COMPLEXITY ANALYSIS:
   - Time: O(n) - must visit every node exactly once
   - Space: O(h) for recursion stack, O(w) for BFS queue
   - Best case: O(log n) for balanced tree
   - Worst case: O(n) for skewed tree

5. IMPLEMENTATION CHOICES:
   - Recursive: Clean, intuitive, preferred for interviews
   - BFS: Good for showing level-order understanding
   - DFS: Shows stack/recursion equivalence
   - Choose recursive unless asked for iterative

6. EDGE CASES:
   - Empty tree (return None)
   - Single node (return as-is)
   - Tree with only left children (becomes only right)
   - Tree with only right children (becomes only left)
   - Perfect binary tree (complete inversion)

7. COMMON MISTAKES:
   - Forgetting to return the root
   - Not handling None nodes properly
   - Swapping values instead of children (wrong interpretation)
   - Modifying tree structure incorrectly

8. VARIATIONS TO DISCUSS:
   - "What if we wanted to create a new tree instead of modifying?" → Copy nodes
   - "What if nodes had parent pointers?" → Update parent references
   - "Can you do this without recursion?" → Show iterative solutions

9. FOLLOW-UP QUESTIONS:
   - "Is the tree still a BST after inversion?" → No, unless symmetric
   - "How would you verify the inversion is correct?" → Compare with expected
   - "What's the iterative approach?" → Show BFS/DFS stack solutions
   - "Can you do this in constant space?" → Not possible, need O(h) space

10. RELATED PROBLEMS:
    - Symmetric Tree (101) - checking mirror property
    - Same Tree (100) - comparing tree structures
    - Maximum Depth (104) - tree traversal foundation
    - Binary Tree Level Order Traversal (102) - BFS patterns

HISTORICAL NOTE:
This problem became famous when Max Howell (creator of Homebrew) tweeted:
"Google: 90% of our engineers use the software you wrote (Homebrew), but you can't 
invert a binary tree on a whiteboard so f*** off."

This sparked debate about interview practices, but the problem itself is actually 
quite reasonable for testing basic tree manipulation skills.

INTERVIEW STRATEGY:
1. Start with the simple recursive approach - it's the most elegant
2. Explain the logic: "swap children, then recursively invert subtrees"
3. Walk through a small example step by step
4. Mention iterative alternatives exist if time permits
5. Code cleanly and handle edge cases (None root)
6. Test with simple examples

The key is to show you understand basic tree manipulation and recursion.
This problem is more about coding cleanly under pressure than algorithmic complexity.
"""
