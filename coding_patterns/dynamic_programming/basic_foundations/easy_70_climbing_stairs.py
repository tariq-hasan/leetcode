class Solution(object):
    def climbStairs(self, n):
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if n == 1:
            return 1

        i, j = 1, 2
        for _ in range(n - 2):
            i, j = j, i + j

        return j
