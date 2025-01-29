class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
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
