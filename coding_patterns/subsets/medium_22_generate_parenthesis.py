from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        The time complexity is n * C_n = O(4^n / sqrt(n)), where C_n is the Catalan number.
        The space complexity is O(n).
        """

        def backtrack(left_count, right_count, path):
            if len(path) == n * 2:
                combinations.append(''.join(path))
                return

            if left_count < n:
                path.append('(')
                backtrack(left_count + 1, right_count, path)
                path.pop()
            if right_count < left_count:
                path.append(')')
                backtrack(left_count, right_count + 1, path)
                path.pop()

        combinations = []
        backtrack(0, 0, [])
        return combinations
