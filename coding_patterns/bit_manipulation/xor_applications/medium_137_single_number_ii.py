from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        loner = 0

        for shift in range(32):
            bit_sum = 0
            for num in nums:
                bit_sum += (num >> shift) & 1
            loner_bit = bit_sum % 3
            loner = loner | (loner_bit << shift)

        if loner >= (1 << 31):
            loner = loner - (1 << 32)

        return loner


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        seen_once = seen_twice = 0

        for num in nums:
            seen_once = (seen_once ^ num) & (~seen_twice)
            seen_twice = (seen_twice ^ num) & (~seen_once)

        return seen_once
