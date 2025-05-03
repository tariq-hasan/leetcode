from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        def findBound(nums: List[int], target: int, is_first: bool) -> int:
            left, right = 0, len(nums) - 1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] < target:
                    left = mid + 1
                elif nums[mid] > target:
                    right = mid - 1
                else:
                    if is_first:
                        if mid == left or nums[mid - 1] < target:
                            return mid
                        right = mid - 1
                    else:
                        if mid == right or nums[mid + 1] > target:
                            return mid
                        left = mid + 1
            return -1

        lower_bound = findBound(nums, target, True)
        if lower_bound == -1:
            return [-1, -1]

        upper_bound = findBound(nums, target, False)

        return [lower_bound, upper_bound]
