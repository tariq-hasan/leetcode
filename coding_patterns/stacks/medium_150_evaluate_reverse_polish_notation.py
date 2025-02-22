from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),
        }

        stack = []
        for token in tokens:
            if token in operations:
                number_2, number_1 = stack.pop(), stack.pop()
                operation = operations[token]
                stack.append(operation(number_1, number_2))
            else:
                stack.append(int(token))
        return stack.pop()
