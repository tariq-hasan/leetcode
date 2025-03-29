from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0
        for k in range(1, len(cost)):
            i, j = j, min(i + cost[k - 1], j + cost[k])
        return j
