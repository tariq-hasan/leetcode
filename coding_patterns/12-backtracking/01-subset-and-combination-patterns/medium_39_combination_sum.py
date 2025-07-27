from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Time Complexity: O(N^(T/M)), where:
            - N is the number of candidates
            - T is the target value
            - M is the minimum value among candidates
        Space Complexity: O(T/M) for the recursion stack
        """
        result = []
        candidates.sort()  # Sort to optimize by breaking early

        def backtrack(start_idx: int, current_sum: int, path: List[int]) -> None:
            # Base cases
            if current_sum == target:
                result.append(path[:])
                return
            if current_sum > target:
                return

            # Try each candidate starting from start_idx
            for i in range(start_idx, len(candidates)):
                # Skip if adding this candidate would exceed target
                if current_sum + candidates[i] > target:
                    break  # Since candidates are sorted, all remaining will exceed

                path.append(candidates[i])
                # Allow reusing current number, so pass i instead of i+1
                backtrack(i, current_sum + candidates[i], path)
                path.pop()  # Backtrack

        backtrack(0, 0, [])
        return result
