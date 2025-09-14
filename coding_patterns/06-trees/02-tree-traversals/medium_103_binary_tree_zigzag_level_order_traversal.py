# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import List, Optional

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        BFS with Alternating Direction (Most Intuitive Solution)
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(w) where w is maximum width of tree
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        left_to_right = True  # Direction flag
        
        while queue:
            level_size = len(queue)
            level_nodes = []
            
            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                level_nodes.append(node.val)
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Reverse if going right to left
            if not left_to_right:
                level_nodes.reverse()
            
            result.append(level_nodes)
            left_to_right = not left_to_right  # Flip direction
        
        return result

    def zigzagLevelOrderDeque(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        BFS with Deque Manipulation (More Efficient, Interview Plus)
        
        Uses deque to add elements in correct order without reversing
        Time Complexity: O(n)
        Space Complexity: O(w)
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        left_to_right = True
        
        while queue:
            level_size = len(queue)
            level_nodes = deque()  # Use deque for current level
            
            for _ in range(level_size):
                node = queue.popleft()
                
                # Add to appropriate end based on direction
                if left_to_right:
                    level_nodes.append(node.val)
                else:
                    level_nodes.appendleft(node.val)
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(list(level_nodes))
            left_to_right = not left_to_right
        
        return result

    def zigzagLevelOrderDFS(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        DFS Approach (Alternative to show algorithmic flexibility)
        
        Time Complexity: O(n)
        Space Complexity: O(h) where h is height (recursion stack)
        """
        if not root:
            return []
        
        result = []
        
        def dfs(node, level):
            if not node:
                return
            
            # Create new level if needed
            if level == len(result):
                result.append([])
            
            # Add node based on level parity
            if level % 2 == 0:  # Even level: left to right
                result[level].append(node.val)
            else:  # Odd level: right to left
                result[level].insert(0, node.val)
            
            # Recurse on children
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        
        dfs(root, 0)
        return result

    def zigzagLevelOrderTwoStacks(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Two Stacks Approach (Classic Interview Alternative)
        
        Uses two stacks to naturally achieve zigzag pattern
        Time Complexity: O(n)
        Space Complexity: O(w)
        """
        if not root:
            return []
        
        result = []
        current_level = [root]
        left_to_right = True
        
        while current_level:
            level_values = []
            next_level = []
            
            # Process all nodes in current level
            while current_level:
                node = current_level.pop()
                level_values.append(node.val)
                
                # Add children in order that gives us zigzag for next level
                if left_to_right:
                    if node.left:
                        next_level.append(node.left)
                    if node.right:
                        next_level.append(node.right)
                else:
                    if node.right:
                        next_level.append(node.right)
                    if node.left:
                        next_level.append(node.left)
            
            result.append(level_values)
            current_level = next_level
            left_to_right = not left_to_right
        
        return result

# Test cases for interview discussion
def test_solutions():
    # Test Case 1: [3,9,20,null,null,15,7]
    #     3
    #    / \
    #   9  20
    #     /  \
    #    15   7
    # Expected: [[3],[20,9],[15,7]]
    
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20)
    root1.right.left = TreeNode(15)
    root1.right.right = TreeNode(7)
    
    # Test Case 2: [1,2,3,4,null,null,5]
    #       1
    #      / \
    #     2   3
    #    /     \
    #   4       5
    # Expected: [[1],[3,2],[4,5]]
    
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.left = TreeNode(4)
    root2.right.right = TreeNode(5)
    
    # Test Case 3: [1]
    # Expected: [[1]]
    root3 = TreeNode(1)
    
    solution = Solution()
    
    print("BFS with Reverse:")
    print(f"Test 1: {solution.zigzagLevelOrder(root1)}")
    print(f"Test 2: {solution.zigzagLevelOrder(root2)}")
    print(f"Test 3: {solution.zigzagLevelOrder(root3)}")
    
    print("\nBFS with Deque:")
    print(f"Test 1: {solution.zigzagLevelOrderDeque(root1)}")
    print(f"Test 2: {solution.zigzagLevelOrderDeque(root2)}")
    
    print("\nDFS Approach:")
    print(f"Test 1: {solution.zigzagLevelOrderDFS(root1)}")
    print(f"Test 2: {solution.zigzagLevelOrderDFS(root2)}")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Level 0: left to right
   - Level 1: right to left  
   - Level 2: left to right
   - And so on...

2. APPROACH PROGRESSION (Show thinking process):
   a) Start with standard BFS, then reverse odd levels
   b) Optimize by using deque to insert in correct order
   c) Mention DFS alternative if asked
   d) Could discuss two-stacks approach for variety

3. SOLUTION RECOMMENDATION:
   - Lead with BFS + reverse (most readable)
   - Mention deque optimization if they care about efficiency
   - DFS shows you can think recursively about level problems

4. EDGE CASES:
   - Empty tree
   - Single node
   - Perfect binary tree
   - Skewed tree

5. FOLLOW-UP QUESTIONS:
   - "Can you avoid the reverse operation?" → Show deque approach
   - "What about memory optimization?" → Discuss in-place vs creating new arrays
   - "How would you handle very wide trees?" → Discuss space complexity

6. COMPLEXITY ANALYSIS:
   - All solutions: O(n) time
   - Space varies: O(w) for BFS approaches, O(h) for DFS

7. IMPLEMENTATION CHOICE:
   - BFS with reverse: Most intuitive, easy to explain
   - Deque approach: Shows optimization thinking
   - Two stacks: Classic alternative, good for showing different data structure usage
"""
