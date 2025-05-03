class Solution:
    def tribonacci(self, n: int) -> int:
        """
        Calculate the nth Tribonacci number where:
        T(0) = 0, T(1) = T(2) = 1, and T(n+3) = T(n) + T(n+1) + T(n+2) for n ≥ 0

        Args:
            n: The position in the Tribonacci sequence

        Returns:
            The nth Tribonacci number

        Time Complexity: O(n) - We compute each number once in a linear pass
        Space Complexity: O(1) - We only store three variables regardless of input size
        """
        if n == 0:
            return 0
        if n <= 2:
            return 1

        # Initialize with base cases
        a, b, c = 0, 1, 1

        # Calculate Tribonacci numbers iteratively
        for _ in range(n - 2):
            a, b, c = b, c, a + b + c

        return c
