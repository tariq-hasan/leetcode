class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = 0
        while a or b or c:
            if c & 1:
                out = out if ((a & 1) or (b & 1)) else out + 1
            else:
                out = out + (a & 1) + (b & 1)
            a, b, c = a >> 1, b >> 1, c >> 1
        return out
