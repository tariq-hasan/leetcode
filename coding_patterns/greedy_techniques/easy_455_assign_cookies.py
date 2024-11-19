from typing import List


class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        """
        The time complexity is O(n log n + m log m) where n is the size of the array g and m is the size of the array s.
        The space complexity is O(m + n) or O(log m + log n) depending on the programming language.
        """
        g, s = sorted(g), sorted(s)
        ans = 0
        for i in range(len(s)):
            if ans < len(g) and g[ans] <= s[i]:
                ans = ans + 1
        return ans
