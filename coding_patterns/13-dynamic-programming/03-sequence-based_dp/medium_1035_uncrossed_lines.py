"""
LeetCode 1035: Uncrossed Lines

Problem: You are given two integer arrays nums1 and nums2. We write the integers of nums1 and nums2 
(in the order they are given) on two separate horizontal lines.

We may draw connecting lines: a straight line connecting two numbers nums1[i] and nums2[j] such that:
- nums1[i] == nums2[j], and
- the line we draw does not intersect any other connecting line.

Note that a connecting line cannot intersect even at the endpoints (i.e., each number can only belong to one connecting line).

Return the maximum number of connecting lines we can draw in this way.

Example 1:
Input: nums1 = [1,4,2], nums2 = [1,2,4]
Output: 2
Explanation: We can draw 2 uncrossed lines as shown.
We cannot draw 3 lines, because the line from nums1[1]=4 and nums2[2]=4 will intersect the line from nums1[2]=2 and nums2[1]=2.

Example 2:
Input: nums1 = [2,5,1,2,5], nums2 = [10,5,2,1,5,2]
Output: 3

Example 3:
Input: nums1 = [1,3,7,1,7,5], nums2 = [1,9,2,5,1]
Output: 2

KEY INSIGHT: This is exactly the Longest Common Subsequence (LCS) problem!
- Uncrossed lines maintain relative order → subsequence property
- Lines connect equal elements → common elements
- Maximum lines → longest common subsequence

Time: O(m*n), Space: O(m*n) → can be optimized to O(min(m,n))
"""

def maxUncrossedLines(nums1, nums2):
    """
    Main solution using 2D DP (classic LCS approach).
    
    DP State: dp[i][j] = max uncrossed lines using nums1[0:i] and nums2[0:j]
    
    Recurrence:
    - If nums1[i-1] == nums2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Args:
        nums1: List[int] - first array
        nums2: List[int] - second array
    
    Returns:
        int - maximum number of uncrossed lines
    """
    m, n = len(nums1), len(nums2)
    
    # dp[i][j] = max uncrossed lines using first i elements of nums1 and first j elements of nums2
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                # Found a match, extend the diagonal
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Take the best from either skipping current element in nums1 or nums2
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def maxUncrossedLines_space_optimized(nums1, nums2):
    """
    Space-optimized solution using only O(min(m, n)) space.
    
    Since we only need the previous row, we can optimize space.
    We process the shorter array as columns to minimize space.
    
    Time: O(m*n), Space: O(min(m, n))
    """
    # Ensure nums1 is the shorter array for space optimization
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    
    # Only need current and previous row
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if nums1[i - 1] == nums2[j - 1]:
                curr[i] = prev[i - 1] + 1
            else:
                curr[i] = max(prev[i], curr[i - 1])
        
        # Swap rows
        prev, curr = curr, prev
    
    return prev[m]


def maxUncrossedLines_1d_optimized(nums1, nums2):
    """
    Ultimate space optimization using only O(min(m, n)) space with single array.
    
    This is the most space-efficient approach but trickier to implement correctly.
    """
    # Ensure nums1 is the shorter array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    dp = [0] * (m + 1)
    
    for j in range(1, n + 1):
        prev_diagonal = 0  # represents dp[i-1][j-1] from previous iteration
        
        for i in range(1, m + 1):
            temp = dp[i]  # save current dp[i] before updating
            
            if nums1[i - 1] == nums2[j - 1]:
                dp[i] = prev_diagonal + 1
            else:
                dp[i] = max(dp[i], dp[i - 1])
            
            prev_diagonal = temp  # update for next iteration
    
    return dp[m]


def maxUncrossedLines_with_path(nums1, nums2):
    """
    Enhanced version that reconstructs the actual connections.
    Useful for follow-up questions about which elements to connect.
    
    Returns both the count and the actual pairs that form uncrossed lines.
    """
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table (same as main solution)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find the actual connections
    connections = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if nums1[i - 1] == nums2[j - 1]:
            # This element is part of the solution
            connections.append((i - 1, j - 1, nums1[i - 1]))
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    connections.reverse()  # reverse to get correct order
    return dp[m][n], connections


