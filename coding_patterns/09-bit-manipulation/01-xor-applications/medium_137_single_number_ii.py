from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Find the single element that appears only once in an array where all other elements appear three times.

        This solution counts the occurrences of each bit position (0-31) across all numbers:
        1. For each bit position, count how many numbers have this bit set to 1
        2. If the count % 3 = 1, then the single number has this bit set
        3. Construct the single number by combining all such bits

        Args:
            nums: A list of integers where every element appears three times except for one

        Returns:
            The element that appears only once

        Time Complexity: O(n) - We iterate through the array 32 times
        Space Complexity: O(1) - We use a constant amount of space
        """
        # Initialize the result
        result = 0

        # Check each bit position (32 bits for an integer)
        for shift in range(32):
            # Count the number of 1s at this bit position
            bit_sum = 0
            for num in nums:
                # Extract the bit at position 'shift'
                bit_sum += (num >> shift) & 1

            # If the single number has a 1 at this position, the sum % 3 will be 1
            result_bit = bit_sum % 3

            # Add this bit to our result
            result |= (result_bit << shift)

        # Handle negative numbers (two's complement)
        if result >= (1 << 31):  # If the sign bit is set
            result = result - (1 << 32)  # Convert to negative in Python

        return result


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
