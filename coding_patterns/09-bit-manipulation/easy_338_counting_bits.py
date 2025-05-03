from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = [0] * (n + 1)
        j = 1
        while j < n + 1:
            i = 0
            while i < j and i + j <= n:
                out[i + j] = out[i] + 1
                i = i + 1
            j = j << 1
        return out


class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = [0] * (n + 1)
        for i in range(1, n + 1):
            # x // 2 is x >> 1 and x % 2 is x & 1
            out[i] = out[i >> 1] + (i & 1) 
        return out


class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = [0] * (n + 1)
        for x in range(1, n + 1):
            out[x] = out[x & (x - 1)] + 1
        return out
