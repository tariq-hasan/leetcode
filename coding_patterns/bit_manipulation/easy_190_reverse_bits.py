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


class Solution:
    def reverseBits(self, n: int) -> int:
        """
        The time complexity if O(1).
        The space complexity if O(1).        
        """
        out = 0
        for _ in range(32):
            out = (out << 1) | (n & 1)
            n = n >> 1
        return out
