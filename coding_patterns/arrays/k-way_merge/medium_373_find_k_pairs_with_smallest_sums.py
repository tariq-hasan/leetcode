from typing import List


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        """
        The time complexity is O(min(k * log k, m * n * log(m * n))).
        The space complexity is O(min(k, m * n)).
        Here m and n are the lengths of nums1 and nums2.
        """
        from heapq import heappush, heappop
        out = []
        seen = set()

        min_heap = [(nums1[0] + nums2[0], (0, 0))]
        seen.add((0, 0))
        count = 0

        while k > 0 and min_heap:
            val, (i, j) = heappop(min_heap)
            out.append([nums1[i], nums2[j]])

            if i + 1 < len(nums1) and (i + 1, j) not in seen:
                heappush(min_heap, (nums1[i + 1] + nums2[j], (i + 1, j)))
                seen.add((i + 1, j))

            if j + 1 < len(nums2) and (i, j + 1) not in seen:
                heappush(min_heap, (nums1[i] + nums2[j + 1], (i, j + 1)))
                seen.add((i, j + 1))
            k = k - 1
        
        return out
