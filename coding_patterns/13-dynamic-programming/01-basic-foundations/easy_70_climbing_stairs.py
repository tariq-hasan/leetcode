class Solution:
    def climbStairs(self, n: int) -> int:
        """
        Find the number of distinct ways to climb to the top when you can take 1 or 2 steps.

        This problem is equivalent to finding the (n+1)th Fibonacci number:
        - To reach step n, we can either:
          1. Take 1 step from (n-1)
          2. Take 2 steps from (n-2)
        - Therefore, ways(n) = ways(n-1) + ways(n-2)

        Args:
            n: The number of steps to climb

        Returns:
            The number of distinct ways to reach the top

        Time Complexity: O(n) - We compute each number once in a linear pass
        Space Complexity: O(1) - We only store two variables regardless of input size
        """
        if n <= 2:
            return n

        # Initialize with base cases: ways(1) = 1, ways(2) = 2
        prev, curr = 1, 2

        # Calculate each step's ways
        for i in range(3, n + 1):
            prev, curr = curr, prev + curr

        return curr
