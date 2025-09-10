import heapq
from collections import defaultdict
from typing import List

# Solution 1: Two Heaps with Lazy Deletion (Optimal - Most Important)
class Solution:
    """
    Optimal solution using two heaps with lazy deletion
    
    Time Complexity: O(n * log k) where n is array length, k is window size
    Space Complexity: O(k) for the heaps and hash map
    """
    
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def add_num(num):
            """Add number to appropriate heap"""
            if not max_heap or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)
        
        def remove_num(num):
            """Mark number for lazy deletion"""
            to_remove[num] += 1
            if num <= -max_heap[0]:
                max_heap_size[0] -= 1
            else:
                min_heap_size[0] -= 1
        
        def balance_heaps():
            """Balance heaps and clean up removed elements"""
            # Clean up max_heap top
            while max_heap and to_remove[-max_heap[0]] > 0:
                to_remove[-max_heap[0]] -= 1
                heapq.heappop(max_heap)
            
            # Clean up min_heap top
            while min_heap and to_remove[min_heap[0]] > 0:
                to_remove[min_heap[0]] -= 1
                heapq.heappop(min_heap)
            
            # Balance sizes
            if max_heap_size[0] > min_heap_size[0] + 1:
                # Move from max to min
                while max_heap and to_remove[-max_heap[0]] > 0:
                    to_remove[-max_heap[0]] -= 1
                    heapq.heappop(max_heap)
                if max_heap:
                    heapq.heappush(min_heap, -heapq.heappop(max_heap))
                    max_heap_size[0] -= 1
                    min_heap_size[0] += 1
            
            elif min_heap_size[0] > max_heap_size[0]:
                # Move from min to max
                while min_heap and to_remove[min_heap[0]] > 0:
                    to_remove[min_heap[0]] -= 1
                    heapq.heappop(min_heap)
                if min_heap:
                    heapq.heappush(max_heap, -heapq.heappop(min_heap))
                    min_heap_size[0] += 1
                    max_heap_size[0] -= 1
        
        def get_median():
            """Get current median"""
            balance_heaps()
            if k % 2 == 1:
                return float(-max_heap[0])
            else:
                return (-max_heap[0] + min_heap[0]) / 2.0
        
        max_heap = []  # smaller half (negated)
        min_heap = []  # larger half
        to_remove = defaultdict(int)  # lazy deletion map
        max_heap_size = [0]  # use list for reference
        min_heap_size = [0]
        result = []
        
        # Initialize first window
        for i in range(k):
            add_num(nums[i])
            max_heap_size[0] += 1 if not max_heap or nums[i] <= -max_heap[0] else 0
            min_heap_size[0] += 1 if max_heap and nums[i] > -max_heap[0] else 0
        
        balance_heaps()
        result.append(get_median())
        
        # Process remaining elements
        for i in range(k, len(nums)):
            # Remove outgoing element
            remove_num(nums[i - k])
            
            # Add incoming element
            add_num(nums[i])
            if not max_heap or nums[i] <= -max_heap[0]:
                max_heap_size[0] += 1
            else:
                min_heap_size[0] += 1
            
            result.append(get_median())
        
        return result


# Solution 2: Cleaner Two Heaps Implementation
class SolutionCleaner:
    """
    Cleaner implementation with better separation of concerns
    Same time/space complexity but easier to understand
    """
    
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def add_number(heaps, num):
            small, large = heaps
            heapq.heappush(small, -heapq.heappushpop(large, num))
            if len(small) > len(large):
                heapq.heappush(large, -heapq.heappop(small))
        
        def get_median(heaps, k):
            small, large = heaps
            if k % 2:
                return float(large[0])
            return (large[0] - small[0]) / 2.0
        
        heaps = [], []
        result = []
        
        # Process first window
        for i in range(k):
            add_number(heaps, nums[i])
        result.append(get_median(heaps, k))
        
        # Process sliding windows
        for i in range(k, len(nums)):
            # Remove old element and add new element
            small, large = heaps
            
            # Find and remove the outgoing element
            outgoing = nums[i - k]
            incoming = nums[i]
            
            # This approach rebuilds heaps for each window (less efficient but simpler)
            window = []
            # Collect current window elements
            window = nums[i-k+1:i+1]
            
            # Rebuild heaps
            heaps = [], []
            for num in window:
                add_number(heaps, num)
            
            result.append(get_median(heaps, k))
        
        return result


