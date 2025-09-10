import heapq
from typing import List

# Solution 1: Two Heaps (Optimal - Most Important for Interviews)
class MedianFinder:
    """
    Optimal solution using two heaps to maintain median in O(log n) time
    
    Time Complexity:
    - addNum: O(log n)
    - findMedian: O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self):
        """
        Initialize data structure.
        
        Strategy:
        - max_heap: stores smaller half of numbers (use negative values for max heap)
        - min_heap: stores larger half of numbers
        - Keep heaps balanced: |max_heap| - |min_heap| <= 1
        """
        self.max_heap = []  # smaller half (negated for max heap behavior)
        self.min_heap = []  # larger half
    
    def addNum(self, num: int) -> None:
        """Add a number to the data structure"""
        # Always add to max_heap first (smaller half)
        heapq.heappush(self.max_heap, -num)
        
        # Move the largest from max_heap to min_heap to maintain order
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # Balance the heaps - max_heap can have at most 1 more element
        if len(self.max_heap) < len(self.min_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def findMedian(self) -> float:
        """Find the median of all elements"""
        if len(self.max_heap) > len(self.min_heap):
            # Odd number of elements, median is top of max_heap
            return -self.max_heap[0]
        else:
            # Even number of elements, median is average of both tops
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0


# Solution 2: Alternative Two Heaps Implementation (Clearer Logic)
class MedianFinderClear:
    """
    Alternative implementation with clearer logic flow
    Same time/space complexity but easier to understand
    """
    
    def __init__(self):
        self.small = []  # max heap (negated) - smaller half
        self.large = []  # min heap - larger half
    
    def addNum(self, num: int) -> None:
        # Add to appropriate heap based on size and values
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)
        
        # Rebalance if necessary
        if len(self.small) > len(self.large) + 1:
            # Move from small to large
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            # Move from large to small
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2.0


# Solution 3: Simple Array (For Comparison - Not Optimal)
class MedianFinderArray:
    """
    Simple array-based solution for comparison
    
    Time Complexity:
    - addNum: O(n) for insertion sort
    - findMedian: O(1)
    
    Space Complexity: O(n)
    
    Not recommended for interviews but good to mention for comparison
    """
    
    def __init__(self):
        self.nums = []
    
    def addNum(self, num: int) -> None:
        # Insert in sorted order
        left, right = 0, len(self.nums)
        while left < right:
            mid = (left + right) // 2
            if self.nums[mid] < num:
                left = mid + 1
            else:
                right = mid
        self.nums.insert(left, num)
    
    def findMedian(self) -> float:
        n = len(self.nums)
        if n % 2 == 1:
            return self.nums[n // 2]
        else:
            return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0


# Solution 4: Advanced - Using Buckets (For Very Large Datasets)
class MedianFinderBuckets:
    """
    Advanced solution using buckets for very large datasets
    Good to mention as a follow-up optimization
    
    Assumes numbers are in a reasonable range (e.g., -50000 to 50000)
    """
    
    def __init__(self):
        self.buckets = {}  # value -> count
        self.total_count = 0
    
    def addNum(self, num: int) -> None:
        self.buckets[num] = self.buckets.get(num, 0) + 1
        self.total_count += 1
    
    def findMedian(self) -> float:
        if self.total_count % 2 == 1:
            # Odd count - find middle element
            target = self.total_count // 2 + 1
            count = 0
            for num in sorted(self.buckets.keys()):
                count += self.buckets[num]
                if count >= target:
                    return num
        else:
            # Even count - find two middle elements
            target1 = self.total_count // 2
            target2 = self.total_count // 2 + 1
            count = 0
            median_nums = []
            
            for num in sorted(self.buckets.keys()):
                count += self.buckets[num]
                if count >= target1 and len(median_nums) == 0:
                    median_nums.append(num)
                if count >= target2:
                    median_nums.append(num)
                    break
            
            return sum(median_nums) / 2.0


# Test cases and demonstration
def test_median_finder():
    """Test the MedianFinder implementations"""
    
    print("Testing MedianFinder (Two Heaps):")
    mf = MedianFinder()
    
    # Test case 1: LeetCode example
    test_sequence = [1, 2, 3]
    expected_medians = [1.0, 1.5, 2.0]
    
    for i, num in enumerate(test_sequence):
        mf.addNum(num)
        median = mf.findMedian()
        print(f"After adding {num}: median = {median} (expected: {expected_medians[i]})")
    
    print("\nTesting with more numbers:")
    # Continue with more numbers
    more_nums = [4, 5, 6]
    for num in more_nums:
        mf.addNum(num)
        median = mf.findMedian()
        print(f"After adding {num}: median = {median}")


def demonstrate_all_solutions():
    """Compare different implementations"""
    solutions = [
        ("Two Heaps (Optimal)", MedianFinder()),
        ("Two Heaps (Clear)", MedianFinderClear()),
        ("Array Based", MedianFinderArray()),
        ("Buckets", MedianFinderBuckets())
    ]
    
    test_nums = [5, 15, 1, 3, 8, 7, 9, 2]
    
    for name, finder in solutions:
        print(f"\n{name}:")
        for num in test_nums:
            finder.addNum(num)
            median = finder.findMedian()
            print(f"Add {num} -> Median: {median}")


# Performance analysis function
def analyze_performance():
    """Analyze time complexity of different approaches"""
    import time
    import random
    
    print("Performance Analysis:")
    print("=" * 50)
    
    test_sizes = [1000, 5000, 10000]
    
    for size in test_sizes:
        print(f"\nTesting with {size} random numbers:")
        
        # Generate random test data
        nums = [random.randint(-10000, 10000) for _ in range(size)]
        
        # Test Two Heaps solution
        mf_heap = MedianFinder()
        start_time = time.time()
        
        for num in nums:
            mf_heap.addNum(num)
        
        # Get final median
        final_median = mf_heap.findMedian()
        heap_time = time.time() - start_time
        
        print(f"  Two Heaps: {heap_time:.4f}s, Final median: {final_median}")
        
        # Test Array solution (only for smaller sizes)
        if size <= 1000:
            mf_array = MedianFinderArray()
            start_time = time.time()
            
            for num in nums:
                mf_array.addNum(num)
            
            final_median = mf_array.findMedian()
            array_time = time.time() - start_time
            
            print(f"  Array:     {array_time:.4f}s, Final median: {final_median}")
            print(f"  Speedup:   {array_time/heap_time:.2f}x faster with heaps")


if __name__ == "__main__":
    test_median_finder()
    # demonstrate_all_solutions()
    # analyze_performance()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Need to support two operations: addNum() and findMedian()
   - Median changes as we add numbers
   - Need to be efficient for both operations

2. APPROACH EVOLUTION:
   Start by mentioning naive approaches, then evolve to optimal:
   
   a) Naive: Sort array each time -> O(n log n) addNum, O(1) findMedian
   b) Better: Keep sorted array -> O(n) addNum, O(1) findMedian  
   c) Optimal: Two heaps -> O(log n) addNum, O(1) findMedian

3. TWO HEAPS EXPLANATION:
   - max_heap: stores smaller half (use negative values)
   - min_heap: stores larger half
   - Keep balanced: |max_heap| - |min_heap| ≤ 1
   - Median is either top of larger heap or average of both tops

4. KEY INSIGHTS TO MENTION:
   - "We need to maintain the middle element(s) efficiently"
   - "Heaps give us O(log n) insertion and O(1) access to extremes"
   - "Two heaps let us access both middle elements in O(1)"

5. EDGE CASES:
   - Single element
   - Even vs odd number of elements
   - Duplicate numbers
   - Very large/small numbers

6. FOLLOW-UP QUESTIONS:
   - What if numbers are in a specific range? (Buckets/Counting)
   - What if we need other percentiles? (Multiple heaps)
   - What about memory constraints? (External sorting)
   - Parallel processing? (Distributed systems)

7. TIME/SPACE COMPLEXITY:
   - Two Heaps: O(log n) add, O(1) find, O(n) space
   - Array: O(n) add, O(1) find, O(n) space
   - Explain why heap solution is optimal

8. IMPLEMENTATION TIPS:
   - Handle heap balancing carefully
   - Remember Python heapq is min-heap (use negatives for max-heap)
   - Test with both odd and even number of elements
"""
