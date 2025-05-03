from typing import List

class Solution:
    def totalHammingDistance(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        out = 0
        for shift in range(32):
            num_ones = 0
            for num in nums:
                bit = ((num >> shift) & 1)
                num_ones = num_ones + 1 if bit else num_ones
            num_zeroes = len(nums) - num_ones
            out = out + (num_ones * num_zeroes)
        return out
