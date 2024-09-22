from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                return mid
        return left