def maxUncrossedLines_memoization(nums1, nums2):
    """
    Top-down approach using memoization.
    Sometimes easier to understand the recursive structure.
    
    Time: O(m*n), Space: O(m*n) + recursion stack
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i, j):
        # Base case: reached end of either array
        if i == len(nums1) or j == len(nums2):
            return 0
        
        # If elements match, we can connect them
        if nums1[i] == nums2[j]:
            return 1 + dp(i + 1, j + 1)
        else:
            # Try skipping either element and take the maximum
            return max(dp(i + 1, j), dp(i, j + 1))
    
    return dp(0, 0)


# Test cases and analysis
def test_solution():
    """Test all solutions with comprehensive examples."""
    
    test_cases = [
        ([1, 4, 2], [1, 2, 4], 2),
        ([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2], 3),
        ([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1], 2),
        ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1], 5),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1], [1], 1),
        ([1, 2], [2, 1], 1),
        ([], [1, 2, 3], 0),
        ([1, 2, 3], [], 0)
    ]
    
    solutions = [
        ("2D DP", maxUncrossedLines),
        ("Space Optimized", maxUncrossedLines_space_optimized),
        ("1D Optimized", maxUncrossedLines_1d_optimized),
        ("Memoization", maxUncrossedLines_memoization)
    ]
    
    print("Testing all solutions:")
    for name, func in solutions:
        print(f"\n{name}:")
        for nums1, nums2, expected in test_cases:
            try:
                result = func(nums1, nums2)
                status = "✓" if result == expected else "✗"
                print(f"  {status} nums1={nums1}, nums2={nums2} → Expected: {expected}, Got: {result}")
            except Exception as e:
                print(f"  ✗ nums1={nums1}, nums2={nums2} → Error: {e}")
    
    print("\n" + "="*60)
    print("Testing path reconstruction:")
    test_path_cases = [
        ([1, 4, 2], [1, 2, 4]),
        ([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]),
        ([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1])
    ]
    
    for nums1, nums2 in test_path_cases:
        count, connections = maxUncrossedLines_with_path(nums1, nums2)
        print(f"\nnums1 = {nums1}")
        print(f"nums2 = {nums2}")
        print(f"Max uncrossed lines: {count}")
        print(f"Connections: {[(f'nums1[{i}]={val}', f'nums2[{j}]={val}') for i, j, val in connections]}")


def trace_example(nums1, nums2):
    """Step-by-step trace of the DP algorithm."""
    print(f"Tracing DP for nums1={nums1}, nums2={nums2}")
    
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    print(f"Initial DP table ({m+1} x {n+1}):")
    print_dp_table(dp, nums1, nums2)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                print(f"\nStep: nums1[{i-1}]={nums1[i-1]} == nums2[{j-1}]={nums2[j-1]}")
                print(f"dp[{i}][{j}] = dp[{i-1}][{j-1}] + 1 = {dp[i-1][j-1]} + 1 = {dp[i][j]}")
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                print(f"\nStep: nums1[{i-1}]={nums1[i-1]} != nums2[{j-1}]={nums2[j-1]}")
                print(f"dp[{i}][{j}] = max(dp[{i-1}][{j}], dp[{i}][{j-1}]) = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}")
            
            print_dp_table(dp, nums1, nums2)
    
    print(f"\nFinal result: {dp[m][n]}")


def print_dp_table(dp, nums1, nums2):
    """Helper function to print DP table nicely."""
    m, n = len(nums1), len(nums2)
    
    # Header
    print("    ", end="")
    print("  ε ", end="")
    for val in nums2:
        print(f"{val:3}", end="")
    print()
    
    # Rows
    for i in range(m + 1):
        if i == 0:
            print("  ε ", end="")
        else:
            print(f"{nums1[i-1]:3} ", end="")
        
        for j in range(n + 1):
            print(f"{dp[i][j]:3}", end="")
        print()


def analyze_approaches():
    """Compare different solution approaches."""
    
    analysis = """
    APPROACH COMPARISON:

    1. 2D DP (Recommended for Interview):
       ✓ Most intuitive and easy to explain
       ✓ Clear relationship to LCS problem
       ✓ Easy to debug and trace
       ✗ O(m*n) space complexity
       
    2. Space Optimized (2 rows):
       ✓ Reduces space to O(min(m,n))
       ✓ Still relatively easy to understand
       ✗ Slightly more complex implementation
       
    3. 1D Space Optimized:
       ✓ Optimal space complexity O(min(m,n))
       ✓ Shows advanced optimization skills
       ✗ Tricky to implement correctly
       ✗ Harder to debug
       
    4. Memoization (Top-down):
       ✓ Natural recursive structure
       ✓ Sometimes easier to derive initially
       ✗ Extra recursion stack space
       ✗ May hit recursion limits for large inputs

    INTERVIEW STRATEGY:
    - Start with 2D DP approach (clearest)
    - Explain the LCS connection
    - Mention space optimizations as follow-up
    - Show path reconstruction if asked
    """
    
    print(analysis)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*60)
    trace_example([1, 4, 2], [1, 2, 4])
    print("\n" + "="*60)
    analyze_approaches()
