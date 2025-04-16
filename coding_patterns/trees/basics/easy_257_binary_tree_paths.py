from collections import deque
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        """
        Find all root-to-leaf paths in a binary tree using recursive DFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(h) for recursion stack where h is the height of the tree
            - O(n) for the paths stored (in the worst case, all nodes form a single path)
        """
        result = []

        def dfs(node, path):
            if not node:
                return

            # Add current node to path
            current_path = path + str(node.val)

            # If leaf node, add path to result
            if not node.left and not node.right:
                result.append(current_path)
                return

            # Continue DFS with arrow "->" added
            current_path += "->"
            dfs(node.left, current_path)
            dfs(node.right, current_path)

        dfs(root, "")
        return result


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        """
        Find all root-to-leaf paths in a binary tree using iterative DFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(h) for the stack where h is the height of the tree
            - O(n) for the paths stored
        """
        if not root:
            return []

        result = []
        # Stack stores (node, path) pairs
        stack = [(root, str(root.val))]

        while stack:
            node, path = stack.pop()

            # If leaf node, add path to result
            if not node.left and not node.right:
                result.append(path)

            # Push children with updated paths
            # We push left first so that right is processed first (LIFO)
            if node.left:
                stack.append((node.left, path + "->" + str(node.left.val)))
            if node.right:
                stack.append((node.right, path + "->" + str(node.right.val)))

        return result


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        """
        Find all root-to-leaf paths in a binary tree using BFS.

        Time Complexity: O(n) - we visit each node once
        Space Complexity:
            - O(w) where w is the maximum width of the tree
            - O(n) in worst case
        """
        if not root:
            return []

        result = []
        # Queue for BFS, storing (node, path) pairs
        queue = deque([(root, str(root.val))])

        while queue:
            node, path = queue.popleft()

            # If leaf node, add path to result
            if not node.left and not node.right:
                result.append(path)

            # Add children to queue with updated paths
            if node.left:
                queue.append((node.left, path + "->" + str(node.left.val)))
            if node.right:
                queue.append((node.right, path + "->" + str(node.right.val)))

        return result
