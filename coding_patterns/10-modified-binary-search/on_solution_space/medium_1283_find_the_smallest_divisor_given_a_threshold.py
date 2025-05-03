from typing import List


class Solution:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        """
        The time complexity is O(n log m), where m is the maximum element of the nums array.
        The space complexity is O(1).
        """
        left, right = 1, max(nums)
        while left < right:
            mid = left + (right - left) // 2
            total = sum([((num - 1) // mid) + 1 for num in nums])
            if total > threshold:
                left = mid + 1
            else:
                right = mid
        return left
