from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        The time complexity is O(n^2).
        The space complexity is O(n).
        """
        word_length = len(words[0])
        substring_size = word_length * len(words)

        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        def check(i):
            remaining = word_count.copy()
            words_used = 0
            for j in range(i, i + substring_size, word_length):
                sub = s[j : j + word_length]
                if remaining.get(sub, 0) > 0:
                    remaining[sub] = remaining[sub] - 1
                    words_used = words_used + 1
                else:
                    break
            return words_used == len(words)

        out = []
        for i in range(len(s) - substring_size + 1):
            if check(i):
                out.append(i)
        return out
