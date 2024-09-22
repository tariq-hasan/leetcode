from math import floor, log2

class Solution:
    def findComplement(self, num: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        todo, bit = num, 1
        while todo:
            num = num ^ bit
            bit = bit << 1
            todo = todo >> 1
        return num


class Solution:
    def findComplement(self, num: int) -> int:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        n = floor(log2(num)) + 1
        bitmask = (1 << n) - 1
        return bitmask ^ num
