class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if len(word1) != len(word2):
            return False

        freq1 = {}
        for c in word1:
            freq1[c] = freq1.get(c, 0) + 1

        freq2 = {}
        for c in word2:
            freq2[c] = freq2.get(c, 0) + 1

        if freq1.keys() != freq2.keys():
            return False

        if sorted(freq1.values()) != sorted(freq2.values()):
            return False

        return True
