"""
LeetCode 1312: Minimum Insertion Steps to Make a String Palindrome

Problem: Given a string s, you can insert any character at any position of the string.
Return the minimum number of steps to make s palindrome.

A Palindrome String is one that reads the same backward as well as forward.

Example 1:
Input: s = "zzazz"
Output: 0
Explanation: The string "zzazz" is already palindrome we don't need any insertions.

Example 2:
Input: s = "mbadm"
Output: 2
Explanation: String can be "mbdadbm" or "mdbabdm".

Example 3:
Input: s = "leetcode"
Output: 5
Explanation: Inserting 5 characters the string becomes "leetcodocteel".

KEY INSIGHT: This problem is equivalent to finding the Longest Palindromic Subsequence (LPS)!
- Answer = len(s) - LPS(s)
- LPS can be found using LCS(s, reverse(s))
- Multiple solution approaches available

Time: O(n²), Space: O(n²) → can be optimized to O(n)
"""

def minInsertions(s):
    """
    Main solution using LPS (Longest Palindromic Subsequence) approach.
    
    Key insight: Minimum insertions = len(s) - LPS(s)
    Why? The LPS gives us the maximum characters we can keep unchanged.
    We need to insert characters to "mirror" the remaining characters.
    
    Args:
        s: str - input string
    
    Returns:
        int - minimum number of insertions needed
    """
    def longestPalindromicSubsequence(s):
        """Find LPS using DP where dp[i][j] = LPS length in s[i:j+1]"""
        n = len(s)
        # dp[i][j] = length of LPS in substring s[i:j+1]
        dp = [[0] * n for _ in range(n)]
        
        # Every single character is a palindrome of length 1
        for i in range(n):
            dp[i][i] = 1
        
        # Fill for substrings of length 2 to n
        for length in range(2, n + 1):  # substring length
            for i in range(n - length + 1):
                j = i + length - 1  # end index
                
                if s[i] == s[j]:
                    if length == 2:
                        dp[i][j] = 2
                    else:
                        dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        
        return dp[0][n - 1]
    
    lps_length = longestPalindromicSubsequence(s)
    return len(s) - lps_length


def minInsertions_lcs_approach(s):
    """
    Alternative solution using LCS(s, reverse(s)) to find LPS.
    
    This connects the problem to the classic LCS algorithm.
    LPS(s) = LCS(s, reverse(s))
    
    Sometimes easier to implement if you're very familiar with LCS.
    """
    def lcs(text1, text2):
        """Standard LCS implementation"""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]
    
    # LPS = LCS(s, reverse(s))
    lps_length = lcs(s, s[::-1])
    return len(s) - lps_length


