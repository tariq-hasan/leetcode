def countNegatives(grid):
    """
    SOLUTION 1: Staircase Search - OPTIMAL for interviews
    
    This is the MOST IMPORTANT solution for big tech interviews.
    Takes advantage of the sorted property in both dimensions.
    
    Time: O(m + n), Space: O(1)
    
    Key insight: Start from top-right or bottom-left corner.
    From top-right: if negative, move left; if positive, move down.
    """
    m, n = len(grid), len(grid[0])
    row, col = 0, n - 1  # Start from top-right corner
    count = 0
    
    while row < m and col >= 0:
        if grid[row][col] < 0:
            # Current element is negative, so all elements below it are negative
            count += (m - row)
            col -= 1  # Move left to find boundary
        else:
            # Current element is non-negative, move down
            row += 1
    
    return count


def countNegativesBinarySearch(grid):
    """
    SOLUTION 2: Binary Search on Each Row
    
    Apply binary search to find first negative in each row.
    Good to mention as alternative approach.
    
    Time: O(m * log n), Space: O(1)
    """
    def findFirstNegative(row):
        """Find index of first negative number in sorted row"""
        left, right = 0, len(row)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if row[mid] < 0:
                right = mid  # First negative might be at mid
            else:
                left = mid + 1  # Look for negatives to the right
        
        return left  # Index of first negative (or len(row) if none)
    
    count = 0
    for row in grid:
        first_negative_idx = findFirstNegative(row)
        count += len(row) - first_negative_idx
    
    return count


def countNegativesBruteForce(grid):
    """
    SOLUTION 3: Brute Force - Simple but not optimal
    
    Mention this first, then optimize. Good for showing thought process.
    Time: O(m * n), Space: O(1)
    """
    count = 0
    for row in grid:
        for num in row:
            if num < 0:
                count += 1
    return count


def countNegativesStaircaseBottomLeft(grid):
    """
    SOLUTION 4: Staircase from Bottom-Left
    
    Alternative staircase approach starting from bottom-left.
    Same complexity as Solution 1, just different starting point.
    """
    m, n = len(grid), len(grid[0])
    row, col = m - 1, 0  # Start from bottom-left corner
    count = 0
    
    while row >= 0 and col < n:
        if grid[row][col] < 0:
            # Current and all elements to the right are negative
            count += (n - col)
            row -= 1  # Move up
        else:
            # Current element is non-negative, move right
            col += 1
    
    return count


def countNegativesOptimizedBinarySearch(grid):
    """
    SOLUTION 5: Optimized Binary Search with Early Termination
    
    Enhanced binary search that stops early when possible.
    Time: O(m * log n) worst case, but often better in practice.
    """
    count = 0
    
    for row in grid:
        # Early termination: if first element is negative, all are negative
        if row[0] < 0:
            count += len(row)
            continue
        
        # Early termination: if last element is non-negative, none are negative
        if row[-1] >= 0:
            continue
        
        # Binary search for first negative
        left, right = 0, len(row)
        while left < right:
            mid = left + (right - left) // 2
            if row[mid] < 0:
                right = mid
            else:
                left = mid + 1
        
        count += len(row) - left
    
    return count


