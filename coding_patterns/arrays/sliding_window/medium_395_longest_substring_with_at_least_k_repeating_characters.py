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


class Solution:
    def longestSubstring(self, s: str, k: int) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        unique = [False] * 26
        max_unique = 0
        for i in range(len(s)):
            if not unique[ord(s[i]) - ord('a')]:
                max_unique = max_unique + 1
                unique[ord(s[i]) - ord('a')] = True

        out = 0
        for curr_unique in range(1, max_unique + 1):
            freq = [0] * 26
            i = j = unique = count_at_least_k = 0
            while j < len(s):
                if unique <= curr_unique:
                    idx = ord(s[j]) - ord('a')
                    if freq[idx] == 0:
                        unique = unique + 1
                    freq[idx] = freq[idx] + 1
                    if freq[idx] == k:
                        count_at_least_k = count_at_least_k + 1
                    j = j + 1
                else:
                    idx = ord(s[i]) - ord('a')
                    if freq[idx] == k:
                        count_at_least_k = count_at_least_k - 1
                    freq[idx] = freq[idx] - 1
                    if freq[idx] == 0:
                        unique = unique - 1
                    i = i + 1
                if unique == curr_unique and unique == count_at_least_k:
                    out = max(out, j - i)
        return out