def minInsertions_recursive(s):
    """
    Top-down recursive approach with memoization.
    
    Good for understanding the problem structure and optimal substructure.
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def lps(i, j):
        """Find LPS in s[i:j+1]"""
        if i > j:
            return 0
        if i == j:
            return 1
        
        if s[i] == s[j]:
            return 2 + lps(i + 1, j - 1)
        else:
            return max(lps(i + 1, j), lps(i, j - 1))
    
    lps_length = lps(0, len(s) - 1)
    return len(s) - lps_length


def minInsertions_space_optimized(s):
    """
    Space-optimized solution using O(n) space instead of O(n²).
    
    Since we only need the current and previous row, we can optimize space.
    Great for follow-up questions about memory constraints.
    """
    n = len(s)
    if n <= 1:
        return 0
    
    # Only need current and previous row
    prev = [0] * n
    curr = [0] * n
    
    # Initialize: single characters are palindromes of length 1
    for i in range(n):
        prev[i] = 1
    
    # Fill for substring lengths 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                if length == 2:
                    curr[i] = 2
                else:
                    curr[i] = prev[i + 1] + 2
            else:
                curr[i] = max(curr[i + 1], prev[i])
        
        # Swap arrays
        prev, curr = curr, prev
    
    lps_length = prev[0]
    return n - lps_length


def minInsertions_with_construction(s):
    """
    Enhanced version that constructs the actual palindrome string.
    
    Useful for follow-up questions asking for the actual result string.
    Returns both the minimum insertions and one possible palindrome.
    """
    n = len(s)
    if n <= 1:
        return 0, s
    
    # Build LPS DP table
    dp = [[0] * n for _ in range(n)]
    
    # Single characters
    for i in range(n):
        dp[i][i] = 1
    
    # Fill DP table
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = 2
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    # Reconstruct the palindrome
    def construct_palindrome(i, j):
        if i > j:
            return ""
        if i == j:
            return s[i]
        
        if s[i] == s[j]:
            return s[i] + construct_palindrome(i + 1, j - 1) + s[j]
        else:
            if dp[i + 1][j] > dp[i][j - 1]:
                # Take from left, insert at right
                return s[i] + construct_palindrome(i + 1, j) + s[i]
            else:
                # Take from right, insert at left  
                return s[j] + construct_palindrome(i, j - 1) + s[j]
    
    lps_length = dp[0][n - 1]
    palindrome = construct_palindrome(0, n - 1)
    
    return n - lps_length, palindrome


def minInsertions_interval_dp_direct(s):
    """
    Direct interval DP approach without explicitly finding LPS first.
    
    dp[i][j] = minimum insertions to make s[i:j+1] palindrome
    This is more intuitive for some people as it directly models the problem.
    """
    n = len(s)
    if n <= 1:
        return 0
    
    # dp[i][j] = min insertions to make s[i:j+1] palindrome
    dp = [[0] * n for _ in range(n)]
    
    # Fill for substring lengths 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                # Characters match, no additional insertions needed for these positions
                dp[i][j] = dp[i + 1][j - 1]
            else:
                # Need to insert one character (either s[i] at end or s[j] at start)
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]


# Test cases and comprehensive analysis
def test_solution():
    """Test all solutions with comprehensive examples."""
    
    test_cases = [
        ("zzazz", 0),      # already palindrome
        ("mbadm", 2),      # example case
        ("leetcode", 5),   # example case
        ("a", 0),          # single character
        ("ab", 1),         # two different chars
        ("aa", 0),         # two same chars
        ("abc", 2),        # no common chars
        ("abcba", 0),      # already palindrome
        ("race", 2),       # becomes "racecar"
        ("", 0),           # empty string
        ("abcdef", 5),     # worst case scenario
        ("abacabad", 2)    # complex case
    ]
    
    solutions = [
        ("LPS Approach", minInsertions),
        ("LCS Approach", minInsertions_lcs_approach),
        ("Recursive + Memo", minInsertions_recursive),
        ("Space Optimized", minInsertions_space_optimized),
        ("Direct Interval DP", minInsertions_interval_dp_direct)
    ]
    
    print("Testing all solutions:")
    for name, func in solutions:
        print(f"\n{name}:")
        for s, expected in test_cases:
            try:
                result = func(s)
                status = "✓" if result == expected else "✗"
                print(f"  {status} '{s}' → Expected: {expected}, Got: {result}")
            except Exception as e:
                print(f"  ✗ '{s}' → Error: {e}")
    
    print("\n" + "="*70)
    print("Testing palindrome construction:")
    construction_cases = [
        "mbadm",
        "leetcode", 
        "race",
        "abcdef"
    ]
    
    for s in construction_cases:
        insertions, palindrome = minInsertions_with_construction(s)
        print(f"'{s}' → {insertions} insertions → '{palindrome}'")


def trace_example(s):
    """Step-by-step trace of the LPS DP algorithm."""
    print(f"Tracing LPS DP for s = '{s}'")
    
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Initialize single characters
    for i in range(n):
        dp[i][i] = 1
    
    print("After initializing single characters:")
    print_dp_table(dp, s)
    
    # Fill for increasing substring lengths
    for length in range(2, n + 1):
        print(f"\nProcessing substrings of length {length}:")
        
        for i in range(n - length + 1):
            j = i + length - 1
            substring = s[i:j+1]
            
            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = 2
                    print(f"  s[{i}:{ j+1}] = '{substring}': chars match, length 2 → dp[{i}][{j}] = 2")
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                    print(f"  s[{i}:{j+1}] = '{substring}': chars match → dp[{i}][{j}] = dp[{i+1}][{j-1}] + 2 = {dp[i+1][j-1]} + 2 = {dp[i][j]}")
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
                print(f"  s[{i}:{j+1}] = '{substring}': chars don't match → dp[{i}][{j}] = max({dp[i+1][j]}, {dp[i][j-1]}) = {dp[i][j]}")
        
        print_dp_table(dp, s)
    
    lps_length = dp[0][n - 1]
    min_insertions = n - lps_length
    print(f"\nLPS length: {lps_length}")
    print(f"Minimum insertions: {n} - {lps_length} = {min_insertions}")


def print_dp_table(dp, s):
    """Helper to visualize the DP table."""
    n = len(s)
    
    # Header
    print("    ", end="")
    for j in range(n):
        print(f"{j:3}", end="")
    print("     ", end="")
    for char in s:
        print(f"  {char}", end="")
    print()
    
    # Rows
    for i in range(n):
        print(f"{i:2}: ", end="")
        for j in range(n):
            if j < i:
                print("  -", end="")
            else:
                print(f"{dp[i][j]:3}", end="")
        print(f"  {s[i]}")


def analyze_approaches():
    """Comprehensive analysis of different solution approaches."""
    
    analysis = """
    APPROACH COMPARISON FOR MINIMUM INSERTIONS:

    1. LPS (Longest Palindromic Subsequence) - RECOMMENDED:
       ✓ Clean separation of concerns
       ✓ Reuses well-known algorithm (LPS)
       ✓ Easy to explain: answer = n - LPS(s)
       ✓ Multiple ways to implement LPS
       ⚠ Requires understanding LPS concept
       
    2. LCS(s, reverse(s)) Approach:
       ✓ Connects to classic LCS algorithm  
       ✓ LPS = LCS(s, reverse(s))
       ✓ Good if you know LCS very well
       ⚠ Less direct than LPS approach
       ⚠ Creates reversed string
       
    3. Direct Interval DP:
       ✓ Most intuitive problem modeling
       ✓ Directly computes minimum insertions
       ✓ Clear recurrence relation
       ⚠ Less connection to other problems
       
    4. Recursive + Memoization:
       ✓ Natural problem decomposition
       ✓ Easy to derive from first principles
       ⚠ Additional recursion overhead
       ✗ May hit recursion limits

    INTERVIEW STRATEGY:
    1. Start with examples and intuition
    2. Recognize connection to palindromes
    3. Choose LPS approach (most elegant)
    4. Implement clean DP solution
    5. Discuss space optimizations
    6. Show construction if asked

    KEY INSIGHTS TO MENTION:
    - "This is really about finding the longest palindromic subsequence"
    - "Characters in LPS don't need insertions"
    - "Each remaining character needs one insertion to 'mirror' it"
    - "Multiple optimal solutions often exist"

    TIME/SPACE COMPLEXITY:
    - Time: O(n²) - optimal, must check all substring pairs
    - Space: O(n²) → can optimize to O(n)
    - Cannot do better than O(n²) time for this problem
    """
    
    print(analysis)


def demonstrate_problem_intuition():
    """Show the intuition behind why answer = n - LPS(s)."""
    
    examples = [
        "mbadm",
        "leetcode", 
        "race",
        "abcdef"
    ]
    
    print("PROBLEM INTUITION: Why answer = len(s) - LPS(s)?")
    print("=" * 55)
    
    for s in examples:
        insertions, palindrome = minInsertions_with_construction(s)
        
        # Calculate LPS manually for demonstration
        def find_lps_chars(s):
            """Simple function to find one LPS for demonstration"""
            n = len(s)
            dp = [[0] * n for _ in range(n)]
            
            for i in range(n):
                dp[i][i] = 1
            
            for length in range(2, n + 1):
                for i in range(n - length + 1):
                    j = i + length - 1
                    if s[i] == s[j]:
                        dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
                    else:
                        dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
            
            return dp[0][n - 1]
        
        lps_length = find_lps_chars(s)
        
        print(f"String: '{s}' (length {len(s)})")
        print(f"LPS length: {lps_length}")
        print(f"Characters needing mirrors: {len(s)} - {lps_length} = {insertions}")
        print(f"One possible result: '{palindrome}'")
        print(f"Verification: '{palindrome}' is palindrome = {palindrome == palindrome[::-1]}")
        print("-" * 55)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70)
    trace_example("mbadm")
    print("\n" + "="*70)
    demonstrate_problem_intuition()
    print("\n" + "="*70)
    analyze_approaches()
