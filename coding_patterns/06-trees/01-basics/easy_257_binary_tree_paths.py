"""
LeetCode 257. Binary Tree Paths
Problem: Given the root of a binary tree, return all root-to-leaf paths in any order.
A leaf is a node with no children.

Example:
Input: root = [1,2,3,null,5]
       1
      / \
     2   3
      \
       5
Output: ["1->2->5","1->3"]

Key Insights:
1. This is a DFS traversal problem with path tracking
2. Need to build path as we go down and backtrack when going up
3. A leaf node (no children) marks the end of a path
4. Multiple approaches: DFS with backtracking, DFS with string building, BFS
"""

from typing import List, Optional
from collections import deque

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        """
        Approach 1: DFS with Backtracking (Most Common Interview Solution)
        Time: O(N * H) where N is number of nodes, H is height (for string operations)
        Space: O(H) for recursion stack
        
        This is the cleanest and most intuitive approach for interviews.
        """
        if not root:
            return []
        
        result = []
        path = []
        
        def dfs(node):
            if not node:
                return
            
            # Add current node to path
            path.append(str(node.val))
            
            # If it's a leaf node, add path to result
            if not node.left and not node.right:
                result.append("->".join(path))
            else:
                # Continue DFS on children
                dfs(node.left)
                dfs(node.right)
            
            # Backtrack: remove current node from path
            path.pop()
        
        dfs(root)
        return result

    def binaryTreePaths_v2(self, root: Optional[TreeNode]) -> List[str]:
        """
        Approach 2: DFS with String Parameter (Memory Efficient)
        Time: O(N * H)
        Space: O(H) for recursion stack
        
        Pass the path as string parameter instead of maintaining a list.
        """
        if not root:
            return []
        
        result = []
        
        def dfs(node, path):
            if not node:
                return
            
            # Build current path
            current_path = path + str(node.val)
            
            # If it's a leaf node, add to result
            if not node.left and not node.right:
                result.append(current_path)
            else:
                # Continue with children, adding arrow
                current_path += "->"
                dfs(node.left, current_path)
                dfs(node.right, current_path)
        
        dfs(root, "")
        return result

    def binaryTreePaths_v3(self, root: Optional[TreeNode]) -> List[str]:
        """
        Approach 3: BFS with Queue (Iterative)
        Time: O(N * H)
        Space: O(N) for queue storage
        
        Good alternative approach using BFS instead of DFS.
        """
        if not root:
            return []
        
        result = []
        # Queue stores (node, path_so_far)
        queue = deque([(root, str(root.val))])
        
        while queue:
            node, path = queue.popleft()
            
            # If it's a leaf node, add path to result
            if not node.left and not node.right:
                result.append(path)
            else:
                # Add children to queue with extended path
                if node.left:
                    queue.append((node.left, path + "->" + str(node.left.val)))
                if node.right:
                    queue.append((node.right, path + "->" + str(node.right.val)))
        
        return result

    def binaryTreePaths_v4(self, root: Optional[TreeNode]) -> List[str]:
        """
        Approach 4: DFS with List Parameter (Alternative)
        Time: O(N * H)
        Space: O(H)
        
        Similar to approach 1 but passes list as parameter instead of using class variable.
        """
        def dfs(node, path, result):
            if not node:
                return
            
            path.append(str(node.val))
            
            if not node.left and not node.right:
                result.append("->".join(path))
            else:
                dfs(node.left, path, result)
                dfs(node.right, path, result)
            
            path.pop()  # backtrack
        
        if not root:
            return []
        
        result = []
        dfs(root, [], result)
        return result

    def binaryTreePaths_v5(self, root: Optional[TreeNode]) -> List[str]:
        """
        Approach 5: Using Stack (Iterative DFS)
        Time: O(N * H)
        Space: O(N)
        
        Iterative version using explicit stack.
        """
        if not root:
            return []
        
        result = []
        # Stack stores (node, path_list)
        stack = [(root, [str(root.val)])]
        
        while stack:
            node, path = stack.pop()
            
            # If it's a leaf node, add path to result
            if not node.left and not node.right:
                result.append("->".join(path))
            else:
                # Add children to stack with extended path
                if node.right:
                    stack.append((node.right, path + [str(node.right.val)]))
                if node.left:
                    stack.append((node.left, path + [str(node.left.val)]))
        
        return result

# Helper function to build tree from list representation
def build_tree(values):
    """Build tree from leetcode array representation"""
    if not values:
        return None
    
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
    
    # Test case 1: [1,2,3,null,5]
    root1 = build_tree([1, 2, 3, None, 5])
    print("Test case 1: [1,2,3,null,5]")
    print("Expected: ['1->2->5', '1->3']")
    print("DFS with backtracking:", solution.binaryTreePaths(root1))
    print("DFS with string:", solution.binaryTreePaths_v2(root1))
    print("BFS:", solution.binaryTreePaths_v3(root1))
    print()
    
    # Test case 2: [1]
    root2 = build_tree([1])
    print("Test case 2: [1]")
    print("Expected: ['1']")
    print("Result:", solution.binaryTreePaths(root2))
    print()
    
    # Test case 3: [1,2,3,4,5]
    root3 = build_tree([1, 2, 3, 4, 5])
    print("Test case 3: [1,2,3,4,5]")
    print("Result:", solution.binaryTreePaths(root3))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Analysis:
   - Need to find ALL paths from root to leaf nodes
   - Path should be represented as string with "->" separator
   - This is a classic tree traversal with path tracking problem

2. Key Insights:
   - A leaf node has no children (both left and right are None)
   - Need to track the path from root to current node
   - When we reach a leaf, add the current path to results
   - Backtracking is important to avoid affecting other paths

3. Approach Selection:
   - DFS with backtracking (Approach 1) is most intuitive and commonly expected
   - String parameter approach (Approach 2) is memory efficient
   - BFS approach (Approach 3) shows alternative thinking
   - Choose based on your comfort and interviewer preference

4. Edge Cases:
   - Empty tree (root is None)
   - Single node tree (root is leaf)
   - Tree with only left children (linked list structure)
   - Tree with only right children
   - Balanced binary tree

5. Time/Space Complexity:
   - Time: O(N * H) where N = number of nodes, H = height of tree
     * The H factor comes from string operations (joining path)
   - Space: O(H) for recursion stack in DFS approaches
   - Space: O(N) for BFS approach due to queue storage

6. Common Mistakes:
   - Forgetting to backtrack (removing node from path)
   - Not checking if node is leaf correctly
   - String concatenation inefficiency
   - Not handling empty tree case

7. Follow-up Questions:
   - What if we want paths with specific sum?
   - What if we want only the longest path?
   - How to modify for paths between any two nodes?
   - What about paths in a graph with cycles?

RECOMMENDED APPROACH FOR INTERVIEW:
- Start with Approach 1 (DFS with backtracking) as it's most intuitive
- Explain the backtracking clearly - why we need to remove node after processing
- Walk through the example step by step
- Mention alternative approaches if you have time
- Always test with edge cases like single node tree
"""
