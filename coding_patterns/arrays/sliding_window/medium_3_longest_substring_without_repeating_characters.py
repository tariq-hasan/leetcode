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


