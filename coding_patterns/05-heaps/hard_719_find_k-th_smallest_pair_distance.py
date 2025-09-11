"""
LeetCode 719 - Find K-th Smallest Pair Distance
Difficulty: Hard

Problem:
The distance of a pair of integers a and b is defined as the absolute difference |a - b|.
Given an integer array nums and an integer k, return the kth smallest distance among all the pairs.

Example 1:
Input: nums = [1,3,1], k = 1
Output: 0
Explanation: Here are all the pairs:
(1,3) -> 2
(1,1) -> 0
(3,1) -> 2
Then the 1st smallest distance pair is (1,1), and its distance is 0.

Example 2:
Input: nums = [1,1,1], k = 2
Output: 0

Example 3:
Input: nums = [1,6,1], k = 3
Output: 5

Solution Strategy:
1. Binary search on the answer (distance value)
2. For each candidate distance, count how many pairs have distance <= candidate
3. Use two pointers to efficiently count pairs with distance <= mid
4. Adjust binary search bounds based on count vs k
"""

from typing import List

def smallestDistancePair(nums: List[int], k: int) -> int:
    """
    Optimal Solution: Binary Search + Two Pointers
    
    Time Complexity: O(n log n + n log(max_distance))
    Space Complexity: O(1)
    
    Args:
        nums: Array of integers
        k: Find kth smallest pair distance
    
    Returns:
        The kth smallest distance among all pairs
    """
    nums.sort()  # Sort to enable two-pointer technique
    n = len(nums)
    
    # Binary search bounds
    left = 0  # Minimum possible distance
    right = nums[-1] - nums[0]  # Maximum possible distance
    
    def count_pairs_with_distance_le(max_distance: int) -> int:
        """
        Count pairs with distance <= max_distance using two pointers
        
        Time Complexity: O(n)
        """
        count = 0
        left_ptr = 0
        
        for right_ptr in range(n):
            # Move left pointer until distance <= max_distance
            while nums[right_ptr] - nums[left_ptr] > max_distance:
                left_ptr += 1
            
            # All pairs from left_ptr to right_ptr-1 with right_ptr
            count += right_ptr - left_ptr
        
        return count
    
    # Binary search on the answer
    while left < right:
        mid = (left + right) // 2
        pairs_count = count_pairs_with_distance_le(mid)
        
        if pairs_count >= k:
            right = mid  # mid might be the answer, don't exclude it
        else:
            left = mid + 1  # mid is too small
    
    return left


def smallestDistancePairBruteForce(nums: List[int], k: int) -> int:
    """
    Brute Force Solution (for understanding and small inputs)
    
    Time Complexity: O(n^2 log(n^2))
    Space Complexity: O(n^2)
    
    This approach generates all pairs and sorts them.
    Only use for understanding or very small inputs.
    """
    distances = []
    n = len(nums)
    
    for i in range(n):
        for j in range(i + 1, n):
            distances.append(abs(nums[i] - nums[j]))
    
    distances.sort()
    return distances[k - 1]


def smallestDistancePairHeap(nums: List[int], k: int) -> int:
    """
    Alternative: Priority Queue approach (less efficient)
    
    Time Complexity: O(n^2 log k)
    Space Complexity: O(k)
    
    Uses max heap to maintain k smallest distances.
    Still generates all pairs but more space efficient.
    """
    import heapq
    
    max_heap = []  # Will store negative values for max heap behavior
    n = len(nums)
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = abs(nums[i] - nums[j])
            
            if len(max_heap) < k:
                heapq.heappush(max_heap, -distance)
            elif distance < -max_heap[0]:
                heapq.heapreplace(max_heap, -distance)
    
    return -max_heap[0]


def smallestDistancePairOptimized(nums: List[int], k: int) -> int:
    """
    Optimized version with early termination and better bounds
    """
    nums.sort()
    n = len(nums)
    
    # Optimized bounds
    left = 0
    right = nums[-1] - nums[0]
    
    # Early termination: if k == 1, return minimum distance
    if k == 1:
        min_dist = float('inf')
        for i in range(1, n):
            min_dist = min(min_dist, nums[i] - nums[i-1])
        return min_dist
    
    def count_pairs_with_distance_le(max_distance: int) -> int:
        count = 0
        left_ptr = 0
        
        for right_ptr in range(n):
            # Move left pointer to maintain distance constraint
            while nums[right_ptr] - nums[left_ptr] > max_distance:
                left_ptr += 1
            
            # Count pairs (left_ptr, right_ptr), (left_ptr+1, right_ptr), ..., (right_ptr-1, right_ptr)
            count += right_ptr - left_ptr
        
        return count
    
    # Binary search with optimized bounds
    while left < right:
        mid = left + (right - left) // 2
        pairs_count = count_pairs_with_distance_le(mid)
        
        if pairs_count >= k:
            right = mid
        else:
            left = mid + 1
    
    return left


def test_kth_smallest_pair_distance():
    """Comprehensive test cases"""
    
    test_cases = [
        ([1, 3, 1], 1, 0),  # Example 1
        ([1, 1, 1], 2, 0),  # Example 2  
        ([1, 6, 1], 3, 5),  # Example 3
        ([1, 2, 3, 4], 3, 1),  # Multiple distances
        ([0, 1, 2, 3], 2, 1),  # Sequential array
        ([38, 33, 57, 65, 13, 2, 86, 75, 4, 56], 26, 36),  # Larger case
    ]
    
    for i, (nums, k, expected) in enumerate(test_cases):
        result_optimal = smallestDistancePair(nums.copy(), k)
        result_brute = smallestDistancePairBruteForce(nums.copy(), k)
        
        print(f"Test {i+1}:")
        print(f"  Input: nums={nums}, k={k}")
        print(f"  Expected: {expected}")
        print(f"  Optimal: {result_optimal}")
        print(f"  Brute Force: {result_brute}")
        print(f"  ✓ Pass" if result_optimal == expected == result_brute else "  ✗ Fail")
        print()


if __name__ == "__main__":
    test_kth_smallest_pair_distance()


"""
Key Insights for Big Tech Interview:

1. **Binary Search on Answer**: 
   - Search space is [0, max(nums) - min(nums)]
   - For each candidate distance, count pairs with distance <= candidate
   - Adjust bounds based on whether count >= k

2. **Two-Pointer Counting Technique**:
   - Sort array first
   - For each right pointer, find leftmost valid left pointer
   - Count = right - left (all valid pairs ending at right)

3. **Why This Works**:
   - If we can find X pairs with distance <= mid, and X >= k,
     then kth smallest distance <= mid
   - Binary search finds the minimum such distance

4. **Time Complexity Breakdown**:
   - Sorting: O(n log n)
   - Binary search: O(log(max_distance)) iterations
   - Each iteration: O(n) for counting
   - Total: O(n log n + n log(max_distance))

5. **Common Pitfalls**:
   - Not sorting the array first
   - Wrong binary search bounds (left < right vs left <= right)
   - Incorrect counting logic in two-pointer method
   - Off-by-one errors in pair counting

Interview Tips:
1. Start with brute force to show understanding
2. Identify that this is "binary search on answer" pattern
3. Explain the two-pointer counting technique clearly
4. Walk through the binary search logic step by step
5. Discuss time/space complexity trade-offs

Follow-up Questions:
- How would you handle duplicate values?
- What if we want the kth largest distance?
- Can you optimize for very large k?
- How would you modify for 2D points (Manhattan/Euclidean distance)?
"""
