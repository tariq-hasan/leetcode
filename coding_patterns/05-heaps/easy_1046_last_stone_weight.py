"""
LeetCode 1046: Last Stone Weight
Easy Difficulty

Problem:
You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones 
and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. 
The result of this smash is:

- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last stone. If there are no stones left, return 0.

Example:
Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation: 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

Time Complexity: O(N log N) where N is number of stones
Space Complexity: O(N) for the heap
"""

import heapq
from typing import List

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Optimal approach: Max Heap using Python's heapq (min-heap with negation)
        
        Key insight: We need to repeatedly access and remove the two largest elements.
        A max heap is perfect for this operation.
        
        Since Python's heapq implements min-heap, we use negative values to simulate max-heap.
        """
        # Convert to max heap by negating all values
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)
        
        # Continue until at most one stone remains
        while len(max_heap) > 1:
            # Get two heaviest stones (remember they're negative)
            first = -heapq.heappop(max_heap)   # Heaviest stone
            second = -heapq.heappop(max_heap)  # Second heaviest stone
            
            # If stones have different weights, add the difference back
            if first != second:
                new_stone = first - second
                heapq.heappush(max_heap, -new_stone)
        
        # Return the last stone weight, or 0 if no stones left
        return -max_heap[0] if max_heap else 0


class AlternativeSolution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Alternative approach: Sort array repeatedly
        Less efficient but easier to understand
        
        Time: O(N^2 log N) - we potentially sort N times
        Space: O(1) if we modify in place, O(N) for safety
        """
        stones_copy = stones.copy()  # Don't modify original
        
        while len(stones_copy) > 1:
            stones_copy.sort()  # Sort to get heaviest stones at end
            
            # Get two heaviest stones
            stone1 = stones_copy.pop()  # Heaviest
            stone2 = stones_copy.pop()  # Second heaviest
            
            # If different weights, add difference back
            if stone1 != stone2:
                stones_copy.append(stone1 - stone2)
        
        return stones_copy[0] if stones_copy else 0


class MaxHeapImplementation:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Custom max heap implementation for educational purposes
        Shows understanding of heap operations
        """
        class MaxHeap:
            def __init__(self):
                self.heap = []
            
            def push(self, val):
                self.heap.append(val)
                self._heapify_up(len(self.heap) - 1)
            
            def pop(self):
                if not self.heap:
                    return None
                if len(self.heap) == 1:
                    return self.heap.pop()
                
                # Store max value, replace with last element
                max_val = self.heap[0]
                self.heap[0] = self.heap.pop()
                self._heapify_down(0)
                return max_val
            
            def _heapify_up(self, index):
                parent_index = (index - 1) // 2
                if parent_index >= 0 and self.heap[index] > self.heap[parent_index]:
                    self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                    self._heapify_up(parent_index)
            
            def _heapify_down(self, index):
                largest = index
                left = 2 * index + 1
                right = 2 * index + 2
                
                if left < len(self.heap) and self.heap[left] > self.heap[largest]:
                    largest = left
                if right < len(self.heap) and self.heap[right] > self.heap[largest]:
                    largest = right
                
                if largest != index:
                    self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                    self._heapify_down(largest)
            
            def size(self):
                return len(self.heap)
        
        max_heap = MaxHeap()
        for stone in stones:
            max_heap.push(stone)
        
        while max_heap.size() > 1:
            first = max_heap.pop()
            second = max_heap.pop()
            
            if first != second:
                max_heap.push(first - second)
        
        return max_heap.pop() if max_heap.size() > 0 else 0


class OptimizedSolution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Slightly optimized version with early termination
        """
        if not stones:
            return 0
        if len(stones) == 1:
            return stones[0]
        
        # Use negative values for max heap simulation
        heap = [-stone for stone in stones]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            # Extract two largest stones
            stone1 = -heapq.heappop(heap)
            stone2 = -heapq.heappop(heap)
            
            # Early termination: if both stones are same weight, continue
            if stone1 == stone2:
                continue
            
            # Add difference back to heap
            heapq.heappush(heap, -(stone1 - stone2))
        
        return -heap[0] if heap else 0


