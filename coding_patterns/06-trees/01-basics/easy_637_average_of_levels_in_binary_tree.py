"""
LeetCode 637. Average of Levels in Binary Tree
Problem: Given the root of a binary tree, return the average value of the nodes 
on each level in the form of an array.

Example:
Input: root = [3,9,20,null,null,15,7]
       3
      / \
     9  20
       /  \
      15   7
Output: [3.00000, 14.50000, 11.00000]
Explanation: Level 0: 3, average = 3
             Level 1: (9+20)/2 = 14.5
             Level 2: (15+7)/2 = 11

Key Insights:
1. This is a level-order traversal (BFS) problem
2. Need to process nodes level by level and calculate average for each level
3. Multiple approaches: BFS with queue, DFS with level tracking, two-queue method
4. Watch out for integer overflow when summing large numbers
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
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 1: BFS with Queue (MOST COMMON INTERVIEW SOLUTION)
        Time: O(N) where N is number of nodes
        Space: O(W) where W is maximum width of tree
        
        This is the most intuitive and commonly expected approach.
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level_sum = 0
            
            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Calculate average for current level
            level_average = level_sum / level_size
            result.append(level_average)
        
        return result

    def averageOfLevels_v2(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 2: DFS with Level Tracking
        Time: O(N)
        Space: O(H) where H is height of tree (recursion stack)
        
        Use DFS to collect sums and counts for each level.
        """
        if not root:
            return []
        
        level_sums = []  # level_sums[i] = sum of nodes at level i
        level_counts = []  # level_counts[i] = count of nodes at level i
        
        def dfs(node, level):
            if not node:
                return
            
            # Initialize level data if first time visiting this level
            if level == len(level_sums):
                level_sums.append(0)
                level_counts.append(0)
            
            # Add current node to level sum and count
            level_sums[level] += node.val
            level_counts[level] += 1
            
            # Recurse on children
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        
        dfs(root, 0)
        
        # Calculate averages
        result = []
        for i in range(len(level_sums)):
            result.append(level_sums[i] / level_counts[i])
        
        return result

    def averageOfLevels_v3(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 3: BFS with Two Queues
        Time: O(N)
        Space: O(W)
        
        Use two queues to separate current level and next level.
        """
        if not root:
            return []
        
        result = []
        current_level = deque([root])
        
        while current_level:
            next_level = deque()
            level_sum = 0
            level_count = 0
            
            # Process all nodes in current level
            while current_level:
                node = current_level.popleft()
                level_sum += node.val
                level_count += 1
                
                # Add children to next level
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            
            # Calculate average and move to next level
            result.append(level_sum / level_count)
            current_level = next_level
        
        return result

    def averageOfLevels_v4(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 4: BFS with Level Separator (Using None as marker)
        Time: O(N)
        Space: O(W)
        
        Use None as a level separator in the queue.
        """
        if not root:
            return []
        
        result = []
        queue = deque([root, None])  # None marks end of level
        level_sum = 0
        level_count = 0
        
        while queue:
            node = queue.popleft()
            
            if node is None:
                # End of current level
                if level_count > 0:
                    result.append(level_sum / level_count)
                    level_sum = 0
                    level_count = 0
                
                # Add level separator for next level if queue not empty
                if queue:
                    queue.append(None)
            else:
                # Process current node
                level_sum += node.val
                level_count += 1
                
                # Add children
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return result

    def averageOfLevels_v5(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 5: DFS with Dictionary
        Time: O(N)
        Space: O(H + L) where L is number of levels
        
        Use dictionary to store level information.
        """
        if not root:
            return []
        
        levels = {}  # level -> [sum, count]
        
        def dfs(node, level):
            if not node:
                return
            
            if level not in levels:
                levels[level] = [0, 0]
            
            levels[level][0] += node.val  # sum
            levels[level][1] += 1         # count
            
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        
        dfs(root, 0)
        
        # Calculate averages in level order
        result = []
        for level in sorted(levels.keys()):
            level_sum, level_count = levels[level]
            result.append(level_sum / level_count)
        
        return result

    def averageOfLevels_overflow_safe(self, root: Optional[TreeNode]) -> List[float]:
        """
        Approach 6: Overflow-Safe Version
        Time: O(N)
        Space: O(W)
        
        Handle potential integer overflow by using running average calculation.
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level_sum = 0.0  # Use float to avoid overflow
            
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level_sum / level_size)
        
        return result

# Helper function to build tree from list
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
    
    # Test case 1: [3,9,20,null,null,15,7]
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    print("Test case 1: [3,9,20,null,null,15,7]")
    print("Expected: [3.0, 14.5, 11.0]")
    print("BFS Queue:", solution.averageOfLevels(root1))
    print("DFS Tracking:", solution.averageOfLevels_v2(root1))
    print("Two Queues:", solution.averageOfLevels_v3(root1))
    print()
    
    # Test case 2: [3,9,20,15,7]
    root2 = build_tree([3, 9, 20, 15, 7])
    print("Test case 2: [3,9,20,15,7]")
    print("Expected: [3.0, 14.5, 11.0]")
    print("Result:", solution.averageOfLevels(root2))
    print()
    
    # Test case 3: Single node [1]
    root3 = build_tree([1])
    print("Test case 3: [1]")
    print("Expected: [1.0]")
    print("Result:", solution.averageOfLevels(root3))
    print()
    
    # Test case 4: Complete binary tree [1,2,3,4,5,6,7]
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print("Test case 4: [1,2,3,4,5,6,7]")
    print("Expected: [1.0, 2.5, 5.5]")
    print("Result:", solution.averageOfLevels(root4))
    print()
    
    # Test case 5: Skewed tree [1,2,null,3,null,4]
    root5 = TreeNode(1)
    root5.left = TreeNode(2)
    root5.left.left = TreeNode(3)
    root5.left.left.left = TreeNode(4)
    print("Test case 5: Skewed tree [1,2,null,3,null,4]")
    print("Expected: [1.0, 2.0, 3.0, 4.0]")
    print("Result:", solution.averageOfLevels(root5))

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - Need to calculate average of node values at each level
   - Return results as array where index i = average of level i
   - This is essentially level-order traversal with aggregation

2. Key Insights:
   - This is a classic BFS (level-order traversal) problem
   - Need to process nodes level by level, not just visit them
   - For each level: sum all values, count nodes, calculate average
   - Multiple approaches possible: BFS, DFS, different queue strategies

3. Approach 1 (BFS with Queue) - Most Common:
   - Use queue to store nodes level by level
   - Process exactly len(queue) nodes at each iteration
   - This ensures we handle one complete level at a time
   - Most intuitive and commonly expected by interviewers

4. Approach 2 (DFS with Level Tracking) - Alternative:
   - Use DFS but track which level each node belongs to
   - Collect sums and counts for each level during traversal
   - Calculate averages after traversal completes
   - Good to show you understand both BFS and DFS approaches

5. Edge Cases:
   - Empty tree (root = null) → return empty array
   - Single node tree → return [node.val]
   - Skewed trees (all left or all right)
   - Trees with negative values
   - Very large values (potential overflow)

6. Common Mistakes:
   - Not processing complete levels (mixing nodes from different levels)
   - Integer overflow when summing large values
   - Forgetting to handle empty tree case
   - Using wrong data type for average (int vs float)

7. Time/Space Complexity:
   - Time: O(N) for all approaches (visit each node once)
   - Space: BFS - O(W) where W is maximum width, DFS - O(H) where H is height
   - BFS generally uses more space but is more intuitive for this problem

8. Optimization Considerations:
   - For very large trees, consider overflow protection
   - Could use streaming average calculation to avoid large sums
   - Memory usage: BFS vs DFS trade-offs

9. Follow-up Questions:
   - What if tree has billions of nodes? (streaming approaches)
   - What if we want median instead of average?
   - How to handle overflow for extremely large values?
   - What about weighted averages based on subtree sizes?

RECOMMENDED APPROACH FOR INTERVIEW:
1. Start with Approach 1 (BFS with Queue) - most intuitive
2. Explain level-by-level processing clearly
3. Show how len(queue) gives you exact count of current level nodes
4. Walk through example step by step
5. Handle edge cases (empty tree, single node)
6. Mention DFS alternative if time permits
7. Discuss potential overflow issues for large values

CRITICAL INSIGHT TO COMMUNICATE:
"The key insight is that we need to process nodes level by level, not just 
traverse them. By using len(queue) at the start of each iteration, we know 
exactly how many nodes belong to the current level."

PATTERN RECOGNITION:
This problem is part of the "level-order traversal" pattern. Similar problems:
- Binary Tree Level Order Traversal
- Binary Tree Zigzag Level Order Traversal  
- Binary Tree Right Side View
- Maximum Width of Binary Tree

The template you learn here applies to many other level-based tree problems.
"""
