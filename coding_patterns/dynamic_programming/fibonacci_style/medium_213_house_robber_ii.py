from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if len(nums) == 1:
            return nums[0]

        def rob_linear(arr: List[int]) -> int:
            i, j = 0, 0
            for num in arr:
                i, j = j, max(j, i + num)
            return j

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
