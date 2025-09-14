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
        Optimal O(1) Space Solution - Using Previously Established Connections
        
        Key insight: Use the next pointers from the previous level to traverse
        the current level without extra space.
        
        Time Complexity: O(n)
        Space Complexity: O(1) - no recursion stack, no queue
        """
        if not root:
            return root
        
        # Start with the leftmost node of each level
        leftmost = root
        
        while leftmost.left:  # While not at leaf level
            # Traverse the current level using next pointers
            head = leftmost
            
            while head:
                # Connection 1: left child -> right child
                head.left.next = head.right
                
                # Connection 2: right child -> next node's left child
                if head.next:
                    head.right.next = head.next.left
                
                # Move to next node in current level
                head = head.next
            
            # Move to next level
            leftmost = leftmost.left
        
        return root

    def connectBFS(self, root: Optional[Node]) -> Optional[Node]:
        """
        BFS Approach with Queue (Intuitive but uses O(w) space)
        
        Standard level-order traversal, connecting nodes at each level
        Time Complexity: O(n)
        Space Complexity: O(w) where w is maximum width
        """
        if not root:
            return root
        
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            
            for i in range(level_size):
                node = queue.popleft()
                
                # Connect to next node in the same level
                if i < level_size - 1:
                    node.next = queue[0]  # Peek at next node
                
                # Add children to queue
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return root

    def connectRecursive(self, root: Optional[Node]) -> Optional[Node]:
        """
        Recursive DFS Approach
        
        Uses the fact that it's a perfect binary tree to make connections
        Time Complexity: O(n)
        Space Complexity: O(log n) due to recursion stack
        """
        if not root or not root.left:
            return root
        
        # Connect left child to right child
        root.left.next = root.right
        
        # Connect right child to next subtree's left child
        if root.next:
            root.right.next = root.next.left
        
        # Recursively connect subtrees
        self.connectRecursive(root.left)
        self.connectRecursive(root.right)
        
        return root

    def connectLevelByLevel(self, root: Optional[Node]) -> Optional[Node]:
        """
        Alternative O(1) Space - Level by Level Processing
        
        Similar to optimal solution but with different structure
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not root:
            return root
        
        level_start = root
        
        while level_start.left:  # While not at the last level
            curr = level_start
            
            # Connect all nodes at the next level
            while curr:
                # Connect children
                curr.left.next = curr.right
                
                # Connect to next subtree if exists
                if curr.next:
                    curr.right.next = curr.next.left
                
                curr = curr.next
            
            # Move to the next level
            level_start = level_start.left
        
        return root

# Utility functions for testing
def print_level_order_with_next(root):
    """Helper function to visualize the next pointers"""
    if not root:
        return
    
    level_start = root
    level = 0
    
    while level_start:
        print(f"Level {level}: ", end="")
        curr = level_start
        
        while curr:
            print(f"{curr.val}", end="")
            if curr.next:
                print(f" -> {curr.next.val}", end="")
            else:
                print(" -> NULL", end="")
            if curr.next:
                print(", ", end="")
            curr = curr.next
        
        print()
        level_start = level_start.left if level_start else None
        level += 1

def build_perfect_binary_tree():
    """Build test case: Perfect binary tree"""
    #       1
    #      / \
    #     2   3
    #    / \ / \
    #   4 5 6  7
    
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    return root

# Test the solutions
def test_solutions():
    print("Original tree structure:")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\ / \\")
    print("   4  5 6  7")
    print()
    
    # Test optimal solution
    root1 = build_perfect_binary_tree()
    solution = Solution()
    solution.connect(root1)
    
    print("After connecting next pointers (O(1) space solution):")
    print_level_order_with_next(root1)
    print()
    
    # Test BFS solution
    root2 = build_perfect_binary_tree()
    solution.connectBFS(root2)
    
    print("BFS solution result:")
    print_level_order_with_next(root2)

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM ANALYSIS:
   - Perfect binary tree: all leaves at same level, every parent has 2 children
   - Need to connect nodes at the same level using 'next' pointers
   - Goal: transform tree so each node points to next node in same level

2. SOLUTION PROGRESSION (Show your thinking):
   
   APPROACH 1 - BFS (Natural first thought):
   - "I can use level-order traversal and connect nodes as I process each level"
   - Time: O(n), Space: O(w) where w is width of tree
   
   APPROACH 2 - Recursive (Building on tree properties):
   - "Since it's perfect binary tree, I can use recursion"
   - Connect left->right, then right->next.left if next exists
   - Time: O(n), Space: O(log n) for recursion
   
   APPROACH 3 - Optimal O(1) Space (The key insight):
   - "I can use already established next pointers from previous level!"
   - Traverse each level using next pointers to connect the next level
   - Time: O(n), Space: O(1) - this is the target solution

3. THE KEY INSIGHT FOR OPTIMAL SOLUTION:
   - Level 0: Just root (no connections needed)
   - Level 1: Connect using root's children
   - Level 2: Use Level 1's next pointers to traverse and connect Level 2
   - Pattern: Use level N's connections to establish level N+1's connections

4. CONNECTION PATTERNS:
   - Within same parent: left child -> right child
   - Across parents: right child -> next parent's left child

5. EDGE CASES:
   - Empty tree
   - Single node
   - Two levels only

6. WHY OPTIMAL SOLUTION WORKS:
   - Perfect binary tree guarantees structure
   - Next pointers from previous level give us "free" traversal
   - No additional data structures needed

7. INTERVIEW TIPS:
   - Start with BFS to show you understand the problem
   - Mention you want O(1) space if possible
   - Walk through the connection logic carefully
   - Use the perfect binary tree property as justification

8. FOLLOW-UP QUESTIONS:
   - "What if it's not a perfect binary tree?" → That's problem 117
   - "Can you do it iteratively with O(1) space?" → Show the optimal solution
   - "Explain why this works" → Walk through the level-by-level connection logic
"""
