from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + (right - left) // 2
            halves_are_even = (right - mid) % 2 == 0
            if nums[mid] == nums[mid + 1]:
                if halves_are_even:
                    left = mid + 2
                else:
                    right = mid - 1
            elif nums[mid - 1] == nums[mid]:
                if halves_are_even:
                    right = mid - 2
                else:
                    left = mid + 1
            else:
                return nums[mid]
        return nums[left]


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + (right - left) // 2
            if mid % 2 == 1:
                mid = mid - 1
            if nums[mid] == nums[mid + 1]:
                left = mid + 2
            else:
                right = mid
        return nums[left]
