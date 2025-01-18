class Solution:
    def longestSubstring(self, s: str, k: int) -> int:
        """
        The time complexity is O(n^2).
        The space complexity is O(n) - space used to store the recursive call stack.
        """
        def longest_substring_util(s, start, end, k):
            if end < k:
                return 0

            freq = [0] * 26
            for i in range(start, end):
                freq[ord(s[i]) - ord('a')] += 1

            for mid in range(start, end):
                if freq[ord(s[mid]) - ord('a')] >= k:
                    continue
                mid_next = mid + 1
                while mid_next < end and freq[ord(s[mid_next]) - ord('a')] < k:
                    mid_next = mid_next + 1
                return max(longest_substring_util(s, start, mid, k), longest_substring_util(s, mid_next, end, k))
            return end - start

        return longest_substring_util(s, 0, len(s), k)
