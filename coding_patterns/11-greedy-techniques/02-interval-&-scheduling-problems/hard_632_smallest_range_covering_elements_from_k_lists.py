"""
LeetCode 632. Smallest Range Covering Elements from K Lists

Problem: You have k lists of sorted integers in non-decreasing order. 
Find the smallest range that includes at least one number from each of the k lists.

Key Insights:
1. We need exactly one element from each list in our range
2. This is essentially a sliding window problem across multiple sorted arrays
3. Use min-heap to track the smallest current elements from each list
4. Track the maximum element to calculate range size
5. Advance the pointer of the list with minimum element

Time Complexity: O(n log k) where n = total elements, k = number of lists
Space Complexity: O(k) for the heap
"""

import heapq
from collections import defaultdict

# Approach 1: Min-Heap with Tracking Maximum (Optimal Solution)
def smallestRange_v1(nums):
    """
    Optimal approach using min-heap to track minimum elements
    and maintaining maximum for range calculation
    """
    if not nums or not nums[0]:
        return []
    
    k = len(nums)
    
    # Min-heap: (value, list_index, element_index)
    min_heap = []
    max_val = float('-inf')
    
    # Initialize heap with first element from each list
    for i in range(k):
        if nums[i]:  # Check if list is not empty
            heapq.heappush(min_heap, (nums[i][0], i, 0))
            max_val = max(max_val, nums[i][0])
    
    # Initialize result with first possible range
    range_start, range_end = 0, float('inf')
    
    while len(min_heap) == k:  # Must have one element from each list
        # Get the minimum element
        min_val, list_idx, elem_idx = heapq.heappop(min_heap)
        
        # Update best range if current is smaller
        if max_val - min_val < range_end - range_start:
            range_start, range_end = min_val, max_val
        
        # Try to advance the pointer in the list that had minimum element
        if elem_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
            max_val = max(max_val, next_val)
        else:
            # Can't advance this list further, so we're done
            break
    
    return [range_start, range_end]

# Approach 2: Merge All Lists with Source Tracking
def smallestRange_v2(nums):
    """
    Alternative approach: merge all lists and use sliding window
    More intuitive but slightly less efficient
    """
    if not nums:
        return []
    
    # Create merged list with (value, list_index)
    merged = []
    for i, lst in enumerate(nums):
        for val in lst:
            merged.append((val, i))
    
    # Sort by value
    merged.sort()
    
    k = len(nums)
    left = 0
    count = defaultdict(int)  # Count of elements from each list in current window
    unique_lists = 0  # Number of lists represented in current window
    
    range_start, range_end = 0, float('inf')
    
    for right in range(len(merged)):
        val, list_idx = merged[right]
        
        # Expand window
        if count[list_idx] == 0:
            unique_lists += 1
        count[list_idx] += 1
        
        # Contract window while we have all k lists
        while unique_lists == k:
            current_range = merged[right][0] - merged[left][0]
            if current_range < range_end - range_start:
                range_start, range_end = merged[left][0], merged[right][0]
            
            # Remove leftmost element
            left_val, left_list = merged[left]
            count[left_list] -= 1
            if count[left_list] == 0:
                unique_lists -= 1
            left += 1
    
    return [range_start, range_end]

# Approach 3: Detailed Step-by-Step (For Interview Explanation)
def smallestRange_explained(nums):
    """
    Detailed version with step-by-step logging for interview explanation
    """
    print(f"Input lists: {nums}")
    
    if not nums or not nums[0]:
        return []
    
    k = len(nums)
    min_heap = []
    max_val = float('-inf')
    
    # Initialize
    print("\nInitializing heap with first element from each list:")
    for i in range(k):
        if nums[i]:
            val = nums[i][0]
            heapq.heappush(min_heap, (val, i, 0))
            max_val = max(max_val, val)
            print(f"  List {i}: added {val}, max_val = {max_val}")
    
    print(f"Initial heap: {sorted(min_heap)}")
    print(f"Initial range: [{min_heap[0][0]}, {max_val}] = {max_val - min_heap[0][0]}")
    
    range_start, range_end = 0, float('inf')
    step = 0
    
    while len(min_heap) == k:
        step += 1
        print(f"\n--- Step {step} ---")
        
        # Get minimum
        min_val, list_idx, elem_idx = heapq.heappop(min_heap)
        print(f"Popped minimum: {min_val} from list {list_idx}[{elem_idx}]")
        
        # Check if this gives us a better range
        current_range = max_val - min_val
        print(f"Current range: [{min_val}, {max_val}] = {current_range}")
        
        if current_range < range_end - range_start:
            range_start, range_end = min_val, max_val
            print(f"*** New best range: [{range_start}, {range_end}] = {range_end - range_start}")
        
        # Try to advance pointer
        if elem_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
            max_val = max(max_val, next_val)
            print(f"Advanced list {list_idx} to {next_val}, new max_val = {max_val}")
            print(f"Heap now: {sorted(min_heap)}")
        else:
            print(f"Cannot advance list {list_idx} further - algorithm terminates")
            break
    
    print(f"\nFinal answer: [{range_start}, {range_end}]")
    return [range_start, range_end]

