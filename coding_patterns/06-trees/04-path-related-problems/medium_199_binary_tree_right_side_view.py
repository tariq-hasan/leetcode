# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from typing import List, Optional

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        BFS Level-Order Traversal (Most Intuitive Solution)
        
        Key insight: The rightmost node at each level is what we see from right side
        Process each level and take the last node
        
        Time Complexity: O(n) where n is number of nodes
        Space Complexity: O(w) where w is maximum width of tree
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            
            # Process all nodes at current level
            for i in range(level_size):
                node = queue.popleft()
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                
                # If this is the last node in the level, it's visible from right
                if i == level_size - 1:
                    result.append(node.val)
        
        return result

    def rightSideViewDFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        DFS Approach - Right First Traversal (Optimal Space Solution)
        
        Key insight: Visit right subtree first, track the first node at each level
        The first node we encounter at each depth is the rightmost visible one
        
        Time Complexity: O(n)
        Space Complexity: O(h) where h is height of tree (better than BFS for tall trees)
        """
        if not root:
            return []
        
        result = []
        
        def dfs(node, depth):
            if not node:
                return
            
            # If this is the first node we've seen at this depth (coming from right),
            # it's the rightmost node at this level
            if depth == len(result):
                result.append(node.val)
            
            # Visit right first, then left
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)
        
        dfs(root, 0)
        return result

    def rightSideViewDFSLeftFirst(self, root: Optional[TreeNode]) -> List[int]:
        """
        DFS Alternative - Left First with Overwriting
        
        Visit left first, but always overwrite with right nodes at same level
        Shows different thinking approach
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return []
        
        result = []
        
        def dfs(node, depth):
            if not node:
                return
            
            # Extend result if we've reached a new depth
            if depth == len(result):
                result.append(node.val)
            else:
                # Overwrite with current node (right nodes will overwrite left)
                result[depth] = node.val
            
            # Visit left first, then right (right will overwrite left)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)
        
        dfs(root, 0)
        return result

    def rightSideViewIterativeDFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Iterative DFS with Stack (Non-recursive DFS alternative)
        
        Use stack to simulate right-first DFS traversal
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return []
        
        result = []
        stack = [(root, 0)]  # (node, depth)
        
        while stack:
            node, depth = stack.pop()
            
            # If first node at this depth, add to result
            if depth == len(result):
                result.append(node.val)
            
            # Add children to stack (left first so right is processed first)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        
        return result

    def rightSideViewReverseLevelOrder(self, root: Optional[TreeNode]) -> List[int]:
        """
        Alternative BFS - Process Each Level Separately
        
        More explicit level processing, easier to understand
        Time Complexity: O(n)
        Space Complexity: O(w)
        """
        if not root:
            return []
        
        result = []
        current_level = [root]
        
        while current_level:
            # The last node in current level is rightmost
            result.append(current_level[-1].val)
            
            next_level = []
            # Collect all nodes for next level
            for node in current_level:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            
            current_level = next_level
        
        return result

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:      1
                   /   \
                  2     3
                   \     \
                    5     4
    
    Right side view: [1, 3, 4]
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    return root

def build_test_tree2():
    """
    Build tree:    1
                    \
                     3
    
    Right side view: [1, 3]
    """
    root = TreeNode(1)
    root.right = TreeNode(3)
    return root

