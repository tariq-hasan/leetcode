class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        letters = '0123456789abcdefghijklmnopqrstuvwxyz'
        s = s.lower()
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] not in letters:
                i = i + 1
            elif s[j] not in letters:
                j = j - 1
            elif s[i] == s[j]:
                i, j = i + 1, j - 1
            else:
                return False
        return True
