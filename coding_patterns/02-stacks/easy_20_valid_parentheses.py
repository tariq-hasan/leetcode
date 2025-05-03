class Solution:
    def isValid(self, s: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        mapping = {")": "(", "}": "{", "]": "["}
        stack = []
        for c in s:
            if c in mapping:
                top_element = stack.pop() if stack else "#"
                if mapping[c] != top_element:
                    return False
            else:
                stack.append(c)
        return not stack
