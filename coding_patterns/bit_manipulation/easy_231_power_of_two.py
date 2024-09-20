class Solution(object):
    def isPowerOfTwo(self, n: int) -> bool:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        if n == 0:
            return False
        return n & (-n) == n


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        if n == 0:
            return False
        return n & (n - 1) == 0
