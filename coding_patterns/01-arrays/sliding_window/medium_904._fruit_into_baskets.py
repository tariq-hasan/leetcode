from typing import List


class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        freq = {}
        i = 0
        for j in range(len(fruits)):
            freq[fruits[j]] = freq.get(fruits[j], 0) + 1
            if len(freq) > 2:
                freq[fruits[i]] = freq[fruits[i]] - 1
                if freq[fruits[i]] == 0:
                    del freq[fruits[i]]
                i = i + 1
        return j - i + 1


class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        freq = {}
        i = out = 0
        for j in range(len(fruits)):
            freq[fruits[j]] = freq.get(fruits[j], 0) + 1
            while len(freq) > 2:
                freq[fruits[i]] = freq[fruits[i]] - 1
                if freq[fruits[i]] == 0:
                    del freq[fruits[i]]
                i = i + 1
            out = max(out, j - i + 1)
        return out
