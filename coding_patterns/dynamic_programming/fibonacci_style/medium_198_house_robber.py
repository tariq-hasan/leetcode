from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if len(nums) == 1:
            return nums[0]

        i = j = 0
        for num in nums:
            i, j = j, max(num + i, j)
        return j


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = j = 0
        for k in range(len(nums) - 1, -1, -1):
            i, j = max(i, j + nums[k]), i
        return i
