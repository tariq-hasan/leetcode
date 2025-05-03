from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Time Complexity: O(4^n), where n is the length of digits
                         Each digit maps to 3-4 letters, worst case is 4 options per digit
        Space Complexity: O(n), for the recursion stack
        """
        # Edge case: empty input
        if not digits:
            return []

        # Digit to letter mapping
        phone_map = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz"
        }

        result = []

        def backtrack(index: int, current_str: str) -> None:
            # Base case: we've processed all digits
            if index == len(digits):
                result.append(current_str)
                return

            # Try each letter for the current digit
            for letter in phone_map[digits[index]]:
                # Add current letter and move to next digit
                backtrack(index + 1, current_str + letter)

        # Start backtracking from the first digit with empty string
        backtrack(0, "")
        return result
