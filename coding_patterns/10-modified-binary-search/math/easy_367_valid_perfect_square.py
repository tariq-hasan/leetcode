class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        """
        if num < 2:
            return num

        left, right = 2, num // 2
        while left <= right:
            mid = left + (right - left) // 2
            if mid * mid < num:
                left = mid + 1
            elif mid * mid > num:
                right = mid - 1
            else:
                return True
        return False