def build_test_tree3():
    """
    Build tree:      1
                   /   \
                  2     3
                 /     /
                4     5
               /
              6
    
    Right side view: [1, 3, 5, 6]
    Note: At depth 3, only left side has nodes, so we see 6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(5)
    root.left.left.left = TreeNode(6)
    return root

def build_test_tree4():
    """
    Single node: 1
    Right side view: [1]
    """
    return TreeNode(1)

def test_solutions():
    solution = Solution()
    
    # Test case 1
    tree1 = build_test_tree1()
    print("Test 1 - Standard tree:")
    print("      1")
    print("    /   \\")
    print("   2     3")
    print("    \\     \\")
    print("     5     4")
    print(f"  BFS: {solution.rightSideView(tree1)}")
    print(f"  DFS: {solution.rightSideViewDFS(tree1)}")
    print(f"  Expected: [1, 3, 4]")
    print()
    
    # Test case 2
    tree2 = build_test_tree2()
    print("Test 2 - Right skewed tree:")
    print(f"  BFS: {solution.rightSideView(tree2)}")
    print(f"  Expected: [1, 3]")
    print()
    
    # Test case 3
    tree3 = build_test_tree3()
    print("Test 3 - Mixed tree (left node visible at deepest level):")
    print(f"  BFS: {solution.rightSideView(tree3)}")
    print(f"  DFS: {solution.rightSideViewDFS(tree3)}")
    print(f"  Expected: [1, 3, 5, 6]")
    print()
    
    # Test case 4
    tree4 = build_test_tree4()
    print("Test 4 - Single node:")
    print(f"  BFS: {solution.rightSideView(tree4)}")
    print(f"  Expected: [1]")
    print()
    
    # Edge case
    print("Test 5 - Empty tree:")
    print(f"  Result: {solution.rightSideView(None)}")
    print(f"  Expected: []")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - Imagine standing to the right of the tree, looking left
   - At each level, you can only see the rightmost node
   - Need to return these rightmost nodes from top to bottom
   - Key insight: "rightmost" means last node encountered at each level

2. TWO MAIN APPROACHES:

   APPROACH 1 - BFS (Level-Order):
   - Process tree level by level
   - Take the last node from each level
   - Most intuitive and easy to explain
   - Space: O(w) where w is width

   APPROACH 2 - DFS (Right-First):
   - Traverse right subtree first, then left
   - First node encountered at each depth is rightmost
   - Better space complexity for tall, narrow trees
   - Space: O(h) where h is height

3. SOLUTION CHOICE FOR INTERVIEW:

   START WITH: BFS approach (more intuitive)
   - "I'll process the tree level by level and take the rightmost node from each level"
   - Easy to visualize and explain
   - Shows solid BFS understanding

   OPTIMIZE IF ASKED: DFS approach
   - "For better space complexity, especially with tall trees, I can use DFS"
   - Shows deeper algorithmic thinking

4. KEY INSIGHTS TO MENTION:
   - Rightmost doesn't always mean "right child" - could be left child if no right exists
   - Need to track level/depth to know which nodes are at same level
   - BFS naturally processes by level, DFS needs depth tracking

5. IMPLEMENTATION DETAILS:
   - BFS: Use queue, track level size, take last node in each level
   - DFS: Visit right first, only add node if it's first at that depth
   - Handle empty tree edge case

6. EDGE CASES TO DISCUSS:
   - Empty tree → []
   - Single node → [that node]
   - Right-skewed tree → all right nodes
   - Left-skewed tree → all left nodes (but they're "rightmost" at their levels)
   - Mixed tree where left nodes are visible at some levels

7. TIME/SPACE COMPLEXITY:
   - Time: O(n) for both approaches - visit every node
   - Space: BFS O(w), DFS O(h)
   - When to prefer each: BFS for wide trees, DFS for tall trees

8. FOLLOW-UP QUESTIONS:
   - "What about left side view?" → Same logic, visit left first in DFS or take first in BFS
   - "What if we want all visible nodes, not just rightmost?" → Different problem
   - "Can you do it without recursion?" → Show iterative DFS or BFS
   - "How would you handle very wide trees?" → Discuss space complexity

9. WHY THESE SOLUTIONS ARE OPTIMAL:
   - BFS: Natural level processing, easy to understand
   - DFS: Better space for tall trees, elegant recursion
   - Both are O(n) time, which is optimal since we need to identify rightmost at each level

10. INTERVIEW PRESENTATION:
    - Clarify problem: "rightmost visible node at each level"
    - Start with BFS for intuitive explanation
    - Code clean solution with proper edge case handling
    - Walk through example showing level processing
    - Mention DFS alternative and its space advantage
    - Discuss when to use which approach

11. COMMON MISTAKES TO AVOID:
    - Assuming rightmost always means right child
    - Forgetting to handle empty tree
    - Not properly tracking levels in DFS
    - Overcomplicating the level processing in BFS

12. VARIATION AWARENESS:
    - This problem tests level-order thinking
    - Similar to other "level-based" problems like zigzag traversal
    - Foundation for more complex tree view problems
"""
