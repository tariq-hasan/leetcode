class Solution:
    def calculate(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        stack = []
        curr_num = 0
        operation = '+'
        for i in range(len(s)):
            if s[i] in '0123456789':
                curr_num = (curr_num * 10) + (ord(s[i]) - ord('0'))
            if s[i] not in '0123456789 ' or i == len(s) - 1:
                if operation == '-':
                    stack.append(-curr_num)
                elif operation == '+':
                    stack.append(curr_num)
                elif operation == '*':
                    stack.append(stack.pop() * curr_num)
                elif operation == '/':
                    stack.append(int(stack.pop() / curr_num))
                operation = s[i]
                curr_num = 0

        out = 0
        while stack:
            out = out + stack.pop()
        return out
