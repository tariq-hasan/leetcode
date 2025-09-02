"""
LeetCode 673: Number of Longest Increasing Subsequence

Problem: Given an integer array nums, return the number of longest increasing subsequences.

Example 1:
Input: nums = [1,3,5,4,7]
Output: 2
Explanation: The two longest increasing subsequences are [1,3,4,7] and [1,3,5,7].

Example 2:
Input: nums = [2,2,2,2,2]
Output: 5
Explanation: The length of longest continuous increasing subsequence is 1, 
and there are 5 subsequences' length is 1, therefore output 5.

Approach: Dynamic Programming
- For each position i, track:
  1. lengths[i]: length of LIS ending at i
  2. counts[i]: number of LIS ending at i
- Time: O(n²), Space: O(n)
"""

def findNumberOfLIS(nums):
    """
    Main solution using dynamic programming.
    
    Args:
        nums: List[int] - input array
    
    Returns:
        int - number of longest increasing subsequences
    """
    if not nums:
        return 0
    
    n = len(nums)
    # lengths[i] = length of LIS ending at index i
    lengths = [1] * n
    # counts[i] = number of LIS ending at index i
    counts = [1] * n
    
    # Fill lengths and counts arrays
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    # Found a longer LIS ending at i
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    # Found another LIS of same length ending at i
                    counts[i] += counts[j]
    
    # Find the maximum length
    max_length = max(lengths)
    
    # Sum up counts for all positions with max length
    result = 0
    for i in range(n):
        if lengths[i] == max_length:
            result += counts[i]
    
    return result


def findNumberOfLIS_optimized(nums):
    """
    Optimized solution using segment tree or coordinate compression.
    This is a more advanced approach for follow-up questions.
    
    Time: O(n log n), Space: O(n)
    """
    if not nums:
        return 0
    
    # Coordinate compression
    sorted_nums = sorted(set(nums))
    coord_map = {num: i for i, num in enumerate(sorted_nums)}
    
    # Segment tree node: (max_length, count)
    class SegmentTree:
        def __init__(self, n):
            self.n = n
            self.tree = [(0, 1)] * (4 * n)
        
        def combine(self, left, right):
            if left[0] > right[0]:
                return left
            elif left[0] < right[0]:
                return right
            else:
                return (left[0], left[1] + right[1])
        
        def update(self, node, start, end, idx, val):
            if start == end:
                self.tree[node] = self.combine(self.tree[node], val)
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    self.update(2*node, start, mid, idx, val)
                else:
                    self.update(2*node+1, mid+1, end, idx, val)
                self.tree[node] = self.combine(
                    self.tree[2*node], 
                    self.tree[2*node+1]
                )
        
        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return (0, 1)
            if l <= start and end <= r:
                return self.tree[node]
            
            mid = (start + end) // 2
            left_result = self.query(2*node, start, mid, l, r)
            right_result = self.query(2*node+1, mid+1, end, l, r)
            return self.combine(left_result, right_result)
    
    st = SegmentTree(len(sorted_nums))
    
    for num in nums:
        coord = coord_map[num]
        
        # Query for all numbers less than current
        if coord > 0:
            max_len, count = st.query(1, 0, len(sorted_nums)-1, 0, coord-1)
            st.update(1, 0, len(sorted_nums)-1, coord, (max_len + 1, count))
        else:
            st.update(1, 0, len(sorted_nums)-1, coord, (1, 1))
    
    # Query the entire range
    _, result = st.query(1, 0, len(sorted_nums)-1, 0, len(sorted_nums)-1)
    return result


# Test cases
def test_solution():
    """Test the solution with example cases."""
    
    test_cases = [
        ([1, 3, 5, 4, 7], 2),
        ([2, 2, 2, 2, 2], 5),
        ([1, 2, 4, 3, 5, 4, 7, 2], 3),
        ([1], 1),
        ([1, 2, 3], 1),
        ([3, 2, 1], 3),
        ([], 0)
    ]
    
    print("Testing basic DP solution:")
    for nums, expected in test_cases:
        result = findNumberOfLIS(nums)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {nums}, Expected: {expected}, Got: {result}")
    
    print("\nStep-by-step trace for [1,3,5,4,7]:")
    trace_example([1, 3, 5, 4, 7])


def trace_example(nums):
    """Trace through the algorithm step by step for understanding."""
    if not nums:
        return 0
    
    n = len(nums)
    lengths = [1] * n
    counts = [1] * n
    
    print(f"Initial: lengths = {lengths}, counts = {counts}")
    
    for i in range(1, n):
        print(f"\nProcessing nums[{i}] = {nums[i]}:")
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                    print(f"  From j={j} (nums[{j}]={nums[j]}): "
                          f"New longer LIS, lengths[{i}]={lengths[i]}, "
                          f"counts[{i}]={counts[i]}")
                elif lengths[j] + 1 == lengths[i]:
                    counts[i] += counts[j]
                    print(f"  From j={j} (nums[{j}]={nums[j]}): "
                          f"Same length LIS, counts[{i}]={counts[i]}")
        
        print(f"After processing i={i}: lengths = {lengths}, counts = {counts}")
    
    max_length = max(lengths)
    result = sum(counts[i] for i in range(n) if lengths[i] == max_length)
    
    print(f"\nMax length: {max_length}")
    print(f"Positions with max length: "
          f"{[i for i in range(n) if lengths[i] == max_length]}")
    print(f"Total count: {result}")


if __name__ == "__main__":
    test_solution()
