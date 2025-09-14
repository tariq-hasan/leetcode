# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import List, Optional

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        BFS Approach using Queue (Most Common Interview Solution)
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(w) where w is maximum width of tree
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level_nodes = []
            
            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                level_nodes.append(node.val)
                
                # Add children to queue for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level_nodes)
        
        return result

    def levelOrderDFS(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        DFS Approach (Alternative solution to show depth of understanding)
        
        Time Complexity: O(n)
        Space Complexity: O(h) where h is height of tree (recursion stack)
        """
        if not root:
            return []
        
        result = []
        
        def dfs(node, level):
            if not node:
                return
            
            # If this is the first node at this level, create new list
            if level == len(result):
                result.append([])
            
            # Add current node to its level
            result[level].append(node.val)
            
            # Recursively process left and right children
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        
        dfs(root, 0)
        return result

# Test cases for interview discussion
def test_solutions():
    # Test Case 1: [3,9,20,null,null,15,7]
    #     3
    #    / \
    #   9  20
    #     /  \
    #    15   7
    # Expected: [[3],[9,20],[15,7]]
    
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20)
    root1.right.left = TreeNode(15)
    root1.right.right = TreeNode(7)
    
    # Test Case 2: [1]
    # Expected: [[1]]
    root2 = TreeNode(1)
    
    # Test Case 3: []
    # Expected: []
    root3 = None
    
    solution = Solution()
    
    print("BFS Results:")
    print(f"Test 1: {solution.levelOrder(root1)}")  # [[3],[9,20],[15,7]]
    print(f"Test 2: {solution.levelOrder(root2)}")  # [[1]]
    print(f"Test 3: {solution.levelOrder(root3)}")  # []
    
    print("\nDFS Results:")
    print(f"Test 1: {solution.levelOrderDFS(root1)}")  # [[3],[9,20],[15,7]]
    print(f"Test 2: {solution.levelOrderDFS(root2)}")  # [[1]]
    print(f"Test 3: {solution.levelOrderDFS(root3)}")  # []

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. APPROACH EXPLANATION:
   - BFS is the natural choice since we want to process nodes level by level
   - Use queue to maintain FIFO order for each level
   - Track level size to know when to move to next level

2. EDGE CASES TO MENTION:
   - Empty tree (root is None)
   - Single node tree
   - Skewed tree (all nodes on one side)

3. FOLLOW-UP QUESTIONS YOU MIGHT GET:
   - "Can you do this without a queue?" → Show DFS solution
   - "How would you do right-to-left traversal?" → Reverse each level or use deque
   - "What if tree is very wide?" → Discuss space complexity implications

4. COMPLEXITY ANALYSIS:
   - Time: O(n) - visit each node exactly once
   - Space: O(w) where w is maximum width, worst case O(n) for complete binary tree

5. ALTERNATIVE IMPLEMENTATIONS:
   - Using list instead of deque (less efficient due to O(n) pop(0))
   - DFS with level parameter (recursive approach)
   - Two queues alternating between levels
"""
