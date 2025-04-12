from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0
        for k in range(2, len(cost) + 1):
            i, j = j, min(i + cost[k - 2], j + cost[k - 1])
        return j
