class Solution:
    def tribonacci(self, n: int) -> int:
        """
        Calculate the nth Tribonacci number where:
        T(0) = 0, T(1) = 1, T(2) = 1, and T(n+3) = T(n) + T(n+1) + T(n+2) for n ≥ 0

        Time complexity: O(n) - We compute each number once
        Space complexity: O(1) - We only store three variables regardless of input size
        """
        if n == 0:
            return 0
        if n <= 2:
            return 1

        a, b, c = 0, 1, 1
        for _ in range(n - 2):
            a, b, c = b, c, a + b + c

        return c