# Approach 4: Priority Queue with Custom Comparator
def smallestRange_v4(nums):
    """
    Using priority queue with more explicit tracking
    Good for showing object-oriented thinking
    """
    if not nums:
        return []
    
    class ListPointer:
        def __init__(self, value, list_idx, elem_idx):
            self.value = value
            self.list_idx = list_idx
            self.elem_idx = elem_idx
        
        def __lt__(self, other):
            return self.value < other.value
        
        def __repr__(self):
            return f"LP({self.value}, L{self.list_idx}[{self.elem_idx}])"
    
    k = len(nums)
    heap = []
    max_val = float('-inf')
    
    # Initialize
    for i in range(k):
        if nums[i]:
            ptr = ListPointer(nums[i][0], i, 0)
            heapq.heappush(heap, ptr)
            max_val = max(max_val, nums[i][0])
    
    best_range = [0, float('inf')]
    
    while len(heap) == k:
        min_ptr = heapq.heappop(heap)
        
        # Update best range
        if max_val - min_ptr.value < best_range[1] - best_range[0]:
            best_range = [min_ptr.value, max_val]
        
        # Advance pointer
        if min_ptr.elem_idx + 1 < len(nums[min_ptr.list_idx]):
            new_val = nums[min_ptr.list_idx][min_ptr.elem_idx + 1]
            new_ptr = ListPointer(new_val, min_ptr.list_idx, min_ptr.elem_idx + 1)
            heapq.heappush(heap, new_ptr)
            max_val = max(max_val, new_val)
        else:
            break
    
    return best_range

# Approach 5: Brute Force (For Comparison)
def smallestRange_bruteforce(nums):
    """
    Brute force approach - try all possible combinations
    Exponential time - only for small inputs
    """
    if not nums:
        return []
    
    def generate_combinations(lists, current, index):
        if index == len(lists):
            yield current[:]
            return
        
        for val in lists[index]:
            current.append(val)
            yield from generate_combinations(lists, current, index + 1)
            current.pop()
    
    best_range = [float('-inf'), float('inf')]
    
    for combination in generate_combinations(nums, [], 0):
        min_val, max_val = min(combination), max(combination)
        if max_val - min_val < best_range[1] - best_range[0]:
            best_range = [min_val, max_val]
    
    return best_range

def analyze_algorithm_intuition():
    """
    Explain the intuition behind the optimal algorithm
    """
    print("=== Algorithm Intuition ===")
    print()
    print("KEY INSIGHT:")
    print("- We must have exactly one element from each of k lists")
    print("- Range = [minimum_selected, maximum_selected]")
    print("- To minimize range, we want to increase minimum while keeping maximum small")
    print()
    print("STRATEGY:")
    print("1. Start with one element from each list (first elements)")
    print("2. Current range = [min_heap.top(), max_so_far]")
    print("3. To potentially improve: advance the list with minimum element")
    print("4. Why? Advancing minimum might increase it, reducing range")
    print("5. Continue until we can't advance the minimum list")
    print()
    print("WHY IT WORKS:")
    print("- We explore all possible 'minimum' values systematically")
    print("- For each minimum, we have the best possible maximum")
    print("- When we can't advance minimum list, no better solution exists")
    print()
    print("HEAP USAGE:")
    print("- Min-heap gives us the current minimum efficiently")
    print("- We track maximum separately as we advance pointers")
    print("- O(log k) operations for heap, O(n) total operations")

def test_comprehensive():
    """
    Test with various examples including edge cases
    """
    test_cases = [
        # Basic examples
        ([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]], [20, 24]),
        ([[1,2,3],[1,2,3],[1,2,3]], [1, 1]),
        ([[10,10],[11,11]], [10, 11]),
        
        # Edge cases
        ([[1]], [1, 1]),  # Single list
        ([[1,3,5],[2,4,6]], [2, 3]),  # Two lists
        ([[1,2,3],[4,5,6],[7,8,9]], [1, 7]),  # No overlap needed
        
        # Larger examples
        ([[1,3,6,8],[2,4,7,9],[3,5,10,11,12]], [6, 7]),
        ([[-1,2,3],[1,4,5],[1,7]], [-1, 1]),  # With negative numbers
    ]
    
    print("=== Comprehensive Testing ===")
    
    approaches = [
        ("Min-Heap Optimal", smallestRange_v1),
        ("Merge + Sliding Window", smallestRange_v2),
        ("Priority Queue OOP", smallestRange_v4),
    ]
    
    for i, (nums, expected) in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {nums}")
        print(f"Expected: {expected}")
        
        results = []
        for name, func in approaches:
            try:
                result = func([lst[:] for lst in nums])  # Deep copy
                results.append(result)
                print(f"{name}: {result}")
            except Exception as e:
                print(f"{name}: ERROR - {e}")
                results.append(None)
        
        # Verify all valid results are the same
        valid_results = [r for r in results if r is not None]
        if valid_results:
            range_sizes = [r[1] - r[0] for r in valid_results]
            assert all(size == range_sizes[0] for size in range_sizes), \
                   f"Different range sizes: {valid_results}"
        
        # For smaller examples, show detailed walkthrough
        if len(nums) <= 3 and all(len(lst) <= 5 for lst in nums):
            print("Detailed walkthrough:")
            smallestRange_explained([lst[:] for lst in nums])

