# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

from collections import deque
from typing import Optional

class Solution:
    def connect(self, root: Optional[Node]) -> Optional[Node]:
        """
        Optimal O(1) Space Solution - Level by Level Processing
        
        Key insight: Use a "dummy" node to track the start of next level
        and maintain connections without extra space.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not root:
            return root
        
        # Start with root level
        curr = root
        
        while curr:
            # dummy node to help build the next level
            dummy = Node(0)
            prev = dummy
            
            # Traverse current level using next pointers
            while curr:
                # Connect left child if exists
                if curr.left:
                    prev.next = curr.left
                    prev = prev.next
                
                # Connect right child if exists
                if curr.right:
                    prev.next = curr.right
                    prev = prev.next
                
                # Move to next node in current level
                curr = curr.next
            
            # Move to the next level (first node of next level)
            curr = dummy.next
        
        return root

    def connectBFS(self, root: Optional[Node]) -> Optional[Node]:
        """
        BFS Approach with Queue (More intuitive but uses extra space)
        
        Standard level-order traversal approach
        Time Complexity: O(n)
        Space Complexity: O(w) where w is maximum width of tree
        """
        if not root:
            return root
        
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            
            for i in range(level_size):
                node = queue.popleft()
                
                # Connect to next node in same level (if not last in level)
                if i < level_size - 1:
                    node.next = queue[0]  # Peek at next node
                
                # Add children to queue for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return root

    def connectWithPointers(self, root: Optional[Node]) -> Optional[Node]:
        """
        Alternative O(1) Space - Using Two Pointers
        
        Maintain pointers for current level and next level
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not root:
            return root
        
        level_start = root
        
        while level_start:
            curr = level_start
            next_level_start = None
            prev = None
            
            # Process current level
            while curr:
                # Process left child
                if curr.left:
                    if prev:
                        prev.next = curr.left
                    else:
                        next_level_start = curr.left
                    prev = curr.left
                
                # Process right child  
                if curr.right:
                    if prev:
                        prev.next = curr.right
                    else:
                        next_level_start = curr.right
                    prev = curr.right
                
                curr = curr.next
            
            # Move to next level
            level_start = next_level_start
        
        return root

    def connectRecursiveDFS(self, root: Optional[Node]) -> Optional[Node]:
        """
        DFS Recursive Approach (Less optimal due to recursion stack)
        
        Uses recursion to process each level
        Time Complexity: O(n)
        Space Complexity: O(h) where h is height of tree
        """
        if not root:
            return root
        
        # Find the next node in the same level
        def get_next_right_node(node):
            level = node
            while level.next:
                level = level.next
                if level.left:
                    return level.left
                if level.right:
                    return level.right
            return None
        
        # Connect children
        if root.left:
            if root.right:
                root.left.next = root.right
            else:
                root.left.next = get_next_right_node(root)
        
        if root.right:
            root.right.next = get_next_right_node(root)
        
        # Process right subtree first (important!)
        # This ensures next pointers are set before we need them
        self.connectRecursiveDFS(root.right)
        self.connectRecursiveDFS(root.left)
        
        return root

# Utility functions for testing
def print_tree_with_next_pointers(root):
    """Print tree level by level showing next pointers"""
    if not root:
        print("Empty tree")
        return
    
    level = 0
    curr = root
    
    while curr:
        print(f"Level {level}: ", end="")
        level_curr = curr
        next_level_start = None
        
        while level_curr:
            print(f"{level_curr.val}", end="")
            
            # Find next level start if we haven't found it yet
            if not next_level_start:
                if level_curr.left:
                    next_level_start = level_curr.left
                elif level_curr.right:
                    next_level_start = level_curr.right
            
            if level_curr.next:
                print(f" -> {level_curr.next.val}", end="")
            else:
                print(" -> NULL", end="")
            
            if level_curr.next:
                print(", ", end="")
            
            level_curr = level_curr.next
        
        print()
        curr = next_level_start
        level += 1

def build_irregular_tree():
    """Build test case: Irregular binary tree"""
    #         1
    #       /   \
    #      2     3
    #     / \     \
    #    4   5     7
    #   /
    #  8
    
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(7)
    root.left.left.left = Node(8)
    return root

def build_skewed_tree():
    """Build test case: Right-skewed tree"""
    #   1
    #    \
    #     2
    #      \
    #       3
    
    root = Node(1)
    root.right = Node(2)
    root.right.right = Node(3)
    return root

# Test the solutions
def test_solutions():
    print("Test Case 1: Irregular Tree")
    print("         1")
    print("       /   \\")
    print("      2     3")
    print("     / \\     \\")
    print("    4   5     7")
    print("   /")
    print("  8")
    print()
    
    root1 = build_irregular_tree()
    solution = Solution()
    solution.connect(root1)
    print_tree_with_next_pointers(root1)
    print()
    
    print("Test Case 2: Right-skewed Tree")
    print("   1")
    print("    \\")
    print("     2")
    print("      \\")
    print("       3")
    print()
    
    root2 = build_skewed_tree()
    solution.connect(root2)
    print_tree_with_next_pointers(root2)
    print()
    
    print("Test Case 3: BFS Solution on irregular tree")
    root3 = build_irregular_tree()
    solution.connectBFS(root3)
    print_tree_with_next_pointers(root3)

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - This is the general case - ANY binary tree (not just perfect)
   - Cannot assume tree structure like in problem 116
   - Still need O(1) extra space for optimal solution

2. KEY DIFFERENCES FROM PROBLEM 116:
   - No guarantee all nodes have 2 children
   - No guarantee all leaves at same level
   - Cannot use simple parent-child connection patterns
   - Need more sophisticated level traversal

3. SOLUTION PROGRESSION (Show your thinking):

   APPROACH 1 - BFS with Queue:
   - "Standard level-order traversal works for any tree"
   - Easy to implement and understand
   - Time: O(n), Space: O(w)

   APPROACH 2 - O(1) Space with Dummy Node:
   - "Use a dummy node to build next level connections"
   - Key insight: process current level to connect next level
   - Time: O(n), Space: O(1) - This is the target!

4. THE DUMMY NODE TECHNIQUE:
   - Create dummy node for each level
   - Use it as a "starter" to build the linked list for next level
   - prev pointer tracks where to connect next node
   - dummy.next gives us the start of next level

5. CRITICAL IMPLEMENTATION DETAILS:
   - Process left child first, then right child
   - Always check if child exists before connecting
   - Use prev pointer to maintain connection chain
   - Move to next level using dummy.next

6. EDGE CASES TO DISCUSS:
   - Empty tree
   - Single node
   - Skewed trees (all left or all right)
   - Trees with gaps (some nodes missing children)

7. WHY THIS IS HARDER THAN 116:
   - Cannot predict next level structure
   - Need to handle arbitrary tree shapes
   - Cannot use parent-child patterns reliably

8. INTERVIEW TALKING POINTS:
   - "This requires more careful level management than problem 116"
   - "I'll use a dummy node technique to build connections level by level"
   - "The key is processing current level to establish next level"
   - Walk through how dummy node helps maintain O(1) space

9. FOLLOW-UP QUESTIONS:
   - "Explain why you process right subtree first in DFS" → To establish next pointers before we need them
   - "How does this differ from problem 116?" → Show understanding of constraints
   - "Can you optimize the BFS solution?" → Show the O(1) space approach

10. COMMON MISTAKES:
    - Forgetting to handle missing children
    - Not properly maintaining prev pointer
    - Getting lost in level transitions
    - Not considering edge cases like skewed trees
"""
