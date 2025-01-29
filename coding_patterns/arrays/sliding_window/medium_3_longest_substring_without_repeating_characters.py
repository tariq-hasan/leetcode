from typing import List


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        seen, out = set(), set()
        for i in range(len(s) - 9):
            word = s[i : i + 10]
            if word in seen:
                out.add(word)
            seen.add(word)
        return list(out)


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        if len(s) <= 10:
            return []

        to_int = {"A": 0, "C": 1, "G": 2, "T": 3}
        nums = [to_int.get(s[i]) for i in range(len(s))]

        h = 0
        seen, out = set(), set()
        for i in range(len(s) - 9):
            if i != 0:
                h = (h * 4) - (nums[i - 1] * (4 ** 10)) + nums[i + 9]
            else:
                for i in range(10):
                    h = (h * 4) + nums[i]
            if h in seen:
                out.add(s[i : i + 10])
            seen.add(h)
        return list(out)


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        if len(s) <= 10:
            return []

        to_int = {"A": 0, "C": 1, "G": 2, "T": 3}
        nums = [to_int.get(s[i]) for i in range(len(s))]

        bitmask = 0
        seen, out = set(), set()
        for i in range(len(s) - 9):
            if i != 0:
                bitmask <<= 2
                bitmask |= nums[i + 9]
                bitmask &= ~(3 << 2 * 10)
            else:
                for i in range(10):
                    bitmask <<= 2
                    bitmask |= nums[i]
            if bitmask in seen:
                out.add(s[i : i + 10])
            seen.add(bitmask)
        return list(out)
