class Solution:
    def removeDuplicates(self, s: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        stack = []
        for c in s:
            if not stack or stack[-1] != c:
                stack.append(c)
            else:
                stack.pop()
        return ''.join(stack)
