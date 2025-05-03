class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        The time complexity is O(log n).
        The space complexity is O(1).
        If we attempt to completely reverse the number we may hit an integer overflow problem. 
        """
        if x < 0 or (x > 0 and x % 10 == 0):
            return False
        y = 0
        while y < x:
            y = (y * 10) + (x % 10)
            x = x // 10
        return x == y or x == y // 10
