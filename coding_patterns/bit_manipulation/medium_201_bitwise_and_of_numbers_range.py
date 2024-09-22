class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        """
        The time complexity is O(1).
        The space complexity if O(1).
        """
        shift = 0
        while left < right:
            left, right = left >> 1, right >> 1
            shift = shift + 1
        return left << shift


class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        """
        The time complexity is O(1).
        The space complexity if O(1).
        """
        while left < right:
            right = right & (right - 1)
        return right