# Solution 3: Multiset Approach (Most Intuitive)
class SolutionMultiset:
    """
    Using a multiset-like structure with binary search
    Time: O(n * k * log k), Space: O(k)
    
    Note: This is less efficient but more intuitive
    Good for explaining the problem before optimizing
    """
    
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        import bisect
        
        result = []
        window = []
        
        # Initialize first window
        for i in range(k):
            bisect.insort(window, nums[i])
        
        # Get median of first window
        if k % 2 == 1:
            result.append(float(window[k // 2]))
        else:
            result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
        
        # Slide the window
        for i in range(k, len(nums)):
            # Remove outgoing element
            outgoing = nums[i - k]
            idx = bisect.bisect_left(window, outgoing)
            window.pop(idx)
            
            # Add incoming element
            bisect.insort(window, nums[i])
            
            # Calculate median
            if k % 2 == 1:
                result.append(float(window[k // 2]))
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
        
        return result


# Solution 4: Segment Tree Approach (Advanced)
class SolutionSegmentTree:
    """
    Advanced solution using coordinate compression + segment tree
    Good for follow-up discussions about handling large value ranges
    """
    
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        # Coordinate compression
        sorted_nums = sorted(set(nums))
        coord_map = {num: i for i, num in enumerate(sorted_nums)}
        
        class SegmentTree:
            def __init__(self, n):
                self.n = n
                self.tree = [0] * (4 * n)
            
            def update(self, node, start, end, idx, val):
                if start == end:
                    self.tree[node] += val
                else:
                    mid = (start + end) // 2
                    if idx <= mid:
                        self.update(2 * node, start, mid, idx, val)
                    else:
                        self.update(2 * node + 1, mid + 1, end, idx, val)
                    self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
            
            def query_kth(self, node, start, end, k):
                if start == end:
                    return start
                mid = (start + end) // 2
                left_count = self.tree[2 * node]
                if k <= left_count:
                    return self.query_kth(2 * node, start, mid, k)
                else:
                    return self.query_kth(2 * node + 1, mid + 1, end, k - left_count)
        
        n = len(sorted_nums)
        seg_tree = SegmentTree(n)
        result = []
        
        # Initialize first window
        for i in range(k):
            seg_tree.update(1, 0, n - 1, coord_map[nums[i]], 1)
        
        # Get median of first window
        if k % 2 == 1:
            median_idx = seg_tree.query_kth(1, 0, n - 1, k // 2 + 1)
            result.append(float(sorted_nums[median_idx]))
        else:
            idx1 = seg_tree.query_kth(1, 0, n - 1, k // 2)
            idx2 = seg_tree.query_kth(1, 0, n - 1, k // 2 + 1)
            result.append((sorted_nums[idx1] + sorted_nums[idx2]) / 2.0)
        
        # Process remaining windows
        for i in range(k, len(nums)):
            # Remove outgoing
            seg_tree.update(1, 0, n - 1, coord_map[nums[i - k]], -1)
            # Add incoming
            seg_tree.update(1, 0, n - 1, coord_map[nums[i]], 1)
            
            # Get median
            if k % 2 == 1:
                median_idx = seg_tree.query_kth(1, 0, n - 1, k // 2 + 1)
                result.append(float(sorted_nums[median_idx]))
            else:
                idx1 = seg_tree.query_kth(1, 0, n - 1, k // 2)
                idx2 = seg_tree.query_kth(1, 0, n - 1, k // 2 + 1)
                result.append((sorted_nums[idx1] + sorted_nums[idx2]) / 2.0)
        
        return result


# Test cases and examples
def test_sliding_window_median():
    """Test all implementations with various cases"""
    
    test_cases = [
        # (nums, k, expected)
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]),
        ([1, 2, 3, 4, 2, 3, 1, 4, 2], 3, [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]),
        ([1, 4, 2, 3], 4, [2.5]),
        ([1, 2], 1, [1.0, 2.0]),
        ([2147483647, 2147483647], 2, [2147483647.0]),  # edge case with large numbers
    ]
    
    solutions = [
        ("Two Heaps with Lazy Deletion", Solution()),
        ("Multiset Approach", SolutionMultiset()),
    ]
    
    for name, solution in solutions:
        print(f"\nTesting {name}:")
        print("=" * 50)
        
        for i, (nums, k, expected) in enumerate(test_cases):
            try:
                result = solution.medianSlidingWindow(nums, k)
                passed = all(abs(r - e) < 1e-9 for r, e in zip(result, expected))
                status = "PASS" if passed else "FAIL"
                
                print(f"Test {i+1}: {status}")
                print(f"  Input: nums={nums}, k={k}")
                print(f"  Expected: {expected}")
                print(f"  Got:      {result}")
                
                if not passed:
                    print(f"  Difference: {[r-e for r, e in zip(result, expected)]}")
                
            except Exception as e:
                print(f"Test {i+1}: ERROR - {str(e)}")


def demonstrate_complexity():
    """Demonstrate time complexity differences"""
    import time
    import random
    
    print("Complexity Demonstration:")
    print("=" * 50)
    
    # Generate test data
    test_sizes = [(100, 10), (500, 20), (1000, 50)]
    
    for n, k in test_sizes:
        nums = [random.randint(-10000, 10000) for _ in range(n)]
        
        print(f"\nTesting with n={n}, k={k}:")
        
        # Test multiset approach
        start = time.time()
        sol_multiset = SolutionMultiset()
        result1 = sol_multiset.medianSlidingWindow(nums, k)
        time1 = time.time() - start
        
        # Test two heaps approach
        start = time.time()
        sol_heaps = Solution()
        result2 = sol_heaps.medianSlidingWindow(nums, k)
        time2 = time.time() - start
        
        print(f"  Multiset:  {time1:.4f}s")
        print(f"  Two Heaps: {time2:.4f}s")
        print(f"  Speedup:   {time1/time2:.2f}x")
        
        # Verify results match
        matches = all(abs(a - b) < 1e-9 for a, b in zip(result1, result2))
        print(f"  Results match: {matches}")


if __name__ == "__main__":
    test_sliding_window_median()
    # demonstrate_complexity()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Find median of each sliding window of size k
   - Window slides one position at a time
   - Need to handle both additions and removals efficiently

2. APPROACH EVOLUTION:
   
   a) Naive: Sort each window -> O(n * k * log k)
   b) Better: Maintain sorted window with insertions/deletions -> O(n * k)  
   c) Optimal: Two heaps with lazy deletion -> O(n * log k)

3. KEY CHALLENGES:
   - Efficiently removing arbitrary elements from heaps
   - Maintaining heap balance during removals
   - Handling duplicate elements correctly

4. TWO HEAPS WITH LAZY DELETION EXPLANATION:
   - Use same two-heap strategy as "Find Median from Data Stream"
   - Instead of actual removal, mark elements for "lazy deletion"
   - Clean up heap tops when accessing
   - Track logical sizes separately from actual heap sizes

5. CRITICAL INSIGHTS TO MENTION:
   - "Direct heap removal is O(k), but lazy deletion makes it O(log k)"
   - "We need to balance heaps after each window slide"
   - "Lazy deletion avoids expensive linear searches in heaps"

6. IMPLEMENTATION DETAILS:
   - Use hash map to track elements to remove
   - Maintain logical heap sizes separately
   - Clean heap tops before accessing median
   - Handle edge cases (k=1, k=n, duplicate elements)

7. TIME/SPACE COMPLEXITY:
   - Two Heaps: O(n * log k) time, O(k) space
   - Multiset: O(n * k * log k) time, O(k) space
   - Explain why heap solution is optimal

8. EDGE CASES:
   - Single element windows (k=1)
   - Window size equals array length (k=n)
   - Duplicate elements
   - Large numbers (integer overflow in median calculation)

9. FOLLOW-UP QUESTIONS:
   - What if k is very large? (Consider different data structures)
   - What if we need other percentiles? (Generalize heap approach)
   - What about memory constraints? (External sorting approaches)
   - Parallel processing? (Segment tree or distributed approaches)

10. COMMON MISTAKES:
    - Not handling lazy deletion correctly
    - Forgetting to balance heaps after removals
    - Integer overflow when calculating median
    - Not cleaning heap tops before accessing

INTERVIEW TIP: Start with the multiset approach to show understanding,
then evolve to the optimal two-heaps solution. This demonstrates
problem-solving progression and deep algorithmic thinking.
"""
