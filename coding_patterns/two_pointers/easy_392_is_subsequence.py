class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i = i + 1
            j = j + 1

        return i == len(s)