def complexity_analysis():
    """
    Detailed complexity analysis of different approaches
    """
    print("=== Complexity Analysis ===")
    print()
    print("APPROACH 1 - Min-Heap (Optimal):")
    print("- Time: O(n log k) where n = total elements, k = number of lists")
    print("- Space: O(k) for the heap")
    print("- Each element processed once, O(log k) heap operations")
    print()
    print("APPROACH 2 - Merge + Sliding Window:")
    print("- Time: O(n log n + n) = O(n log n) for sorting merged array")
    print("- Space: O(n) for merged array")
    print("- Less efficient due to sorting all elements")
    print()
    print("APPROACH 5 - Brute Force:")
    print("- Time: O(m^k) where m = average list length")
    print("- Space: O(k) for recursion")
    print("- Exponential - only feasible for very small inputs")
    print()
    print("WINNER: Min-heap approach")
    print("- Best time complexity: O(n log k)")
    print("- Minimal space usage: O(k)")
    print("- Most intuitive algorithm")

def interview_discussion_points():
    """
    Key points to discuss during interview
    """
    print("=== Interview Discussion Points ===")
    print()
    print("1. PROBLEM UNDERSTANDING:")
    print("   - Must include exactly one element from each list")
    print("   - Want to minimize [max - min] of selected elements")
    print("   - Lists are individually sorted (key constraint)")
    print()
    print("2. APPROACH RECOGNITION:")
    print("   - This is NOT a typical sliding window (single array)")
    print("   - More like 'coordinated advancement' across multiple arrays")
    print("   - Min-heap helps track current minimums efficiently")
    print()
    print("3. KEY INSIGHTS:")
    print("   - Always advance the pointer with minimum value")
    print("   - Track maximum separately as we advance")
    print("   - Stop when we can't advance the minimum pointer")
    print()
    print("4. WHY GREEDY WORKS:")
    print("   - We systematically explore all possible minimums")
    print("   - For each minimum, we have optimal maximum")
    print("   - No point exploring after minimum list is exhausted")
    print()
    print("5. ALTERNATIVE APPROACHES:")
    print("   - Merge all lists: O(n log n) but more space")
    print("   - Brute force: exponential time")
    print("   - Binary search: complex and not more efficient")
    print()
    print("6. EDGE CASES:")
    print("   - Single list: range is [val, val]")
    print("   - Empty lists: handle gracefully")
    print("   - Negative numbers: algorithm works unchanged")
    print("   - All same values: range is [val, val]")

if __name__ == "__main__":
    print("=== Smallest Range Covering Elements from K Lists ===")
    
    # Algorithm intuition
    analyze_algorithm_intuition()
    
    # Comprehensive testing
    test_comprehensive()
    
    # Complexity analysis
    complexity_analysis()
    
    # Interview tips
    interview_discussion_points()

"""
Critical Interview Discussion Points:

1. **Problem Classification**:
   - Multi-array coordination problem
   - NOT traditional sliding window (single array)
   - Greedy optimization with heap-based tracking
   - Range minimization under constraints

2. **Key Algorithmic Insight**:
   - Must systematically explore all possible minimum values
   - For each minimum, find the best possible maximum
   - Advance the list contributing the minimum element

3. **Why Min-Heap is Perfect**:
   - Efficiently tracks current minimum across k lists
   - O(log k) insertion/deletion operations
   - Natural way to coordinate advancement across lists

4. **Algorithm Correctness**:
   - Explores all possible ranges optimally
   - Stops when no improvement is possible
   - Greedy advancement is provably optimal

5. **Complexity Trade-offs**:
   - Min-heap: O(n log k) time, O(k) space - optimal
   - Merge+sort: O(n log n) time, O(n) space - less efficient
   - Brute force: O(m^k) - exponential, infeasible

6. **Implementation Details**:
   - Heap stores (value, list_index, element_index)
   - Track maximum separately (not in heap)
   - Terminate when any list is exhausted

7. **Edge Cases**:
   - Single list: range is [element, element]
   - Lists of different lengths
   - Negative numbers (algorithm unchanged)
   - All identical elements

8. **Similar Problems**:
   - Merge k sorted lists (different objective)
   - Sliding window maximum (single array)
   - Range queries with multiple constraints

9. **Follow-up Questions**:
   - What if we wanted k-th smallest range?
   - How to handle dynamic list updates?
   - What if lists weren't sorted?

10. **Interview Strategy**:
    - Start with brute force to show understanding
    - Identify the key insight (advance minimum)
    - Explain why min-heap is perfect tool
    - Code the optimal solution cleanly
    - Discuss complexity and alternatives
    - Handle edge cases systematically
"""
