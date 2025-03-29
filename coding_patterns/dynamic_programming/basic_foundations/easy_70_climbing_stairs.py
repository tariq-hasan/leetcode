class Solution(object):
    def climbStairs(self, n):
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j = 0, 1
        for _ in range(n):
            i, j = j, i + j
        return j
