class Solution:
    def reverseBits(self, n: int) -> int:
        """
        The time complexity if O(1).
        The space complexity if O(1).        
        """
        res, power = 0, 31
        while n:
            res += (n & 1) << power
            n = n >> 1
            power -= 1
        return res
