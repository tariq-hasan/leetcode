from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        """
        Time Complexity: O(n choose k) = O(n! / (k! * (n-k)!))
            This represents the number of possible combinations
        Space Complexity: O(k) for the recursion stack and temporary path storage
        """
        result = []

        def backtrack(start_idx: int, path: List[int]) -> None:
            # Base case: we've selected k numbers
            if len(path) == k:
                result.append(path[:])
                return

            # Optimization: calculate how many numbers we can skip
            # need = numbers we still need to pick
            # remain = total numbers remaining available
            # available = how many numbers we can choose from at this step
            need = k - len(path)
            remain = n - start_idx + 1
            available = remain - need + 1

            # Try each valid starting number
            for i in range(start_idx, start_idx + available):
                path.append(i)
                backtrack(i + 1, path)
                path.pop()  # Backtrack

        backtrack(1, [])  # Start with 1 since we're using 1-indexed numbers
        return result
