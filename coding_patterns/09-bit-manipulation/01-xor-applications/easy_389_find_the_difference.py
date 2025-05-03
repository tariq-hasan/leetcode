class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1

        for c in t:
            if c not in s or freq[c] == 0:
                return c
            else:
                freq[c] = freq[c] - 1


class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = 0
        for c in s + t:
            out = out ^ ord(c)
        return chr(out)
