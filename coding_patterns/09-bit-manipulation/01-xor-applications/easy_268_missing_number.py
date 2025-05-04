from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        """
        Find the missing number in an array containing distinct numbers in range [0, n].

        This problem can be solved using XOR by:
        1. XORing all numbers from 0 to n
        2. XORing with all numbers in the array
        3. The result will be the missing number (as all other numbers XOR to 0)

        Args:
            nums: A list of distinct integers in the range [0, n] except for one number

        Returns:
            The missing number in the range

        Time Complexity: O(n) - We iterate through the array once
        Space Complexity: O(1) - We use only one variable regardless of input size
        """
        # Initialize with n (the length of the array)
        # This accounts for the fact that the range should be [0, n]
        missing = len(nums)

        # XOR with each index and value pair
        for i, num in enumerate(nums):
            # By XORing both index and value, pairs will cancel out
            # The only remaining value will be the missing number
            missing ^= i ^ num

        return missing
