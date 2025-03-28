class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        seen = set()
        i = out = 0
        for j in range(len(s)):
            if s[j] in seen:
                while s[j] in seen:
                    seen.remove(s[i])
                    i = i + 1
            seen.add(s[j])
            out = max(out, len(seen))
        return out


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        freq = {}
        i = out = 0
        for j in range(len(s)):
            freq[s[j]] = freq.get(s[j], 0) + 1
            while freq[s[j]] > 1:
                freq[s[i]] = freq[s[i]] - 1
                i = i + 1
            out = max(out, j - i + 1)
        return out


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        mapping = {}
        i = out = 0
        for j in range(len(s)):
            if s[j] in mapping:
                i = max(mapping[s[j]], i)
            out = max(out, j - i + 1)
            mapping[s[j]] = j + 1
        return out
