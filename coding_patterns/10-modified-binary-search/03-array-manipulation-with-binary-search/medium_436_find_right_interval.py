"""
LeetCode 436: Find Right Interval

Problem: You are given an array of intervals, where intervals[i] = [starti, endi] 
and each starti is unique. The right interval for an interval i is an interval j 
such that startj >= endi and startj is minimized. Return an array of right interval 
indices for each interval i. If no right interval exists for interval i, then put -1 
at index i.

Key insights:
1. For each interval, we need to find the interval with the smallest start >= current end
2. This is a perfect use case for binary search after sorting
3. We need to maintain original indices after sorting
"""

def findRightInterval_sorting_binary_search(intervals):
    """
    Approach 1: Sorting + Binary Search (Optimal)
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Strategy:
    1. Create array of (start, original_index) pairs
    2. Sort by start values
    3. For each interval's end, binary search for the smallest start >= end
    
    Best for: Most interviews - shows sorting and binary search skills
    """
    n = len(intervals)
    if n == 0:
        return []
    
    # Create (start_value, original_index) pairs and sort by start_value
    starts = [(intervals[i][0], i) for i in range(n)]
    starts.sort()
    
    result = [-1] * n
    
    # For each interval, find its right interval
    for i in range(n):
        end = intervals[i][1]
        
        # Binary search for the smallest start >= end
        left, right = 0, n - 1
        right_interval_idx = -1
        
        while left <= right:
            mid = (left + right) // 2
            if starts[mid][0] >= end:
                right_interval_idx = starts[mid][1]  # Store original index
                right = mid - 1  # Look for potentially smaller start
            else:
                left = mid + 1
        
        result[i] = right_interval_idx
    
    return result


def findRightInterval_bisect(intervals):
    """
    Approach 2: Using Python's bisect module
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Cleaner implementation using built-in binary search
    """
    import bisect
    
    n = len(intervals)
    if n == 0:
        return []
    
    # Create sorted list of (start, original_index) pairs
    starts = sorted((intervals[i][0], i) for i in range(n))
    start_values = [start for start, _ in starts]
    
    result = []
    for i in range(n):
        end = intervals[i][1]
        
        # Find the leftmost position where start >= end
        pos = bisect.bisect_left(start_values, end)
        
        if pos < n:
            result.append(starts[pos][1])  # Return original index
        else:
            result.append(-1)
    
    return result


def findRightInterval_brute_force(intervals):
    """
    Approach 3: Brute Force (For comparison)
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    
    Strategy: For each interval, check all other intervals
    Good for: Understanding the problem, small inputs
    """
    n = len(intervals)
    result = [-1] * n
    
    for i in range(n):
        end_i = intervals[i][1]
        min_start = float('inf')
        right_idx = -1
        
        # Check all intervals to find the one with smallest start >= end_i
        for j in range(n):
            start_j = intervals[j][0]
            if start_j >= end_i and start_j < min_start:
                min_start = start_j
                right_idx = j
        
        result[i] = right_idx
    
    return result


def findRightInterval_treemap_simulation(intervals):
    """
    Approach 4: TreeMap Simulation (Advanced)
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Simulates TreeMap/SortedDict behavior for educational purposes
    Shows understanding of balanced BST concepts
    """
    from sortedcontainers import SortedDict
    
    n = len(intervals)
    if n == 0:
        return []
    
    # SortedDict maintains sorted order of keys
    # Key: start value, Value: original index
    sorted_starts = SortedDict()
    
    for i, (start, end) in enumerate(intervals):
        sorted_starts[start] = i
    
    result = []
    for i, (start, end) in enumerate(intervals):
        # Find the smallest key >= end
        keys = sorted_starts.keys()
        
        # Binary search in sorted keys
        import bisect
        pos = bisect.bisect_left(keys, end)
        
        if pos < len(keys):
            key = keys[pos]
            result.append(sorted_starts[key])
        else:
            result.append(-1)
    
    return result


