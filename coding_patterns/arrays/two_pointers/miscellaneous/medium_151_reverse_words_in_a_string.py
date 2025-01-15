class Solution:
    def reverseWords(self, s: str) -> None:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        words = list()
        i = -1
        for j in range(len(s)):
            if s[j] == ' ' and i != j:
                if s[i + 1:j]:
                    words.append(s[i + 1:j])
                i = j
            elif j == len(s) - 1 and i != j:
                words.append(s[i + 1:])
        return ' '.join(words[::-1])


from collections import deque
class Solution:
    def reverseWords(self, s: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        i, j = 0, len(s) - 1
        while i <= j and s[i] == ' ':
            i = i + 1
        while i <= j and s[j] == ' ':
            j = j - 1

        d, word = deque(), []
        while i <= j:
            if s[i] == ' ' and word:
                d.appendleft(''.join(word))
                word = []
            elif s[i] != ' ':
                word.append(s[i])
            i = i + 1
        d.appendleft(''.join(word))

        return ' '.join(d)
