from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible subsets of the given array using an iterative approach.

        For each number, we take all existing subsets and create new ones by adding
        the current number to each existing subset.

        Time Complexity: O(n * 2^n)
            - We generate 2^n subsets, and each operation to copy a subset takes O(n) time
        Space Complexity: O(n * 2^n)
            - We store 2^n subsets, and each subset can have up to n elements
        """
        result = [[]]  # Start with the empty subset

        for num in nums:
            # Create new subsets by adding current number to existing subsets
            new_subsets = []
            for subset in result:
                # Create a copy of the current subset and add the new number
                new_subset = subset.copy()
                new_subset.append(num)
                new_subsets.append(new_subset)

            # Add all new subsets to our result
            result.extend(new_subsets)

        return result
