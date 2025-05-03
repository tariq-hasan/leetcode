class Solution:
    def fib(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number where:
        F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1

        Args:
            n: The position in the Fibonacci sequence

        Returns:
            The nth Fibonacci number

        Time Complexity: O(n) - We compute each number once in a linear pass
        Space Complexity: O(1) - We only store two variables regardless of input size
        """
        if n < 2:
            return n

        # Initialize with base cases
        prev, curr = 0, 1

        # Calculate Fibonacci numbers iteratively
        for _ in range(n - 1):
            prev, curr = curr, prev + curr

        return curr
