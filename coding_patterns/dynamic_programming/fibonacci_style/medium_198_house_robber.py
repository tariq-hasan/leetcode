from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j = nums[-1], 0
        for k in range(len(nums) - 2, -1, -1):
            i, j = max(i, j + nums[k]), i
        return i
