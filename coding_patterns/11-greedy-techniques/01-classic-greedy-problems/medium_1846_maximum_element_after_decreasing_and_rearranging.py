"""
LeetCode 1846. Maximum Element After Decreasing and Rearranging

Problem: You are given an array of positive integers arr. Perform some operations 
(possibly none) on arr so that it satisfies these conditions:
1. The value of the first element in arr must be 1.
2. The absolute difference between any two adjacent elements must be at most 1.
3. You can decrease any element to any smaller positive value.
4. You can rearrange the elements of arr in any order.

Return the maximum possible value of an element in arr after performing the operations.

Key Insights:
1. We want to maximize the largest element while satisfying constraints
2. Sorting helps us build the optimal sequence greedily
3. Each position has a maximum possible value based on previous elements
4. Greedy approach: make each element as large as possible given constraints

Time Complexity: O(n log n) due to sorting
Space Complexity: O(1) if sorting in-place, O(n) otherwise
"""

# Approach 1: Greedy with Sorting (Optimal Solution)
def maximumElementAfterDecrementingAndRearranging_v1(arr):
    """
    Optimal greedy approach:
    1. Sort the array to process elements in ascending order
    2. Set first element to 1 (required constraint)
    3. For each subsequent element, set it to min(current_value, prev_value + 1)
    4. This ensures we satisfy constraints while maximizing each element
    """
    arr.sort()  # Sort to process in ascending order
    
    # First element must be 1
    arr[0] = 1
    
    # Greedily set each element to maximum possible value
    for i in range(1, len(arr)):
        # Element can be at most prev_element + 1 (constraint)
        # But also can't exceed its original value (can only decrease)
        arr[i] = min(arr[i], arr[i-1] + 1)
    
    return arr[-1]  # Return the maximum element (last after sorting)

# Approach 2: Without Modifying Input Array
def maximumElementAfterDecrementingAndRearranging_v2(arr):
    """
    Same logic but without modifying the input array
    """
    arr = sorted(arr)  # Create sorted copy
    
    current_max = 1  # First element must be 1
    
    for i in range(1, len(arr)):
        # Each element can be at most previous + 1
        current_max = min(arr[i], current_max + 1)
    
    return current_max

# Approach 3: Mathematical Insight (Most Efficient)
def maximumElementAfterDecrementingAndRearranging_v3(arr):
    """
    Key insight: The maximum possible value is bounded by the array length
    Since we start at 1 and can increase by at most 1 each step,
    the maximum possible value for n elements is n.
    """
    arr.sort()
    n = len(arr)
    
    # The theoretical maximum is min(max(arr), n)
    # But we need to check if we can actually achieve it
    
    current = 1
    for num in arr:
        current = min(num, current + 1)
    
    return current

# Approach 4: Detailed Step-by-Step (For Interview Explanation)
def maximumElementAfterDecrementingAndRearranging_explained(arr):
    """
    Version with detailed logging for interview explanation
    """
    print(f"Original array: {arr}")
    
    arr.sort()
    print(f"After sorting: {arr}")
    
    print("\nStep-by-step processing:")
    print("Position 0: Set to 1 (constraint)")
    arr[0] = 1
    
    for i in range(1, len(arr)):
        original = arr[i]
        max_possible = arr[i-1] + 1
        new_value = min(original, max_possible)
        
        print(f"Position {i}: original={original}, max_possible={max_possible}, chosen={new_value}")
        arr[i] = new_value
    
    print(f"\nFinal array: {arr}")
    print(f"Maximum element: {arr[-1]}")
    
    return arr[-1]

# Approach 5: Counting Sort Optimization (For Special Cases)
def maximumElementAfterDecrementingAndRearranging_v5(arr):
    """
    If array values are small, we can use counting sort for O(n + k) time
    where k is the range of values
    """
    if not arr:
        return 0
    
    max_val = max(arr)
    n = len(arr)
    
    # If max value is much larger than n, regular sorting is better
    if max_val > 2 * n:
        return maximumElementAfterDecrementingAndRearranging_v1(arr)
    
    # Count occurrences
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    
    # Process in ascending order
    current = 1
    for value in range(1, max_val + 1):
        while count[value] > 0 and current <= n:
            current = min(value, current + 1)
            count[value] -= 1
            if current == n:
                return current
    
    return current - 1

def prove_optimality():
    """
    Explain why the greedy approach is optimal
    """
    print("=== Why Greedy Approach is Optimal ===")
    print()
    print("1. CONSTRAINT ANALYSIS:")
    print("   - First element must be 1")
    print("   - Adjacent elements differ by at most 1")
    print("   - Can only decrease elements (not increase)")
    print("   - Can rearrange elements")
    print()
    print("2. GREEDY STRATEGY:")
    print("   - Sort array to process small to large")
    print("   - At each position, choose maximum possible value")
    print("   - This is locally optimal and globally optimal")
    print()
    print("3. WHY IT'S OPTIMAL:")
    print("   - Any larger choice would violate constraints")
    print("   - Any smaller choice is suboptimal")
    print("   - Maximum final value depends on building optimal sequence")
    print()
    print("4. MATHEMATICAL BOUND:")
    print("   - Maximum possible value is min(max(arr), n)")
    print("   - We start at 1, can increase by 1 each step")
    print("   - With n elements, max reachable value is n")