def findRightInterval_segment_tree(intervals):
    """
    Approach 5: Coordinate Compression + Segment Tree (Advanced)
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Advanced approach using coordinate compression and segment tree
    Good for showing knowledge of advanced data structures
    """
    n = len(intervals)
    if n == 0:
        return []
    
    # Coordinate compression
    all_coords = set()
    for start, end in intervals:
        all_coords.add(start)
        all_coords.add(end)
    
    sorted_coords = sorted(all_coords)
    coord_to_idx = {coord: i for i, coord in enumerate(sorted_coords)}
    
    # Segment tree for range minimum query
    class SegmentTree:
        def __init__(self, size):
            self.size = size
            self.tree = [float('inf')] * (4 * size)
            self.indices = [-1] * (4 * size)
        
        def update(self, node, start, end, idx, val, original_idx):
            if start == end:
                if val < self.tree[node]:
                    self.tree[node] = val
                    self.indices[node] = original_idx
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    self.update(2 * node, start, mid, idx, val, original_idx)
                else:
                    self.update(2 * node + 1, mid + 1, end, idx, val, original_idx)
                
                left_val, left_idx = self.tree[2 * node], self.indices[2 * node]
                right_val, right_idx = self.tree[2 * node + 1], self.indices[2 * node + 1]
                
                if left_val <= right_val:
                    self.tree[node] = left_val
                    self.indices[node] = left_idx
                else:
                    self.tree[node] = right_val
                    self.indices[node] = right_idx
        
        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return float('inf'), -1
            if l <= start and end <= r:
                return self.tree[node], self.indices[node]
            
            mid = (start + end) // 2
            left_val, left_idx = self.query(2 * node, start, mid, l, r)
            right_val, right_idx = self.query(2 * node + 1, mid + 1, end, l, r)
            
            if left_val <= right_val:
                return left_val, left_idx
            else:
                return right_val, right_idx
    
    coord_size = len(sorted_coords)
    seg_tree = SegmentTree(coord_size)
    
    # Insert all intervals into segment tree
    for i, (start, end) in enumerate(intervals):
        start_coord = coord_to_idx[start]
        seg_tree.update(1, 0, coord_size - 1, start_coord, start, i)
    
    result = []
    for i, (start, end) in enumerate(intervals):
        end_coord = coord_to_idx[end]
        
        # Query for minimum start >= end
        _, idx = seg_tree.query(1, 0, coord_size - 1, end_coord, coord_size - 1)
        result.append(idx)
    
    return result


# Test cases
def test_solutions():
    test_cases = [
        {
            "intervals": [[1,2]],
            "expected": [-1]
        },
        {
            "intervals": [[3,4], [2,3], [1,2]],
            "expected": [-1, 0, 1]
        },
        {
            "intervals": [[1,4], [2,3], [3,4]],
            "expected": [-1, 2, -1]
        },
        {
            "intervals": [[1,2], [2,3], [0,1], [3,4]],
            "expected": [1, 3, 0, -1]
        },
        {
            "intervals": [[4,5], [2,3], [1,2], [3,4]],
            "expected": [-1, 3, 1, 0]
        },
        {
            "intervals": [],
            "expected": []
        }
    ]
    
    solutions = [
        ("Sorting + Binary Search", findRightInterval_sorting_binary_search),
        ("Using Bisect", findRightInterval_bisect),
        ("Brute Force", findRightInterval_brute_force),
    ]
    
    # Only test segment tree if sortedcontainers is available
    try:
        findRightInterval_treemap_simulation([[1,2]])
        solutions.append(("TreeMap Simulation", findRightInterval_treemap_simulation))
    except ImportError:
        print("Note: sortedcontainers not available, skipping TreeMap simulation")
    
    for i, test in enumerate(test_cases):
        print(f"Test Case {i + 1}: {test['intervals']}")
        print(f"Expected: {test['expected']}")
        
        for name, solution in solutions:
            result = solution(test['intervals'][:])  # Pass copy
            is_correct = result == test['expected']
            print(f"{name:20}: {result} {'✓' if is_correct else '✗'}")
        
        print("-" * 60)