class SimulationSolution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Simulation approach with detailed step tracking
        Useful for explaining the algorithm step by step
        """
        stones_list = stones.copy()
        
        while len(stones_list) > 1:
            # Sort to easily find two heaviest stones
            stones_list.sort()
            
            # Take two heaviest stones
            stone1 = stones_list.pop()  # Heaviest
            stone2 = stones_list.pop()  # Second heaviest
            
            print(f"Smashing {stone1} and {stone2}", end=" -> ")
            
            # Calculate result
            if stone1 == stone2:
                print("Both destroyed")
            else:
                new_weight = stone1 - stone2
                stones_list.append(new_weight)
                print(f"Remaining stone weighs {new_weight}")
            
            print(f"Remaining stones: {sorted(stones_list, reverse=True)}")
            print()
        
        result = stones_list[0] if stones_list else 0
        print(f"Final result: {result}")
        return result


def test_solutions():
    """Test all solutions with various inputs"""
    test_cases = [
        [2, 7, 4, 1, 8, 1],  # Expected: 1
        [1],                  # Expected: 1
        [2, 2],              # Expected: 0
        [3, 7, 2],           # Expected: 2
        [1, 3],              # Expected: 2
        [4, 3, 2, 1, 1],     # Expected: 1
        []                   # Expected: 0
    ]
    
    expected = [1, 1, 0, 2, 2, 1, 0]
    
    solutions = [
        ("Heap Solution", Solution()),
        ("Alternative Sort", AlternativeSolution()), 
        ("Custom Max Heap", MaxHeapImplementation()),
        ("Optimized Heap", OptimizedSolution())
    ]
    
    print("Last Stone Weight Test Results:")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases):
        print(f"Test {i+1}: {test_case} -> Expected: {expected[i]}")
        
        for name, sol in solutions:
            try:
                result = sol.lastStoneWeight(test_case.copy())
                status = "✓" if result == expected[i] else "✗"
                print(f"  {name:20}: {result} {status}")
            except Exception as e:
                print(f"  {name:20}: ERROR - {e}")
        print()


def trace_example():
    """Trace through the main example step by step"""
    print("Tracing example: [2, 7, 4, 1, 8, 1]")
    print("=" * 40)
    
    sol = SimulationSolution()
    result = sol.lastStoneWeight([2, 7, 4, 1, 8, 1])
    
    return result


def performance_comparison():
    """Compare performance of different approaches"""
    import time
    import random
    
    # Generate larger test case
    large_stones = [random.randint(1, 1000) for _ in range(1000)]
    
    solutions = [
        ("Heap Solution (Optimal)", Solution()),
        ("Sort Solution", AlternativeSolution())
    ]
    
    print("Performance Comparison (1000 stones):")
    print("-" * 40)
    
    for name, sol in solutions:
        start_time = time.time()
        result = sol.lastStoneWeight(large_stones.copy())
        end_time = time.time()
        
        print(f"{name:25}: {end_time - start_time:.6f}s -> Result: {result}")


"""
Interview Strategy and Key Points:

1. **Problem Recognition**:
   "This is a classic heap problem. We need to repeatedly find and process 
   the two largest elements, which is exactly what a max heap is designed for."

2. **Approach Explanation**:
   - Use max heap to efficiently get two heaviest stones
   - Python's heapq is min-heap, so we use negative values
   - Keep processing until at most one stone remains

3. **Algorithm Steps**:
   1. Convert all stones to negative values and heapify
   2. While more than one stone exists:
      - Pop two heaviest stones (largest negative values)
      - If weights differ, push difference back to heap
   3. Return remaining stone weight or 0

4. **Complexity Analysis**:
   - Time: O(N log N) - each of N operations takes O(log N)
   - Space: O(N) for the heap storage

5. **Key Insights to Mention**:
   - Max heap is perfect for "repeatedly access largest elements"
   - Python heapq trick: use negative values for max heap
   - Early termination when stones have equal weight

6. **Alternative Approaches** (if asked):
   - Sorting repeatedly: O(N^2 log N) time - less efficient
   - Custom max heap: shows data structure understanding
   - Priority queue: essentially same as heap approach

7. **Edge Cases**:
   - Empty array -> return 0
   - Single stone -> return that stone
   - All stones same weight -> return 0
   - Two stones -> return difference or 0

8. **Follow-up Questions**:
   - "What if we need to track the sequence of operations?" -> Store steps
   - "Can you implement without using heapq?" -> Show custom max heap
   - "What about memory optimization?" -> Discuss in-place modifications

9. **Common Mistakes to Avoid**:
   - Forgetting to negate values for max heap simulation
   - Not handling the case where stones have equal weight
   - Off-by-one errors in heap operations
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60 + "\n")
    trace_example()
    print("\n" + "="*60 + "\n")
    performance_comparison()
