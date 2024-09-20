from typing import List

class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = [0] * (n + 1)
        x, b = 0, 1
        # [0, b) is calculated
        while b <= n:
            # generate [b, 2b) or [b, n) from [0, b)
            while x < b and x + b <= n:
                out[x + b] = out[x] + 1
                x = x + 1
            x = 0 # reset x
            b = b << 1 # b = 2b
        return out


class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = [0] * (n + 1)
        for x in range(1, n + 1):
            # x // 2 is x >> 1 and x % 2 is x & 1
            out[x] = out[x >> 1] + (x & 1) 
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
