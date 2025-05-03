from typing import List


class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        events = []
        for interval in intervals:
            events.append((interval[0], 1))
            events.append((interval[1] + 1, -1))
        events.sort(key=lambda x: (x[0], x[1]))

        concurrent_intervals = out = 0
        for event in events:
            concurrent_intervals = concurrent_intervals + event[1]
            out = max(out, concurrent_intervals)
        return out


class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(n).
        """
        freq = {}
        for interval in intervals:
            freq[interval[0]] = freq.get(interval[0], 0) + 1
            freq[interval[1] + 1] = freq.get(interval[1] + 1, 0) - 1

        out = concurrent_intervals = 0
        for i in sorted(freq.keys()):
            concurrent_intervals = concurrent_intervals + freq[i]
            out = max(out, concurrent_intervals)
        return out


class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        """
        The time complexity is O(n + k).
        The space complexity is O(k).
        Here, n is the number of intervals and k is the count of numbers between range_start and range_end.
        """
        range_start, range_end = float("inf"), float("-inf")
        for interval in intervals:
            range_start = min(range_start, interval[0])
            range_end = max(range_end, interval[1])

        freq = [0] * (range_end + 2)
        for interval in intervals:
            freq[interval[0]] = freq[interval[0]] + 1
            freq[interval[1] + 1] = freq[interval[1] + 1] - 1

        out = concurrent_intervals = 0
        for i in range(range_start, range_end + 1):
            concurrent_intervals = concurrent_intervals + freq[i]
            out = max(out, concurrent_intervals)
        return out