def analyze_examples():
    """
    Analyze examples to show the algorithm working
    """
    examples = [
        ([2, 2, 1, 2, 1], 2),
        ([100, 1, 1000], 3),
        ([1, 2, 3, 4, 5], 5),
        ([73, 98, 9, 73, 114, 31, 69, 84], 8),
        ([1], 1),
        ([5, 4, 3, 2, 1], 5)
    ]
    
    print("=== Example Analysis ===")
    for i, (arr, expected) in enumerate(examples):
        print(f"\nExample {i+1}: {arr}")
        result = maximumElementAfterDecrementingAndRearranging_explained(arr[:])
        print(f"Expected: {expected}, Got: {result}")
        assert result == expected, f"Mismatch in example {i+1}"

def test_edge_cases():
    """
    Test various edge cases
    """
    test_cases = [
        ([1], 1),                    # Single element
        ([2, 1], 2),                 # Two elements
        ([1, 1, 1], 3),             # All same elements
        ([1000000], 1),             # Large single element
        ([1, 2, 3, 4, 5], 5),       # Already optimal
        ([5, 4, 3, 2, 1], 5),       # Reverse order
        ([100, 100, 100], 3),       # Large identical elements
        ([1, 1000, 1000000], 3)     # Mixed large values
    ]
    
    print("=== Edge Case Testing ===")
    for i, (arr, expected) in enumerate(test_cases):
        approaches = [
            maximumElementAfterDecrementingAndRearranging_v1,
            maximumElementAfterDecrementingAndRearranging_v2,
            maximumElementAfterDecrementingAndRearranging_v3
        ]
        
        results = []
        for approach in approaches:
            result = approach(arr[:])  # Pass copy to avoid modification
            results.append(result)
        
        print(f"Test {i+1}: {arr} → {results[0]}")
        
        # Verify all approaches give same result
        assert all(r == results[0] for r in results), f"Approaches disagree on {arr}"
        
        # Verify against expected
        if expected is not None:
            assert results[0] == expected, f"Expected {expected}, got {results[0]} for {arr}"

def complexity_analysis():
    """
    Detailed complexity analysis for interview
    """
    print("=== Complexity Analysis ===")
    print()
    print("TIME COMPLEXITY:")
    print("- Sorting: O(n log n)")
    print("- Single pass through array: O(n)")
    print("- Overall: O(n log n)")
    print()
    print("SPACE COMPLEXITY:")
    print("- In-place sorting: O(1) extra space")
    print("- If creating copy: O(n) extra space")
    print("- Recursion in sorting: O(log n)")
    print()
    print("CAN WE DO BETTER?")
    print("- Sorting is necessary to apply greedy strategy")
    print("- Could use counting sort if values are small: O(n + k)")
    print("- But comparison-based sorting lower bound is O(n log n)")
    print("- So O(n log n) is optimal for general case")

if __name__ == "__main__":
    print("=== Maximum Element After Decreasing and Rearranging ===")
    
    # Test all approaches
    test_edge_cases()
    
    # Detailed analysis
    analyze_examples()
    
    # Explain the algorithm
    prove_optimality()
    
    # Complexity discussion
    complexity_analysis()

"""
Critical Interview Discussion Points:

1. **Problem Understanding**:
   - Can decrease any element (but not increase)
   - Can rearrange elements in any order
   - First element must be 1
   - Adjacent elements can differ by at most 1
   - Goal: maximize the largest element

2. **Key Insights**:
   - Sorting allows us to build optimal sequence greedily
   - Each position has a maximum achievable value
   - Greedy choice: make each element as large as possible
   - Mathematical bound: maximum possible value is min(max(arr), n)

3. **Why Greedy Works**:
   - At each step, choosing maximum possible value is locally optimal
   - This leads to globally optimal solution
   - Any larger choice violates constraints
   - Any smaller choice is suboptimal

4. **Algorithm Steps**:
   1. Sort array to process elements in ascending order
   2. Set first element to 1 (required constraint)
   3. For each subsequent element, set to min(original_value, prev_value + 1)
   4. Return the last element (maximum)

5. **Complexity Analysis**:
   - Time: O(n log n) due to sorting (optimal for comparison-based)
   - Space: O(1) if sorting in-place, O(n) for copy
   - Could optimize to O(n + k) with counting sort if values are small

6. **Edge Cases**:
   - Single element: always returns 1
   - All large elements: limited by array length
   - Already optimal sequence: no changes needed
   - Reverse sorted: demonstrates the algorithm working

7. **Mathematical Properties**:
   - Maximum possible value is bounded by array length
   - Sequence must form: 1, 2, 3, ..., k for some k ≤ n
   - Each element contributes at most 1 to the maximum increase

8. **Alternative Approaches**:
   - Could use dynamic programming (overkill)
   - Could try all permutations (exponential time)
   - Greedy is both simple and optimal

9. **Follow-up Questions**:
   - What if we could increase elements? (different problem)
   - What if constraint was difference ≤ k instead of 1?
   - How would you handle negative numbers?

10. **Implementation Tips**:
    - Sort first (crucial for greedy strategy)
    - Handle first element specially (must be 1)
    - Use min() to respect both constraints (original value and adjacency)
    - Return last element after processing (maximum value)
"""
