from collections import defaultdict
from heapq import heappush, heappop
from typing import List

class MedianFinder:
    """
    A data structure that maintains the median of a sliding window of size k.
    Uses two heaps (max heap for smaller half, min heap for larger half) with lazy deletion.
    
    Time Complexity: O(log k) for add/remove operations
    Space Complexity: O(k) for storing elements
    """
  
    def __init__(self, k: int):
        """Initialize the MedianFinder with window size k."""
        self.k = k
        # Max heap for smaller half (negated values for max heap behavior)
        self.small = []
        # Min heap for larger half
        self.large = []
        # Track elements to be lazily deleted with their counts
        self.delayed = defaultdict(int)
        # Actual size of elements in small heap (excluding delayed deletions)
        self.small_size = 0
        # Actual size of elements in large heap (excluding delayed deletions)
        self.large_size = 0

    def add_num(self, num: int) -> None:
        """Add a number to the data structure."""
        # Determine which heap to add the number to
        if not self.small or num <= -self.small[0]:
            # Add to small heap (negate for max heap behavior)
            heappush(self.small, -num)
            self.small_size += 1
        else:
            # Add to large heap
            heappush(self.large, num)
            self.large_size += 1
      
        # Ensure heaps remain balanced
        self.rebalance()

    def find_median(self) -> float:
        """Find the median of current elements in the window."""
        # If k is odd, median is the top of small heap
        # If k is even, median is average of tops of both heaps
        return -self.small[0] if self.k & 1 else (-self.small[0] + self.large[0]) / 2

    def remove_num(self, num: int) -> None:
        """Remove a number from the data structure using lazy deletion."""
        # Mark the number for lazy deletion
        self.delayed[num] += 1
      
        # Update size and prune if the number is at the top
        if num <= -self.small[0]:
            self.small_size -= 1
            if num == -self.small[0]:
                self.prune(self.small)
        else:
            self.large_size -= 1
            if num == self.large[0]:
                self.prune(self.large)
      
        # Ensure heaps remain balanced
        self.rebalance()

    def prune(self, heap: List[int]) -> None:
        """Remove all delayed elements from the top of the heap."""
        # Determine sign for value conversion (-1 for small heap, 1 for large heap)
        sign = -1 if heap is self.small else 1
      
        # Remove all delayed elements from the top
        while heap and sign * heap[0] in self.delayed:
            # Decrease the delay count
            self.delayed[sign * heap[0]] -= 1
            # Remove from delayed dict if count reaches 0
            if self.delayed[sign * heap[0]] == 0:
                self.delayed.pop(sign * heap[0])
            # Remove from heap
            heappop(heap)

    def rebalance(self) -> None:
        """
        Rebalance the two heaps to maintain the median property.
        Small heap should have equal or one more element than large heap.
        """
        # If small heap has too many elements, move one to large heap
        if self.small_size > self.large_size + 1:
            heappush(self.large, -heappop(self.small))
            self.small_size -= 1
            self.large_size += 1
            # Clean up any delayed elements exposed at the top
            self.prune(self.small)
        # If large heap has more elements, move one to small heap
        elif self.small_size < self.large_size:
            heappush(self.small, -heappop(self.large))
            self.large_size -= 1
            self.small_size += 1
            # Clean up any delayed elements exposed at the top
            self.prune(self.large)


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        """
        Find the median of each sliding window of size k in the array.
        
        Approach: Two heaps + lazy deletion
        - Maintain two heaps: small (max heap) and large (min heap)
        - Small heap contains smaller half, large heap contains larger half
        - Use lazy deletion to handle element removal efficiently
        
        Time Complexity: O(n log k) where n is length of nums
        Space Complexity: O(k) for the heaps and delayed deletion tracking
        
        Args:
            nums: The input array of numbers
            k: The size of the sliding window
          
        Returns:
            List of medians for each window position
        """
        # Initialize the median finder with window size k
        finder = MedianFinder(k)
      
        # Add the first k elements to initialize the window
        for num in nums[:k]:
            finder.add_num(num)
      
        # Calculate the median for the first window
        result = [finder.find_median()]
      
        # Slide the window through the rest of the array
        for i in range(k, len(nums)):
            # Add new element entering the window
            finder.add_num(nums[i])
            # Remove element leaving the window
            finder.remove_num(nums[i - k])
            # Calculate and store the median for current window
            result.append(finder.find_median())
      
        return result

# Alternative simpler solution (less optimal but easier to implement in interview)
class SimplerSolution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        """
        Simpler approach using sorting for each window.
        Less optimal but easier to implement under pressure.
        
        Time Complexity: O(n * k log k)
        Space Complexity: O(k)
        """
        result = []
        
        for i in range(len(nums) - k + 1):
            # Extract current window and sort it
            window = sorted(nums[i:i + k])
            
            # Calculate median
            if k % 2 == 1:
                median = float(window[k // 2])
            else:
                median = (window[k // 2 - 1] + window[k // 2]) / 2.0
            
            result.append(median)
        
        return result

# Test cases to verify solution
def test_solutions():
    solution = Solution()
    simpler = SimplerSolution()
    
    # Test case 1
    nums1 = [1,3,-1,-3,5,3,6,7]
    k1 = 3
    expected1 = [1.0,-1.0,-1.0,3.0,5.0,6.0]
    
    result1 = solution.medianSlidingWindow(nums1, k1)
    result1_simple = simpler.medianSlidingWindow(nums1, k1)
    
    print(f"Test 1 - Optimized: {result1}")
    print(f"Test 1 - Simple: {result1_simple}")
    print(f"Test 1 - Expected: {expected1}")
    print(f"Test 1 - Passed: {result1 == expected1}\n")
    
    # Test case 2
    nums2 = [1,2,3,4,2,3,1,4,2]
    k2 = 3
    expected2 = [2.0,3.0,3.0,3.0,2.0,3.0,2.0]
    
    result2 = solution.medianSlidingWindow(nums2, k2)
    result2_simple = simpler.medianSlidingWindow(nums2, k2)
    
    print(f"Test 2 - Optimized: {result2}")
    print(f"Test 2 - Simple: {result2_simple}")
    print(f"Test 2 - Expected: {expected2}")
    print(f"Test 2 - Passed: {result2 == expected2}")

if __name__ == "__main__":
    test_solutions()
