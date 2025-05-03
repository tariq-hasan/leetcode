class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        if k >= len(s):
            return len(s)

        def is_valid(size):
            freq = {}
            for i in range(size):
                freq[s[i]] = freq.get(s[i], 0) + 1

            if len(freq) <= k:
                return True

            for i in range(size, len(s)):
                freq[s[i]] = freq.get(s[i], 0) + 1
                freq[s[i - size]] = freq[s[i - size]] - 1
                if freq[s[i - size]] == 0:
                    del freq[s[i - size]]
                if len(freq) <= k:
                    return True
            return False

        left, right = k, len(s)
        while left < right:
            mid = (left + right + 1) // 2 # mid = right - (right - left) // 2
            if is_valid(mid):
                left = mid
            else:
                right = mid - 1

        return left


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(k).
        """
        freq = {}
        i = out = 0
        for j in range(len(s)):
            freq[s[j]] = freq.get(s[j], 0) + 1
            while len(freq) > k:
                freq[s[i]] = freq[s[i]] - 1
                if freq[s[i]] == 0:
                    del freq[s[i]]
                i = i + 1
            out = max(out, j - i + 1)
        return out


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        freq = {}
        out = 0
        for j in range(len(s)):
            freq[s[j]] = freq.get(s[j], 0) + 1
            if len(freq) <= k:
                out = out + 1
            else:
                freq[s[j - out]] = freq[s[j - out]] - 1
                if freq[s[j - out]] == 0:
                    del freq[s[j - out]]
        return out
