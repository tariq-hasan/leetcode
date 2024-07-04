from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i, j, k = 0, 0, len(nums) - 1
        while j <= k:
            if nums[j] == 0:
                nums[i], nums[j] = nums[j], nums[i]
                i, j = i + 1, j + 1
            elif nums[j] == 2:
                nums[j], nums[k] = nums[k], nums[j]
                k = k - 1
            else:
                j = j + 1
