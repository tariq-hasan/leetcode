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
