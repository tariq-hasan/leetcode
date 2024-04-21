from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        min_price, max_profit = float('inf'), 0
        for i in range(len(prices)):
            profit = prices[i] - min_price
            if profit > max_profit:
                max_profit = profit
            elif prices[i] < min_price:
                min_price = prices[i]
        return max_profit
