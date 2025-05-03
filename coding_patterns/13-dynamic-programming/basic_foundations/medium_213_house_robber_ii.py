from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Determine the maximum amount of money you can rob without alerting the police,
        but with houses arranged in a circle (first and last houses are adjacent).

        You cannot rob adjacent houses (houses that share a border), as this would
        automatically alert the police.

        Args:
            nums: A list of non-negative integers representing the amount of money in each house

        Returns:
            The maximum amount of money you can rob without alerting the police

        Time Complexity: O(n) - We process each house twice in separate linear passes
        Space Complexity: O(1) - We only use constant extra space
        """
        # Handle edge case
        if len(nums) == 1:
            return nums[0]

        def rob_linear(houses: List[int]) -> int:
            """
            Helper function to solve the original house robber problem (non-circular).
            """
            prev_max = curr_max = 0
            for money in houses:
                prev_max, curr_max = curr_max, max(money + prev_max, curr_max)
            return curr_max

        # Since houses are in a circle, we can't rob both first and last houses
        # So we consider two scenarios and take the maximum:
        # 1. Rob houses from 0 to n-2 (exclude the last house)
        # 2. Rob houses from 1 to n-1 (exclude the first house)
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
