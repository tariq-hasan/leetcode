def kWeakestRows(mat, k):
    """
    SOLUTION 1: Binary Search + Sorting - OPTIMAL for interviews
    
    This is the MOST IMPORTANT solution for big tech interviews.
    Uses binary search to count soldiers efficiently, then sorts by strength.
    
    Time: O(m * log n + m * log m), Space: O(m)
    where m = number of rows, n = number of columns
    """
    def countSoldiers(row):
        """Binary search to find number of soldiers (1s) in sorted row"""
        left, right = 0, len(row)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if row[mid] == 1:
                left = mid + 1  # Look for more soldiers to the right
            else:
                right = mid     # First civilian found, soldiers are to the left
        
        return left  # Number of soldiers
    
    # Calculate strength for each row: (soldier_count, row_index)
    row_strengths = []
    for i in range(len(mat)):
        soldier_count = countSoldiers(mat[i])
        row_strengths.append((soldier_count, i))
    
    # Sort by soldier count, then by row index (both ascending)
    row_strengths.sort()
    
    # Return the first k row indices
    return [row_index for _, row_index in row_strengths[:k]]


def kWeakestRowsHeap(mat, k):
    """
    SOLUTION 2: Binary Search + Min Heap - Great for large matrices
    
    Uses a heap to efficiently find k smallest elements.
    More space efficient when k << m.
    
    Time: O(m * log n + m * log m), Space: O(m)
    """
    import heapq
    
    def countSoldiers(row):
        left, right = 0, len(row)
        while left < right:
            mid = left + (right - left) // 2
            if row[mid] == 1:
                left = mid + 1
            else:
                right = mid
        return left
    
    # Create list of (soldier_count, row_index) tuples
    strengths = []
    for i in range(len(mat)):
        soldier_count = countSoldiers(mat[i])
        strengths.append((soldier_count, i))
    
    # Use heapify for O(m) heap creation, then extract k smallest
    heapq.heapify(strengths)
    
    result = []
    for _ in range(k):
        _, row_index = heapq.heappop(strengths)
        result.append(row_index)
    
    return result


def kWeakestRowsLinearCount(mat, k):
    """
    SOLUTION 3: Linear Count + Sorting - Simple but less efficient
    
    Good to mention as the straightforward approach before optimizing.
    Time: O(m * n + m * log m), Space: O(m)
    """
    # Count soldiers in each row using linear scan
    row_strengths = []
    for i in range(len(mat)):
        soldier_count = sum(mat[i])  # Count 1s in the row
        row_strengths.append((soldier_count, i))
    
    # Sort and return first k indices
    row_strengths.sort()
    return [row_index for _, row_index in row_strengths[:k]]


def kWeakestRowsOptimalHeap(mat, k):
    """
    SOLUTION 4: Binary Search + Max Heap (Size K) - Most space efficient
    
    Maintains a heap of only k elements. Best when k is small.
    Time: O(m * log n + m * log k), Space: O(k)
    """
    import heapq
    
    def countSoldiers(row):
        left, right = 0, len(row)
        while left < right:
            mid = left + (right - left) // 2
            if row[mid] == 1:
                left = mid + 1
            else:
                right = mid
        return left
    
    # Use max heap (negate values for min heap behavior)
    max_heap = []
    
    for i in range(len(mat)):
        soldier_count = countSoldiers(mat[i])
        
        if len(max_heap) < k:
            # Heap not full, add current row
            heapq.heappush(max_heap, (-soldier_count, -i))
        else:
            # Compare with the strongest row in our current k weakest
            strongest_count, strongest_idx = max_heap[0]
            if soldier_count < -strongest_count or (soldier_count == -strongest_count and i < -strongest_idx):
                heapq.heapreplace(max_heap, (-soldier_count, -i))
    
    # Extract results and sort (heap doesn't guarantee order)
    result = [(-idx) for _, idx in max_heap]
    
    # Sort the result since heap doesn't maintain sorted order
    strengths_for_result = []
    for idx in result:
        soldier_count = countSoldiers(mat[idx])
        strengths_for_result.append((soldier_count, idx))
    
    strengths_for_result.sort()
    return [idx for _, idx in strengths_for_result]


