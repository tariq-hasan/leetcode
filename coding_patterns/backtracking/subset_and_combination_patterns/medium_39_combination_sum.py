from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        The time complexity is O(n^(T/M)).
        The space complexity is O(T/M).
        Here, N is the number of candidates,
        T is the target value,
        and M is the minimum value in candidates.
        """
        results = []

        def backtrack(remaining: int, combination: List[int], start: int):
            if remaining == 0:
                # Found a valid combination
                results.append(combination[:])
                return
            if remaining < 0:
                # Exceeded the target, backtrack
                return

            for i in range(start, len(candidates)):
                combination.append(candidates[i])
                # Allow the same number to be used again by passing i (not i+1)
                backtrack(remaining - candidates[i], combination, i)
                combination.pop()  # Undo the last choice

        backtrack(target, [], 0)
        return results
