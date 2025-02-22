class Solution:
    def simplifyPath(self, path: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        stack = []
        for portion in path.split("/"):
            if portion == "..":
                if stack:
                    stack.pop()
            elif portion not in ['.', '']:
                stack.append(portion)
        return "/" + "/".join(stack)