def kWeakestRowsBruteForce(mat, k):
    """
    SOLUTION 5: Brute Force - For comparison only
    
    Mention this to show understanding, then optimize.
    Time: O(m * n + m * log m), Space: O(m)
    """
    strengths = []
    
    # Count soldiers in each row using nested loops
    for i in range(len(mat)):
        count = 0
        for j in range(len(mat[i])):
            if mat[i][j] == 1:
                count += 1
            else:
                break  # Since soldiers come first, we can break early
        strengths.append((count, i))
    
    # Sort and return first k
    strengths.sort()
    return [idx for _, idx in strengths[:k]]


# Comprehensive test suite
def test_k_weakest_rows():
    test_cases = [
        # [matrix, k, expected, description]
        ([
            [1,1,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,1,0,0,0],
            [1,1,1,1,1]
        ], 3, [2, 0, 3], "Standard example from problem"),
        
        ([
            [1,0,0,0],
            [1,1,1,1],
            [1,0,0,0],
            [1,0,0,0]
        ], 2, [0, 2], "Multiple rows with same strength"),
        
        ([
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ], 1, [0], "All rows have same strength"),
        
        ([
            [0,0,0],
            [1,1,1],
            [0,0,0]
        ], 2, [0, 2], "Mix of empty and full rows"),
        
        ([
            [1]
        ], 1, [0], "Single row, single column"),
        
        ([
            [1,1,1,1,1],
            [1,0,0,0,0],
            [0,0,0,0,0]
        ], 2, [2, 1], "Decreasing strength pattern"),
        
        ([
            [0,0,0,0,0],
            [1,1,1,1,1],
            [1,1,0,0,0]
        ], 3, [0, 2, 1], "All three rows different strengths")
    ]
    
    print("Testing K Weakest Rows in Matrix")
    print("=" * 50)
    
    for i, (mat, k, expected, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print(f"Matrix:")
        for row in mat:
            print(f"  {row}")
        print(f"k = {k}")
        
        # Test main solutions
        result1 = kWeakestRows(mat, k)
        result2 = kWeakestRowsHeap(mat, k)
        result3 = kWeakestRowsLinearCount(mat, k)
        
        print(f"Binary Search + Sort: {result1}")
        print(f"Binary Search + Heap: {result2}")
        print(f"Linear Count + Sort:  {result3}")
        
        # Verify correctness
        status = "✓" if result1 == expected else "✗"
        print(f"Expected: {expected}, Got: {result1} {status}")
        print("-" * 30)


# Step-by-step demonstration
def demonstrateAlgorithm():
    """
    Visual demonstration of the binary search + sorting approach
    """
    print("\nALGORITHM DEMONSTRATION")
    print("=" * 40)
    
    mat = [
        [1,1,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,1,0,0,0],
        [1,1,1,1,1]
    ]
    k = 3
    
    print("Matrix:")
    for i, row in enumerate(mat):
        print(f"  Row {i}: {row}")
    print(f"\nFinding {k} weakest rows...\n")
    
    def countSoldiers(row):
        left, right = 0, len(row)
        steps = []
        
        while left < right:
            mid = left + (right - left) // 2
            steps.append(f"    left={left}, right={right}, mid={mid}, row[{mid}]={row[mid]}")
            
            if row[mid] == 1:
                left = mid + 1
                steps.append(f"    Found soldier, search right: left={left}")
            else:
                right = mid
                steps.append(f"    Found civilian, search left: right={right}")
        
        return left, steps
    
    # Step 1: Count soldiers in each row using binary search
    print("Step 1: Count soldiers using binary search")
    row_strengths = []
    
    for i in range(len(mat)):
        print(f"\n  Row {i}: {mat[i]}")
        soldier_count, steps = countSoldiers(mat[i])
        for step in steps:
            print(step)
        print(f"    Result: {soldier_count} soldiers")
        row_strengths.append((soldier_count, i))
    
    # Step 2: Sort by strength
    print(f"\nStep 2: Row strengths before sorting: {row_strengths}")
    row_strengths.sort()
    print(f"After sorting: {row_strengths}")
    
    # Step 3: Extract first k indices
    result = [row_index for _, row_index in row_strengths[:k]]
    print(f"\nStep 3: First {k} weakest rows: {result}")


# Complexity analysis
def analyzeComplexity():
    """
    Compare different approaches and their complexities
    """
    print("\nCOMPLEXITY ANALYSIS")
    print("=" * 50)
    
    approaches = [
        ("Brute Force", "O(m * n)", "O(m)", "Linear scan each row"),
        ("Linear + Sort", "O(m * n + m log m)", "O(m)", "sum() each row + sort"),
        ("Binary + Sort", "O(m * log n + m log m)", "O(m)", "Binary search + sort"),
        ("Binary + Min Heap", "O(m * log n + m log m)", "O(m)", "Binary search + heapify"),
        ("Binary + Max Heap(k)", "O(m * log n + m log k)", "O(k)", "Maintain heap of size k")
    ]
    
    print(f"{'Approach':<20} {'Time Complexity':<22} {'Space':<8} {'Description'}")
    print("-" * 80)
    
    for approach, time, space, desc in approaches:
        print(f"{approach:<20} {time:<22} {space:<8} {desc}")
    
    print(f"\nFor m=1000 rows, n=1000 cols, k=10:")
    print(f"  Brute Force:       ~1,000,000 operations")
    print(f"  Linear + Sort:     ~1,010,000 operations")
    print(f"  Binary + Sort:     ~20,000 operations")
    print(f"  Binary + Heap(k):  ~13,000 operations (best for small k)")


# Run all demonstrations
test_k_weakest_rows()
demonstrateAlgorithm()
analyzeComplexity()

# INTERVIEW STRATEGY AND KEY POINTS:
"""
PROBLEM ANALYSIS:

This problem combines several important concepts:
1. Binary search on sorted arrays
2. Sorting with custom comparisons
3. Heap data structures
4. Time-space complexity trade-offs

KEY INSIGHTS:

1. SORTED PROPERTY EXPLOITATION:
   - Each row has soldiers (1s) followed by civilians (0s)
   - Can use binary search to count soldiers in O(log n) time
   - Much better than O(n) linear counting

2. COMPARISON CRITERIA:
   - Primary: number of soldiers (ascending)
   - Secondary: row index (ascending)
   - This naturally sorts tuples: (soldier_count, row_index)

3. ALGORITHM CHOICES:
   - Sort: Simple and efficient for most cases
   - Min Heap: Good when all elements needed
   - Max Heap (size k): Optimal when k << m

INTERVIEW TALKING POINTS:

1. APPROACH PROGRESSION:
   "I'll start with linear counting O(m*n), then optimize using binary search O(m*log n)."

2. OPTIMIZATION RECOGNITION:
   "Since soldiers come before civilians, I can use binary search to count efficiently."

3. COMPLEXITY ANALYSIS:
   "Binary search gives O(m*log n) for counting, sorting adds O(m*log m)."

4. SPACE-TIME TRADE-OFFS:
   "For small k, a size-k max heap uses O(k) space vs O(m) for sorting."

5. IMPLEMENTATION DETAILS:
   "The binary search finds the first civilian, which equals the soldier count."

COMMON FOLLOW-UPS:

1. "What if k is very large (close to m)?"
   → Sorting approach is better than heap extraction

2. "What if the matrix isn't sorted within rows?"
   → Would need O(m*n) linear counting, no binary search optimization

3. "How would you handle ties in soldier count?"
   → Already handled by secondary sort on row index

4. "Can you optimize further for very sparse matrices?"
   → Could stop binary search early if we find a 0 at the start

5. "What about streaming/online version?"
   → Would need a running heap of size k

6. "Memory constraints - what if you can't store all strengths?"
   → Use the max heap of size k approach (Solution 4)

IMPLEMENTATION STRATEGY:
1. Start with binary search + sorting (Solution 1) as your main answer
2. Explain the binary search logic clearly
3. Walk through the sorting criteria
4. Mention heap alternatives for space optimization
5. Compare time complexities
6. Discuss when to use each approach

The key insight is recognizing that binary search can optimize the soldier counting,
turning an O(m*n) problem into O(m*log n), which is crucial for large matrices!
"""