# Comprehensive test suite
def test_count_negatives():
    test_cases = [
        # [grid, expected, description]
        ([
            [4,  3,  2, -1],
            [3,  2,  1, -1],
            [1,  1, -1, -2],
            [-1, -1, -2, -3]
        ], 8, "Standard example from problem"),
        
        ([
            [3, 2],
            [1, 0]
        ], 0, "No negative numbers"),
        
        ([
            [1, -1],
            [-1, -1]
        ], 3, "Mix of positive and negative"),
        
        ([
            [-1, -1, -1],
            [-1, -1, -1]
        ], 6, "All negative numbers"),
        
        ([
            [5, 1, 0]
        ], 0, "Single row, no negatives"),
        
        ([
            [-1, -2, -3]
        ], 3, "Single row, all negative"),
        
        ([
            [1],
            [0],
            [-1]
        ], 1, "Single column"),
        
        ([
            [5, 4, 3, 2, 1, 0, -1, -2]
        ], 2, "Long single row"),
        
        ([
            [7, 6, 5],
            [4, 3, 2],
            [1, 0, -1]
        ], 1, "Only bottom-right negative")
    ]
    
    print("Testing Count Negative Numbers in Sorted Matrix")
    print("=" * 60)
    
    for i, (grid, expected, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print("Grid:")
        for row in grid:
            print(f"  {row}")
        
        # Test all solutions
        result1 = countNegatives(grid)
        result2 = countNegativesBinarySearch(grid)
        result3 = countNegativesBruteForce(grid)
        result4 = countNegativesStaircaseBottomLeft(grid)
        
        print(f"Staircase (top-right): {result1}")
        print(f"Binary search: {result2}")
        print(f"Brute force: {result3}")
        print(f"Staircase (bottom-left): {result4}")
        
        # Verify all solutions match
        all_correct = all(r == expected for r in [result1, result2, result3, result4])
        status = "✓" if all_correct else "✗"
        print(f"Expected: {expected}, All match: {all_correct} {status}")
        print("-" * 40)


# Visual demonstration of staircase algorithm
def demonstrateStaircase():
    """
    Step-by-step visualization of the staircase algorithm
    """
    print("\nSTAIRCASE ALGORITHM DEMONSTRATION")
    print("=" * 50)
    
    grid = [
        [4,  3,  2, -1],
        [3,  2,  1, -1],
        [1,  1, -1, -2],
        [-1, -1, -2, -3]
    ]
    
    print("Grid:")
    for i, row in enumerate(grid):
        print(f"  Row {i}: {row}")
    print()
    
    m, n = len(grid), len(grid[0])
    row, col = 0, n - 1  # Start from top-right
    count = 0
    step = 1
    
    print("Starting from top-right corner (0, 3)")
    print()
    
    while row < m and col >= 0:
        current = grid[row][col]
        print(f"Step {step}: Position ({row}, {col}), Value = {current}")
        
        if current < 0:
            negatives_in_column = m - row
            count += negatives_in_column
            print(f"  Negative! All {negatives_in_column} elements below are negative")
            print(f"  Count += {negatives_in_column}, Total count = {count}")
            print(f"  Move left: col = {col} - 1 = {col - 1}")
            col -= 1
        else:
            print(f"  Non-negative, move down: row = {row} + 1 = {row + 1}")
            row += 1
        
        print()
        step += 1
    
    print(f"Final count: {count}")


# Complexity analysis helper
def analyzeComplexity():
    """
    Compare time complexities of different approaches
    """
    print("\nCOMPLEXITY ANALYSIS")
    print("=" * 30)
    
    approaches = [
        ("Brute Force", "O(m * n)", "O(1)", "Check every element"),
        ("Binary Search", "O(m * log n)", "O(1)", "Binary search each row"),
        ("Staircase", "O(m + n)", "O(1)", "Start from corner, eliminate row/col each step"),
    ]
    
    print(f"{'Approach':<15} {'Time':<12} {'Space':<8} {'Description'}")
    print("-" * 60)
    
    for approach, time, space, desc in approaches:
        print(f"{approach:<15} {time:<12} {space:<8} {desc}")
    
    print()
    print("For a 1000x1000 matrix:")
    print(f"  Brute Force:    ~1,000,000 operations")
    print(f"  Binary Search:  ~10,000 operations") 
    print(f"  Staircase:      ~2,000 operations")


# Run all demonstrations
test_count_negatives()
demonstrateStaircase()
analyzeComplexity()

# INTERVIEW STRATEGY AND KEY POINTS:
"""
PROBLEM ANALYSIS:

This problem tests your ability to:
1. Recognize and exploit sorted properties
2. Choose optimal algorithms based on constraints
3. Implement efficient search techniques

KEY INSIGHTS:

1. SORTED PROPERTY EXPLOITATION:
   - Rows are sorted in descending order
   - Columns are sorted in descending order
   - This creates a "staircase" pattern for negatives

2. WHY STAIRCASE IS OPTIMAL:
   - Each step eliminates either an entire row or column
   - At most m + n steps needed
   - No element is examined more than once

3. STARTING CORNER CHOICE:
   - Top-right: if negative, go left; if positive, go down
   - Bottom-left: if negative, go up; if positive, go right
   - Top-left/bottom-right don't work efficiently

INTERVIEW TALKING POINTS:

1. APPROACH PROGRESSION:
   "I'll start with brute force O(m*n), then optimize using the sorted property."

2. PATTERN RECOGNITION:
   "Since both rows and columns are sorted, I can use a staircase search starting from a corner."

3. ALGORITHM CHOICE:
   "Staircase is optimal at O(m+n), better than binary search's O(m*log n)."

4. IMPLEMENTATION DETAILS:
   "Starting from top-right: negative means all below are negative, positive means move down."

5. EDGE CASES:
   - Empty grid
   - All positive numbers  
   - All negative numbers
   - Single row/column

COMMON FOLLOW-UPS:

1. "What if we wanted to count positive numbers?"
   → Similar staircase approach, just flip the conditions

2. "What if the matrix wasn't sorted?"
   → Would need O(m*n) brute force approach

3. "Can you optimize the binary search approach?"
   → Yes, with early termination (Solution 5)

4. "What about memory usage?"
   → All approaches use O(1) space, which is optimal

5. "How would you handle very large matrices?"
   → Staircase approach scales linearly, making it ideal for large inputs

IMPLEMENTATION STRATEGY:
1. Start with staircase approach (Solution 1) as your main answer
2. Explain the intuition clearly with a visual example
3. Walk through the algorithm step by step
4. Mention binary search as an alternative
5. Compare time complexities
6. Discuss why staircase is optimal

The staircase algorithm is elegant and demonstrates mastery of exploiting sorted properties!
"""
