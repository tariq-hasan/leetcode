"""
LeetCode 1143: Longest Common Subsequence

Problem: Given two strings text1 and text2, return the length of their longest common subsequence.
If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters 
(can be none) deleted without changing the relative order of the remaining characters.

Example 1:
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

This is the CLASSIC Dynamic Programming problem that appears in almost every algorithms course!
Time: O(m*n), Space: O(m*n) → can be optimized to O(min(m,n))
"""

def longestCommonSubsequence(text1, text2):
    """
    Main solution using 2D DP - the standard LCS algorithm.
    
    DP State: dp[i][j] = LCS length using text1[0:i] and text2[0:j]
    
    Recurrence:
    - If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Args:
        text1: str - first string
        text2: str - second string
    
    Returns:
        int - length of longest common subsequence
    """
    m, n = len(text1), len(text2)
    
    # dp[i][j] = LCS length using first i chars of text1 and first j chars of text2
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # Characters match - extend the diagonal LCS
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match - take best from either direction
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def longestCommonSubsequence_space_optimized(text1, text2):
    """
    Space-optimized solution using only O(min(m, n)) space.
    
    Key insight: We only need the current and previous row to compute DP values.
    Process the shorter string as rows to minimize space usage.
    
    Time: O(m*n), Space: O(min(m, n))
    """
    # Ensure text1 is the shorter string for space optimization
    if len(text1) > len(text2):
        text1, text2 = text2, text1
    
    m, n = len(text1), len(text2)
    
    # Only store current and previous row
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[i] = prev[i - 1] + 1
            else:
                curr[i] = max(prev[i], curr[i - 1])
        
        # Swap rows for next iteration
        prev, curr = curr, prev
    
    return prev[m]


def longestCommonSubsequence_1d_optimized(text1, text2):
    """
    Ultimate space optimization using only O(min(m, n)) space with single array.
    
    This requires careful handling of the diagonal element (dp[i-1][j-1]).
    Most space-efficient but trickiest to implement correctly.
    """
    # Ensure text1 is shorter for space optimization
    if len(text1) > len(text2):
        text1, text2 = text2, text1
    
    m, n = len(text1), len(text2)
    dp = [0] * (m + 1)
    
    for j in range(1, n + 1):
        prev_diagonal = 0  # This represents dp[i-1][j-1]
        
        for i in range(1, m + 1):
            temp = dp[i]  # Save current dp[i] before overwriting
            
            if text1[i - 1] == text2[j - 1]:
                dp[i] = prev_diagonal + 1
            else:
                dp[i] = max(dp[i], dp[i - 1])
            
            prev_diagonal = temp  # Update for next iteration
    
    return dp[m]


def longestCommonSubsequence_recursive(text1, text2):
    """
    Top-down recursive solution with memoization.
    
    Sometimes easier to derive initially and understand the recursive structure.
    Good for explaining the problem's optimal substructure.
    
    Time: O(m*n), Space: O(m*n) + recursion stack
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def lcs(i, j):
        # Base case: reached end of either string
        if i == len(text1) or j == len(text2):
            return 0
        
        # If characters match, include both and recurse
        if text1[i] == text2[j]:
            return 1 + lcs(i + 1, j + 1)
        else:
            # Try skipping either character and take maximum
            return max(lcs(i + 1, j), lcs(i, j + 1))
    
    return lcs(0, 0)


def longestCommonSubsequence_with_reconstruction(text1, text2):
    """
    Enhanced version that reconstructs the actual LCS string.
    
    Essential for follow-up questions asking for the actual subsequence.
    Uses backtracking through the DP table to find the solution path.
    
    Returns:
        tuple: (length, actual_lcs_string)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table (same as main solution)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to reconstruct the LCS
    lcs_chars = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # This character is part of the LCS
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # Move up (skip character in text1)
            i -= 1
        else:
            # Move left (skip character in text2)
            j -= 1
    
    # Reverse to get correct order
    lcs_chars.reverse()
    return dp[m][n], ''.join(lcs_chars)


