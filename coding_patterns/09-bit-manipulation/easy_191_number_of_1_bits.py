class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out = 0
        while n:
            out = out + (n & 1)
            n = n >> 1
        return out


class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out, mask = 0, 1
        for i in range(32):
            if n & mask:
                out = out + 1
            mask = mask << 1
        return out


class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out = 0
        while n:
            out = out + 1
            n = n & (n - 1)
        return out
