from typing import List


class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        mod = 10 ** 9 + 7
        out = 0
        nums.sort()
        for i in range(len(nums)):
            left, right = i, len(nums) - 1
            while left <= right:
                mid = left + (right - left) // 2
                if nums[i] + nums[mid] <= target:
                    left = mid + 1
                else:
                    right = mid - 1
            if i <= left - 1:
                out = out + ((2 ** (left - 1 - i)) % mod)
        return out % mod


class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        mod = 10 ** 9 + 7
        out = 0
        nums.sort()
        left, right = 0, len(nums) - 1
        while left <= right:
            if nums[left] + nums[right] <= target:
                out = out + ((2 ** (right - left)) % mod)
                left = left + 1
            else:
                right = right - 1
        return out % mod
