class Solution:
    def isHappy(self, n: int) -> bool:
        """
        The time complexity is O(log n).
        The space complexity is O(log n).
        """
        def get_next(n):
            total = 0
            while n:
                total = total + ((n % 10) * (n % 10))
                n = n // 10
            return total

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_next(n)
        return n == 1


