from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        i, j = 0, len(nums) - 1
        while i <= j:
            mid = i + ((j - i) // 2)
            if nums[mid] < target:
                i = mid + 1
            elif nums[mid] > target:
                j = mid - 1
            else:
                return mid
        return i
