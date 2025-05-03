from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Determine the maximum amount of money you can rob without alerting the police.

        You cannot rob adjacent houses (houses that share a border), as this would
        automatically alert the police.

        Args:
            nums: A list of non-negative integers representing the amount of money in each house

        Returns:
            The maximum amount of money you can rob without alerting the police

        Time Complexity: O(n) - We process each house once in a linear pass
        Space Complexity: O(1) - We only store two variables regardless of input size
        """
        # Initialize previous two max values
        # prev_max: Maximum money if we consider houses up to i-2
        # curr_max: Maximum money if we consider houses up to i-1
        prev_max = curr_max = 0

        # For each house, decide whether to rob it based on maximum possible profit
        for money in nums:
            # New maximum is either:
            # 1. Rob current house + maximum from houses before previous (prev_max + money)
            # 2. Skip current house and keep previous maximum (curr_max)
            prev_max, curr_max = curr_max, max(money + prev_max, curr_max)

        return curr_max
