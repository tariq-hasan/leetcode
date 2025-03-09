from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        def rob_simple(nums: List[int]) -> int:
            i = j = 0
            for num in nums:
                i, j = j, max(num + i, j)
            return j

        if len(nums) == 1:
            return nums[0]

        return max(rob_simple(nums[:-1]), rob_simple(nums[1:]))
