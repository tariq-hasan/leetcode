from typing import List


class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(1).
        """
        nums.sort()
        for i in range(len(nums)):
            if nums[i] < 0 and k > 0:
                nums[i] = -nums[i]
                k = k - 1

        nums.sort()
        if k > 0 and k % 2 != 0:
            nums[0] = - nums[0]

        return sum(nums)
