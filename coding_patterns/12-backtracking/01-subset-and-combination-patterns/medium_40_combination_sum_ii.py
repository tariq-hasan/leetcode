from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Time Complexity: O(2^n), where n is the length of candidates
                        Each element can either be included or excluded
        Space Complexity: O(n) for the recursion stack
        """
        result = []
        candidates.sort()  # Sort to handle duplicates and optimize

        def backtrack(start_idx: int, current_sum: int, path: List[int]) -> None:
            # Base cases
            if current_sum == target:
                result.append(path[:])
                return
            if current_sum > target:
                return

            # Try each candidate starting from start_idx
            for i in range(start_idx, len(candidates)):
                # Skip duplicates at the same level
                if i > start_idx and candidates[i] == candidates[i-1]:
                    continue

                # Optimization: break if adding this candidate would exceed target
                if current_sum + candidates[i] > target:
                    break

                path.append(candidates[i])
                # Move to next index (i+1) since each number can be used only once
                backtrack(i + 1, current_sum + candidates[i], path)
                path.pop()  # Backtrack

        backtrack(0, 0, [])
        return result
