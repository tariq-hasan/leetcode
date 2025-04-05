from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution1:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative BFS
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(1) if both trees are null or root-only
            - Average: O(w) where w = max width of the tree
            - Worst: O(n) if all nodes are at one level
        """
        # Helper function to compare two nodes
        def check(node1: TreeNode, node2: TreeNode) -> bool:
            if not node1 and not node2:
                return True
            if not node1 or not node2:
                return False
            if node1.val != node2.val:
                return False
            return True

        # Initialize queue with root pair
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            # Check current pair of nodes
            if not check(node1, node2):
                return False

            # If nodes are valid, add their children to queue
            if node1:  # (and thus node2 as well due to check function)
                queue.append((node1.left, node2.left))
                queue.append((node1.right, node2.right))

        return True


class Solution2:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Recursive DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Base cases
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        
        # Recursive checks (pre-order: root, left, right)
        return (self.isSameTree(p.left, q.left) and 
                self.isSameTree(p.right, q.right))


class Solution3:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative DFS (pre-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) if balanced
            - Average: O(log n)
            - Worst: O(n) if tree is skewed
        """
        # Initialize stack with root pair
        stack = [(p, q)]
        
        while stack:
            node1, node2 = stack.pop()
            
            # Both nodes are None, continue checking other nodes
            if not node1 and not node2:
                continue
                
            # One node is None or values don't match
            if not node1 or not node2 or node1.val != node2.val:
                return False
                
            # Pre-order: Push right then left (so left is processed first)
            stack.append((node1.right, node2.right))
            stack.append((node1.left, node2.left))
            
        return True


class Solution4:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Recursive DFS (in-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n) 
            - Worst: O(n) for skewed tree
        """
        # Helper function for in-order traversal
        def inorder(node1, node2):
            # Base cases
            if not node1 and not node2:
                return True
            if not node1 or not node2:
                return False
            
            # In-order: left, root, right
            return (inorder(node1.left, node2.left) and
                   node1.val == node2.val and
                   inorder(node1.right, node2.right))
            
        return inorder(p, q)


class Solution5:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative DFS (in-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) if balanced
            - Average: O(log n)
            - Worst: O(n) if tree is skewed
        """
        # Separate stacks for each tree
        stack1, stack2 = [], []
        
        # In-order: left, root, right
        while (p or stack1) and (q or stack2):
            # Traverse to leftmost nodes
            while p and q:
                stack1.append(p)
                stack2.append(q)
                p = p.left
                q = q.left
                
            # If one tree has more left children than the other
            if p or q:
                return False
                
            # Process current nodes
            p = stack1.pop()
            q = stack2.pop()
            if p.val != q.val:
                return False
                
            # Move to right subtrees
            p = p.right
            q = q.right
            
        # Check if both trees were fully traversed
        return not p and not q and not stack1 and not stack2


class Solution6:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Recursive DFS (post-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) for balanced tree
            - Average: O(log n)
            - Worst: O(n) for skewed tree
        """
        # Helper function for post-order traversal
        def postorder(node1, node2):
            # Base cases
            if not node1 and not node2:
                return True
            if not node1 or not node2:
                return False
            
            # Post-order: left, right, root
            return (postorder(node1.left, node2.left) and
                   postorder(node1.right, node2.right) and
                   node1.val == node2.val)
            
        return postorder(p, q)


class Solution7:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Strategy: Iterative DFS (post-order)
        Time Complexity: O(n)
        Space Complexity:
            - Best: O(log n) if balanced
            - Average: O(log n)
            - Worst: O(n) if tree is skewed
        """
        # Helper function to get post-order traversal result
        def postorder_traversal(root):
            result, stack = [], []
            last_visited = None
            node = root
            
            # Post-order: left, right, root
            while node or stack:
                # Go to leftmost node
                if node:
                    stack.append(node)
                    node = node.left
                else:
                    # Peek at the top of stack
                    peek = stack[-1]
                    
                    # If right child exists and not visited yet, go right
                    if peek.right and last_visited != peek.right:
                        node = peek.right
                    else:
                        # Visit the node
                        result.append(peek)
                        last_visited = stack.pop()
            
            return result
        
        # Get post-order traversal results for both trees
        nodes_p = postorder_traversal(p)
        nodes_q = postorder_traversal(q)
        
        # Compare lengths
        if len(nodes_p) != len(nodes_q):
            return False
            
        # Compare values
        for node1, node2 in zip(nodes_p, nodes_q):
            if node1.val != node2.val:
                return False
                
        return True
