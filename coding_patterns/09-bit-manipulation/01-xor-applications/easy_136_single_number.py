from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Find the single element that appears only once in an array where all other elements appear twice.

        This problem can be solved using the XOR operation properties:
        - XOR of a number with itself is 0: a ^ a = 0
        - XOR of a number with 0 is the number itself: a ^ 0 = a
        - XOR operation is commutative and associative

        Args:
            nums: A list of integers where every element appears twice except for one

        Returns:
            The element that appears only once

        Time Complexity: O(n) - We iterate through the array once
        Space Complexity: O(1) - We use only one variable regardless of input size
        """
        # Initialize result to 0 (XOR identity)
        result = 0

        # XOR all numbers together
        for num in nums:
            result ^= num  # result = result ^ num

        # The final result will be the single number
        return result
