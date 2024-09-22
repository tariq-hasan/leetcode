class Solution:
    def hammingDistance(self, x: int, y: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out = 0
        n = x ^ y
        while n:
            out = out + (n & 1)
            n = n >> 1
        return out


class Solution:
    def hammingDistance(self, x: int, y: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out = 0
        n = x ^ y
        while n:
            out = out + (n & 1)
            n = n & (n - 1)
        return out
