class Solution:
    def minSteps(self, n: int) -> int:
        """
        The time complexity is O(n^1/2).
        The space complexity is O(1).
        """
        out = 0
        d = 2
        while n > 1:
            while n % d == 0:
                out = out + d
                n = n // d
            d = d + 1
        return out