def longestCommonSubsequence_print_all(text1, text2):
    """
    Advanced version that finds ALL longest common subsequences.
    
    Useful for understanding that there might be multiple optimal solutions.
    Uses backtracking to explore all paths that lead to optimal solution.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    def backtrack(i, j, current_lcs):
        # Base case
        if i == 0 or j == 0:
            all_lcs.add(current_lcs[::-1])  # reverse and add
            return
        
        if text1[i - 1] == text2[j - 1]:
            # Character is part of LCS
            backtrack(i - 1, j - 1, current_lcs + text1[i - 1])
        else:
            # Explore both directions if they lead to optimal solution
            if dp[i - 1][j] == dp[i][j]:
                backtrack(i - 1, j, current_lcs)
            if dp[i][j - 1] == dp[i][j]:
                backtrack(i, j - 1, current_lcs)
    
    all_lcs = set()
    backtrack(m, n, "")
    return dp[m][n], sorted(list(all_lcs))


# Test cases and comprehensive analysis
def test_solution():
    """Test all solutions with comprehensive examples."""
    
    test_cases = [
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("abcdefghijklmnop", "ace", 3),
        ("ABCDGH", "AEDFHR", 3),  # classic example
        ("AGGTAB", "GXTXAYB", 4),  # another classic
        ("", "abc", 0),
        ("abc", "", 0),
        ("", "", 0),
        ("a", "a", 1),
        ("abcd", "acbdef", 4),
        ("AAAA", "AA", 2)
    ]
    
    solutions = [
        ("2D DP", longestCommonSubsequence),
        ("Space Optimized (2 rows)", longestCommonSubsequence_space_optimized),
        ("1D Optimized", longestCommonSubsequence_1d_optimized),
        ("Recursive + Memo", longestCommonSubsequence_recursive)
    ]
    
    print("Testing all solutions:")
    for name, func in solutions:
        print(f"\n{name}:")
        for text1, text2, expected in test_cases:
            try:
                result = func(text1, text2)
                status = "✓" if result == expected else "✗"
                print(f"  {status} '{text1}' vs '{text2}' → Expected: {expected}, Got: {result}")
            except Exception as e:
                print(f"  ✗ '{text1}' vs '{text2}' → Error: {e}")
    
    print("\n" + "="*70)
    print("Testing LCS reconstruction:")
    reconstruction_cases = [
        ("ABCDGH", "AEDFHR"),
        ("AGGTAB", "GXTXAYB"),
        ("abcde", "ace"),
        ("programming", "contest")
    ]
    
    for text1, text2 in reconstruction_cases:
        length, lcs_str = longestCommonSubsequence_with_reconstruction(text1, text2)
        print(f"'{text1}' vs '{text2}' → Length: {length}, LCS: '{lcs_str}'")
    
    print("\n" + "="*70)
    print("Finding all LCS (for small examples):")
    small_cases = [
        ("ABC", "AC"),
        ("ABCD", "ACBDEF"),
    ]
    
    for text1, text2 in small_cases:
        length, all_lcs = longestCommonSubsequence_print_all(text1, text2)
        print(f"'{text1}' vs '{text2}' → Length: {length}")
        print(f"  All LCS: {all_lcs}")


def trace_example(text1, text2):
    """Step-by-step trace of the DP algorithm for understanding."""
    print(f"Tracing LCS DP for text1='{text1}', text2='{text2}'")
    
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    print(f"Initial DP table ({m+1} x {n+1}):")
    print_dp_table(dp, text1, text2)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                print(f"\nStep: text1[{i-1}]='{text1[i-1]}' == text2[{j-1}]='{text2[j-1]}'")
                print(f"dp[{i}][{j}] = dp[{i-1}][{j-1}] + 1 = {dp[i-1][j-1]} + 1 = {dp[i][j]}")
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                print(f"\nStep: text1[{i-1}]='{text1[i-1]}' != text2[{j-1}]='{text2[j-1]}'")
                print(f"dp[{i}][{j}] = max(dp[{i-1}][{j}], dp[{i}][{j-1}]) = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}")
            
            print_dp_table(dp, text1, text2)
    
    print(f"\nFinal LCS length: {dp[m][n]}")
    
    # Show reconstruction
    length, lcs_str = longestCommonSubsequence_with_reconstruction(text1, text2)
    print(f"Reconstructed LCS: '{lcs_str}'")


def print_dp_table(dp, text1, text2):
    """Helper function to visualize the DP table."""
    m, n = len(text1), len(text2)
    
    # Header row
    print("      ", end="")
    print("  ε ", end="")
    for char in text2:
        print(f"  {char} ", end="")
    print()
    
    # Data rows
    for i in range(m + 1):
        if i == 0:
            print("  ε   ", end="")
        else:
            print(f"  {text1[i-1]}   ", end="")
        
        for j in range(n + 1):
            print(f"{dp[i][j]:3} ", end="")
        print()


def analyze_approaches():
    """Comprehensive analysis of different LCS approaches."""
    
    analysis = """
    LCS APPROACH COMPARISON:

    1. 2D DP (RECOMMENDED FOR INTERVIEWS):
       ✓ Most intuitive and widely recognized
       ✓ Easy to explain and trace through
       ✓ Clear visualization with DP table
       ✓ Easy to extend for reconstruction
       ⚠ O(m*n) space complexity
       
    2. Space Optimized (2 rows):
       ✓ Reduces space to O(min(m,n))
       ✓ Still maintains clarity
       ✓ Shows optimization thinking
       ⚠ Slightly more complex implementation
       ✗ Cannot easily reconstruct LCS
       
    3. 1D Space Optimized:
       ✓ Optimal O(min(m,n)) space
       ✓ Demonstrates advanced DP skills
       ⚠ Tricky diagonal element handling
       ✗ Error-prone implementation
       ✗ Difficult to debug
       
    4. Recursive + Memoization:
       ✓ Natural problem structure
       ✓ Easy to derive from scratch
       ✓ Good for explaining optimal substructure
       ⚠ Additional recursion stack space
       ✗ May hit recursion limits

    INTERVIEW STRATEGY:
    1. Start with problem understanding and examples
    2. Identify optimal substructure and overlapping subproblems
    3. Design 2D DP solution with clear recurrence
    4. Implement clean, readable code
    5. Discuss space optimizations as follow-up
    6. Show reconstruction if time permits

    COMMON INTERVIEW VARIATIONS:
    - "Find the actual LCS string" → reconstruction
    - "Optimize space complexity" → rolling array techniques
    - "Find all possible LCS" → backtracking exploration
    - "Edit distance" → related DP problem
    - "Uncrossed lines" → same problem in disguise
    """
    
    print(analysis)


def demonstrate_classic_examples():
    """Show the classic textbook examples that often appear in interviews."""
    
    classic_examples = [
        ("ABCDGH", "AEDFHR", "Expected LCS: 'ADH' (length 3)"),
        ("AGGTAB", "GXTXAYB", "Expected LCS: 'GTAB' (length 4)"),
        ("HUMAN", "CHIMPANZEE", "Expected LCS: 'HMAN' or 'HAN' (length 4)"),
        ("ABCDEFGHIJKLMNOPQRS", "ACEG", "Expected LCS: 'ACEG' (length 4)"),
    ]
    
    print("CLASSIC LCS EXAMPLES:")
    print("=" * 50)
    
    for text1, text2, description in classic_examples:
        length, lcs_str = longestCommonSubsequence_with_reconstruction(text1, text2)
        print(f"Text1: '{text1}'")
        print(f"Text2: '{text2}'")
        print(f"Result: Length = {length}, LCS = '{lcs_str}'")
        print(f"Note: {description}")
        print("-" * 50)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70)
    trace_example("ABCDGH", "AEDFHR")
    print("\n" + "="*70)
    demonstrate_classic_examples()
    print("\n" + "="*70)
    analyze_approaches()