def demonstrate_algorithm():
    """Demonstrate the algorithm step by step"""
    intervals = [[3,4], [2,3], [1,2]]
    print("Algorithm Demonstration:")
    print("=" * 50)
    print(f"Input intervals: {intervals}")
    print()
    
    # Show the sorting step
    n = len(intervals)
    starts = [(intervals[i][0], i) for i in range(n)]
    print(f"Before sorting - (start, original_index): {starts}")
    
    starts.sort()
    print(f"After sorting by start: {starts}")
    print()
    
    # Show binary search for each interval
    print("Finding right interval for each:")
    for i in range(n):
        end = intervals[i][1]
        print(f"  Interval {i}: {intervals[i]}, looking for start >= {end}")
        
        # Manual binary search demonstration
        left, right = 0, n - 1
        right_interval_idx = -1
        steps = []
        
        while left <= right:
            mid = (left + right) // 2
            steps.append(f"    Check mid={mid}, start={starts[mid][0]}")
            
            if starts[mid][0] >= end:
                right_interval_idx = starts[mid][1]
                steps.append(f"    Found candidate: interval {right_interval_idx}")
                right = mid - 1
            else:
                left = mid + 1
        
        for step in steps:
            print(step)
        
        print(f"    Result for interval {i}: {right_interval_idx}")
        print()


def analyze_complexity():
    """Analyze different approaches"""
    print("Complexity Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Brute Force", "O(n²)", "O(1)", "Check all pairs"),
        ("Sorting + Binary Search", "O(n log n)", "O(n)", "Sort once, binary search n times"),
        ("TreeMap/SortedDict", "O(n log n)", "O(n)", "Balanced BST operations"),
        ("Segment Tree", "O(n log n)", "O(n)", "Advanced but overkill")
    ]
    
    print(f"{'Approach':<25} {'Time':<12} {'Space':<8} {'Notes'}")
    print("-" * 65)
    
    for approach, time, space, notes in approaches:
        print(f"{approach:<25} {time:<12} {space:<8} {notes}")


if __name__ == "__main__":
    test_solutions()
    print("\n")
    demonstrate_algorithm()
    print("\n")
    analyze_complexity()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Right interval for i: interval j where start[j] >= end[i] and start[j] is minimized
   - Need to return original indices, not the intervals themselves
   - Each start value is unique (important constraint)

2. KEY INSIGHTS:
   - This is essentially finding the "ceiling" element in a sorted array
   - Binary search is perfect for finding "smallest element >= target"
   - Need to maintain original indices after sorting

3. APPROACH PROGRESSION:

   Step 1: Brute Force - O(n²)
   - Good for understanding the problem
   - Check all intervals for each interval
   
   Step 2: Sorting + Binary Search - O(n log n)
   - Optimal and most common interview solution
   - Sort starts with original indices
   - Binary search for each interval's end

4. IMPLEMENTATION DETAILS:
   - Sort by start values while keeping track of original indices
   - Use binary search to find leftmost position where start >= end
   - Handle the case where no right interval exists (-1)

5. BINARY SEARCH TEMPLATE:
   - Looking for leftmost position where condition is true
   - When starts[mid] >= end: store answer and search left half
   - When starts[mid] < end: search right half

6. COMMON MISTAKES:
   - Forgetting to maintain original indices after sorting
   - Wrong binary search bounds (use bisect_left logic)
   - Not handling the "no right interval" case properly

7. FOLLOW-UP QUESTIONS:
   - "What if start values are not unique?" → Handle ties appropriately
   - "What if we want left intervals instead?" → Similar approach, reverse condition
   - "Memory optimization?" → Can't do much better than O(n)
   - "Online processing?" → Use TreeMap/SortedDict

8. EDGE CASES:
   - Empty intervals array
   - Single interval (result is [-1])
   - No right intervals exist for any interval
   - All intervals have the same start (impossible given constraints)

9. VARIANTS:
   - Find left interval instead of right
   - Find all right intervals within a range
   - Weighted intervals with priority

10. REAL-WORLD APPLICATIONS:
    - Meeting room scheduling
    - Task scheduling with dependencies
    - Event processing systems
    - Calendar applications

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem (right interval definition)
2. Work through example manually
3. Identify that this is a "ceiling" search problem
4. Start with brute force to show understanding
5. Optimize with sorting + binary search
6. Code the solution cleanly
7. Handle edge cases
8. Discuss complexity and potential optimizations

KEY INSIGHTS TO MENTION:
- "This is like finding the ceiling in a sorted array"
- "We need binary search because we want the minimum start >= end"
- "Maintaining original indices is crucial"
- "Each start is unique simplifies the problem"

This problem excellently tests:
- Binary search implementation
- Sorting with custom keys
- Index tracking after transformation
- Problem reduction skills (ceiling search)
"""
