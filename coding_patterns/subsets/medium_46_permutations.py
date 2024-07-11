from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        The time complexity is O(n * n!).
        The time complexity is O(n).
        """
        def backtrack(path):
            if len(path) == len(nums):
                combinations.append(path[:])
                return

            for num in nums:
                if num not in path:
                    path.append(num)
                    backtrack(path)
                    path.pop()

        combinations = []
        backtrack([])
        return combinations
