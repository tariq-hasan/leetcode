from typing import List


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        i = zero_count = out = 0
        for j in range(len(nums)):
            zero_count = zero_count + (nums[j] == 0)
            while zero_count > 1:
                zero_count = zero_count - (nums[i] == 0)
                i = i + 1
            out = max(out, j - i)
        return out
