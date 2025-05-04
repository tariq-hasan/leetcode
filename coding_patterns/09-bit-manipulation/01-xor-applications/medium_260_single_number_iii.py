from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        """
        Find two elements that appear only once in an array where all other elements appear twice.

        This solution uses XOR and bit manipulation:
        1. XOR all numbers to get xor_result = a ^ b (where a and b are the two single numbers)
        2. Find a bit that is different between a and b (a set bit in xor_result)
        3. Use this bit to partition the array into two groups
        4. Apply Single Number I solution to each group separately

        Args:
            nums: A list of integers where two elements appear once and others appear twice

        Returns:
            The two elements that appear only once

        Time Complexity: O(n) - We iterate through the array twice
        Space Complexity: O(1) - We use a constant amount of space
        """
        # Step 1: XOR all numbers to get a ^ b
        xor_result = 0
        for num in nums:
            xor_result ^= num

        # Step 2: Find the rightmost set bit in xor_result
        # This bit is different between our two target numbers
        # diff is a mask with only this different bit set to 1
        diff = xor_result & (-xor_result)  # Get the rightmost set bit

        # Step 3: Partition numbers into two groups based on this bit
        # and XOR each group separately
        first_num = 0
        for num in nums:
            # If this bit is set in num, put it in the first group
            if num & diff:
                first_num ^= num

        # Step 4: The second number is the XOR of first_num and xor_result
        second_num = xor_result ^ first_num

        return [first_num, second_num]
