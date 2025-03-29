class Solution:
    def checkValidString(self, s: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0

        for k in range(len(s)):
            if s[k] == '(' or s[k] == '*':
                i = i + 1
            else:
                i = i - 1

            if s[len(s) - k - 1] == ')' or s[len(s) - k - 1] == '*':
                j = j + 1
            else:
                j = j - 1

            if i < 0 or j < 0:
                return False

        return True
