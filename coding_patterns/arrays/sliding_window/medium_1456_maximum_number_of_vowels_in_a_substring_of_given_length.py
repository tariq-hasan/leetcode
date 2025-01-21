class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        vowels = {'a', 'e', 'i', 'o', 'u'}
        count = 0
        for i in range(k):
            count = count + int(s[i] in vowels)
        out = count
        for i in range(k, len(s)):
            count = count - int(s[i - k] in vowels)
            count = count + int(s[i] in vowels)
            out = max(out, count)
        return out
