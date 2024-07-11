from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        The time complexity is O(n * 4^n), where 4 is the maximum value length in letters.
        The space complexity is O(n).
        """

        if len(digits) == 0: return []
        letters = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
            }

        def backtrack(index, path):
            if len(path) == len(digits):
                combinations.append("".join(path))
                return

            possible_letters = letters[digits[index]]
            for letter in possible_letters:
                path.append(letter)
                backtrack(index + 1, path)
                path.pop()

        combinations = []
        backtrack(0, [])
        return combinations


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        The time complexity is O(n * 4^n), where 4 is the maximum value length in letters.
        The space complexity is O(n).
        """

        if n == 0:
            return ['']

        combinations = []
        for left_count in range(n):
            for left_string in self.generateParenthesis(left_count):
                for right_string in self.generateParenthesis(n - 1 - left_count):
                    combinations.append('(' + left_string + ')' + right_string)

        return combinations
