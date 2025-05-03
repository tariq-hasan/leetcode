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


class Solution:
    def isHappy(self, n: int) -> bool:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        def get_next(n):
            total = 0
            while n:
                total = total + ((n % 10) * (n % 10))
                n = n // 10
            return total

        slow_runner, fast_runner = n, get_next(n)
        while fast_runner != 1 and slow_runner != fast_runner:
            slow_runner = get_next(slow_runner)
            fast_runner = get_next(get_next(fast_runner))
        return fast_runner == 1
