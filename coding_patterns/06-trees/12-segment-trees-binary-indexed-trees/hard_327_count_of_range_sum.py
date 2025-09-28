"""
LeetCode 327: Count of Range Sum
Hard

Given an integer array nums and two integers lower and upper, 
return the number of range sums that lie in [lower, upper] inclusive.

Range sum S(i, j) is defined as the sum of the elements in nums 
between indices i and j inclusive, where i <= j.

Example:
Input: nums = [-2,5,-1], lower = -2, upper = 2
Output: 3
Explanation: The three ranges are: [0,0], [2,2], and [0,2] 
with sums -2, -1, and 2 respectively.
"""

from typing import List
import bisect


class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """
        Approach 1: Merge Sort with Divide and Conquer
        Time: O(n log n), Space: O(n)
        
        Key insight: For range sum S(i,j) = prefix[j+1] - prefix[i],
        we need to count pairs where lower <= prefix[j+1] - prefix[i] <= upper
        This is equivalent to: prefix[j+1] - upper <= prefix[i] <= prefix[j+1] - lower
        """
        # Build prefix sum array
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)
        
        def mergeSort(left, right):
            if left >= right:
                return 0
            
            mid = (left + right) // 2
            count = mergeSort(left, mid) + mergeSort(mid + 1, right)
            
            # Count valid pairs across the divide
            # For each j in [mid+1, right], count i in [left, mid] 
            # such that lower <= prefix[j] - prefix[i] <= upper
            j = k = mid + 1
            for i in range(left, mid + 1):
                # Find first j where prefix[j] - prefix[i] >= lower
                while j <= right and prefix[j] - prefix[i] < lower:
                    j += 1
                # Find first k where prefix[k] - prefix[i] > upper
                while k <= right and prefix[k] - prefix[i] <= upper:
                    k += 1
                count += k - j
            
            # Merge the two sorted halves
            temp = []
            i = left
            j = mid + 1
            while i <= mid and j <= right:
                if prefix[i] <= prefix[j]:
                    temp.append(prefix[i])
                    i += 1
                else:
                    temp.append(prefix[j])
                    j += 1
            
            while i <= mid:
                temp.append(prefix[i])
                i += 1
            while j <= right:
                temp.append(prefix[j])
                j += 1
            
            for i, val in enumerate(temp):
                prefix[left + i] = val
            
            return count
        
        return mergeSort(0, len(prefix) - 1)


class Solution2:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """
        Approach 2: Fenwick Tree (Binary Indexed Tree)
        Time: O(n log n), Space: O(n)
        
        Use coordinate compression + BIT to count inversions efficiently
        """
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)
        
        # Coordinate compression
        all_values = []
        for p in prefix:
            all_values.extend([p, p - lower, p - upper])
        
        sorted_values = sorted(set(all_values))
        value_to_index = {v: i + 1 for i, v in enumerate(sorted_values)}
        
        class BIT:
            def __init__(self, n):
                self.n = n
                self.tree = [0] * (n + 1)
            
            def update(self, i, delta):
                while i <= self.n:
                    self.tree[i] += delta
                    i += i & (-i)
            
            def query(self, i):
                result = 0
                while i > 0:
                    result += self.tree[i]
                    i -= i & (-i)
                return result
            
            def range_query(self, l, r):
                return self.query(r) - self.query(l - 1)
        
        bit = BIT(len(sorted_values))
        result = 0
        
        # Process prefix sums from left to right
        bit.update(value_to_index[0], 1)  # Add prefix[0] = 0
        
        for i in range(1, len(prefix)):
            # Count how many previous prefix sums p satisfy:
            # lower <= prefix[i] - p <= upper
            # => prefix[i] - upper <= p <= prefix[i] - lower
            left_bound = value_to_index[prefix[i] - upper]
            right_bound = value_to_index[prefix[i] - lower]
            result += bit.range_query(left_bound, right_bound)
            
            # Add current prefix sum to BIT
            bit.update(value_to_index[prefix[i]], 1)
        
        return result


class Solution3:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """
        Approach 3: Using Python's bisect for simpler implementation
        Time: O(n^2) in worst case, but often faster in practice
        Space: O(n)
        
        This approach is easier to understand and implement in interviews
        """
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)
        
        count = 0
        sorted_prefix = []
        
        for p in prefix:
            # For current prefix sum p, count how many previous prefix sums q
            # satisfy lower <= p - q <= upper
            # This means p - upper <= q <= p - lower
            left = bisect.bisect_left(sorted_prefix, p - upper)
            right = bisect.bisect_right(sorted_prefix, p - lower)
            count += right - left
            
            # Insert current prefix sum maintaining sorted order
            bisect.insort(sorted_prefix, p)
        
        return count


# Test cases
def test_solutions():
    solutions = [Solution(), Solution2(), Solution3()]
    test_cases = [
        ([-2, 5, -1], -2, 2, 3),
        ([0], 0, 0, 1),
        ([-2, 5, -1], -2, 2, 3),
        ([1, 2, 3, 4], 2, 4, 4),
        ([-1, 1], 0, 0, 1)
    ]
    
    for i, solution in enumerate(solutions):
        print(f"Testing Solution {i + 1}:")
        for nums, lower, upper, expected in test_cases:
            result = solution.countRangeSum(nums, lower, upper)
            status = "✓" if result == expected else "✗"
            print(f"  {status} nums={nums}, lower={lower}, upper={upper} -> {result} (expected: {expected})")
        print()


if __name__ == "__main__":
    test_solutions()


"""
Interview Tips:

1. **Start with the key insight**: Range sum S(i,j) = prefix[j+1] - prefix[i]
   The problem becomes: count pairs (i,j) where lower <= prefix[j] - prefix[i] <= upper

2. **Discuss approaches in order of complexity**:
   - Brute force: O(n^3) - check all ranges
   - Optimized brute force: O(n^2) - use prefix sums
   - Advanced: O(n log n) - merge sort or data structures

3. **For interviews, Solution 3 (bisect) is often preferred**:
   - Easier to implement correctly under pressure
   - Clear logic and readable code
   - Good enough performance for most test cases

4. **If asked for optimal solution, use Solution 1 (merge sort)**:
   - Guaranteed O(n log n) time complexity
   - Shows understanding of divide-and-conquer
   - More impressive algorithmically

5. **Key edge cases to mention**:
   - Empty array or single element
   - All negative or all positive numbers
   - lower = upper (exact sum matching)
   - Large numbers that might cause overflow

6. **Space-time tradeoffs**: All solutions use O(n) extra space for prefix sums,
   but merge sort uses additional O(n) space for merging.
"""
