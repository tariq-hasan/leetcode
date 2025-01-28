from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        left = out = 0
        for i in range(1, len(prices)):
            out = max(out, prices[i] - prices[left])
            if prices[i] < prices[left]:
                left = i
        return out
