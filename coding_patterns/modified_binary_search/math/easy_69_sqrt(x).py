class Solution:
    def mySqrt(self, x: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        if x < 2:
            return x

        left, right = 2, x // 2
        while left <= right:
            mid = left + (right - left) // 2
            if mid * mid > x:
                right = mid - 1
            elif mid * mid < x:
                left = mid + 1
            else:
                return mid
        return right


class Solution:
    def mySqrt(self, x: int) -> int:
        """
        The time complexity is O(log n).
        The space complexity is O(log n).
        """
        if x < 2:
            return x

        left = self.mySqrt(x >> 2) << 1
        right = left + 1
        return left if right * right > x else right
